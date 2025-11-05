
from particles import Particle, Particles, get_landmark_cov  
from PyQt5.QtWidgets import (QGraphicsItem,
                             QGraphicsItemGroup
                             )
import numpy as np
from typing import Callable


class ParticleCloud:
    """A class that handles the displaying of a set of particles. MORE INFO HERE.

    Attributes:
    data: The particle data class that we are drawing.
    particle_creator: The function in charge of creating particles.
    particle_updater: A function that can update the position of each particle """
    def __init__(
            self,
            particles_data: Particles,
            particle_creator: Callable[[], QGraphicsItem],
            particle_updater: Callable[[Particles, QGraphicsItem], None],
            opacity,
            color
            ):
        
        # initialise model.
        self.data = particles_data

        # initialise creators and updators.
        self.create_fn = particle_creator
        self.update_fn = particle_updater
        
        self.items = []

        # initialise display properties
        self.opacity = opacity
        self.color = color

        # group everything in a view
        self.group = QGraphicsItemGroup()

        self.set_visibility(False) # hides our group while we update everything.

        for _ in range(self.data.number_of_particles): 
            item = self.create_fn() #creates an item for each particle!
            self.items.append(item)
            self.group.addToGroup(item)

        self.set_visibility(True)

    def create_particles(self, number_of_particles, particle_factory):
        """ creates a set of particledisplayitems from the underlying particle data. requires a factory to set up particles in the first place. 

        requires a **particle factory** that is capable of creating a particle, and a **particle updater** that can update specific features of a particle that is already in the cache."""
        
        for particle_data in self.particles_data:
            particle = self.create_fn()
            particle.color = self.color 
            self.items.append(particle)

    def update_particles(self):
        """updates particles current position based off current particle data."""
        for particle_data, particle_view in zip(self.data, self.items):
            self.update_fn(particle_data, particle_view)

    def set_visibility(self, visible):
        self.group.setVisible(visible)
    
    def set_opacity(self, opacity):
        self.group.setOpacity(opacity)

