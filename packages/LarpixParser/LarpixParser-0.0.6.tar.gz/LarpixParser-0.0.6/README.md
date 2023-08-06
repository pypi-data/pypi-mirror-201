# LarpixParser
This package provides simple function to parse LArPix readout position [mm], read out charge [thousand electrons(ke-)] and deposited energy [MeV], as well as truth information inherited from larnd-sim output if run on simulation files.\
This package is also available on pypi: https://pypi.org/project/LarpixParser/. 
```
pip install LarpixParser
```

## Get LArPix layout and run configuration 
**Option 1:** Use the default, pre-installed package data \
**Option 2:** Point to a pre-load LArPix geometry dictionary stored in a pickle file and a run configuration yaml file \
**Option 3:** Build a LArPix geometry dictionary on the fly and load a run configuration yaml file \
You can find examples in `example/parsing_example.py` or `example/NDLAr_eventdisplay.ipynb`. **Option 1** is a recommended way to load this configuration, unless you are trying to do something unusual.

## A few words about the LArPix layout and run configuration files
- A LArPix layout yaml file: \
    An example can be found in `src/LarpixParser/config_repo/multi_tile_layout-3.0.40.yaml` for a nd-lar configuration. The geometry yaml files are produced using scripts in package `larpix/larpix-geometry` (https://github.com/larpix/larpix-geometry). It is also on PyPI: https://pypi.org/project/larpix-geometry/. Note that different runs of the same detector can lead to different geometry yaml file depending on the pixel channel routing set up before the run. Note that `multi_tile_layout-3.0.40.yaml` and `multi_tile_layout-2.3.16.yaml` only represent one nd-lar and one 2x2 module respectively. Each module is assumed to have the same laypix layout, which needs to be updated in future. 
- A configuration file: \
    An example can be found in `src/LarpixParser/config_repo/ndlar-module.yaml`. It should store information about the LArPix charge calibration, run conditions (electric field, electron lifetime, etc.), coordinate shifts and detector physics parameters (LAr density, recombination model parameters, etc.). Note that `LarpixParser` assumes the units as shown in the example configuration file. They are based on configuration files in `DUNE/larnd-sim/larndsim/detector_properties/`.
    
## Special note for using Option 2 to load the LArPix layout
In case you don't have a ready-made LArPix layout dictionary as this package would consume, you can use `src/LarpixParser/geom_to_dict.py` to convert the LArPix geometry yaml to a dictionary and store it in a pickle file. It is a standalone script. If no dedicated output path is specified, by default the output pickle file will be stored in the same folder where the yaml file is, e.g `dict_repo/LARPIX_GEOM_NAME.pkl`. Please check your writing permission of the output folder. Run the following command to execute this step. 

```
python3 src/LarpixParser/geom_to_dict.py --geom_repo=PATH_TO_LARPIX_GEOMETRY_YAML --larpix_layout_name=NAME_LARPIX_GEOMETRY_YAML [--dict_out=PATH_TO_OUTPUT_PKL]
```

## Example usage:
Examples can be found in `example/`. `parsing_example.py` shows the basic usage of transforming packets from individual events to higher level information (x, y, z, dQ, dE...). `NDLAr_eventdisplay.ipynb` gives an event display example in addition, drawing the larpix output (larnd-sim output) and edepsim output if it's simulation. Given the package does not include event parser, truth information of event parsing was borrowed in these examples. Also, the translation of the packet information does not produce "hit"-level data product. If you are interested in that aspect, please follow the development of `module0-flow` or the future `2x2-flow`.

Function `hit_parser_position` outputs x, y, z and the drift time with respect to the "t0" of the event. <br /> 
Function `hit_parser_charge` outputs x, y, z and dQ [ke-] which is the read out charge per channel (All the channels share the same calibration constants for now, and they are required in the configuration file. The calibration constants are used for converting the readout from [ADC] to [mV] and then to [ke-]). <br />
Function `hit_parser_energy` outputs x, y, z and dE [MeV] which meant to be the energy deposition corresponding to the read out charge at their origin. Therefore, the detector physics calibration (work function, recombination and electron attenuation) is folded in. One caveat is that dE/dx is assumed to be 2 MeV/cm for all in the recombination model which is definitely a simplification. <br />
Function `hit_parser_charge_n_truth` outputs x, y, z, dQ [ke-], segID, frac and pdg, where the last three are from simulation truth. `segID` gives a list of G4 segments which contribute to this packet; `frac` shows their contribution by percentage in charge which is normalised to 1 (Note: due to induced charge, the contribution can be negative or above 1); `pdg` is the pdg code of the contributed segments.

`x` is along the drift axis; `y` is along the vertical axis; `z` is along the horizontal axis of the LArPix plane. The origin of the coordinate system depends on the detector (defined in the detector configuration file). LArPix configuration files by default use x-y for the pixel planes, so if one wants to convert `x` to the drift axis as indicated above, `switch_xz` should be set to True (the default setting). Fancier coordinate transformation can be implemented if needed. 
