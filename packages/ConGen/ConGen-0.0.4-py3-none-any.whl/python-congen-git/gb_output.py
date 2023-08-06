import subprocess
import json
import gurobipy

def print_stats(args, timer, m):
    ''' print stats about the runtime: HPC '''
    if args.output:
        results = {
            "application": {
                "name": "coco",
                "version": "0.1",
                "git_hash": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True).stdout.decode().strip()
            },
            "args": args.__dict__,
            "times": {
                "analysis_start_time": timer.start_set_ns,
                "gurobi_start_time": timer.start_sol_ns,
                "analysis_end_time": timer.stop_set_ns,
            },
            "gurobi": {
                "json_solution": json.loads(m.getJSONSolution())
            }
        }
        with open('../analysis/solution.json', 'w') as outfile:
            json.dump(results, outfile)

