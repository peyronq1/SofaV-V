import Component.SolidMechanics.FEM.TetrahedronFEMForceField.TetrahedronFEMForceField_cantilever_v2 as case1
import Sofa

def generate():

    print("Test")

    param,min_value,max_value,nb,Niter = case1.getConfig()

    print("Niter: " + str(Niter))

    for k in range(0,len(param)):
        for w in range(0, nb[k]):
            param_value = min_value[k]+k*(max_value[k]-min_value[k])

            root = Sofa.Core.Node("root") # Generate the root node     
            case1.createScene(root, param_value) # Create the scene graph
            Sofa.Simulation.init(root) # Initialization of the scene graph
            for step in range(Niter[k]):
                Sofa.Simulation.animate(root, root.dt.value)

            Sofa.Simulation.reset(root)

    return 