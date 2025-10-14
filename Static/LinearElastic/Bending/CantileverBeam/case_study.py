import numpy as np

def get_scenario_id():

    index = 1
    return index

def get_parameters():
    name = ["Force","Young's modulus","Length","Cross-section width"]
    F = 0.01
    E = 50.0
    L = 100.0
    r = 5.0
    value = [F,E,L,r]
    return name,value

def generate_groundtruth(param):
    F = param[0]
    E = param[1]
    L = param[2]
    r = param[3]

    I = (r**4)/12
    disp = F*(L**3)/(3*E*I)

    return disp

def generate_error(gt_value,sim_value):
    
    return abs(sim_value-gt_value)*100.0/abs(gt_value)