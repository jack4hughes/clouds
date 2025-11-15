
from particles import Particle, Particles, get_landmark_cov  
from PyQt5.QtWidgets import (QGraphicsItem,
                             QGraphicsItemGroup
                             )
import numpy as np
from typing import Callable, Dict

from PyQt5.QtGui import QBrush, QPen, QPainter, QPolygonF, QTransform 
from PyQt5.QtCore import Qt, QPointF, QRectF
import numpy as np
from particles import Particles


class BatchedParticleCloud(QGraphicsItem):
    """A class that handles the displaying of a set of particles. MORE INFO HERE.

    Attributes:
    data: The particle data class that we are drawing.
    color config: This will be a dict with a pen and brush.""" 
    def __init__(
            self,
            data: Particles,
            color_config: Dict
            ):
        super().__init__()
        
        # initialise model.
        self.data = data
        self.color_config = color_config
    
    def paint(self, painter, option, widget):
        raise NotImplementedError("""This is just an abstract class! It has no paint function. 

You can inherit from this class and define a paint statement.""")


class BatchedVehicleCloud(BatchedParticleCloud):
    def __init__(
            self,
            data: Particles,
            height: float,
            triangle_ratio: float,
            color_config: Dict

            ):
        super().__init__(data, None)
        self.points = [QPointF(0., 0.) for point in range(self.data.number_of_particles)]

        self.base_triangle = self.__create_base_triangle(height, triangle_ratio)
        self.triangle_ratio = triangle_ratio
        # allocates transforms so they can be accessed later.!
        self.transforms = [QTransform() for i in range(self.data.number_of_particles)]

        self.current_scale = 1
        self.screen_height = height

    def update_positions(self):
        relative_positions = self.data.get_relative_positions()
        for point, position in zip(self.points, relative_positions):
            print(point)
            print(position)

    def __create_base_triangle(self, height, base_ratio):
        """A helper function that makes the creation of a base triangle easier. 

        Could probably just put this inside __init__ and save a few cycles if you care about them!"""

        width = height * base_ratio
        p1 = QPointF(0., 0.)           # tip
        p2 = QPointF(-width, height/2)  # Bottom left
        p3 = QPointF(-width, -height/2)   # Bottom right

        return QPolygonF([p1, p2, p3])


    def boundingRect(self):
        bounding_rect = self.data.get_bounding_rect()
        return QRectF(
        QPointF(bounding_rect[0][0], bounding_rect[0][1]),  # min point
        QPointF(bounding_rect[1][0], bounding_rect[1][1])   # max point
    )


    def update_transforms(self):
        for i, particle in enumerate(self.data):
            x, y, theta = particle.pose

            #This should transform the base shape (a triangle) and show it easily.
            transform = self.transforms[i]
            transform.translate(x, y)
            transform.rotateRadians(theta)

            self.transforms[i] = transform #Do we need this? Might be passed as a reference here, but im being explicit.

    
    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QBrush(Qt.GlobalColor.red))
        painter.setPen(QPen(Qt.PenStyle.NoPen))  # No outline
        
        self.update_transforms() #might not be needed here!
        
        for transform in self.transforms:

            painter.save()
            painter.setTransform(transform, True)
            painter.drawPolygon(self.base_triangle)
            painter.restore()


    def update_scale(self, view_scale):
        """Call this when the view scale changes

        -VIBECODED, need to profile and test.."""
        if abs(view_scale - self.current_scale) > 0.01:  # Avoid unnecessary updates
            self.current_scale = view_scale
            # Create triangle with compensated size
            world_height = self.screen_height / view_scale
            self.base_triangle = self.__create_base_triangle(world_height, self.triangle_ratio)
            self.update()  # Trigger repaint


if __name__ == "__main__":
    initial_pose = np.array((0., 0., 0.))
    inital_error = np.array(((1., 1., np.pi/16)))
    particles = Particles(10, initial_pose, inital_error)
    
    particle_cloud = BatchedVehicleCloud(particles, 10, 3, None)
    print(particle_cloud)
    print(particles.poses)

