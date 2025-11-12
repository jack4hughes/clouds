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

from PyQt5.QtCore import QTimer, QElapsedTimer
from particles import Particles, get_landmark_offset, get_landmark_cov, ackermann_motion_update
import sys
import time
import numpy as np
from math import pi

from PyQt5.QtWidgets import QApplication, QShortcut
from particle_viewer import (
        create_direction_particle_cloud,
        ParticleView,
        create_landmark_particle_cloud)

MODE = "dynamic"
NUMBER_OF_PARTICLES = 200
MAX_LANDMARKS = 100

INITIAL_PARTICLE_POSITION = (0., -0., 0)
PARTICLE_ERROR = np.array((1, 1, 0.002))

ALPHAS = [0.1, 0.1, 0.000001, 0.000001, 0.0000001, 0.0000001]
TEST_VELOCITY = (200, 0.1)

SENSOR_COVARIANCE = np.array(((0.3, 0.2), (0.2, 0.5)))
POLAR_LANDMARK_DETECTION = np.array((55., pi/2))

MOTION_UPDATE_TIMESTEP = 1/10 # 30fps update for now, but system should be able to handle 60.
LANDMARK_DETECTION_TIMESTEP = 300

if __name__ == "__main__":
    app = QApplication(sys.argv)
    timer = QTimer()
    landmark_timer = QTimer()

    particles = Particles(NUMBER_OF_PARTICLES, INITIAL_PARTICLE_POSITION, PARTICLE_ERROR, MAX_LANDMARKS)

    position_cloud = create_direction_particle_cloud(particles)

    polar_landmark_detection = POLAR_LANDMARK_DETECTION 

    cartesian_landmark_offset = get_landmark_offset(
        particles, 
        polar_landmark_detection
        )

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
    view.add_cloud(position_cloud)
 
 # The amount of state means that this should be a class or a lambda in actual code.   
    last_call = time.time()
    update_simulation_time = QElapsedTimer()
    def update_simulation():
        time_since_last_update = update_simulation_time.elapsed()
        print(time_since_last_update)
        
        #time ackermann update.
        new_particle_locations = ackermann_motion_update(particles, TEST_VELOCITY, MOTION_UPDATE_TIMESTEP, ALPHAS)
        
        # time redraw
        particles.poses = new_particle_locations
        view.update_clouds()
        update_simulation_time.restart()
    n = 1

    def add_landmark_cloud():
        global n
        polar_landmark_detection = np.array((55., pi/2))
    
    # Convert the landmark detection from a single polar detection to 50 seperate landmark hypotheses in cartesian space. 
        cartesian_landmark_offset = get_landmark_offset(
        particles, 
        polar_landmark_detection
        )

        calculation_start = time.time()
        cartesian_landmark_positions = cartesian_landmark_offset + particles.poses[:, :2]
        lm_covariances = get_landmark_cov(polar_landmark_detection, SENSOR_COVARIANCE)
        
        particles.add_landmark(cartesian_landmark_positions)
        particles.add_covariance(lm_covariances) 

        landmark_cloud_1 = create_landmark_particle_cloud(particles, n)
        n += 1
        view.add_cloud(landmark_cloud_1)

    timer.timeout.connect(update_simulation)
    landmark_timer.timeout.connect(add_landmark_cloud)
    
    if MODE == "dynamic":
        #runs a simple animation if you set dynamic mode.
        timer.start(MOTION_UPDATE_TIMESTEP)
        landmark_timer.start(LANDMARK_DETECTION_TIMESTEP)

    # We have to attach clouds to our view individually.
       
    view.setWindowTitle("Particle Filter Visualiser")
   
    quit_shortcut = QShortcut('Q', view)
    quit_shortcut.activated.connect(app.quit)

    view.show()
    sys.exit(app.exec())  # Use sys.exit for clean shutdown
