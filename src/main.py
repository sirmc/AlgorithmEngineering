#!/usr/bin/env python3.4
import sys
from graph_tool.all import *
from numpy import *

def euclidean_steiner_tree(g):
    tree = min_spanning_tree(g)
    g.set_edge_filter(tree)
    return g

def get_positions(g):
    x = g.vertex_properties["x"].get_array()
    y = g.vertex_properties["y"].get_array()
    coord = dstack((x,y))
    pos = g.new_vertex_property("vector<double>")
    for i,v in enumerate(g.vertices()):
        pos[v] = coord[0][i]
    return pos

def start():
    filename = sys.argv[1]
    g = load_graph(filename)
    solution = euclidean_steiner_tree(g)

    pos = get_positions(solution)
    graph_draw(solution, pos=pos, output_size=(800, 800), output="out.png")
    print("Solved for: " + filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start()
    else:
        print('Usage: {0} filename'.format(sys.argv[0]))
