import Sofa
import importlib
import os
import matplotlib.pyplot as plt
import csv

object_path = "Component/SolidMechanics/FEM/TetrahedronFEMForceField/"

def generate():
    # Need to scan all the test scenario in the TestScenario folder and generate the corresponding data
    # the -1 is for not considering the pycache folder
    Nscenario = len(os.listdir(object_path+"TestScenario/"))-1

    # Need also to flush the existing data
    for name in os.listdir(object_path+"Data/"):
        filename,fileextension = os.path.splitext(name)
        if fileextension=='.csv':
            os.remove(object_path+"Data/"+name)

    for currTestScenario in range(1,Nscenario+1):
        generate_data(currTestScenario)
        generate_plot(currTestScenario)
    
    return

def generate_data(testScenarioIndex):
    
    print("Test")

    testScenario = importlib.import_module("Component.SolidMechanics.FEM.TetrahedronFEMForceField.TestScenario.test_scenario_"+str(testScenarioIndex))

    param,min_value,max_value,nb,Niter = testScenario.getConfig()

    print("Niter: " + str(Niter))

    for k in range(0,len(param)):
        for w in range(0, nb[k]):
            param_value = min_value[k]+w*(max_value[k]-min_value[k])/(nb[k]-1)

            root = Sofa.Core.Node("root") # Generate the root node     
            testScenario.createScene(root, param_value) # Create the scene graph
            Sofa.Simulation.init(root) # Initialization of the scene graph
            for step in range(Niter[k]):
                print("Simulation step: " +str(step) + "/" + str(Niter))
                Sofa.Simulation.animate(root, root.dt.value)

            Sofa.Simulation.reset(root)

    return 

def generate_plot(testScenarioIndex):

    testScenario = importlib.import_module("Component.SolidMechanics.FEM.TetrahedronFEMForceField.TestScenario.test_scenario_"+str(testScenarioIndex))

    param,min_value,max_value,nb,Niter = testScenario.getConfig()

    fig_error, ax_error = plt.subplots(1,len(param),figsize=(5,5*len(param)))

    for k in range(0,len(param)):

        param_value = list(min_value[k]+w*(max_value[k]-min_value[k])/(nb[k]-1) for w in range(0,nb[k]))
        error = []
        elapsed_time = []
        with open(object_path+"Data/test_scenario_"+str(testScenarioIndex)+".csv",newline = '') as f:
            reader  = csv.reader(f, delimiter=',', quotechar='|')
            for row in reader:
                error.append(float(row[1]))
                elapsed_time.append(float(row[0]))
            

        # ax_error[k].plot(param_value,error,'bo')
        # ax_error[k].set_xlabel(param[k])
        # ax_error[k].set_ylabel('Error')
        # ax_error[k].grid()
        ax_error.plot(param_value,error,'bo')
        ax_error.set_xlabel(param[k])
        ax_error.set_ylabel('Error')
        ax_error.grid()

        fig_error.savefig( object_path+"Data/test_scenario_"+str(testScenarioIndex)+".png", transparent=None, dpi='figure', format=None,
        metadata=None, bbox_inches=None, pad_inches=0.1,
        facecolor='auto', edgecolor='auto', backend=None)


    return