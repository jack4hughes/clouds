from particles import Particles

from PyQt5.QtWidgets import (QGraphicsView, 
                             QGraphicsScene, 
                             )

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ParticleCloud(QGraphicsItem):
    """This Abstract Class is in charge of drawing our particle clouds on the QGraphicsView map."""
    def __init__(self, data, color_options=None):
        super().__init__()
        self.data = data

    def paint(self, painter, option, widget):
        painter.setPen(QPen("#FFFFFF", 5))
        painter.setBrush(QBrush("FFFFFF"))

    def boundingRect(self):
        pass
        
class ParticleView(QGraphicsView):
    """This draws and then displays our particles on the screen."""
    
    def __init__(self, particles, update_function=None, update_freq=None):
        super().__init__()

        self.update_freq = update_freq
        
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.scene.setSceneRect(-2, -2, 2, 2) 
        self.scale(1/25, 1/25)
        self.setGeometry(0, 0, 800, 800)
        
        self.setDragMode(QGraphicsView.ScrollHandDrag)
         
        self.clouds = []
        self.current_zoom = 1
   
    def add_cloud(self, cloud: ParticleCloud):
        """Add a named particle cloud to the scene."""
        # Remove existing cloud with same name if present
        
        # Add to scene and store
        self.scene.addItem(cloud)
        self.clouds.append(cloud)

    def update_clouds(self):
        for cloud in self.clouds:
            cloud.update_particles()
        
        # Initial update

    def wheelEvent(self, event):
        """Handle mouse wheel for zooming"""
        # Get the zoom factor
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        # Calculate zoom
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        
        # Apply zoom
        self.scale(zoom_factor, zoom_factor)
        
        # Update current zoom level
        self.current_zoom *= zoom_factor
        
        # Update all particle clouds
        for cloud in self.clouds:
            cloud.update_scale(self.current_zoom)
    
    

