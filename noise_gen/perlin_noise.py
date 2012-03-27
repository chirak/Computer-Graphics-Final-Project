import math
from random import random
# ------------------------------------------------------------------------
# If you want to generate plots and experiment with the noise funciton,
# you must install matplotlib. Instructions on how to do so can be found
# here: http://matplotlib.sourceforge.net/users/installing.html. You must
# also uncomment the code in the perlin noise function.
# ------------------------------------------------------------------------

# -----------------------------------------
# Interpolation methods
# -----------------------------------------
def linear_interpolation(a, b, x):
	return a*(1-x) + b*x

def cosine_interpolation(a, b, x):
	ft = x * math.pi
	f = (1 - math.cos(ft)) * .5

	return a*(1-f) + b*f

# Returns a 3-tuple which is used as the input for the interpolation methods
def sample_points(x, t, max_x):
	x0 = x // t * t # '//' simply floors result of 'x / t'
	return x0, (x0 + t) % max_x, (x - x0) / t

# -----------------------------------------
# White Noise Generation
# -----------------------------------------

# Fills a list of size n with random values between [0, 1]
def generate_white_noise_1d(n):
	noise = []
	for x in range(0, n):
		noise.append(random())
	return noise

# Fills a 2d array [width x height] with random values between [0, 1]
def generate_white_noise_2d(width, height):
	noise = []
	for i in range(width):
		noise.append([])
		for j in range(height):
			noise[i].append(random())
	return noise

# -----------------------------------------
# Smooth Noise Geneartion
# -----------------------------------------

# Interpolates between all of the base_noise values using the specefied
# interpolation function. Defaults to linear interpolation if none specefied
def generate_smooth_noise_1d(base_noise, interpolation, octave):
	if(interpolation == 'linear'):
		interpolation_fun = linear_interpolation
	else:
		interpolation_fun = cosine_interpolation

	noise_len = len(base_noise)
	t = 2**octave
	smooth_noise = []
	for i in range(noise_len):	
		a, b, x = sample_points(i, t, noise_len)							
		smooth_noise.append(interpolation_fun(base_noise[a], base_noise[b], x))
	return smooth_noise

def generate_smooth_noise_2d(base_noise, octave):

	width = len(base_noise)
	height = len(base_noise[0])
	t = 2**octave
	smooth_noise = []

	for i in range(width):	
		smooth_noise.append([])
		x0, x1, xalpha = sample_points(i, t, width)							
		for j in range(height):
			y0, y1, yalpha = sample_points(j, t, height)
			a0 = (1 - xalpha)*base_noise[x0][y0] +(xalpha)*base_noise[x1][y0]
			a1 = (1 - xalpha)*base_noise[x0][y1] + (xalpha)*base_noise[x1][y1]
			smooth_noise[i].append(linear_interpolation(a0, a1, yalpha))
	return smooth_noise

# -----------------------------------------
# Perlin Noise Generation
# -----------------------------------------
# Basic idea of algorithm:
# 	1) Generate random noise values
# 	2) 'Smoothen' each random value out so it appears less random.
# 	   This is done for each octave iteration.
# 	3) Combine all of the smooth values 
# 	4) Normalize the values so that they are between [0, 1]

def perlin_noise_1d(n, layers, persistence, interpolation='linear'):
	base_noise = generate_white_noise_1d(n)
	perlin_noise = []
	for x in range(n):
		perlin_noise.append(0)

	amplitude = 1
	total_amplitude = 0
	for k in range(layers):
		amplitude *= persistence
		total_amplitude += amplitude
		smooth_noise = generate_smooth_noise_1d(base_noise, interpolation, layers - k - 1)

		for p in range(n):
			perlin_noise[p] += smooth_noise[p] * amplitude

	for p in range(n):
		perlin_noise[p] /= total_amplitude
			
	return perlin_noise
			
def perlin_noise_2d(width, height, layers, persistence):
	base_noise = generate_white_noise_2d(width, height)
	perlin_noise = []
	for i in range(width):
		perlin_noise.append([])
		for j in range(height):
			perlin_noise[i].append(0)

	amplitude = 1
	total_amplitude = 0
	for k in range(layers):
		amplitude *= persistence
		total_amplitude += amplitude
		smooth_noise = generate_smooth_noise_2d(base_noise, layers - k - 1)

		for i in range(width):
			for j in range(height):
				perlin_noise[i][j] += smooth_noise[i][j] * amplitude

	for i in range(width):
		for j in range(height):
			perlin_noise[i][j] /= total_amplitude

	return perlin_noise

# Debugging...
perlin_noise = perlin_noise_2d(20, 5, 6, .5)

for p in perlin_noise:
	print p
