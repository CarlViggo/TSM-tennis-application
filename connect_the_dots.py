import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import numpy as np
from scipy.spatial import distance_matrix
from itertools import permutations
import time

# define tennis_court class
class Tennis_Court:
    def __init__(self, settings):
        self.num_balls = settings["num_balls"]
        self.std = settings["std"]
        self.speed = settings["speed"]
        self.length = settings["length"]
        self.width = settings["width"]
        self.padding_length = 5
        self.padding_width = 2.5
		
# returns x and y coordinates for each ball. 
# number of subareas should be five, since balls tend to accumulate around 
# the middle of the net and the four courners of the court. 
def generate_court(settings, num_subareas = 5): 
	
	# number of balls accumulated around the middle of the net and the four courners of the court
	balls_per_subarea = int(settings.num_balls / num_subareas)
	
	# the balls are scattered around these "center coordinates" with a gaussian distribution
	# "padding" is added around the court coordinates (otherwise it would be difficult to play tennis...)
	center_coordinates = {
		"lower_left": (0,0),
		"upper_left": (0, settings.width + 2 * settings.padding_length),
		"lower_right": (settings.length + 2 * settings.padding_width, 0),
		"upper_right": (settings.length + 2 * settings.padding_width, settings.width + 2 * settings.padding_length),
		"middle": ((settings.length + 2 * settings.padding_width)/2 , (settings.width + 2 * settings.padding_length)/2)
	}

	# lists to store x and y coordinates
	x_cor = []
	y_cor = []

	# generate ball coordinates
	for coordinate in center_coordinates.values(): 
		
		# problem! balls are scattered outside court, therefor put in while loop until distribution is valid   
		number_added = 0
		while number_added < balls_per_subarea:
			
			# generate single balls (mean, std)
			x = np.random.normal(coordinate[0], settings.std)
			y = np.random.normal(coordinate[1], settings.std)
			
			# ensure the ball is generated within court + padding boundary
			if (0 <= x <= settings.length + 2 * settings.padding_width) and (0 <= y <= settings.width + 2 * settings.padding_length):
				x_cor.append(x)
				y_cor.append(y)

				#tracker
				number_added += 1 

	# convert lists to np arrays
	x_array = np.array(x_cor)
	y_array = np.array(y_cor)

	# create "template" xy coordinate matrix
	# it should have same number of rows as x_array and 2 columns for x and y
	xy_coor = np.zeros((x_array.shape[0], 2))  

	# fill xy_coor with the coordinates
	xy_coor[:, 0] = x_array  
	xy_coor[:, 1] = y_array 

	# xy_coor contains x and y coordinates. 
	return xy_coor

# returns 2d adjacency matrix
def generate_adjacency_matrix(settings, xy_coor): 
	
	# computes euclidean distance between all points, i.e, 
	# the edges of the densely connected graph
	distance_mat = distance_matrix(xy_coor, xy_coor)

	return distance_mat

# generates minimum spanning tree "MST" using prims algorithm 
def generate_minimum_spanning_tree(settings, distance_matrix):

	visited_balls = set()
	mst = []

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
						min_edge = (ball, neighbour, min_distance)

		# add the node pair to the list after finding the minimum edge
		mst.append(min_edge)
		
		# store neighbour ball as visited (not the current ball)
		visited_balls.add(min_edge[1])

	# final mininum spanning tree, a list with edges [(ball1, ball2, distance), ... n-1 times]
	return mst

# helper function using DFS to find minimum path 
# The DFS will first make it pick a random ball, then it will jump furthest out and move itself inward. 
# this is not optimal (but acceptable for now)... 
def approximate_optim_path(mst, cur_ball, visited, path):

	# mst is a list with edges [(ball1, ball2, distance), ... n-1 times]
	for ball1, ball2, distance in mst:
		
		# check if the current edge connects cur_ball to another unvisited ball
		if ball1 == cur_ball and ball2 not in visited:
			visited.add(ball2)
			# tricky part: explore ball2 using recursion
			approximate_optim_path(mst, ball2, visited, path)
			# add ball2 to the path when it's fully explored
			path.append(ball2)
		
		elif ball2 == cur_ball and ball1 not in visited:
			visited.add(ball1)
			# tricky part: explore ball1 using recursion
			approximate_optim_path(mst, ball1, visited, path)
			# add ball1 to the path when it's fully explored
			path.append(ball1)
	
	return path

