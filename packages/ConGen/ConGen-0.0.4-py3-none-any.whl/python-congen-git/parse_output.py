#!/usr/bin/env python3

import argparse
import json
import os
import sqlite3
import logging
import pandas


def parse_args():
    parser = argparse.ArgumentParser(description='Command line arguments for parsing conservation planning output '
                                                 'into a sqlite database')

    parser.add_argument('-m', '--marxan', type=MarxanOutputParser, help="Paths of Marxan input files to parse",
                        nargs='*', action='extend', dest='inputfiles')
    parser.add_argument('-c', '--coco', type=CocoOutputParser, help="Paths of Coco input files to parse", nargs='*',
                        action='extend', dest='inputfiles')
    parser.add_argument('-p', '--prioritizr', type=PrioritizrOutputParser,
                        help="Paths of Prioritizr input files to parse", nargs='*', action='extend', dest='inputfiles')
    parser.add_argument('-o', '--output', type=str,
                        help="Path to the SQLite3 database (will be created if nonexistent)", required=True)
    parser.add_argument('--loglevel', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], type=str, help='Set log level',
                        default='INFO')
    parser.add_argument('--flag-done', action='store_true',
                        help="Flag parsed data as done by adding a '.done' file to the directory")

    return parser.parse_args()


# General OutputParser construct to extend
class OutputParser:
    def __init__(self, filename):
        self.filename = filename
        self.done_filename = self.filename + ".done"
        self.raw = dict()
        self.data = dict()
        self.tablename = "undefined"

    # Do the actual parsing.
    def parse(self):
        self.read()
        self.flatten(self.raw)

    # By default, the output will be assumed to be in JSON format
    def read(self):
        with open(self.filename, 'r') as f:
            self.raw = json.load(f)

    # By default, the output will be flattened into a single-level dict for insertion into the database
    def flatten(self, value, key=None):
        if key is None:
            key = ['root']
        if type(value) is dict:
            # Descend into nested dicts
            for curkey, curvalue in value.items():
                newkey = key.copy()
                newkey.append(curkey)
                self.flatten(curvalue, newkey)
        else:
            # Add attribute to the data dict with the last two levels of keys concatenated by _
            self.data["_".join(key[-2:])] = json.dumps(value) if type(value) in [list, dict] else str(value)

    def check_done(self):
        logging.debug("Checking if", self.done_filename, "exists")
        return os.path.isfile(self.done_filename)

    def flag_done(self):
        logging.debug(f'Flagging {self.filename} as done: {self.done_filename}')
        with open(self.done_filename, 'w'):
            pass

    def __str__(self):
        return "{} input: {}".format(self.tablename, self.filename)


