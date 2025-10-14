
import case_studies
import os
import importlib

if __name__ ==  "__main__":

    list_testScenarios = case_studies.get_list()

    # Generate the table of content

    toc = ""
    toc += "| Case study | Name | Test scene | Name | \n"
    toc += "| ---------- | ---- | ---------- | ---- | \n"

    for k in range(0,len(list_testScenarios)):

        caseStudy_path = list_testScenarios[k].replace('.','/')

        Nscene = len(os.listdir(caseStudy_path+"/TestScenes/"))-1

        toc += "| " + str(k) + " | " + list_testScenarios[k] + " | | | \n"

        for w in range(0,Nscene):

            testScene = importlib.import_module(list_testScenarios[k]+".TestScenes.test_scene_"+str(w+1))

            toc += "| |  | " + str(w+1) + " | " + testScene.get_name() + " | \n"
    
    # Read the current main documentation, remove the table of content
    actualDoc = ""
    with open('./README.md',newline='') as f:
        actualDoc = f.read()
    
    index = actualDoc.find("## Case studies and test scenario")

    newDoc = actualDoc[0:index+35]
    newDoc += toc
    
    with open('./README.md', 'w', newline='') as f:
        f.write(newDoc)
