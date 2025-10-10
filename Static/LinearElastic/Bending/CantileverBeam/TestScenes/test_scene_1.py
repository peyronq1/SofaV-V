
#--------------------------------- Test scenario 1 --------------------------
#--------------------------------- Cantilever Beam --------------------------
# ---------------------------------------------------------------------------
# Author: Quentin Peyron

import Sofa
import numpy as np
from splib3.numerics import Vec3
import csv
import time

object_path = "Static/LinearElastic/Bending/CantileverBeam/"

#----------------------------- The configuration function --------------------

def getConfig():
    # list of parameters to be varied
    name = ["Number of elements along x", "Number of elements along y,z"]
    # nominal value, per parameter
    nom = [10,5]
    # minimum value, per parameter
    min = [10,2]
    # maximum value, per parameter
    max = [110,22]
    # number of samples
    nb = [10,10]
    # number of simulation iterations
    Niter = [30,30]

    return name,nom,min,max,nb,Niter

#----------------------------- The scene creation --------------------

def createScene(rootNode, param_idx, param):

    # Unpack parameter vector
    Nx = int(param[0])
    Ne = int(param[1])

    rootNode.addObject('RequiredPlugin', name='SoftRobots')
    rootNode.addObject('RequiredPlugin', name='SofaPython3')
    rootNode.addObject('RequiredPlugin', pluginName=[
        "Sofa.Component.AnimationLoop",  # Needed to use components FreeMotionAnimationLoop
        "Sofa.Component.Constraint.Lagrangian.Correction",  # Needed to use components GenericConstraintCorrection
        "Sofa.Component.Constraint.Lagrangian.Solver",  # Needed to use components GenericConstraintSolver
        "Sofa.Component.Constraint.Projective",  # Needed to use components PartialFixedProjectiveConstraint
        "Sofa.Component.Engine.Select",  # Needed to use components BoxROI
        "Sofa.Component.IO.Mesh",  # Needed to use components MeshSTLLoader, MeshVTKLoader
        "Sofa.Component.LinearSolver.Direct",  # Needed to use components SparseLDLSolver
        "Sofa.Component.LinearSolver.Iterative",  # Needed to use components ShewchukPCGLinearSolver
        "Sofa.Component.Mass",  # Needed to use components UniformMass
        "Sofa.Component.ODESolver.Backward",  # Needed to use components EulerImplicitSolver
        "Sofa.Component.SolidMechanics.FEM.Elastic",  # Needed to use components TetrahedronFEMForceField
        "Sofa.Component.Topology.Container.Constant",  # Needed to use components MeshTopology
        "Sofa.Component.Visual",  # Needed to use components VisualStyle
        "Sofa.Component.StateContainer",
        "Sofa.Component.Mapping.Linear",
        "Sofa.Component.MechanicalLoad",
        "Sofa.GL.Component.Rendering3D",  # Needed to use components OglModel
        "Sofa.Component.Topology.Container.Dynamic",
        "Sofa.Component.Topology.Container.Grid",
        "Sofa.Component.Topology.Mapping",
    ])
    rootNode.addObject('RequiredPlugin', name='CSparseSolvers')

    rootNode.addObject("FreeMotionAnimationLoop")
    rootNode.addObject("GenericConstraintSolver")
    rootNode.addObject("VisualStyle", displayFlags='showBehavior')
    rootNode.gravity.value = [0.0,0.0,0.0]

    modeling = rootNode.addChild('Modeling')
    simulation = rootNode.addChild('Simulation')
    simulation.addObject('EulerImplicitSolver',firstOrder = True)
    simulation.addObject('SparseLDLSolver')
    simulation.addObject('GenericConstraintCorrection')

    beam = modeling.addChild("Beam")

    # Create a regular tetrahedron mesh with controlled number of element in the 3 dimensiosn
    topo = beam.addObject('RegularGridTopology', name='grid', n = [Nx,Ne+1,Ne+1], min = [0.0,-5.0/2,-5.0/2], max = [100.0,5.0/2,5.0/2])
    topo.init()

    beam.addObject('TetrahedronSetTopologyContainer', name= 'container', position=topo.position.value)
    beam.addObject('TetrahedronSetTopologyModifier')
    beam.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3")
    beam.addObject('Hexa2TetraTopologicalMapping', input="@grid", output="@container")

    # Physical properties
    beam.addObject('MechanicalObject',showObject=True,showObjectScale = 2.,name='dof')
    beam.addObject('UniformMass',totalMass=0.001)
    beam.addObject('TetrahedronFEMForceField',youngModulus=50.,poissonRatio=0.0)

    box = beam.addObject('BoxROI',box=[[-0.1, -10.0 + 0.0, -10.0], [0.1, 10.0 + 0.0, 10.0]], drawBoxes = True, name = "box")
    box.init()
    beam.addObject('FixedProjectiveConstraint',indices='@box.indices')

    beam.addObject('BoxROI', box=[[100.0-0.1, -10.0 + 0.0, -10.0], [100.0+0.1, 10.0 + 0.0, 10.0]], drawBoxes=True, name="box2")
    # box2.init()
    beam.addObject('ConstantForceField', indices='@box2.indices', totalForce = [0.0,0.0,-0.01])

    tip = beam.addChild("TipBarycenter")
    tip_mo = tip.addObject('MechanicalObject',position=[100.0,0.0,0.0], name='tip_mo')
    tip.addObject('BarycentricMapping')

    simulation.addChild(beam)

    rootNode.addObject(ErrorEvaluation(rootNode=rootNode, tip_mo = tip_mo, param_idx=param_idx))

