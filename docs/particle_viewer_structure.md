# Particle Viewer:
The particle viewer is a particle filter visualiser, written in PyQT. This should have significant perofrmance improvements over a graohing solution like MatPlotLib. Its also an excuse for me (jack) to learn some PyQt.

## Basic Structure - V2:
Particle filters have lots of different hypotheses of the same objects position in space. In code this means that the graphics engine needs to desplay a lot of identical objects, drawn with slightly different attributes. Initially, the particle visualiser was structured like this:

The simple approach, of assigning each particle a seperate QGraphicsItem object have been too slow, so we need to try some other approaches, I'll list them below:

1. Cloud-based drawing. We keep the particle cloud classes, but the draw function should be included in the cloud class, and is responsible for drawing all possible hypotheses in that cloud. This should lead to some speed up.

2. Detection-type based drawing monolith: A single object that draws ALL particles of a particular type. E.G. All blue cones, no matter what the landmark.

1 is easier to implement and reason about, but reduces the number of seperate particles from 20,000 to 100 or so. It also introduces signifcantly more complex draw functions, which could slow our function down even more.

2 will be the fastest (I think), but the complexity of batching all 


```mermaid
classDiagram
```
