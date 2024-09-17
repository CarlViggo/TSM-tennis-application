import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import distance_matrix
from sys import maxsize
from itertools import permutations

# define tennis_court class
class Tennis_Court:
    def __init__(self, settings):
        self.num_balls = settings["num_balls"]
        self.std = settings["std"]
        self.speed = settings["speed"]
        self.length = settings["length"]
        self.width = settings["width"]
        self.padding_length = settings["padding_length"]
        self.padding_width = settings["padding_width"]

# ADD A LOT OF EXCEPTION HANDLING
# returns user specified settings
def retrieve_metrics(num_balls = 20, 
					 std = 1.5, 
					 length = 24, 
					 width = 11, 
					 padding_length = 2, 
					 padding_width = 4, 
					 debug = False): 
	
	print("WELCOME! This application calculates the minimum path of traversal through a weighted graph.")
	print("First, specify your graph. Either choose advanced settings or standard settings.")
	
	advanced_y_n = input("Advances settings? y/n: ")
	not_answered = True
	while not_answered == True: 
		if advanced_y_n == "y" or "Y": 
			setting_mode = "Advanced"
			not_answered = False
		elif advanced_y_n == "n" or "N": 
			setting_modE = "Standard"
			not_answered = False
		else: 
			print("Enter either 'y' for yes or 'n' for no")
			print("Returning to menue...")

	print("Setting mode: {setting_mode}")

	speed = float(input("Enter estimated speed (m/s): "))
	num_balls = int(input("Enter number of tennis-balls: "))

	if setting_mode == "Advanced": 
		s_diviation =  float(input("Determine standard deviation for ball scattering: "))
		length =  float(input("Determine length of tennis-court (meters): "))
		width =  float(input("Determine width of tennis-court (meters): "))
		padding_length =  float(input("Determine padding along the length (side-lines) of the court, i.e, the margin to the walls (meters): "))
		padding_width  =  float(input("Determine padding along the width (baseline) of the court, i.e, the margin to the walls (meters): "))
		# Exception handling... 

	# summarize settings 
	settings_dict = {
		"num_balls": num_balls,
		"std": std,
		"speed": speed,
		"length": length,
		"width": width, 
		"padding_length": padding_length, 
		"padding_width": padding_width
	}

	# instantiate setting class SHOULD BE DONE SOMEWHERE ELSE IN MAIN FUNCTION 
	settings = Tennis_Court(settings_dict)
	
	print("""Your settings are: PRINT SETTINGS settings_obj.num_balls, 
    settings_obj.std, 
    settings_obj.speed, 
    settings_obj.length, 
    settings_obj.width, 
    settings_obj.padding_length, 
    settings_obj.padding_width """)

	return settings

# returns x and y coordinates for each ball. 
# number of subareas should be five, since balls tend to accumulate around the middle of the net and the four courners of the court. 
def generate_court(settings, num_subareas = 5): 
	
	# retrieve setting values
	"""
	num_balls, s_deviation, speed, length, width, padding_length, padding_width = (
    settings.num_balls, 
    settings.s_deviation, 
    settings.speed, 
    settings.length, 
    settings.width, 
    settings.padding_length, 
    settings.padding_width)
	"""
	
	# number of balls accumulated around the middle of the net and the four courners of the court
	balls_per_subarea = int(settings.num_balls / num_subareas)
	
	# The balls will be scattered around these "center coordinates" with a gaussian distribution
	# Notice how padding must be added around the court coordinates (otherwise it would be difficult to play tennis...)
	center_coordinates = {
		"lower_left": (0,0),
		"upper_left": (0, settings.width + 2 * settings.padding_length),
		"lower_right": (settings.length + 2 * settings.padding_width, 0),
		"upper_right": (settings.length + 2 * settings.padding_width, settings.width + 2 * settings.padding_length),
		"middle": ((settings.length + 2 * settings.padding_width)/2 , (settings.width + 2 * settings.padding_length)/2)
	}

	x_cor = []
	y_cor = []

	# generate ball coordinates
	for coordinate in center_coordinates.values(): 
		
		# problem! balls are scattered outside court, therefor put in while loop until valid   
		# a smart way of making sure that balls are scattered inside court, while also generating correct number of balls! 
		# tracker
		number_added = 0
		while number_added < balls_per_subarea:
			# generate single balls
			x = np.random.normal(coordinate[0], settings.std)
			y = np.random.normal(coordinate[1], settings.std)
			
			# ensure the ball is generated within court + padding boundary
			if (0 <= x <= settings.length + 2 * settings.padding_width) and (0 <= y <= settings.width + 2 * settings.padding_length):
				x_cor.append(x)
				y_cor.append(y)

				#tracker
				number_added += 1 

	# convert lists to arrays and reshape to 1d array
	x_array = np.array(x_cor).reshape(-1)
	y_array = np.array(y_cor).reshape(-1)

	# create "template" f
	# or concatenaded xy coordinate matrix
	# it should have same number of rows as x_array and 2 columns for x and y
	xy_coor = np.zeros((x_array.shape[0], 2))  

	# fill xy_coor with the coordinates
	xy_coor[:, 0] = x_array  
	xy_coor[:, 1] = y_array 

	# xy_coor contains x and y coordinates. 
	return xy_coor

