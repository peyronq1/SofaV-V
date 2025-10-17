
#--------------------------------- Test scenario 3 --------------------------
# Author: Quentin Peyron
#----------------------------------------------------------------------------

import Sofa
import numpy as np
from splib3.numerics import Vec3
import csv
import time

#----------------------------- The description of the test scene --------------------

class TestScene():

    def __init__(self,*args,**kwargs):

        self.name = "Co-rotational FEM with 1D beam elements"

        # list of parameters to be varied
        self.param_name = ["Number of elements along x"]
        # nominal value, per parameter
        self.nom = [10]
        # minimum value, per parameter
        self.min = [2]
        # maximum value, per parameter
        self.max = [50]
        # number of samples
        self.nb = [30]
        # number of simulation iterations
        self.Niter = [30]
        
    #----------------------------- The scene creation --------------------

    def createScene(self,rootNode, cs_param, param_idx, param, caseStudy_path):

        # Unpack test scene parameter vector
        Nx = int(param[0])
        # print("TEST Nx = " + str(Nx))

        # Unpack case study parameter vector
        F = cs_param[0]
        E = cs_param[1]
        L = cs_param[2]
        r = cs_param[3]

        print("param: " + str(cs_param))


        rootNode.addObject('RequiredPlugin', name='SoftRobots')
        rootNode.addObject('RequiredPlugin', name='BeamAdapter')
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

        rootNode.addObject("DefaultAnimationLoop")
        rootNode.addObject("VisualStyle", displayFlags='showBehavior')
        rootNode.gravity.value = [0.0,0.0,0.0]

        modeling = rootNode.addChild('Modeling')
        simulation = rootNode.addChild('Simulation')
        simulation.addObject('EulerImplicitSolver',firstOrder = True)
        simulation.addObject('SparseLDLSolver')

        beam = modeling.addChild("Beam")

        # Create a regular 1D mesh with a controlled number of elements
        topo = beam.addObject('RegularGridTopology', name='grid', n = [Nx,1,1], min = [0.0,0.0,0.0], max = [L,0.0,0.0],drawEdges=False)
        topo.init()

        # Physical properties
        mo = beam.addObject('MechanicalObject',template = 'Rigid3', showObject=True, showObjectScale = 1.0, name='dof', position='@grid.position')
        mo.init()

        # print("TEST topo pos = " + str(topo.position.value))
        # print("TEST mo pos = " + str(mo.position.value))
        
        beam.addObject('BeamInterpolation', name = 'beamInterp', defaultYoungModulus = E,
                         defaultPoissonRatio = 0.,
                         crossSectionShape = 'rectangular',
                         lengthY = r, lengthZ = r)
        beam.addObject('AdaptiveBeamForceFieldAndMass', name = 'beamForceField', computeMass = True, massDensity = 0.000001)

        beam.addObject('FixedProjectiveConstraint',indices=0)

        beam.addObject('ConstantForceField', indices=Nx-1, totalForce = [0.0,0.0,-F])

        simulation.addChild(beam)

        rootNode.addObject(ErrorEvaluation(rootNode=rootNode, beam_mo = mo, param_idx=param_idx, caseStudy_path = caseStudy_path, Niter = self.Niter[param_idx]))

    #----------------------------- The controller for the data generation --------------------


class ErrorEvaluation(Sofa.Core.Controller):

    def __init__(self,*args,**kwargs):
        Sofa.Core.Controller.__init__(self,*args,**kwargs)

        self.root_node = kwargs['rootNode']
        self.beam_mo = kwargs['beam_mo']
        self.param_idx = kwargs['param_idx']
        self.caseStudy_path = kwargs['caseStudy_path']
        self.Niter = kwargs["Niter"]

        # print("position = " +str(self.beam_mo.position.value))
        mean_pos = self.beam_mo.position.value[-1]
        self.pos_z_init = mean_pos[2]

        self.disp_z = 0
        self.disp_z_gt = 0
        # self.time = 0
        self.iter = 0
        self.flag = False

        self.prev_time = time.time()
        self.elapsed_time = []

    def onAnimateBeginEvent(self,event):

        self.elapsed_time.append(time.time()-self.prev_time)
        self.prev_time = time.time()

        if self.iter>=self.Niter-2 and not self.flag:

            mean_pos = self.beam_mo.position.value[-1]
            self.disp_z = abs(self.pos_z_init-mean_pos[2])

            # print("Simulated data")
            # print(str(self.disp_z))
            
            # Add the new data to the existing data file, or create the data file

            data = []

            try:
                f = open(self.caseStudy_path + '/Data/test_scene_3_'+str(self.param_idx+1)+'.csv', newline='')
                # f = open('./../Data/test_scene_3_'+str(self.param_idx+1)+'.csv', newline='')
            except FileNotFoundError:
                data = []
            else:
                reader = csv.reader(f, delimiter=',', quotechar='|')
                for row in reader:
                    data_row = []
                    # print("Row length: "+str(len(row)))
                    for k in range(0,len(row)):
                        data_row.append(float(row[k]))
                    data.append(data_row)

            mean_elapsed_time = np.mean(list(self.elapsed_time[k] for k in range(1,len(self.elapsed_time)-1)))
            data.append([mean_elapsed_time, self.disp_z])

            with open(self.caseStudy_path + '/Data/test_scene_3_'+str(self.param_idx+1)+'.csv' , 'w', newline='') as f:
            # with open('./../Data/test_scene_3_'+str(self.param_idx+1)+'.csv' , 'w', newline='') as f:
                # using csv.writer method from CSV package
                write = csv.writer(f, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                
                for k in range(0,len(data)):
                    write.writerow(data[k])

            self.flag=True

        self.iter += 1 


