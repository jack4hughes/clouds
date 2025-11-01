This is a pretty rough draft of a numpy explainer. I need to go through and edit it next week.

# Optimising the Particle Filter:

When we -- and by we I mean Yee -- First implemented a fastSLAM algorithm using a particle filter, we ran into multiple timing issues. I've collected the main issues we've run into in this document. To understand it, it might help if you have come across these topics before. If you havent, go and read about them!:

- dynamic vs static arrays (IE Lists in Python vs C arrays).
- Pointers.
- Numpy arrays.
- Allocating memory for data in the stack/heap.

# Issue 1: For Loop Speed and Vectorisation.
The first issue we ran across was the speed of for loops in python. You might have heard that python is a slow language before, and this is true. "Pure" Python -- that's Python that doesnt use external libraries -- can be very slow. However, we can import external libraries that can make python much faster when it does certian tasks. The main library used in the SLAM team is NumPy. 

NumPy can speed code up by up to 100x, but only if used correctly. To unlock the full speed gains of numpy, you need to let numpy do the work. This leads us to the first rule of speeding up python code: **Dont use for loops if you can avoid it.**

Instead, try to use built in numpy functions. Numpy is designed to be vectorisable. This means that we can add two numpy arrays just by calling np.add(arr_1, arr_2). This is much faster than calling np.add within a for loop.

Lets take a look at an example: consider the following code:

```python

    list_1 = np.array(range(0, 1000000))
    list_2 = np.array(range(0, 2000000, 2))

```
here were simply defining two lists, list_1 and list_2. We're going to add these lists together using np.add and a for loop.

first, lets look at the for loop code:
```python
 for item_1, item_2 in zip(list_1, list_2):
        output_entry = np.add(item_1, item_2)
        output_list.append(output_entry)
    return output_list

```
This code takes about a second to run on my computer. Now lets look at a vectorised example:

```python
output_list = np.add(list_1, list_2)

```

This code takes 0.0023 seconds to run on my computer. Thats a 400x speed increase!

The takeaway from this should be that were you can, use numpy functions instead of for loops.

## Speed Issue 2: Pre-Allocation.
Numpy is generally faster than Python, but it's easy to fall into allocation traps: don't assume that all NumPy functions are designed for speed. The library isn't just just designed for real-time applications like ours, so some numpy functions are slow.

One example of this is np.append(). This adds new data to the end of a numpy array, and is an example of a **dynamic array**. Dynamic arrays are great! They mean that we don't need to know how big the arrays we make with a program will end up being. This is the opposite to static arrays, which have a maximum size that they can reach.

Unfortunately, dynamic arrays are slow. Even worse — np.append is actually the slowest kind of dynamic array there is. Every time we call np.append, the computer makes an entirely new array, copying every number in the existing array to a new location in memory, before adding anything we appended to the end.

to copy numbers, the computer has to do three things:
- find some free space in memory.
- check if the free space it has found is large enough to store the array.
- Copy every number from the first array to the brand new, slightly longer array.

This is a very slow operation. In addition to being slow, its also non-deterministic. This means we dont know how long the operation will take. When we might be running that function many times a second this can become a serious issue. (ill go over the problems non-deterministic operations can cause later.)

This leads us to the second rule of using numpy for real-time applications: **Always use static arrays.** You'll notice that this is not a suggestion. Rule 1 is not possible in every scenario, but you can always use rule 2 to speed up your code.

Whenever you are designing a real-time system, its far easier to define a static-


