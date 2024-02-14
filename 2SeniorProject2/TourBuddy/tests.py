from django.test import TestCase

import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations
from .models import Trip

all_trips = Trip.objects.all()

# สร้างรายการเมือง
cities = [trip for trip in all_trips]

def make_tsp_graph(cities):
    """
    Create a complete graph representing all possible paths between cities.
    """
    # Create a complete graph with nodes representing cities
    G = nx.Graph()

    # Add nodes to the graph
    for trip in cities:
        G.add_node(trip)

    # Add edges to the graph representing all possible paths between cities
    for trip1, trip2 in permutations(cities, 2):
        distance = trip1.distance_to(trip2)  # Calculate distance between two trips
        G.add_edge(trip1, trip2, weight=distance)  # Add edge with weight representing distance

    return G

# Create a complete graph representing all possible paths between cities
tsp_graph = make_tsp_graph(cities)

# Draw the graph
plt.figure(figsize=(12, 8))
positions = nx.spring_layout(tsp_graph)  # Define positions of nodes
nx.draw(tsp_graph, pos=positions, with_labels=True, node_color='skyblue', node_size=500, font_size=10)
plt.title("Complete Graph of Possible Paths between Cities")
plt.show()
