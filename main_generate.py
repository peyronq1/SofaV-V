import Sofa
import importlib
import sys
import case_studies


if __name__ == "__main__":
    list_testScenarios = case_studies.get_list()

    indexCaseStudy = int(sys.argv[1])
    indexTestScene = int(sys.argv[2])
        
    lib = importlib.import_module(list_testScenarios[indexCaseStudy-1]+".generate")
        
    lib.generate_testScene(indexTestScene)