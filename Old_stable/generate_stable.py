import Sofa
import importlib
import os
import matplotlib.pyplot as plt
import csv
import case_studies
import case_study

# caseStudy_path = "Static/LinearElastic/Bending/CantileverBeam/"


list_testScenarios = case_studies.get_list()
caseStudy_path = list_testScenarios[case_study.get_scenario_id()-1].replace('.','/')+'/'
caseStudy = importlib.import_module(list_testScenarios[case_study.get_scenario_id()-1])

# caseStudy = importlib.import_module("Static.LinearElastic.Bending.CantileverBeam.case_study")

# caseStudy = importlib.import_module(caseStudy_path.replace('/','.')+"case_study")

def generate():
    # Need to scan all the test scenario in the TestScenario folder and generate the corresponding data
    # the -1 is for not considering the pycache folder
    Nscene = len(os.listdir(caseStudy_path+"TestScenes/"))-1

    for currTestScene in range(1,Nscene+1):

        generate_testScene(currTestScene)
    
    return

def generate_testScene(testSceneIndex):

    # Need also to flush the existing data
    remove_data(testSceneIndex)

    generate_data(testSceneIndex)
    generate_plot(testSceneIndex)


def generate_data(testSceneIndex):

    name,caseStudy_param = caseStudy.get_parameters()

    testScene = importlib.import_module(caseStudy_path.replace('/','.')+"TestScenes.test_scene_"+str(testSceneIndex))

    name,nom_value,min_value,max_value,nb,Niter = testScene.get_parameters()

    for k in range(0,len(name)):
        param = nom_value.copy()
        for w in range(0, nb[k]):
            param_value = min_value[k]+w*(max_value[k]-min_value[k])/(nb[k]-1)
            param[k] = param_value
            
            root = Sofa.Core.Node("root") # Generate the root node     
            testScene.createScene(root, caseStudy_param, k, param) # Create the scene graph
            Sofa.Simulation.init(root) # Initialization of the scene graph
            for step in range(0,Niter[k]):
                print("param nominal value = "+str(nom_value))
                print("w = " +str(w+1) + "/" + str(nb[k]))
                print("Simulation step: " +str(step+1) + "/" + str(Niter[k]))
                Sofa.Simulation.animate(root, root.dt.value)

            Sofa.Simulation.reset(root)

    return 

def generate_plot(testSceneIndex):

    name,caseStudy_param = caseStudy.get_parameters()
    gt_value = caseStudy.generate_groundtruth(caseStudy_param)

    testScene = importlib.import_module(caseStudy_path.replace('/','.')+"TestScenes.test_scene_"+str(testSceneIndex))

    name,nom_value,min_value,max_value,nb,Niter = testScene.get_parameters()

    
    for k in range(0,len(name)):

        fig_error, ax_error = plt.subplots(1,2,figsize=(10,5))

        param_value = list(min_value[k]+w*(max_value[k]-min_value[k])/(nb[k]-1) for w in range(0,nb[k]))
        error = []
        elapsed_time = []
        with open(caseStudy_path+"Data/test_scene_"+str(testSceneIndex)+"_"+str(k+1)+".csv",newline = '') as f:
            reader  = csv.reader(f, delimiter=',', quotechar='|')
            for row in reader:
                error.append(caseStudy.generate_error(gt_value,float(row[1])))
                elapsed_time.append(float(row[0]))


        ax_error[0].plot(param_value,error,'bo')
        ax_error[0].set_xlabel(name[k])
        ax_error[0].set_ylabel('Error')
        ax_error[0].grid()

        ax_error[1].plot(param_value,elapsed_time,'bo')
        ax_error[1].set_xlabel(name[k])
        ax_error[1].set_ylabel('Computation time per iteration (s)')
        ax_error[1].grid()

        fig_error.savefig( caseStudy_path+"Data/test_scene_"+str(testSceneIndex)+"_"+str(k+1)+".png", transparent=None, dpi='figure', format=None,
        metadata=None, bbox_inches=None, pad_inches=0.1,
        facecolor='auto', edgecolor='auto', backend=None)


    return

def remove_data(testSceneIndex):

    testScene = importlib.import_module(caseStudy_path.replace('/','.')+"TestScenes.test_scene_"+str(testSceneIndex))

    name,nom_value,min_value,max_value,nb,Niter = testScene.get_parameters()

    for k in range(0,len(name)):
        try:
            f = open(caseStudy_path + 'Data/test_scene_'+str(testSceneIndex)+'_'+str(k+1)+'.csv', newline='')
        except FileNotFoundError:
            return
        else:
            os.remove(caseStudy_path + 'Data/test_scene_'+str(testSceneIndex)+'_'+str(k+1)+'.csv')

    return

def remove_data_all():

    # Need also to flush the existing data
    for name in os.listdir(caseStudy_path+"Data/"):
        filename,fileextension = os.path.splitext(name)
        if fileextension=='.csv':
            os.remove(caseStudy_path+"Data/"+name)