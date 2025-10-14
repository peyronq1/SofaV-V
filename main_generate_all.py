import Sofa
# import importlib
import case_studies


if __name__ == "__main__":
    
    list_caseStudies = case_studies.get_list()

    for k in range(0,len(list_caseStudies)):
        
        # lib = importlib.import_module(list_testScenarios[k]+".generate")
        
        caseStudy = list_caseStudies[k]
        caseStudy.generate()