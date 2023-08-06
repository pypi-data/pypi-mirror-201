# ConGen: Creating conservation planning datasets intuitively by playing with parameters and getting instant visualized feedback

## Requirements
For python library requirements, see pyproject.toml. Additionally, the following system libraries and development headers are required:
- basic build tools (gcc, make etc.)
- 
- gdal for building the Python GDAL module

## TODOs
- [ ] Fix WardClusteredPointLayer
- [ ] CLI Interface
- [ ] Benchmark different conservation planning software
- [ ] Improve UI / UX
  - [ ] Onboarding / Instructions
  - [ ] Project creation wizard with predefined templates?
  - [ ] Project template files
  - [ ] Tooltips for parameters 

## Archievements
- Object-oriented design
  - All layer types are implemented as classes that inherit from common layer types, overriding common methods if needed
- wxPython GUI with Model-View-Controller Design
  - LayerListCtrl controller class manages both a wxPython list control and the underlying data structure
  - List view and underlying data structure are always in sync
  - On parameter change: Corresponding value in underlying data structure gets automatically updated, list view and rendering are automatically refreshed
- Custom implementation for parameters
  - Wrapping a single value (e.g. int, bool, string) with metadata (default, min, max values, parameter name and description, etc.)
  - Stored in a list for each layer type to distinguish parameters from other layer instance variables
  - Each layer type requires different parameters, extends the parameter list from inherited classes
  - Automatically render appropriate parameter controls for each layer type based on parameter list
  - Future: automatically render columns in layer list based on parameter list
  - Caching: Specify which parameters invalidate the calculated cache, only re-calculate layer data if relevant parameters change, don't recalculate for parameters that can be applied to existing data -> minifies computational overhead, especially for applications with many layers
  - Python magic so parameters of each layer can still be accessed via `layer.parameterName` despite being
    a) stored in a list variable instead of being class instance members themselves
    b) classes that wrap the actual value with additional metadata

## Material
### Ecology
- [BC Marine Conservation Analysis](https://bcmca.ca/)

### Procedural map generation
- [Notes on Procedural Map Generation Techniques](https://christianjmills.com/posts/procedural-map-generation-techniques-notes/index.html)
- [java - Procedural Map Generation - Stack Overflow](https://stackoverflow.com/questions/9448386/procedural-map-generation)
- [Map Generation - Procedural Content Generation Wiki](http://pcg.wikidot.com/pcg-algorithm%3amap-generation)
- [Procedural Map Generation with Godot — Part 1](https://medium.com/pumpkinbox-blog/procedural-map-generation-with-godot-part-1-1b4e78191e90)
- [A Guide to Procedural Generation - GameDev Academy](https://gamedevacademy.org/procedural-2d-maps-unity-tutorial/)
- [Procedural Map | Rust Wiki | Fandom](https://rust.fandom.com/wiki/Procedural_Map)
- [Map generator - Minetest Wiki](https://wiki.minetest.net/Map_generator)

#### Perlin Noise
- [Noise and Turbulence - Ken's Academy Award](https://mrl.cs.nyu.edu/~perlin/doc/oscar.html) -> Ken Perlin
- [Lecture 14 Procedural Generation: Perlin Noise](https://www.cs.umd.edu/class/fall2019/cmsc425/handouts/lect14-perlin.pdf)
- [Perlin Noise - Scratchapixel](https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/perlin-noise-part-2)
- 
- [Playing with Perlin Noise: Generating Realistic Archipelagos](https://medium.com/@yvanscher/playing-with-perlin-noise-generating-realistic-archipelagos-b59f004d8401)
- [Perlin 2D Noise in python](https://engineeredjoy.com/blog/perlin-noise/)
- [Exploring Perlin Noise in Python](https://samclane.dev/Perlin-Noise-Python/)
- [Perlin noise in python - Stack Overflow](https://stackoverflow.com/questions/71040845/perlin-noise-in-python)
- 

##### Python Libraries
Not exhaustive
- [EasyPerlinNoise](https://pypi.org/project/EasyPerlinNoise/)
- [pythonperlin](https://pypi.org/project/pythonperlin/)
- [perlin](https://pypi.org/project/perlin/)
- [perlin-numpy](https://github.com/pvigier/perlin-numpy)
- [perlin-cupy](https://pypi.org/project/perlin-cupy/)
- [vec-noise](https://pypi.org/project/vec-noise/)
- [noise](https://pypi.org/project/noise/)
- [noise-randomized](https://pypi.org/project/noise-randomized/)
- [perlin-noise](https://pypi.org/project/perlin-noise/)
- [nPerlinNoise](https://pypi.org/project/nPerlinNoise/)
- [pyfastnoisesimd](https://pypi.org/project/pyfastnoisesimd/)
- [pyperlin](https://pypi.org/project/pyperlin/)
- [shades](https://pypi.org/project/shades/)
- [opensimplex](https://pypi.org/project/opensimplex/)
- [noisemaker](https://pypi.org/project/noisemaker/) -> Olsen Noise(?)
- [pyramage](https://pypi.org/project/pyramage/)
- [processing](https://py.processing.org/reference/noise.html)
- [perlin.py](https://gist.github.com/eevee/26f547457522755cb1fb8739d0ea89a1)