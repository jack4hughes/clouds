"""
#Particles:
This is the main particles class. Its used to model the pose and landmarks detected by each particle.
"""


import numpy as np
from numpy import sin, cos
import time
from typing import NamedTuple, Union, Optional
import matplotlib.pyplot as plt
from time import perf_counter


np.set_printoptions(suppress=True, precision=5)

NUMBER_OF_PARTICLES = 50
TIMESTEP = 0.01
NUMBER_OF_LANDMARKS = 100

class Particles:
    """A class that holds informatiom about a particle set.

    This class is how we initialise and modify particle sets.

    inputs:
    ___________
    - number_of_particles: Defines the number of particles we want to use in our particle set. This is a static maximum.
    - initial_pose: The initial mean pose of all the particles.
    - initial_error: the covaraince error of the particles. (We should probably switch this out.)
    - max_landmarks: The maximum number of landmarks we can detect before we start to replace landmarks with new detections.

    attributes:
    ___________
    - observed_landmarks: The number of landmarks that have been observed so far.
    - observed_covariances: the number of covarainces that have been observed so far. This should match landmarks in most cases.
    - poses: The current pose of every particle hypothesis. – This is stored in a numpy array.
    - importance_factors: A vector of importance importance_factors
    - landmarks: an array of landmark detections. This is a numpy array that has dimensions number_of_particles x detected_landmarks x landmark_pose_hypotheses.
    - 

    """
    def __init__(
        self,
        number_of_particles: int,
        initial_pose: np.ndarray,
        initial_error: Optional[np.ndarray] = None,
        max_landmarks: int = NUMBER_OF_LANDMARKS
    ):
        # Setting info about the 
        self.number_of_particles = number_of_particles
        self.observed_landmarks = 0
        self.observed_covariances = 0
        self.max_landmarks = max_landmarks

        # Creates a numpy array where each particle has the same pose.
        self.poses = np.tile(initial_pose, (number_of_particles, 1))

        # Initialises weights, These are set to 1/Number of particles.
        self.importance_factors = np.repeat(1 / number_of_particles, number_of_particles)

        """These variables set up the underlying memory accessed by views later on,
        
        You can read the README for more information, but the basic jist is that we
        initalise these here with placeholder data, then set up a view into them that
        is resized every time add_landmark is called. This way, we are just resizing
        a view instead of finding more data. This saves a lot of time during operation,
        however, it means that the numbers inside these attributes can be UNINITIALISED
        Please dont use these if you don't know exactly what youre doing with then."""
        self.__landmark_estimate_array = np.empty(
            (number_of_particles, max_landmarks, 2), np.float32
        )

        # This array stores Tau in Truns book probabalistic Robotics.
        self.__landmark_likelihood_array = np.empty(
            (number_of_particles, max_landmarks), np.float32
        )   
        
        # Creating covariance array estimate
        self.__covariance_array = np.empty(
            (number_of_particles, max_landmarks, 2, 2), np.float32
        )

        #  creating numpy views that let us access data stored in empty arrays.
        self.landmarks = self.__landmark_estimate_array[:0]
        self.covariance = self.__covariance_array[:0]
        self.landmark_likelihood = self.__landmark_likelihood_array[:0]

        if initial_error is not None:
            error = np.random.randn(*self.poses.shape) * initial_error
            self.poses += error

        self._particles = [Particle(self, i) for i in range(number_of_particles)] #should we make this into an __index__ thing instead?

    def __str__(self):
        output = f"number of particles:\t{self.number_of_particles}\n"
        output += f"variance of particles: {np.std(self.poses, axis=0)}\n"

        return output

    def __getitem__(self, index):
        #get item is designed to return a Particle. This is the most obvious return from particles. If you disagree with this, please let me know why!
        return Particle(self, index)
    
    def __iter__(self):
        for i in range(self.number_of_particles):
            yield Particle(self, i)
    
    def get_particle(self, particle_index):
        pose = self.poses[particle_index, :]
        return pose
    
    def get_landmark_positions(self, landmark_index):
        """Returns all hypotheses of a specific landmark

        IE landmarks[landmark_index]: [particle1, particle2 ... particleN]"""
        return self.landmarks[:, landmark_index, :].reshape(NUMBER_OF_PARTICLES, 2)

    def get_particle_landmark_hypotheses(self, particle_index):
        """

        Gets all the landmark hypotheses associated with a specific particle.

        IE landmarks[particle]: [landmark1, landmark2 ..., landmarkN]

        """
        return self.landmarks[particle_index].reshape(self.observed_landmarks, 2)
    
    def add_landmark(self, landmark_positions: np.ndarray) -> None:
        """adds a landmark data to the particle set. particles
        
        inputs:
        ___________
        landmark_positions: An already calculated array of particle hypotheses in cartesian space.
        You need to calculate where the landmarks are before you add them to this function using 
        get_landmark_offset (or your own equivilent function.)

        outputs:
        ___________
        none.

        TODO: Implement a way to define the noise profile of a landmark."""        
        array_size = min(self.observed_landmarks, self.max_landmarks)
        array_end = array_size + 1 
        # Update view to add a new landmark.
        self.landmarks = self.__landmark_estimate_array[:, :array_end, :]

        # Set landmark position according to each particle.
        self.landmarks[:, self.observed_landmarks] = landmark_positions
        self.observed_landmarks += 1

    def update_landmark(
        self, landmark_index: int, landmark_position: np.ndarray
    ) -> None:
        self.landmarks[:, landmark_index, :] = landmark_position

    def add_covariance(self, covariances: np.ndarray) -> None:
        """
        adds a covariance matrix to self.covariance in a fast way.

        inputs:
        ___________
        covariances: an array of covariance matrices. These need to be calculated before being passed to 
        this function (use get_landmark_cov for this, or your own function.) 
        """
        array_size = min(self.observed_covariances, self.max_landmarks)
        array_end = array_size + 1
        self.covariance = self.__covariance_array[:, :array_end, :, :]
        self.covariance[:, self.observed_covariances] = covariances
        self.observed_covariances += 1

    def update_covariance(self, landmark_index, covariances) -> None:
        """
        Updates an already exisiting set of covariance matrices (need to adjust this when we add exiting landmark detections where not all particles detect particles.)
        """
        self.landmarks[:, landmark_index] = covariances
   
    def get_bounding_rect(self):
        """
        Returns a bounding rectange with the furthest points.
        """
        max_particles = np.max(self.poses, 0)[0:2] #slice to remove angle.
        min_particles = np.min(self.poses, 0)[0:2]

        return (min_particles, max_particles)

    def get_mean(self) -> np.ndarray:
        """returns the mean of the entire dataset."""
        return np.mean(self.poses, 0)

    def get_relative_positions(self) -> np.ndarray:
        """gets the position of each point in the dataset relative to the mean."""
        return self.data - self.get_mean()

    def get_lm_cov_eigendecomposition(self):
        """Gets the eigendecomposition for each covariance matrix and returns it """
        return np.linalg.eigh(self.covariance) #Covariance matricies have nice properties that we can use to speed this up a little.

