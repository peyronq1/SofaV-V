import importlib
import os

class CaseStudyTemplate:

    def __init__(self,*args,**kwargs):

        self.name = kwargs["name"]
        self.id = kwargs["id"]
        self.path = kwargs["path"]
        self.include_path = kwargs["include_path"]

        Nscene = len(os.listdir(self.path+self.name+"/TestScenes/"))-1
        self.test_scenes = []
        for k in range(0,Nscene):
            dir = importlib.import_module(self.include_path+self.name+".TestScenes.test_scene_"+str(k+1))
            testScene = dir.TestScene()
            self.test_scenes.append(testScene)
        
        self.error_unit = ""
        self.param = []
        self.param_name = []

    def generate(self):
    # Need to scan all the test scenario in the TestScenario folder and generate the corresponding data
    # the -1 is for not considering the pycache folder

        Nscene = len(os.listdir(self.path+self.name+"/TestScenes/"))-1

        for currTestScene in range(1,Nscene+1):

            self.generate_testScene(currTestScene)
        
        return

    def generate_testScene(self, testSceneIndex):

        # Need also to flush the existing data
        self.remove_data(testSceneIndex)

        self.generate_data(testSceneIndex)
        self. generate_plot(testSceneIndex)
    
    def remove_data(self,testSceneIndex):

        # testScene = importlib.import_module(caseStudy_path.replace('/','.')+"TestScenes.test_scene_"+str(testSceneIndex))
        # testScene = importlib.import_module(self.include_path+self.name+".TestScenes.test_scene_"+str(testSceneIndex))
        
        # name,nom_value,min_value,max_value,nb,Niter = testScene.get_parameters()

        testScene = self.test_scenes[testSceneIndex-1]

        for k in range(0,len(testScene.param_name)):
            try:
                f = open(self.path+self.name + '/Data/test_scene_'+str(testSceneIndex)+'_'+str(k+1)+'.csv', newline='')
            except FileNotFoundError:
                return
            else:
                os.remove(self.path+self.name + '/Data/test_scene_'+str(testSceneIndex)+'_'+str(k+1)+'.csv')

        return

    def remove_data_all(self):

        # Need also to flush the existing data
        for name in os.listdir(self.path+self.name+"/Data/"):
            filename,fileextension = os.path.splitext(name)
            if fileextension=='.csv':
                os.remove(self.path+self.name+"/Data/"+name)

    # To be overriden in each specific case study
    def generate_data(self,testSceneIndex):
        return 0
    
    def generate_plot(self,testSceneIndex):
        return 0
    
    def set_parameters(self):
        return 0
    
    def compute_groundtruth(self,param):
        return 0
    
    def compute_error(self,gt_value,sim_value):
        return 0


    
# class TestSceneTemplate:

#     def __init__(self,*args,**kwargs):
        
#         self.name = kwargs["name"]
#         self.param_name = kwargs["param_name"]
#         self.nom = kwargs["norminal_value"]
#         self.min = kwargs["minimum_value"]
#         self.max = kwargs["maximal_value"]
#         self.nb = kwargs["discrete_value_number"]
#         self.Niter = kwargs["iteration_number"]

#     def createScene(self,rootNode):
#         return rootNode
