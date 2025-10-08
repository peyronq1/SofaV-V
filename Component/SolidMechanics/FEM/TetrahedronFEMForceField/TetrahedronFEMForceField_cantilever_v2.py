import Sofa
import numpy as np
from splib3.numerics import Vec3

def getConfig():
    # list of parameters to be varied
    param = ["Meshfile density"]
    # minimum value, per parameter
    min = [0.1]
    # maximum value, per parameter
    max = [0.5]
    # number of samples
    nb = [5]
    # number of simulation iterations
    Niter = [10]

    return param,min,max,nb,Niter

def createScene(rootNode, param):

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
    ])
    rootNode.addObject('RequiredPlugin', name='CSparseSolvers')

    rootNode.addObject("FreeMotionAnimationLoop")
    rootNode.addObject("GenericConstraintSolver")
    rootNode.addObject("VisualStyle", displayFlags='showBehavior')
    rootNode.gravity.value = [0.0,0.0,0.0]

    modeling = rootNode.addChild('Modeling')
    simulation = rootNode.addChild('Simulation')
    simulation.addObject('EulerImplicitSolver')
    simulation.addObject('SparseLDLSolver')
    simulation.addObject('GenericConstraintCorrection')
    
    beam = modeling.addChild("Beam")
    beam.addObject('MeshVTKLoader', filename='Component/SolidMechanics/FEM/TetrahedronFEMForceField/Mesh/cylindre_0p'+str(int(param*10)) + '.vtk',name="loader",translation=[0.0, 0.0,0.0])
    beam.addObject('MeshTopology', src = "@loader")
    beam.addObject('MechanicalObject',showObject=True,showObjectScale = 2.,name='dof')
    beam.addObject('UniformMass',totalMass=0.000001)
    beam.addObject('TetrahedronFEMForceField',youngModulus=1.,poissonRatio=0.0)

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

    print("Tip box indices:")
    print(str(tip_mo.position.value))

    rootNode.addObject(ErrorEvaluation(rootNode=rootNode, tip_mo = tip_mo))

def findMeanPoint(list_points):
    mean_point = Vec3(list_points[0])
    for k in range (1,len(list_points)):
        mean_point += Vec3(list_points[k])
    return mean_point/len(list_points)

class ErrorEvaluation(Sofa.Core.Controller):

    def __init__(self,*args,**kwargs):
        Sofa.Core.Controller.__init__(self,*args,**kwargs)

        self.root_node = kwargs['rootNode']
        self.tip_mo = kwargs['tip_mo']

        mean_pos = self.tip_mo.position.value[0]
        self.pos_z_init = mean_pos[2]
        print("Simulated data")
        print(str(self.pos_z_init))

        self.disp_z = []
        self.disp_z_gt = []
        # self.time = 0
        self.iter = 0
        self.flag = False

        param,min,max,nb,Niter = getConfig()
        self.Niter = Niter[0]

    def onAnimateBeginEvent(self,event):

        if self.iter>=self.Niter and not self.flag:
            # Simulated data
            # pos = self.list_beam[k].dof.position.value
            # mean_pos = findMeanPoint(pos[self.list_indices[k]])
            mean_pos = self.tip_mo.position.value[0]
            self.disp_z = abs(self.pos_z_init-mean_pos[2])

            # Theoretical data
            r = 5.0
            I = (np.pi*(r**4)/4.0)
            E = 1.0
            F = 1.0e-2
            L = 100.0
            self.disp_z_gt.append(F*L**3/(3*E*I))

            print("Simulated data")
            print(str(self.disp_z))
            print("Theoretical data")
            print(str(self.disp_z_gt))
            self.flag=True

        # self.time += self.root_node.dt.value
        self.iter += 1 