class Particle:
    """A particle class is how we get information about a single particle from our particles class.
    This doesnt store any data, instead it stores a view of the data stored in our numpy particles class.
    
    You can directly change values in Particles using the Particle class, which is super useful!

    im setting these up as properties because I want it to be super clear that they are slices of the current information.

    This means that you cant deepcopy a Particle to see where it has gone (i think)"""
    def __init__(self, particles_ref: Particles, index):
        self._particles = particles_ref
        self._index = index
        # In your Particle class
    
    @property
    def importance_factor(self):
        return self._particles.importance_factors[self._index]
    
    @importance_factor.setter
    def importance_factor_setter(self, value):
        self._particles.importance_factors[self._index] = value
    
    @property
    def pose(self):
        return self._particles.poses[self._index, :]
    
    @pose.setter
    def pose(self, value):
        self._particles.poses[self._index, :] = value
    
    @property
    def landmarks(self):
        return self._particles.landmarks[self._index]
    
    @landmarks.setter
    def landmarks_setter(self, value):
        self._particles.landmarks[self._index] = value
    
    @property
    def covariances(self):
        return self._particles.covariance[self._index]
    
    @covariances.setter
    def set_covariance(self, landmark_index, value):
        self._particles.covariance[self._index, landmark_index] = value

    @property
    def landmark_likelihood(self):
        return self._particles.landmarks[self._index]
    
    def __str__(self):
        string = ""
        string +=  f"index: {self._index}"
        string += f"importance factor: {self.importance_factor}"
        string += f"pose: {self.pose}"
        string += f"Landmarks: {self.landmarks}"

    
    # We dont need a landmarks setter as landmarks[i] already checks for issues.


