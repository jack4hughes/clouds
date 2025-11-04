"""
PARTICLE FILTER AND VISUALISER DEMO SCRIPT:
========================================================
This is a simple test of our particle viewer! It checks the following criteria:

    - Particles have been spawned properly, and are displaying in the correct place.
    - Particles are easily visible.
    - Landmarks and particles can be added and displayed easily.

This also doubles as a bit of a tutorial for how to add particles and display them.

In implementations, You might want to split this script out into two seperate ROS nodes with shared memory for viewing particles.

This script generates and displays a particle that has detected a single landmark.

You can zoom in and out and drag to move on the fastSLAM landmark.

Just press Q to quit.
"""


from PyQt5.QtCore import QTimer
from particles import Particles, get_landmark_offset, get_landmark_cov, ackermann_motion_update
import sys
import time
import numpy as np
from math import pi

from PyQt5.QtWidgets import QApplication, QShortcut
from particle_viewer import (
        create_direction_particle_cloud,
        ParticleView,
        create_landmark_particle_cloud
        )

PARTICLE_ERROR = np.array((1.5, 1.5, 0.2))
NUMBER_OF_PARTICLES = 50
INITIAL_PARTICLE_POSITION = (0., 0., 0.)
MAX_LANDMARKS = 100
SENSOR_COVARIANCE = np.array(((0.3, 0.2), (0.2, 0.5)))
ALPHAS = [0.1, 0.01, 0.001, 0.0001, 0.0001, 0.0001]
TEST_VELOCITY = (2, 0.2)
MOTION_UPDATE_TIMESTEP = 0.1 # 10fps update for now.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer = QTimer()
    
    particles = Particles(NUMBER_OF_PARTICLES, INITIAL_PARTICLE_POSITION, PARTICLE_ERROR, MAX_LANDMARKS)



    
    #A "cloud" is a way of viewing our particles object in a GUI. create_direction_particle_cloud is used for dispalying objects with poses (IE our particles.)
    position_cloud = create_direction_particle_cloud(particles)

    # Now we are simulating a landmark detection using some data
    polar_landmark_detection = np.array((-20., pi))
    
    # Convert the landmark detection from a single polar detection to 50 seperate landmark hypotheses in cartesian space. 
    cartesian_landmark_offset = get_landmark_offset(
        particles, 
        polar_landmark_detection
        )

    # This can be combined with prev. line in prod. code if you feel like it.
    cartesian_landmark_positions = cartesian_landmark_offset + particles.poses[:, :2]
   
    """And now we just calculate the covariance at that specific distance."""
    lm_covariances = get_landmark_cov(polar_landmark_detection, SENSOR_COVARIANCE)

    """Once we have calculated the correct positions and covariance values, we can add them to our Particles class."""
    particles.add_landmark(cartesian_landmark_positions)
    particles.add_covariance(SENSOR_COVARIANCE) #We shouldnt be using SENSOR_COVARIANCE like this! fix!

    # And then finally, we can create a landmark particle cloud that lets us see the position of every landmark in space.
    # This will eventually visualise the concentration ellipse of every landmark as well, but this isnt implemented yet.
    landmark_cloud_1 = create_landmark_particle_cloud(particles, 0)
    
    # The final step is to create our View.
    view = ParticleView(particles)
    
    # Probably shouldnt be done like this!
    def update_simulation():
        new_particle_locations = ackermann_motion_update(particles, TEST_VELOCITY, MOTION_UPDATE_TIMESTEP, ALPHAS)
        particles.poses = new_particle_locations
        view.update_clouds()
    
    timer.timeout.connect(update_simulation)
    timer_update_speed = MOTION_UPDATE_TIMESTEP * 1000
    timer.start(timer_update_speed)

    # We have to attach clouds to our view individually.
    view.add_cloud(position_cloud)
    view.add_cloud(landmark_cloud_1)
    
    # This is the section that should be anitmated!

    # Animtation function ends here.

    # And update_clouds just makes sure that each cloud is up to date. IF you were running this in a while loop youd call this on every iteration.
    
    view.setWindowTitle("Particle Filter Visualiser")
   
    quit_shortcut = QShortcut('Q', view)
    quit_shortcut.activated.connect(app.quit)

    view.show()
    sys.exit(app.exec())  # Use sys.exit for clean shutdown
