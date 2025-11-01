# Particle Viewer:

The particle viewer is a particle filter visualiser, written in PyQT. This should have significant perofrmance improvements over a graohing solution like MatPlotLib. Its also an excuse for me (jack) to learn some PyQt.

## Basic Structure:
Particle filters have lots of different hypotheses of the same objects position in space. In code this means that the graphics engine needs to desplay a lot of identical objects, drawn with slightly different attributes. To do this, follow these steps:

1. Define how a particle should look and behave: This is a child of QGraphicsItem that draws an object. In vehicle_cloud, this is a triangle set up using a QPolygonF object.

2. Create the create and update functions: These functions are used to create and update the particle objects defined in section 1. These are standalone functions. I prefer keeping them separate from the individual particle class, as they can vary quite a bit depending on the kind of shape you use to model your particles in section 1.

3. Create a ParticleCloud: This is a small class that groups particles together in a QGraphicsItemGroup, then handles creating, updating, and destroying them using the functions defined in section 2. This allows us to easily group particles that represent the same object and act on them as a single entity.

4. Add your ParticleCloud to the ParticleViewer class: Add your cloud to the ParticleViewer class. This class creates a graphics scene and links our particle primitives (which we've grouped into clouds) to our data. This means we can call a single update_particles function and easily update all particle positions at once.


```mermaid
classDiagram
```
