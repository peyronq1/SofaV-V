import Sofa
import importlib

list_objects = ["Component.SolidMechanics.FEM.TetrahedronFEMForceField"]

for k in range(0,len(list_objects)):
    
    lib = importlib.import_module(list_objects[k]+".generate")
    
    lib.generate()