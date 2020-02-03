from numpy import arange, sin, pi
from pylab import plot
##################
# PART ONE
##################
def doubleme(x):
    return 2*x

def compose_twice(fn):
    # lets create a new function
    def g(x):
        return fn(fn(x))
    # return the function we just made
    return g

# three ways of increasing cleverness to write the same function
def compose_four_times(fn):
    def g(x):
        return fn(fn(fn(fn(x))))
    return g
def compose_four_times(fn):
    return compose_twice(compose_twice(fn))
compose_four_times = compose_twice(compose_twice)


def compose_N_times(fn, N):
    def g(x):
        for i in range(N):
            x = fn(x)
        return x
    return g

# Example of currying
def compose_three_times(fn):
     g = compose_N_times(fn, 3)
     return g

# They saw this in lecture but it'd be good for them to do/see it again
def map(fn, input_list):
    output_list = []
    for x in input_list:
        output_list.append(fn(x))
    return output_list

##################
# PART TWO
##################
# Practical example. Lets build up to real-valued derivatives

# Here are two real valued functions to play with
def sync(x):
    if x!=0:
        return sin(pi*x) / x
    else:
        return 1

def quadratic(x):
    return 2*x**2 - 6*x + 3

# Hey look, a way to nicely plot a function - maybe we give this to them?
def plot_function(fn):
    x = arange(-10, 10, .1)
    y = map(fn, x)
    plot(x,y)

# Here is a function that approximates the derivative of sync at a point x
# We would like to generalize this to apply to any function
def sync_slope(x):
    dx = .00001
    return (sync(x+dx) - sync(x)) / dx

# Here is a function which produces functions like the above
# Maybe this should be the end goal?
def derivative(fn):
    dx = .00001
    def fn_prime(x):
        return (fn(x+dx) - fn(x)) / dx
    return fn_prime


# Hey look higher order derivatives are just repeating the derivative function
def second_derivative(fn):
    return derivative(derivative(fn))

# We already built a way to do this. Neat.
second_derivative = compose_twice(derivative)
fourth_derivative = compose_N_times(derivative, 4)
def nth_derivative(fn, n):
    nderivatives= compose_N_times(derivative, n)
    return nderivatives(fn)

def create_nth_derivative_function(n):
    return compose_N_times(derivative, n)


# Try
# plot_function(sync)
# plot_function(derivative(sync))
# plot_funciton(second_derivative(sync))