#----------------------------- The controller for the data generation --------------------


class ErrorEvaluation(Sofa.Core.Controller):

    def __init__(self,*args,**kwargs):
        Sofa.Core.Controller.__init__(self,*args,**kwargs)

        self.root_node = kwargs['rootNode']
        self.tip_mo = kwargs['tip_mo']
        self.param_idx = kwargs['param_idx']

        mean_pos = self.tip_mo.position.value[0]
        self.pos_z_init = mean_pos[2]

        self.disp_z = 0
        self.disp_z_gt = 0
        # self.time = 0
        self.iter = 0
        self.flag = False

        self.prev_time = time.time()

        name,nom,min,max,nb,Niter = getConfig()
        self.Niter = Niter[0]

    def onAnimateBeginEvent(self,event):

        elaspsed_time = time.time()-self.prev_time
        self.prev_time = time.time()
        # print("prevTime = "+str(self.prev_time))

        if self.iter>=self.Niter-2 and not self.flag:

            mean_pos = self.tip_mo.position.value[0]
            self.disp_z = abs(self.pos_z_init-mean_pos[2])

            # Theoretical data
            e = 5.0
            I = (e**4)/12.0
            E = 50.0
            F = 1.0e-2
            L = 100.0
            self.disp_z_gt = F*L**3/(3*E*I) 

            error = abs(self.disp_z-self.disp_z_gt)*100.0/abs(self.disp_z_gt)

            print("Simulated data")
            print(str(self.disp_z))
            print("Theoretical data")
            print(str(self.disp_z_gt))

            
            # Add the new data to the existing data file, or create the data file

            data = []

            try:
                f = open(object_path + 'Data/test_scene_1_'+str(self.param_idx+1)+'.csv', newline='')
            except FileNotFoundError:
                data = []
            else:
                # with open(object_path + 'Data/test_scenario_1.csv' , newline='') as f:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                for row in reader:
                    data_row = []
                    print("Row length: "+str(len(row)))
                    for k in range(0,len(row)):
                        data_row.append(float(row[k]))
                    data.append(data_row)

            data.append([elaspsed_time, error])

            with open(object_path + 'Data/test_scene_1_'+str(self.param_idx+1)+'.csv' , 'w', newline='') as f:
                # using csv.writer method from CSV package
                write = csv.writer(f, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                
                for k in range(0,len(data)):
                    write.writerow(data[k])

            self.flag=True

        self.iter += 1 


