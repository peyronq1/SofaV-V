import Sofa
import importlib

list_testScenarios = ["Static.LinearElastic.Bending.CantileverBeam"]

for k in range(0,len(list_testScenarios)):
    
    lib = importlib.import_module(list_testScenarios[k]+".generate")
    
    lib.generate()