def vectorised_motion_model(
    current_poses: np.ndarray, velocity_inputs: np.ndarray, timestep: float
):
    # Setting up numpy views for velocities and angular velocities per particle.
    particle_velocities = velocity_inputs[:, 0]
    particle_omegas = velocity_inputs[:, 1]
    # Calculating useful vectors for motion update.
    v_over_w = particle_velocities / particle_omegas
    theta = current_poses[:, 2]
    d_theta = particle_omegas * timestep
    new_theta = theta + d_theta

    final_poses = np.empty(current_poses.shape)
    final_poses[:, 0] = (
        current_poses[:, 0] - v_over_w * np.sin(theta) + v_over_w * sin(new_theta)
    )
    final_poses[:, 1] = (
        current_poses[:, 1] + v_over_w * np.cos(theta) - v_over_w * cos(new_theta)
    )
    final_poses[:, 2] = theta + new_theta

    return final_poses


def get_noisy_velocity_inputs(
    velocity_vector: np.ndarray, alphas: np.ndarray, number_of_particles: int
) -> np.ndarray:
    noise_vector_input = np.random.randn(number_of_particles, 2)

    theta_noise = alphas[0] * velocity_vector[0] ** 2
    theta_noise += alphas[1] * velocity_vector[1] ** 2

    omega_noise = alphas[2] * velocity_vector[0] ** 2
    omega_noise += alphas[3] * velocity_vector[1] ** 2
    noise_vector_input *= np.array([theta_noise, omega_noise])
    noise_vector_input += velocity_vector

    return noise_vector_input


def motion_update(particles, velocities, timestep, alphas, debug=False):
    v_hat, w_hat = velocities[0], velocities[1]
    
    # Sample noisy velocities for each particle
    v_noise = np.sqrt(alphas[0]*v_hat**2 + alphas[1]*w_hat**2)
    w_noise = np.sqrt(alphas[2]*v_hat**2 + alphas[3]*w_hat**2) 
    gamma_noise = np.sqrt(alphas[4]*v_hat**2 + alphas[5]*w_hat**2)
    
    v = v_hat + np.random.normal(0, v_noise, particles.poses.shape[0])
    w = w_hat + np.random.normal(0, w_noise, particles.poses.shape[0])
    gamma = np.random.normal(0, gamma_noise, particles.poses.shape[0])
    
    # Handle division by zero
    w_nonzero = np.where(np.abs(w) < 1e-6, 1e-6, w)
    
    x, y, theta = particles.poses[:, 0], particles.poses[:, 1], particles.poses[:, 2]
    
    # Motion update
    new_x = x - (v/w_nonzero) * np.sin(theta) + (v/w_nonzero) * np.sin(theta + w*timestep)
    new_y = y + (v/w_nonzero) * np.cos(theta) - (v/w_nonzero) * np.cos(theta + w*timestep)
    new_theta = theta + w * timestep + gamma*timestep
    
    return np.column_stack([new_x, new_y, new_theta])


