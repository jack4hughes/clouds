# Optimising the Particle Filter:

When we -- and by we I mean Yee -- First implemented a fastSLAM algorithm using a particle filter, we ran into multiple timing issues. I've collected the main issues we've run into in this document. To understand it, it might help if you have come across these topics before. If you havent, go and read about them!:

- dynamic vs static arrays (IE Lists in Python vs C arrays).
- Pointers.
- Numpy arrays and views.
- Allocating memory for data in the stack/heap.

# The Rules:
if you dont want to read the reasoning behind these rules, then just read the following rules:
1. **dont use for loops if you can avoid it.**
2. **Preallocate arrays.**
3. **Use dictionaries for more complex lookups.**

if you want to know the reasoning for each rule, then read on.

# Rule 1: Dont use for loops if you can avoid it.
The first issue we ran across was the speed of for loops in python. You might have heard that python is a slow language before, and this is true. "Pure" Python -- that's Python that doesnt use external libraries -- can be very slow. However, we can import external libraries that can make python much faster when it does certian tasks. The main library used in the SLAM team is NumPy. 

NumPy can speed code up by up to 100x, but only if used correctly. To unlock the full speed gains of numpy, you need to let numpy do the work. This leads us to the first rule of speeding up your python code: **Dont use for loops if you can avoid it.**

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

The takeaway from this is that numpy functions are much, much faster than for loops. Use them where you can!

## Rule 2: Preallocate arrays 
Numpy is generally faster than Python, but it's easy to fall into allocation traps: don't assume that all NumPy functions are designed for speed. The library isn't just just designed for real-time applications like ours, so some numpy functions are slow.

One example of this is np.append(). This appends new data to the end of a numpy array. If you don't care about speed, np.append can be very useful. using append means that we don't need to know the size of our numpy array before we do anything with it.

Unfortunately, dynamic array implementations can be much slower than static arrays. Even worse — np.append is actually the slowest kind of append function there is. Every time we call np.append, the computer makes an entirely new array, copying every number in the existing array to a new location in memory, before adding anything we appended to the end.

to copy numbers, the computer has to do three things:
```
- find some free space in memory.
- check if the free space it has found is large enough to store the array.
- Copy every number from the first array to the brand new, slightly longer array.
```
This can be a very slow operation. Depending on how much memory in RAM your computer is already using, it might take a while for it to find a space within RAM that is big enough to contain our array. In addition, we are passing large amounts of data 

This leads us to the second rule for using numpy for real-time applications: **Use static arrays.** You'll notice that this is not a suggestion. Rule 1 is not possible in every scenario, but you can always use rule 2 to speed up your code.

However, we still want our arrays to *look* like dynamic arrays. We don't want a tonne of null values at the end of our array. to do this, we define a nupy Array object, then a numpy View object that lets us "look into" a part of that array. We usually keep the underlying numpy array as a private variable, and only expose our view into the underlying array. (If youre confused by this, I highly reccomend looking up the difference between views and arrays in numpy. Its possibly numpys best feature!)

When we want to add a landmark to our array, we just change the numpy view instead of copying the underlying array, this is a much faster operation, and can lead to significant speed improvements. It is also more deterministic. All we are doing at each update step is modifying the already existing numpy views. This means that our computer doesnt need to work to find unallocated memory that it can write to, it can just modify memory that is already there.

This is easier to reason about in static languages like C, C++ and Rust, where modifying variables and creating new objects are explicitly different.


