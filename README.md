# ![logo Sofa V&V](./Utils/logo.png) SofaV-V 



This project aims at providing a template, a structure and data for the verification and validation of Sofa scenes in different scenarios of deformation. The test scenes are structured according to the case study considered. This case study must correspond to practical scenarios where groundtruth data are available, whether these data are given by analytical or numerical models previously validated with experiments, or are experimental values directly. The goal is then to evaluate the performance of the test scene and plot the resulting graph to obtain finally a tractable documentation.

## Structure

Each case study directory is structured as follows:
* "Data" folder containing the generated simulation data as well as the graphs comparing them to the groundtruth
* "TestScenes" folder containing only one file per test scene
* "Mesh" folder containing the mesh files eventually required by the test scenes
* "doc.md" file containing the documentation of the case study and the different test scenes, incorporating the comparison graphs
* "case_study.py" file, to generate automatically the simulation data, groundtruth data and plots related to all or one particular test scene.

## Commands

Executing the following command will generate the data of all test scenes of all case studies. 

```console
python3 main_generate_all.py
```

Executing the following command will generate only the data of the desired case study and test scene. The indices of both can be found in the table below

```console
python3 main_generate_all.py idCaseStudy idTestScene
```

Executing the following command will regenerate the summary table of the case studies and test scenarios bellow.

```console
python3 main_generate_readme.py 
```

## How to contribute

### Adding new case studies

The first step is to create a repository with the name of the case study, in the correct sub-folder (organiezd for the moment according to the deformation modes, in static or dynamic regimes). Reproduce then the default organization, with case_study.py and a doc.md files at the root, and Data, Mesh and TestScenes folders.

In case_study.py, the case study must be defined as a python class called "CaseStudy" inheriting from the CaseStudyTemplate class defined in the Utils/classes.py file. There are several functions to adapt to the considered case study:
- `generate_data(self,testSceneIndex)`: to generate the csv files containing the simulated data for a given test scene. The csv file must be saved in the Data folder and named specifically as "test_scene_testSceneIndex_variedParameterIndex.csv" where the two indices must be specified as integers.
- `generate_plot(self,testSceneIndex)`: to generate the plots to be included in the documentation for a given test scene. The plots must be saved in the Data folder and named specifically as "test_scene_testSceneIndex_variedParameterIndex.png" where the two indices must be specified as integers.
- `set_parameters()`: to get the list of physical parameters required to compute the groundtruth, that must be reused by the test scene.
- `gt_value = compute_groundtruth()`: to compute the groundtruth values from the physical parameters, either using an analytical solution of the problem or a numerical one. Could also return experimental values, that would have to be stored in a csv file (in the Data folder for example).
- `error = compute_error()`: to compute the error between the groundtruth and the simulated data. Different expressions could be used, such as relative or absolute errors. In this function, the user must also specify the error unit to be displayed on the graphs.

Finally, in case_studies.py, at the root of the V&V directory, the case study must be added to the list following the template given. The CaseStudy class must be created with the corresponding name, id and paths, and must be added to the list returned by `get_list()`.

### Adding new test scenes

The first step is creating a test scene python file in the TestScenes folder of the corresponding case study. The file must be named "test_scene_testSceneIndex.py" where index must be replaced by its integer value.

In this file, a class "TestScene" must be created with the following functions:
- `__init__(self)`: to define the parameters specific to the test scenes, which are:
    - `name`: name of the test scene, which should be explicit about the main feature to be tested (for example the elasticity model)
    - `param_name`: a list of the name of the parameters to be varied one by one to obtain the comparison graphs
    - `nom`: a list of the nominal value of these parameters. When one parameter is varied, the others are taken as their nominal value.
    - `min, max`: lists of the minimum and maximum values of each parameter. The parameters are varied one by one in this interval using a linear interpolation. The interpolation is currently done in the generate_data() function of the case study. When the parameter is the number of element in a mesh, the result of the interpolation must be further casted into an integer.
    - `nb`: list of points to be taken between the min and max value for each parameter.
    - `Niter`: list of the number of simulation steps to perform to reach the solution of the model. This number must ensure that the scene converged properly. It can be determined empirically by launching the test scene for increasing value until convergence is reached. 
- `rootNode createScene(self,rootNode, cs_param, param_idx, param, caseStudy_path)`: the function where the test scene is built, stored in rootNode, according to the case study parameters cs_param, the test scene parameters param. The index of the parameter to be varied param_idx and the case study path caseStudy_path are only used to be transmitted to the Sofa controller of the scene to generate a csv file with the proper name.

Finally, a Sofa controller must be written to monitor the simulated data of interest and store them in a csv file in the Data folder, after the number of simulation step is reached. The csv file must be saved in the Data folder and named specifically as "test_scene_testSceneIndex_variedParameterIndex.csv" where the two indices must be specified as integers.

After having added a new test scene or case study, don't forget to run the main_generation_readme.py file to update the table of content below.

[comment]: <> (This list of case studies and test scenario must always be placed at the end of the readme, and the section title should always be "Case studies and test scenario" for the main_generate_readme.py script to work properly.)
## Case studies and test scenario

| Case study | Name | Test scene | Name | 
| ---------- | ---- | ---------- | ---- | 
| 1 | Static/LinearElastic/Bending/ CantileverBeam | | | 
| |  | 1 | Co-rotational FEM with tetra elements | 
| |  | 2 | Co-rotational FEM with hexa elements | 
| |  | 3 | Co-rotational FEM with 1D beam elements | 
| |  | 4 | Constant strain Cosserat elements | 
| 2 | Static/LinearElastic/Extension/ CantileverBeam | | | 
| |  | 1 | Co-rotational FEM with tetra elements | 
| |  | 2 | Co-rotational FEM with hexa elements | 
| |  | 3 | Co-rotational FEM with 1D beam elements | 
