from particles import Particles

from PyQt5.QtWidgets import (QGraphicsView, 
                             QGraphicsScene, 
                             )
from particle_cloud import ParticleCloud

from vehicle_cloud import (
        create_direction_particle,
        update_direction_particle, 
                        )

from landmark_cloud import (
        create_landmark_mean_dot,
        update_landmark_mean_dot
        )
import numpy as np
from functools import partial




PARTICLE_ERROR = np.array((1.5, 1.5, 0.2))

def create_direction_particle_cloud(
        data: Particles
        ) -> ParticleCloud:
    particle_cloud = ParticleCloud(
            data,
            create_direction_particle,
            update_direction_particle, 
            None,
            None
            )

    particle_cloud.update_particles()

    return particle_cloud

def create_landmark_particle_cloud(
        data: Particles,
        landmark_index: int
        ) -> ParticleCloud:

    # need to curry this function
    landmark_creation_fn = partial(
            create_landmark_mean_dot,
            landmark_index
            )

    particle_cloud = ParticleCloud(
            data, 
            landmark_creation_fn,
            update_landmark_mean_dot, 
            None,
            None
            )  

    particle_cloud.update_particles()

    return particle_cloud


class ParticleView(QGraphicsView):
    """This draws and then displays our particles on the screen."""
    
    def __init__(self, particles):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.scene.setSceneRect(-3, -3, 6, 6)  
        self.setGeometry(0, 0, 800, 800)
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        self.clouds = []
   
    def wheelEvent(self, event):
        """Enable zoom with mouse wheel."""
        scale_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(scale_factor, scale_factor)
        else:
            self.scale(1/scale_factor, 1/scale_factor)

    def add_cloud(self, cloud: ParticleCloud):
        """Add a named particle cloud to the scene."""
        # Remove existing cloud with same name if present
        
        # Add to scene and store
        self.scene.addItem(cloud.group)
        self.clouds.append(cloud)

    def update_clouds(self):
        for cloud in self.clouds:
            cloud.update_particles()
        
        # Initial update