# returns approximation to minimum distance + the its path 
def find_min_distance(mst, distance_mat):
	
	# always start att ball no 0
	start = 0
	cur_ball = start
	visited = {start} 
	path = [start] 

	# approximate optimal path
	path = approximate_optim_path(mst = mst, 
							   cur_ball = cur_ball, 
							   visited = visited, 
							   path = path)

	# compute total distance of the path by using the distance matrix
	total_distance = 0
	for idx in range(len(path)-1): 
		cur_ball = path[idx]
		next_ball = path[idx + 1]
		total_distance += distance_mat[cur_ball, next_ball]
	return path, total_distance

# plots minimum spanning tree + how the algorithm gradually reaches 
# an approximation to the optimal path

"""
OBS! Because of matplotlib complexity and boringness, some of these very 
specific commands have been taken from internet. These are not main parts of the 
P-uppgift, just esthetic features! 
"""

def plot_mst(points, mst_edges, settings, min_path=None):
	
	court_length = settings.length + 2 * settings.padding_width
	court_width = settings.width + 2 * settings.padding_length

	# fix background image
	background_image = "/mnt/c/Users/Johan/Documents/Programmering/KTH/TSM-tennis-application/court.jpg"
	img = mpimg.imread(background_image)
	plt.imshow(img, extent=[0, court_length, 0, court_width], aspect='auto', zorder=0)

	# scatter balls
	plt.scatter(points[:, 0], points[:, 1], color='#56ff1b', s=100, zorder=2)

	# add label to each ball
	for i, point in enumerate(points):
		plt.text(point[0], point[1], f'P{i}', fontsize=12, ha='right')

	# plot distances
	for edge in mst_edges:
		i, j, weight = edge
		p1, p2 = points[i], points[j]
		plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'blue', zorder=1) 

	
	plt.xlim(0, court_length)
	plt.ylim(0, court_width)
	plt.title('Optimal Path Approximation')
	plt.xlabel('X coordinate')
	plt.ylabel('Y coordinate')
	plt.grid(True)

	# show mst and court
	plt.grid(False)
	plt.show(block=False)

	# add a short path, so that the minimum spanning tree 
	# is first exposed. Doesnt work yet... 
	time.sleep(3)  

	# ff min_path is defined, then "simulate" how it 
	# graduallt finds the ideal path
	if min_path:
		for i in range(len(min_path) - 1):
			p1 = points[min_path[i]]
			p2 = points[min_path[i+1]]
			
			# add onedistance line at a time
			plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'red', linewidth=2.5, zorder=3) 
			plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='red', s=150, zorder=4) 
			
			# add a pause 
			plt.pause(settings.speed) 
	
	plt.show()

# this function provides an exact solution for benchmarking purposes. O(n!) complexity... 
# this is taken from a previous project of mine # https://github.com/CarlViggo/Carl-Viggo-Projects/blob/main/Tenniscourt.py 
def old_algorithm(settings, graph):
	
	# tennis-ball to start on (could be random number)
	start = 0
	
	# store all balls except the starting ball 
	tennis_balls = [ball for ball in range(settings.num_balls) if ball != start]

	# initially, all distances will be improvements
	min_distance = float('inf')

	# for example: permutations([1, 2, 3]) generates: (1, 2, 3) (1, 3, 2) (2, 1, 3) (2, 3, 1) (3, 1, 2) (3, 2, 1)
	next_permutation = permutations(tennis_balls)
	for ball in next_permutation:
		# this will be updated as algorithm starts
		distance = 0
		current_ball = start
		#iterates through neighbors 
		for neighbour in ball:
			# computes distance between current ball and neighbour 
			distance += graph[current_ball][neighbour]
			# sets neighbour to current ball
			current_ball = neighbour
		
		#stores the current computed distance 
		distance += graph[current_ball][start]
		# updates the minimum distance found 
		min_distance = min(min_distance, distance)

	# distance 
	return min_distance

# wrapper for all the above functions
def main(settings_dict):

	settings = Tennis_Court(settings_dict)

	xy_cor = generate_court(settings)

	distance_mat = generate_adjacency_matrix(settings, xy_cor)

	mst = generate_minimum_spanning_tree(settings, distance_mat)

	# gets both the optimal path and its distance 
	path, approx_min_distance = find_min_distance(mst, distance_mat)
	
	# plots mst and how the algorithm gradually reaches optimal path
	plot_mst(xy_cor, mst, settings, path)

	#obs will crash if num_balls > around 10 
	#optim_min_distance = old_algorithm(settings, distance_mat)
	optim_min_distance = False

	return approx_min_distance, optim_min_distance
