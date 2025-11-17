from PyQt5.QtCore import QTimer, QElapsedTimer
from particle_cloud import BatchedVehicleCloud
from particles import Particles, get_landmark_offset, get_landmark_cov, ackermann_motion_update
import sys
import time
import numpy as np
from math import pi

from PyQt5.QtWidgets import QApplication, QShortcut
from particle_viewer import (
        ParticleView,
        )


MODE = "dynamic"
NUMBER_OF_PARTICLES = 200
MAX_LANDMARKS = 100

INITIAL_PARTICLE_POSITION = (0., -0., 0)
PARTICLE_ERROR = np.array((15, 15, 0.8))

ALPHAS = [0.1, 0.1, 0.000001, 0.000001, 0.0000001, 0.0000001]
TEST_VELOCITY = (200, 0.1)

SENSOR_COVARIANCE = np.array(((0.3, 0.2), (0.2, 0.5)))
POLAR_LANDMARK_DETECTION = np.array((55., pi/2))


app = QApplication(sys.argv)
particles = Particles(
        NUMBER_OF_PARTICLES, 
        INITIAL_PARTICLE_POSITION, 
        PARTICLE_ERROR, 
        MAX_LANDMARKS
        )

print(f"Created {particles.number_of_particles} particles")
print(f"Bounding rect: {particles.get_bounding_rect()}")

vehicle_cloud = BatchedVehicleCloud(particles, 11)
print(f"Vehicle cloud bounding rect: {vehicle_cloud.boundingRect()}")
view = ParticleView(particles, None)

view.add_cloud(vehicle_cloud)
view.show()

view.setWindowTitle("Particle Filter Visualiser")
   
quit_shortcut = QShortcut('Q', view)
quit_shortcut.activated.connect(app.quit)
view.scale(50, 50)
view.show()
sys.exit(app.exec())  # Use s