# returns 2d adjacency matrix
def generate_adjacency_matrix(settings, xy_coor): 
	
	# computes euclidean distance between all points, i.e, in the densely connected graph. 
	distance_mat = distance_matrix(xy_coor, xy_coor)

	return distance_mat

# generates minimum spanning tree (MST) using prims algorithm 
def generate_minimum_spanning_tree(settings, distance_matrix):

	visited_balls = set()
	optim_edges = []

    # start with random ball
	visited_balls.add(np.random.randint(0, settings.num_balls))

	# number of edges in MST = num_nodes - 1 (basic math formula)
	for edge in range(settings.num_balls - 1): 
		
		min_edge = None

		# initially, all distances will be improvements
		min_distance = float('inf')
		# compare distances from current ball to neighbours for each edge
		# select the neighbour with shortest distance to current ball	
		for ball in visited_balls: 
			
			# loop thorugh all of the neighbouring balls 
			for neighbour in range(settings.num_balls): 
				
				# check if neighbour already visited 	
				if neighbour not in visited_balls: 
					
					# calculate difference between current ball and its neighbour
					distance = distance_matrix[ball, neighbour]
					
					# update minimum distance
					if distance < min_distance:
						min_distance = distance
						min_edge = (ball, neighbour)

		# add the node pair to the list after finding the minimum edge
		optim_edges.append(min_edge)
		
		# store neighbour ball as visited (not the current ball)
		visited_balls.add(min_edge[1])

	print(optim_edges)
	return optim_edges

settings_dict = {
		"num_balls": 50,
		"std": 1.5,
		"speed": 2,
		"length": 27,
		"width": 11, 
		"padding_length": 2, 
		"padding_width": 4
}

settings = Tennis_Court(settings_dict)

xy_cor = generate_court(settings)

distance_mat = generate_adjacency_matrix(settings, xy_cor)

edges = generate_minimum_spanning_tree(settings, distance_mat)

plot_mst(xy_cor, edges, settings)


def minimum_distance(graph, s):
	nodes = []

	for i in range(settings.num_balls):
		if i != s:
			nodes.append(i)
	min_path = maxsize
	next_permutation=permutations(nodes)
	for i in next_permutation:
		distance = 0
		k = s
		for j in i:
			distance += graph[k][j]
			k = j
		distance += graph[k][s]
		min_path = min(min_path, distance)
	return min_path

# returns 2d adjacency matrix
def generate_adjacency_matrix(settings, xy_coor): 
	
	# computes euclidean distance between all points, i.e, in the densely connected graph. 
	distance_mat = distance_matrix(xy_coor, xy_coor)

	return distance_mat

"""
	if __name__ == "__main__":
		graph = rounded_matrix
		s = 0
		print("The minimum distance is:", round(minimum_distance(graph, s),1), "meters")

	minimal_distance = minimum_distance(graph, s) 
	print("This would take", round(minimal_distance / speed, 1), "seconds to collect")

	img = plt.imread("tenniscourt blue.jpg")
	plt.imshow(img, extent=[0, 30, 0, 20])
	plt.show()

"""