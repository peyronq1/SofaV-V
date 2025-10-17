
import case_studies
import os
import importlib

if __name__ ==  "__main__":

    list_caseStudies = case_studies.get_list()

    # Generate the table of content

    toc = ""
    toc += "| Case study | Name | Test scene | Name | \n"
    toc += "| ---------- | ---- | ---------- | ---- | \n"

    for k in range(0,len(list_caseStudies)):

        caseStudy = list_caseStudies[k]

        Nscene = len(caseStudy.test_scenes)

        toc += "| " + str(caseStudy.id) + " | " + caseStudy.path+' '+caseStudy.name + " | | | \n"

        for w in range(0,Nscene):

            testScene = caseStudy.test_scenes[w]

            toc += "| |  | " + str(w+1) + " | " + testScene.name + " | \n"
    
    # Read the current main documentation, remove the table of content
    actualDoc = ""
    with open('./README.md',newline='') as f:
        actualDoc = f.read()
    
    index = actualDoc.find("## Case studies and test scenario")

    newDoc = actualDoc[0:index+35]
    newDoc += toc
    
    with open('./README.md', 'w', newline='') as f:
        f.write(newDoc)
