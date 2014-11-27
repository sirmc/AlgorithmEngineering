#!/usr/bin/env python3.4
import sys
from graph_tool.all import *

def euclidean_steiner_tree(g):
    tree = min_spanning_tree(g)
    g.set_edge_filter(tree)
    return g

def start():
    filename = sys.argv[1]
    g = load_graph(filename)
    solution = euclidean_steiner_tree(g)

    pos = solution.new_vertex_property("vector<double>")
    # Set all positions to (0,0)
    for v in solution.vertices():
        pos[v] = (0,0)

    graph_draw(solution, pos=pos, output_size=(800, 800), output="out.png")
    print("Solved for: " + filename)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start()
    else:
        print('Usage: {0} filename'.format(sys.argv[0]))
