#!/usr/bin/env python3.4
import sys
from math import sqrt
from graph_tool.all import *
from numpy import *
from itertools import permutations


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

def find_triangles(g):
    for v1 in g.vertices():
        neighbors = list(v1.out_neighbours())
        if len(neighbors) > 1:
            for pe in permutations(neighbors,2):
                yield (v1,) + pe


def improve(g):
    g_best = g.copy()
    triangles = find_triangles(g)
    #(a,b,c) = next(triangles, None)
    for (a,b,c) in triangles:
        a_pos = g.vertex_properties["position"][a]
        b_pos = g.vertex_properties["position"][b]
        c_pos = g.vertex_properties["position"][c]
        v_pos = tuple(map(lambda a: 1/3*sum(a),zip(a_pos,b_pos,c_pos)))

        g2 = Graph(g=g.copy(), prune=True)
        v = g2.add_vertex()
        g2.vertex_properties["position"][v] = v_pos

        # Add new edges
        te1 = g2.add_edge(a,v)
        set_edge_weight(te1,g2)

        te2 = g2.add_edge(b,v)
        set_edge_weight(te2,g2)

        te3 = g2.add_edge(c,v)
        set_edge_weight(te3,g2)
        
        # Remove old edges
        e1 = g2.edge(a,b)
        e2 = g2.edge(a,c)
        g2.remove_edge(e1)
        g2.remove_edge(e2)

        if total_weight(g2) < total_weight(g_best):
            g_best = g2
    return g_best


def set_edge_weight(e, g):
    v1 = g.vertex_properties["position"][e.source()]
    v2 = g.vertex_properties["position"][e.target()]
    g.edge_properties["weights"][e] = sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1]) ** 2)

def total_weight(g):
    return sum([g.edge_properties["weights"][e] for e in g.edges()])

def start():

    input_file = sys.argv[1]
    time = int(float(sys.argv[2])) # Not used for now.
    threads = int(float(sys.argv[3]))
    output_file = sys.argv[4]

    assert threads == 1 # Only single threaded it supported at the moment.

    g = read_input(input_file, output_file)

    tree = min_spanning_tree(g, weights=g.edge_properties["weights"])
    g.set_edge_filter(tree)


    for e in g.edges():
        print("%s - (%f)" %(e, g.edge_properties["weights"][e]))

    print("Total weight: %f" % total_weight(g))
    graph_draw(g, vertex_text=g.vertex_index, pos=g.vertex_properties["position"], output_size=(800, 800), output="out.png")

    g2 = g.copy()
    for i in range(10):
        g2 = improve(g2)
        print("Total weight: %f" % total_weight(g2))
        graph_draw(g2, vertex_text=g2.vertex_index, pos=g2.vertex_properties["position"], output_size=(800, 800), output="out2.png")






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
