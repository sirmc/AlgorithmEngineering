#!/usr/bin/env python3.4
import sys
import time
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


def improve_solution(g):
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
        add_edge(g2, a, v)
        add_edge(g2, b, v)
        add_edge(g2, c, v)

        # Remove old edges
        g2.remove_edge(g2.edge(a, b))
        g2.remove_edge(g2.edge(a, c))

        if total_weight(g2) < total_weight(g_best):
            g_best = g2
    return g_best

def add_edge(g, start, end):
    e = g.add_edge(start, end)

    v1 = g.vertex_properties["position"][e.source()]
    v2 = g.vertex_properties["position"][e.target()]
    g.edge_properties["weights"][e] = sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1]) ** 2)

def total_weight(g):
    return sum([g.edge_properties["weights"][e] for e in g.edges()])

def start():
    input_file = sys.argv[1]
    max_time = int(float(sys.argv[2]))
    assert int(float(sys.argv[3])) == 1 # Amount of threads
    output_file = open(sys.argv[4], 'w')

    start_time = time.time()

    """ Create base solution using MST """
    g = read_input(create_graph(), input_file, output_file)
    make_graph_complete(g)
    tree = min_spanning_tree(g, weights=g.edge_properties["weights"])
    g.set_edge_filter(tree)


    output_file.write("SECTION Solutions\n")

    mst_total_weight = current_total_weight = total_weight(g)
    print_solution(start_time, current_total_weight, output_file, mst_total_weight)
    plot_graph(g, "out1.png")

    """ Improve solution """
    g2 = g.copy()
    optimum_found = False
    while (time.time() - start_time < max_time and not optimum_found):
        g2 = improve_solution(g2)
        new_total_weight = total_weight(g2)
        optimum_found = (new_total_weight == current_total_weight)
        current_total_weight = new_total_weight
        print_solution(start_time, current_total_weight, output_file, mst_total_weight)
    output_file.write("End\n\n")
    plot_graph(g2, "out2.png")

    print_run_section(output_file, start_time, current_total_weight)
    print_final_solution_section(output_file, g2)

def print_final_solution_section(output_file, g):
    output_file.write(  "SECTION Finalsolution\n"
                        "Points %d\n"
                        "Edges %d\n" % (g.num_vertices(), g.num_edges()))
    for v in g.vertices():
        output_file.write("PP %f %f\n" % (tuple(g.vertex_properties["position"][v])))

    for e in g.edges():
        output_file.write("E %s %s\n" % (e.source(), e.target()))

    output_file.write("End\n")


def print_run_section(output_file, start_time, best_solution):
    output_file.write(  "SECTION Run\n"
                        "Threads 1\n"
                        "Time %.2f\n"
                        "Primal %.6f\n"
                        "End\n\n" % (time.time() - start_time, best_solution))

def print_solution(start_time, quality, output_file, mst_total_weight):
    output = "Solution %.2fs %.6f" % (time.time() - start_time, quality)
    print(output + " (%.5fx best)" % (quality / (mst_total_weight / 1.1547)))
    output_file.write(output + "\n")

def plot_graph(g, name):
    graph_draw(g,
            vertex_text=g.vertex_index,
            pos=g.vertex_properties["position"],
            output_size=(800, 800),
            output=name)


def read_input(g, input_file, output_file):
    with open(input_file) as fp:
        line = fp.readline()
        while line:
            if "section comments" in line.lower():
                write_comment_section(read_program_name(fp), output_file)
            elif "section graph" in line.lower():
                read_graph(g, fp)
            elif "section coordinates" in line.lower():
                read_coordinates(g, fp)
            elif "eof" in line.lower():
                break
            line = fp.readline()
    return g

def make_graph_complete(g):
    for i in g.vertices():
        for j in g.vertices():
            if not i == j:
                add_edge(g, i, j)

def create_graph():
    g = Graph(directed=False)
    pos = g.new_vertex_property("vector<double>")
    g.vertex_properties["position"] = pos

    weights = g.new_edge_property("double")
    g.edge_properties["weights"] = weights
    return g

def write_comment_section(name, output_file):
    output_file.write(  "SECTION Comment\n"
                        "Name %s\n"
                        "Problem \"ESMT\"\n"
                        "Program \"ESMT Solver\"\n"
                        "Version \"0.11\"\n"
                        "End\n\n" % (name))

def read_program_name(fp):
    return fp.readline().split()[1]

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
