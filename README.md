# clouds

A simple fastSLAM particle filter implementation using numpy. 

## Motivation
This project began in UWE AI's Formula Student SLAM team. As part of that project, a fastSLAM implementation was written using Python and NumPy. Numpy had significant speed improvements over raw Python. However, it was possible to fall into memory allocation traps that ruined Numpy's speed advantage and complex indexing patterns that made code complex. This library is designed to avoid these speed and complexity problems by creating an interface for the underlying numpy arrays. It also includes a particle viewer that uses PyQt to display the particle positions.
> [!IMPORTANT]
>
> ## How to run:
>
> To get this module working on your computer, you'll need to create a Python environment with Python 3.8 or newer. You'll need to install Numpy and Qt in this environment,
>
> I'd recommend creating a seperate virtual environment; this will prevent awkward Qt issues. If you don't know how to create a virtual environment and install numpy and PyQt, there are some resources below:
>
> [numpy install instructions](https://numpy.org/install/)
> [PyQt quickstart guide](https://doc.qt.io/qtforpython-6/gettingstarted.html#getting-started)
>
> Once you've done that, navigate to the parent folder and type `python3 particle_viewer_test.py` into your terminal. This will start the test program. You should see the following view appear in a new window on your computer:
>
> ![Screenshot 2025-11-01 at 01.54.32](/Users/jackhughes/Library/Application Support/typora-user-images/Screenshot 2025-11-01 at 01.54.32.png)

There are two main components to this library: The particle interface, and the particle viewer.

# Particle API:

This class acts like a facade for our underlying particle data arrays. This makes common operations like adding new particles or getting a slice of the full landmark detection and covariance array that only contains detected landmarks for specific particles.

This interface was designed with the following principles in mind:

- **Always Preallocate:** By defining an array with the maximum number of landmarks and particles at the start and then slicing into it, the cost of allocating new numpy arrays can be avoided whenever a new landmark is added. This means we can avoid expensive allocation operations like np.concat or np.vstack, while keeping the code clean.
- **Vectorise, Vectorise, Vectorise.** Numpy offers powerful vectorisation features. This library allows you to use them whilst still being able to fall back on pythonic for loops for protoyping and in places where vectorisation is impossible.
- **Slices over Object Lists.** Instead of defining each particle as its own object, partciles are defined in large arrays, and then sliced down using helper functions. This allows you to use numpy functions on many different parts of the array.

# Particle Viewer:
The particle viewer is a way of viewing the current position of the particles in 2D space in a graphical way.

It has the following features:
- Interactive GUI, allowing you to explore the space the particles are in.
- Customisable classes for displaying landmarks and vehicle position.
- Fast redraw when displaying many particles at once.

The particle filter is implemented using PyQt at this stage. A Qt version written in C++ is currently planned once an MVP capable of SLAM has been implemented.

# TODO:

- [ ] Implement Landmark concentration ellipse display.
- [x] Rewrite Landmark drawing to remove calling draw() for individual landmarks. (probably a big one!) - DONE FOR VEHICLE PARTICLES AND POINTS.
- [ ] Rewrite particle_viewer_test and particle_viewer to handle dynamic updates in a more compartmentalised fashion. (again, probably a big one!)
- [x] Full speed test of PyQt window draw time.
- [ ] Write the README more professionally.
- [ ] Create unit tests.
- [ ] Remove strong linking between redrawing and particle position/landmark position updates. (maybe not possible?)
- [ ] Find way to invert graphicsView so we dont need to remember to invert y in each particle updater.
+ many more!

