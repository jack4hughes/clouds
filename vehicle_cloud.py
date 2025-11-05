from particles import Particle
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QBrush, QPen, QPainter, QPolygonF 
from PyQt5.QtCore import Qt, QPointF, QRectF
import numpy as np

class DirectionalParticleItem(QGraphicsItem):
    """This class is used to create a direction particle. A direction particle is anything with a full pose (IE a position and heading. This is represented by an arrow at the moment. The direction particle does not handle movement or uncertanty for now, its only a point. If you want to change how this is displayed, please read the docs! It should be fairly flexible."""
    def __init__(self, x, y, angle, height):
        super().__init__()
        self.height = height
        self.height = 3 * self.height
        self.setPos(x, y)
        self.setRotation(np.degrees(angle))  # Convert radians to degrees
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)

    def boundingRect(self):
        # Fixed bounding box to properly contain the arrow
        # Added small margin to prevent artifacts
        margin = 1
        return QRectF(-self.width - margin, -self.height/2 - margin, 
                      self.width + 2*margin, self.height + 2*margin)
    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        #TODO: This needs to point left by default.
        # Tip at top, base at bottom
        p1 = QPointF(0, 0)           # tip
        p2 = QPointF(-self.width, self.height/2)  # Bottom left
        p3 = QPointF(-self.width, -self.height/2)   # Bottom right

        triangle = QPolygonF([p1, p2, p3])

        # Draw the triangle
        painter.setBrush(QBrush(Qt.GlobalColor.red))
        painter.setPen(QPen(Qt.PenStyle.NoPen))  # No outline
        painter.drawPolygon(triangle)


def create_direction_particle():
    """Creates an uninitialised directional particle. This particle represents anhything with a pose. In our simple example, this represents the robots current pose hypotheses, but you could easilly use it to display the state of other robots/moving objects!"""

    x = 0
    y = 0
    theta = 0

    particle = DirectionalParticleItem(x, y, theta, width=9)
    return particle

def update_direction_particle(particle_data: Particle, particle_view: DirectionalParticleItem):
    x, y, theta = particle_data.pose
    particle_view.setPos(x, -y)
    particle_view.setRotation(np.degrees(-theta))
    