# Parse output of a Marxan run
class MarxanOutputParser(OutputParser):
    def __init__(self, filename):
        super(MarxanOutputParser, self).__init__(filename)
        self.tablename = "marxan"

    # In case of Marxan, Marxan's input.dat file is read and parsed. From that, the path of the output_sums.csv file
    # is derived and also read and parsed.
    def read(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                words = line.split()
                if len(words) and words[0].isupper():
                    # Marxan parameters are all-uppercase
                    if words[0] in ['INPUTDIR', 'OUTPUTDIR']:
                        words[1] = os.path.abspath(os.path.join(os.path.dirname(self.filename), words[1]))
                    self.raw[words[0]] = words[1]

        sum_filename = os.path.join(self.raw['OUTPUTDIR'], "_".join([self.raw['SCENNAME'], "sum.csv"]))

        with open(sum_filename, 'r') as f:
            sums = pandas.read_csv(f)
            self.raw['sums'] = sums.to_dict('records')

    # Flattening is not required for Marxan
    def flatten(self, value, key=None):
        self.data = self.raw


# Parse JSON output of prioritizr-cli
class PrioritizrOutputParser(OutputParser):
    def __init__(self, filename):
        super(PrioritizrOutputParser, self).__init__(filename)
        self.tablename = "prioritizr"


# Parse coco JSON output
class CocoOutputParser(OutputParser):
    def __init__(self, filename):
        super(CocoOutputParser, self).__init__(filename)
        self.tablename = "coco"

    # Read JSON into memory, no conversion necessary
    def read(self):
        with open(self.filename, 'r') as f:
            self.raw = json.load(f)


# This class extends the functionality of Python's integrated sqlite package. It allows to insert data into the
# database without taking care that the needed tables and columns inside the tables exist. Instead, tables and
# columns are created on-the-fly based on the passed data. Furthermore, it allows handling of list-valued attributes
# by automatically creating a sub-table with a backreference to the original dataset.
class SQLiteManager:
    def __init__(self, filename):
        self.filename = filename
        self.con = sqlite3.connect(filename)

    # Translate Python datatypes into SQL datatypes for column creation.
    @staticmethod
    def translate_datatype(data):
        if type(data) is int:
            return "INTEGER"
        elif type(data) is str:
            return "TEXT"
        elif type(data) is float:
            return "REAL"
        else:
            raise ValueError("Unknown datatype encountered: " + str(data))

    # Return required columns with their datatype for column creation.
    @staticmethod
    def get_columns(data):
        columns = []

        for key, value in data.items():
            columns.append([key, SQLiteManager.translate_datatype(value)])

        return columns

    # Create table with required columns if it does not exist
    def make_table(self, data, tablename):
        cur = self.con.cursor()

        column_string = ", ".join([" ".join(i) for i in SQLiteManager.get_columns(data)])

        create_string = "CREATE TABLE IF NOT EXISTS {} ( {} );".format(tablename, column_string)

        cur.execute(create_string)

    # Create additional columns in the table if data has more attributes than the existing table
    def make_columns(self, data, tablename):
        cur = self.con.cursor()

        data_columns = SQLiteManager.get_columns(data)
        pragma_result = cur.execute("PRAGMA table_info({})".format(tablename)).fetchall()
        cur_columns = [item[1] for item in pragma_result]

        for i in data_columns:
            if not i[0] in cur_columns:
                logging.debug("Adding column", i)
                cur.execute("ALTER TABLE {} ADD COLUMN {}".format(tablename, " ".join(i)))

    # Add actual data to the table
    def add_data(self, data, tablename, extra_fields=None):
        if extra_fields is None:
            extra_fields = {}
        if type(data) is list:
            # If multiple rows are passed, add each of them to the table
            for row in data:
                self.add_data(row, tablename, extra_fields)
            return

        # Add extra fields to the data (used for references for each list data item to its corresponding dataset)
        data = {**data, **extra_fields}

        # Ignore list valued attributes for now
        filtered_data = {key: value for key, value in data.items() if type(value) is not list}

        cur = self.con.cursor()

        # Make sure table and columns exist
        self.make_table(filtered_data, tablename)
        self.make_columns(filtered_data, tablename)

        # Prepare SQL statement
        column_string = ", ".join(list(filtered_data.keys()))
        value_string = ", ".join(["?"]*len(filtered_data))

        sql_command = "INSERT INTO {} ( {} ) VALUES ( {} );".format(tablename, column_string, value_string)
        value_list = list(filtered_data.values())

        # Execute SQL statement
        logging.debug(sql_command, value_list)
        cur.execute(sql_command, value_list)
        rowid = cur.lastrowid

        # Deal with list valued attributes
        for key, value in data.items():
            if type(value) is list:
                # If one of the attributes is a list, add each item to a new table with a back-reference
                new_tablename = "_".join([tablename, key])
                new_extra_fields = {**extra_fields, tablename: rowid}
                self.add_data(value, new_tablename, new_extra_fields)

        self.con.commit()


def main():
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.loglevel),
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')
    sqlite_manager = SQLiteManager(args.output)

    for parser in args.inputfiles:
        # Parse input and insert into database
        if not args.flag_done or (args.flag_done and not parser.check_done()):
            logging.info(f'Parsing {str(parser)}')
            parser.parse()
            sqlite_manager.add_data(parser.data, parser.tablename)
            if args.flag_done:
                parser.flag_done()


if __name__ == '__main__':
    main()
