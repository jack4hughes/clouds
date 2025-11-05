# clouds

A simple fastSLAM particle filter implementation using numpy.

## Version

V0.0 (Alpha - Important features like ROS nodes, full fastSLAM animated visualisation not implemented.

## Motivation

This project spun out of UWE AI's Formula Student SLAM team. As part of that project, a fastSLAM implementation was written using Python and NumPy. Using Numpy had significant speed improvements over raw Python. However, it was possible to fall into memory allocation traps that ruined Numpy's speed advantage and complex indexing patterns that made code unreadable. This library is designed to avoid common programming issues when implementing particle-filter-based algorithms by wrapping numpy functions in a more user-friendly API.

> [!IMPORTANT]
>
> ## How to run:
>
> To get this module working on your computer, you'll need to create a Python environment with Python 3.8 or newer. You'll need to install Numpy and Qt in this environment,
>
> I'd recommend creating a seperate virtual environment; this will prevent awkward Qt issues. If you want to learn how to create a virtual environment and install numpy and PyQt, there are some resources below:
>
> [numpy install instructions](https://numpy.org/install/)
> [PyQt quickstart guide](https://doc.qt.io/qtforpython-6/gettingstarted.html#getting-started)
>
> Once you've done that, type `python3 particle_viewer_test.py` into your terminal. This will start the test program. You should see the following view appear in a new window on your computer:
>
> ![Screenshot 2025-11-01 at 01.54.32](/Users/jackhughes/Library/Application Support/typora-user-images/Screenshot 2025-11-01 at 01.54.32.png)

# Design Philosophy:

This library sets out to simplify developing particle-filter algorithms using numpy. There are three main concepts behind the module's design:

- **Always Preallocate:** By defining an array with the maximum number of landmarks and particles at the start and then slicing into it, the cost of allocating new numpy arrays can be avoided whenever a new landmark is added. This means we can avoid expensive allocation operations like np.concat or np.vstack, while keeping the code clean.
- **Vectorise, Vectorise, Vectorise.** Numpy offers powerful vectorisation features. This library allows you to use them while allowing you to fall back on clean, Pythonic for and while loops if vectorisation is impossible.
- **Slices over Object Lists.** Instead of defining each particle as its own object, we define Particles as our primitive, then use iterators to return classes or views that slice down the numpy array. This way, you can easily write pythonic code for complex operations while relying on numpy's powerful vectorisation capabilities.

# TODO:

- [ ] Implement Landmark concentration ellipses.
- [ ] Full speed test of PyQt window draw time.
- [ ] Write the README more professionally.
- [ ] Create unit tests.
- [ ] Fix landmark inversion issue.
- [ ] Rewrite display_viewer_test to avoid nested function definition. (not very cute.)
- [ ] Remove strong linking between redrawing and particle position/landmark position updates.
- [ ] Find way to invert graphicsView so we dont need to remember to invert y in each particle updater.
+ many more!

