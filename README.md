# SofaV-V

This project aims at providing a template, a structure and data for the verification and validation of Sofa scenes in different scenarios of deformation. The test scenes are structured according to the case study considered. This case study must correspond to practical scenarios where groundtruth data are available, whether these data are given by analytical or numerical models previously validated with experiments, or are experimental values directly. The goal is then to evaluate the performance of the test scene and plot the resulting graph to obtain finally a tractable documentation.

## Structure

Each case study directory is structured as follows:
* "Data" folder containing the generated simulation data as well as the graphs comparing them to the groundtruth
* "TestScenes" folder containing only one file per test scene
* "Mesh" folder containing the mesh files eventually required by the test scenes
* "doc.md" file containing the documentation of the case study and the different test scenes, incorporating the comparison graphs
* "generate.py" file, to generate automatically the data and plots related to all or one particular test scene.

## Command

Executing the following command will generate the data of all test scenes of all case studies. 

```console
python3 main_generate_all.py
```

Executing the following command will generate only the data of the desired case study and test scene. The indices of both can be found in the table below

```console
python3 main_generate_all.py idCaseStudy idTestScene
```

## Case studies and test scenario

| Case study | Name | Test scene | Name|
|------------|-------|------------|------|     
| 1 | Static Bending Cantilever Beam | 1 | Co-rotational FEM with tetra elements|
|  |  | 2 | Co-rotational FEM with hexa elements|
|  |  | 3 | Linear FEM with tetra elements|
| 2 | Static Bending Force Follower |  | no test scene yet |
| 3 | Static Extension Cantilever Beam |  | no test scene yet |

## Contributing

### Adding new test scenes

### Adding new case studies

