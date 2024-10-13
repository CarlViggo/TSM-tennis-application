"""
Program som approximerar optimala väggen mellan utspridda punkter, i detta program: tennisbollar. 
    1. Användarinput: antal bollar, spridningsavstån etc. 
    2. Tennisbollar normalförderade över planen.  
    3. Tennisbollarna representeras av en graf.
    4. Minimum spanning tree skapas av grafen mha. Prim's algoritm. 
    5. Approximation till optimala vägen hittas genom DFS 
        - Gradvis visualisering i takt med att optimala vägen återfinns. 
    6. Approximationen jämförs med optimala vägen som beräknas genom permutationer mellan bollarna. 
    7. Program med meny + matplotlib UIs
"""

class Tennis_Court:
    def __init__(self, settings):
        self.num_balls = settings["num_balls"]
        self.std = settings["std"]
        self.speed = settings["speed"]
        self.length = settings["length"]
        self.width = settings["width"]
        self.padding_length = settings["padding_length"]
        self.padding_width = settings["padding_width"]

class Node:
    def __init__(self, index):
        self.index = index  
        self.edge = []      
        
    def add_edge(self, edge):
        self.edges.append(edge)  

class Edge:
    def __init__(self, start_node, end_node, distance=1):
        self.start_node = start_node 
        self.end_node = end_node 
        self.distance = distance       

# get user input
def retrieve_metrics(): 

# get x and y coordinates for each tennis-ball
def generate_court(): 

# get 2d adjacency matrix
def generate_adjacency_matrix(): 

# generate minimum spanning tree (MST) using prims algorithm 
def generate_minimum_spanning_tree():

# find approximation to optimal path
def approximate_otpimal_path():

# plot scattered balls and how it reaches the its path
def plot_mst():

# get exact solution from old algorithm
def old_algorithm(settings, graph):

# wrapper for all functions above 
def main():
	
	"""
    settings = {
			"num_balls":,
			"std":,
			"speed":,
			"length":,
			"width":, 
			"padding_length":, 
			"padding_width":
	}
     
    Court = Tennis_Court(settings)
    """ 
     
    # generate court 
	generate_court()
    # create adjacency matrix from court
	generate_adjacency_matrix()
    # generate mst from adjacency matrix
	generate_minimum_spanning_tree()
    # generate old solution from adjacency matrix 
	old_algorithm()
    # plot the court and optimal 
	plot_mst()