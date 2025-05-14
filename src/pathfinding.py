# Module for pathfinding algorithms

import networkx as nx
from src.geospatial import is_in_dangerous_area

def find_safe_path(start, goal, wildfire_data, volcanic_ash_data):
    graph = nx.grid_2d_graph(100, 100)
    for node in graph.nodes():
        if is_in_dangerous_area(node, wildfire_data, volcanic_ash_data):
            graph.remove_node(node)
    return nx.astar_path(graph, start, goal)
