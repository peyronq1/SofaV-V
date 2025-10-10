import Sofa
import importlib
import os
import matplotlib.pyplot as plt
import csv

object_path = "Static/LinearElastic/Bending/CantileverBeam/"

def generate():
    # Need to scan all the test scenario in the TestScenario folder and generate the corresponding data
    # the -1 is for not considering the pycache folder
    Nscene = len(os.listdir(object_path+"TestScenes/"))-1

    # Need also to flush the existing data
    for name in os.listdir(object_path+"Data/"):
        filename,fileextension = os.path.splitext(name)
        if fileextension=='.csv':
            os.remove(object_path+"Data/"+name)

    for currTestScene in range(1,Nscene+1):
        generate_data(currTestScene)
        generate_plot(currTestScene)
    
    return

def generate_data(testSceneIndex):
    
    print("Test")

    testScene = importlib.import_module("Static.LinearElastic.Bending.CantileverBeam.TestScenes.test_scene_"+str(testSceneIndex))

    name,nom_value,min_value,max_value,nb,Niter = testScene.getConfig()

    print("Niter: " + str(Niter))

    for k in range(0,len(name)):
        param = nom_value.copy()
        for w in range(0, nb[k]):
            param_value = min_value[k]+w*(max_value[k]-min_value[k])/(nb[k]-1)
            param[k] = param_value
            
            root = Sofa.Core.Node("root") # Generate the root node     
            testScene.createScene(root, k, param) # Create the scene graph
            Sofa.Simulation.init(root) # Initialization of the scene graph
            for step in range(Niter[k]):
                print("param = "+str(nom_value))
                print("w = " +str(w) + "/" + str(nb[k]))
                print("Simulation step: " +str(step) + "/" + str(Niter[k]))
                Sofa.Simulation.animate(root, root.dt.value)

            Sofa.Simulation.reset(root)

    return 

def generate_plot(testSceneIndex):

    testScene = importlib.import_module("Static.LinearElastic.Bending.CantileverBeam.TestScenes.test_scene_"+str(testSceneIndex))

    name,nom_value,min_value,max_value,nb,Niter = testScene.getConfig()

    
    for k in range(0,len(name)):

        fig_error, ax_error = plt.subplots(1,2,figsize=(10,5))

        param_value = list(min_value[k]+w*(max_value[k]-min_value[k])/(nb[k]-1) for w in range(0,nb[k]))
        error = []
        elapsed_time = []
        with open(object_path+"Data/test_scene_"+str(testSceneIndex)+"_"+str(k+1)+".csv",newline = '') as f:
            reader  = csv.reader(f, delimiter=',', quotechar='|')
            for row in reader:
                error.append(float(row[1]))
                elapsed_time.append(float(row[0]))


        ax_error[0].plot(param_value,error,'bo')
        ax_error[0].set_xlabel(name[k])
        ax_error[0].set_ylabel('Error')
        ax_error[0].grid()

        ax_error[1].plot(param_value,elapsed_time,'bo')
        ax_error[1].set_xlabel(name[k])
        ax_error[1].set_ylabel('Computation time per iteration (ms)')
        ax_error[1].grid()

        fig_error.savefig( object_path+"Data/test_scene_"+str(testSceneIndex)+"_"+str(k+1)+".png", transparent=None, dpi='figure', format=None,
        metadata=None, bbox_inches=None, pad_inches=0.1,
        facecolor='auto', edgecolor='auto', backend=None)


    return