def ackermann_motion_update(particles, velocities, timestep, alphas, debug=False, track_width=0.):
    v_hat, w_hat = velocities[0], velocities[1]
    
    # Sample noisy velocities for each particle
    v_noise = np.sqrt(alphas[0]*v_hat**2 + alphas[1]*w_hat**2)
    w_noise = np.sqrt(alphas[2]*v_hat**2 + alphas[3]*w_hat**2) 
    gamma_noise = np.sqrt(alphas[4]*v_hat**2 + alphas[5]*w_hat**2)
    
    v = v_hat + np.random.normal(0, v_noise, particles.poses.shape[0])
    
    w = w_hat + np.random.normal(0, w_noise, particles.poses.shape[0])
    
    gamma = np.random.normal(0, gamma_noise, particles.poses.shape[0])
    
    #Get the ackermann 
    # Handle division by zero
    w_nonzero = np.where(np.abs(w) < 1e-6, 1e-6, w)
    
    x, y, theta = particles.poses[:, 0], particles.poses[:, 1], particles.poses[:, 2]
    
    # Motion update
    axle_offset = np.array([np.cos(theta - np.pi/4)*track_width, np.sin(theta-np.pi/4)*track_width])
    new_x = x - (v/w_nonzero) * np.sin(theta) + (v/w_nonzero) * np.sin(theta + w*timestep) + axle_offset[0]
    new_y = y + (v/w_nonzero) * np.cos(theta) - (v/w_nonzero) * np.cos(theta + w*timestep) + axle_offset[1]
    
    centre_x = new_x + np.sin(particles.poses[0, 2] - np.pi/4) * 0.5
    centre_y = new_y + np.cos(particles.poses[0, 2] - np.pi/4) * 0.5 
    new_theta = theta + w*timestep + gamma*timestep
    return np.column_stack([centre_x, centre_y, new_theta])


def get_landmark_offset(particles: Particles, landmark_vect):
    """Converts a landmark detection in (r, θ) into their (x, y) position for each particle.

    TODO: Write some documentation for this because this is a nasty fastSLAM concept at first."""
    r = landmark_vect[0]
    theta = landmark_vect[1] + particles.poses[:, 2]

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return np.array([x, y]).T


def get_landmark_cov(landmark_polar_offset, sensor_noise_cov):
    """
    Transform polar measurement covariance to Cartesian landmark covariance
    
    Args:
        landmark_polar_offset: [r, theta] - range and bearing to landmark
        sensor_noise_cov: 2x2 covariance matrix in polar coordinates (R matrix)
    
    Returns:
        landmark_covariance: 2x2 covariance matrix in Cartesian coordinates

   TODO: need to unit test this and make sure it works for single covariances, and vectorised operations.
    """

    r = landmark_polar_offset[0]
    theta = landmark_polar_offset[1]
    # print(f"r: {r}")
    # print(f"theta: {theta}")
    # Jacobian matrix for polar to Cartesian transformation
    # x = r * cos(theta)
    # y = r * sin(theta)
    # J = [dx/dr, dx/dtheta]
    #     [dy/dr, dy/dtheta]
    
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    
    jacobian = np.array([[cos_theta, -r * sin_theta],
                        [sin_theta,  r * cos_theta]])
    
    # print(f"Jacobian shape:\n{jacobian.shape}\n{jacobian}")
    # Transform covariance: C_cartesian = J * C_polar * J^T
    landmark_covariance = jacobian @ sensor_noise_cov @ jacobian.T
    return landmark_covariance


if __name__ == "__main__":
    particles = Particles(100, np.array([0 ,0. ,0.]),np.array([0.01, 0.01, 0.001]))
    print("Particles:")
    decomposition_times_dict = {}
    for i in range(100):
        particles.add_landmark(np.array((1., 1.))) 
        particles.add_covariance(np.array([[1., 0.], [0., 2.]]))
        
        start_time =time.perf_counter()
        particles.get_lm_cov_eigendecomposition()
        end_time = time.perf_counter() - start_time
        decomposition_times_dict[i] = end_time

    print("Basic Particle analysis.")
    for particle in particles:
        print(particle.pose)
    bounding_rect = particles.get_bounding_rect()
    print(f"bounding rect: {bounding_rect}")
    print(f"mean: {particles.get_mean()}")

    print("Basic Landmark Analysis:")
    decomposition_start_time = perf_counter()
    print(f"landmark positions: {particles.landmarks[0]}")
    print(f"landmark covariances: {particles.covariance[0]}")
    print("landmark eigendecomposition times:")

    plt.plot(decomposition_times_dict.keys(), decomposition_times_dict.values())
    plt.show()
