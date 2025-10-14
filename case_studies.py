import Utils.classes as utils
import importlib

# def get_list():
#     list_testScenarios = ["Static.LinearElastic.Bending.CantileverBeam",
#                           "Static.LinearElastic.Bending.ForceFollower",
#                           "Static.LinearElastic.Extension.CantileverBeam"]
#     return list_testScenarios

def get_list():

    id = 1
    name = "CantileverBeam"
    path = "Static/LinearElastic/Bending/"
    include_path = path.replace('/','.')
    caseStudy_current = importlib.import_module(include_path+name+".case_study")
    case1 = caseStudy_current.CaseStudy(name=name, path=path, include_path=include_path, id =id)

    # name = "ForceFollower"
    # path = "Static/LinearElastic/Bending/"
    # include_path = "Static.LinearElastic.Bending."
    # id = 2
    # test_scenes = []
    # case2 = utils.CaseStudyTemplate(name=name, path=path, include_path=include_path, id =id, test_scenes = test_scenes)

    # name = "CantileverBeam"
    # path = "Static/LinearElastic/Extension/"
    # include_path = "Static.LinearElastic.Extension."
    # id = 3
    # test_scenes = []
    # case3 = utils.CaseStudyTemplate(name=name, path=path, include_path=include_path, id =id, test_scenes = test_scenes)

    return [case1]