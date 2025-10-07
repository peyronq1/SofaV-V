import Sofa
import numpy as np
from splib3.numerics import Vec3

def createScene(rootNode):
    rootNode.addObject("FreeMotionAnimationLoop")
    rootNode.addObject("GenericConstraintSolver")
    rootNode.addObject("VisualStyle", displayFlags='showBehavior')
    rootNode.gravity.value = [0.0,0.0,0.0]

    modeling = rootNode.addChild('Modeling')
    simulation = rootNode.addChild('Simulation')
    simulation.addObject('EulerImplicitSolver')
    simulation.addObject('SparseLDLSolver')
    simulation.addObject('GenericConstraintCorrection')

    list_beam = []
    list_tipmo = []
    list_mesh = ['cylindre_0p5.vtk','cylindre_0p4.vtk','cylindre_0p3.vtk','cylindre_0p2.vtk','cylindre_0p1.vtk','cylindre_0p08.vtk']
    for k in range(0,len(list_mesh)):

        beam = modeling.addChild("Beam" +str(k))
        beam.addObject('MeshVTKLoader', filename='../../../Mesh/'+list_mesh[k],name="loader"+str(k),translation=[0.0, k*30.0,0.0])
        beam.addObject('MeshTopology', src = "@loader"+str(k))
        beam.addObject('MechanicalObject',showObject=True,showObjectScale = 2.,name='dof')
        beam.addObject('UniformMass',totalMass=0.000001)
        beam.addObject('TetrahedronFEMForceField',youngModulus=1.,poissonRatio=0.0)

        box = beam.addObject('BoxROI',box=[[-0.1, -10.0 + k*30.0, -10.0], [0.1, 10.0 + k*30.0, 10.0]], drawBoxes = True, name = "box")
        box.init()
        beam.addObject('FixedProjectiveConstraint',indices='@box.indices')

        beam.addObject('BoxROI', box=[[100.0-0.1, -10.0 + k*30.0, -10.0], [100.0+0.1, 10.0 + k*30.0, 10.0]], drawBoxes=True, name="box2")
        # box2.init()
        beam.addObject('ConstantForceField', indices='@box2.indices', totalForce = [0.0,0.0,-0.01])

        tip = beam.addChild("TipBarycenter")
        tip_mo = tip.addObject('MechanicalObject',position=[100.0,0.0,0.0], name='tip_mo')
        tip.addObject('BarycentricMapping')

        simulation.addChild(beam)

        list_beam.append(beam)
        print("Tip box indices:")
        print(str(tip_mo.position.value))
        list_tipmo.append(tip_mo)

    rootNode.addObject(ErrorEvaluation(rootNode=rootNode,list_beam=list_beam, list_mo=list_tipmo))

def findMeanPoint(list_points):
    mean_point = Vec3(list_points[0])
    for k in range (1,len(list_points)):
        mean_point += Vec3(list_points[k])
    return mean_point/len(list_points)

class ErrorEvaluation(Sofa.Core.Controller):

    def __init__(self,*args,**kwargs):
        Sofa.Core.Controller.__init__(self,*args,**kwargs)

        self.root_node = kwargs['rootNode']
        self.list_beam = kwargs['list_beam']
        self.list_tipmo = kwargs['list_mo']

        self.pos_z_init = []
        for k in range(0,len(self.list_beam)):
            #pos = self.list_beam[k].dof.position.value
            # self.list_box[k].init()
            # print("Tip box indices:")

            #print(str(self.list_box[k].position.value))
            #mean_pos = findMeanPoint(pos[self.list_box[k].indices.value])
            mean_pos = self.list_tipmo[k].position.value[0]
            self.pos_z_init.append(mean_pos[2])
        print("Simulated data")
        print(str(self.pos_z_init))

        self.list_disp_z = []
        self.list_disp_z_gt = []
        self.time = 0
        self.flag = False

    def onAnimateBeginEvent(self,event):

        if self.time>=0.5 and not self.flag:
            for k in range(0,len(self.list_beam)):
                # Simulated data
                # pos = self.list_beam[k].dof.position.value
                # mean_pos = findMeanPoint(pos[self.list_indices[k]])
                mean_pos = self.list_tipmo[k].position.value[0]
                self.list_disp_z.append(abs(self.pos_z_init[k]-mean_pos[2]))

                # Theoretical data
                r = 5.0
                I = (np.pi*(r**4)/4.0)
                E = 1.0
                F = 1.0e-2
                L = 100.0
                self.list_disp_z_gt.append(F*L**3/(3*E*I))

            print("Simulated data")
            print(str(self.list_disp_z))
            print("Theoretical data")
            print(str(self.list_disp_z_gt))
            self.flag=True

        self.time += self.root_node.dt.value


