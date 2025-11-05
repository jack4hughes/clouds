"""
This file holds the logic for our ellipse drawer and mean position drawer

MEAN PARTICLE DRAWER:
This is a class that draws the mean position of a landmark. This simply tells us the point that the landmark is most likely to be. You can use

ELLIPSE DRAWER: NOT IMPLEMENTED!
his draws an "uncertanty ellipse". This is an area we can be 95% certian that a landmark would be in, given a gaussian probability distribution, and our prior guess about the robots current position being in the right place.

This class is only concerned with drawing these ellipses, not calculating or storing them. Please go to particles.py for the storage implementation, and read robablisitic Robotics (Thrun et al.) for fastSLAM implementation details.


Most of this is vibe coded right now: use with caution!

TODO:
Full analysis of Claudes first draft -- Need to remove Chi Squared calculation within this class so we dont do it thousands of times per update loop! Insstead do it in clouds object.
Will come back to it when I have more time, wanted to check the mutability of objects and functions in particle_viewer.

Chi-Squared calculator allowing for more distinct values for p.
"""

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt
import numpy as np
from dataclasses import dataclass
from particles import Particle

# Define constants.
DEFAULT_CONFIDENCE_THRESHOLD = 0.95
DEFAULT_CHI_SQUARED_VALUE = 5.991  # Two sigma.
DEFAULT_LM_MEAN = np.array((0, 0))
DEFAULT_LM_COVARIANCE = np.eye(2, 2) * 50
DEFAULT_LM_AXES_SIZE = np.array((1, 1))
DEFAULT_LM_ANGLE = 0

DEFAULT_LM_DOT_SIZE = 5.0  # This wont change on zoom-in, so might need to increase!


# Handle default brushes externally (Think this will be a speed up? but might cause lifetime headaches.)
@dataclass(frozen=True)
class DefaultMeanColors:
    fill = QColor(Qt.blue)
    outline = QColor(Qt.blue)


DEFAULT_LM_DOT_PENCILCASE = {
    "pen": QPen(DefaultMeanColors.fill),
    "brush": QBrush(DefaultMeanColors.outline),
}


class LandmarkMeanDot(QGraphicsEllipseItem):
    def __init__(self, index, lm_pencilcase=DEFAULT_LM_DOT_PENCILCASE):
        self.index = index  # This is the landmark we will be drawing.
        super().__init__(0, 0, DEFAULT_LM_DOT_SIZE, DEFAULT_LM_DOT_SIZE)
        self.setBrush(lm_pencilcase["brush"])
        self.setPen(lm_pencilcase["pen"])

        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)


def create_landmark_mean_dot(
    index, pencilcase=DEFAULT_LM_DOT_PENCILCASE
) -> LandmarkMeanDot:
    """Creates a new landmark mean dot. This is more lightweight than a full ellipse."""

    return LandmarkMeanDot(index, pencilcase)


def update_landmark_mean_dot(particle: Particle, landmark_mean_dot: LandmarkMeanDot):
    """Updates the landmarks position based off data contained within"""
    index = landmark_mean_dot.index
    position = particle.landmarks[index, :]
    landmark_mean_dot.setPos(position[0], -position[1])
