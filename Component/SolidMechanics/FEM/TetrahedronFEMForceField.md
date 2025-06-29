# TetrahedronFEMForceField

## Case study 1: Cantilever beam - bending

### Description

A cantilever beam is a beam, so an elastic body at least 10 times longer in one direction than the others, which is clamped at one end. In this scenario, we consider a force to be applied at the tip of the beam.

### Groundtruth

Could be analytical (mention the assumptions and equations), numerical (mention the algorithms, git repo, or database where the data are stored) or experimental (mention the database where the data are stored)

Type: Analytical

Assumptions:
* Beam assumptions: slender elastic body that can be defined by a centerline and composed of of non-deformable cross-sections
* The beam position is fixed at (0,0) at the base
* A force with a constant orientation and magnitude is applied at the tip
* The deformations are small: the non-linearities due to the beam orientation are negligible 
* The beam is incompressible
* The material is isotropic, linear and elastic

Equations:

We assume the beam deforms in the $(x,z)$ plane and is aligned with the $x$ axis at rest. For a tip force in the $(0,-1)$ direction, the vertical displacement at the tip $\Delta p_z$ of the beam is:
$$ \Delta p_z = \frac{F L^3}{3 E I} $$
where:
* $F$ is the tip force magnitude in N
* $L$ is the beam length in m
* $E$ is the Young's modulus of the beam material in Pa
* $I$ is the second moment of area of the beam's cross section in m $^4$. For a circular cross-section of radius $r$, $I=\pi r^4/4$

### Scene

Description:

Error metrics:


### Results