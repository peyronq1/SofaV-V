import numpy as np
from Utils.classes import CaseStudyTemplate
import Sofa
import matplotlib.pyplot as plt
import csv

class CaseStudy(CaseStudyTemplate):

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        self.set_parameters()

    def generate_data(self, testSceneIndex):

        testScene = self.test_scenes[testSceneIndex-1]

        for k in range(0,len(testScene.param_name)):
            param = testScene.nom.copy()
            for w in range(0, testScene.nb[k]):
                param_value = testScene.min[k]+w*(testScene.max[k]-testScene.min[k])/(testScene.nb[k]-1)
                param[k] = param_value

                caseStudy_path = self.path+self.name
                
                root = Sofa.Core.Node("root") # Generate the root node     
                # testScene.createScene(root, caseStudy_param, k, param, caseStudy_path) # Create the scene graph
                testScene.createScene(root, self.param, k, param, caseStudy_path) # Create the scene graph
                Sofa.Simulation.init(root) # Initialization of the scene graph
                for step in range(0,testScene.Niter[k]):
                    print("param value = "+str(param_value))
                    print("w = " +str(w+1) + "/" + str(testScene.nb[k]))
                    print("Simulation step: " +str(step+1) + "/" + str(testScene.Niter[k]))
                    Sofa.Simulation.animate(root, root.dt.value)

                Sofa.Simulation.reset(root)

        return 

    def generate_plot(self, testSceneIndex):

        gt_value = self.compute_groundtruth()

        testScene = self.test_scenes[testSceneIndex-1]
        
        for k in range(0,len(testScene.param_name)):

            fig_error, ax_error = plt.subplots(1,2,figsize=(10,5))

            param_value = list(testScene.min[k]+w*(testScene.max[k]-testScene.min[k])/(testScene.nb[k]-1) for w in range(0,testScene.nb[k]))
            error = []
            elapsed_time = []
            with open(self.path+self.name + "/Data/test_scene_"+str(testSceneIndex)+"_"+str(k+1)+".csv",newline = '') as f:
                reader  = csv.reader(f, delimiter=',', quotechar='|')
                for row in reader:
                    error.append(self.compute_error(gt_value,float(row[1])))
                    elapsed_time.append(float(row[0]))


            ax_error[0].plot(param_value,error,'bo')
            ax_error[0].set_xlabel(testScene.param_name[k])
            ax_error[0].set_ylabel('Error ('+self.error_unit+')')
            ax_error[0].grid()

            ax_error[1].plot(param_value,elapsed_time,'bo')
            ax_error[1].set_xlabel(testScene.param_name[k])
            ax_error[1].set_ylabel('Mean computation time per iteration (s)')
            ax_error[1].grid()

            fig_error.savefig(self.path+self.name +"/Data/test_scene_"+str(testSceneIndex)+"_"+str(k+1)+".png", transparent=None, dpi='figure', format=None,
            metadata=None, bbox_inches=None, pad_inches=0.1,
            facecolor='auto', edgecolor='auto', backend=None)

    
    def set_parameters(self):
        name = ["Force","Young's modulus","Length","Cross-section width"]
        F = 100.0
        E = 50.0
        L = 100.0
        r = 5.0
        self.param_name = name
        self.param = [F,E,L,r]

    def compute_groundtruth(self):
        F = self.param[0]
        E = self.param[1]
        L = self.param[2]
        r = self.param[3]

        A = r**2
        disp = F*L/(E*A)

        return disp

    def compute_error(self,gt_value,sim_value):

        self.error_unit = "%"
        return abs(sim_value-gt_value)*100.0/abs(gt_value)

