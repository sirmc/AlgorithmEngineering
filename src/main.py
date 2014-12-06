#!/usr/bin/env python3.4
import sys
from math import sqrt
from graph_tool.all import *
from numpy import *


def euclidean_steiner_tree(g):
    tree = min_spanning_tree(g)
    g.set_edge_filter(tree)
    return g


def get_positions(g):
    x = g.vertex_properties["x"].get_array()
    y = g.vertex_properties["y"].get_array()
    coord = dstack((x, y))
    pos = g.new_vertex_property("vector<double>")
    for i, v in enumerate(g.vertices()):
        pos[v] = coord[0][i]
    return pos


def start():

    input_file = sys.argv[1]
    time = int(float(sys.argv[2])) # Not used for now.
    threads = int(float(sys.argv[3]))
    output_file = sys.argv[4]

    assert threads == 1 # Only single threaded it supported at the moment.

    g = read_input(input_file, output_file)


    weights = g.new_edge_property("double")
    g.edge_properties["weights"] = weights


    for i in g.vertices():
        for j in g.vertices():
            if not i == j:
                v1 = g.vertex_properties["position"][i]
                v2 = g.vertex_properties["position"][j]
                weight = sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1]) ** 2)
                e = g.add_edge(i, j)
                g.edge_properties["weights"][e] = weight

    tree = min_spanning_tree(g, weights=g.edge_properties["weights"])
    g.set_edge_filter(tree)

    for e in g.edges():
        print("%s - (%f)" %(e, g.edge_properties["weights"][e]))


    graph_draw(g, vertex_text=g.vertex_index, pos=g.vertex_properties["position"], output_size=(800, 800), output="out.png")





def read_input(input_file, output_file):

    g = Graph(directed=False)
    pos = g.new_vertex_property("vector<double>")
    g.vertex_properties["position"] = pos

    with open(input_file) as fp:
        line = fp.readline()
        while line:
            if "section graph" in line.lower():
                read_graph(g, fp)
            elif "section coordinates" in line.lower():
                read_coordinates(g, fp)
            elif "eof" in line.lower():
                break
            line = fp.readline()

    return g

def read_graph(g, fp):
    node_count = int(fp.readline().split()[1])

    for n in range(node_count):
        g.add_vertex()


def read_coordinates(g, fp):
    line = fp.readline()
    while line and "end" not in line.lower():
        words = line.split()
        id = int(words[1]) - 1
        coordinate = tuple(words[2:4])
        g.vertex_properties["position"][g.vertex(id)] = coordinate



        line = fp.readline()

if __name__ == "__main__":
    if len(sys.argv) == 5:
        start()
    else:
        print('Usage: %s filename time threads outputfile\n' % (sys.argv[0]))
