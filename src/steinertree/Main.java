package steinertree;


import java.util.Random;
import java.util.TreeSet;


public class Main {

    void start() {
        test();
    }

    void test() {
        Random rnd = new Random();
        TreeSet<Vertex> vertices = new TreeSet<Vertex>();
        TreeSet<Edge> edges = new TreeSet<Edge>();

        for (int i = 0; i < 100; i++) {
            vertices.add(new Vertex(String.valueOf(i)));
        }

        for (Vertex v1: vertices) {
            for (Vertex v2: vertices) {
                if (rnd.nextDouble() > 0.95) {
                    edges.add(new Edge(v1, v2));
                }
            }

        }

        Graph graph = new Graph(vertices, edges);

        printGraph(graph);
        System.out.println("SUBGRAPH:\n");
        printGraph(graph.subGraph(vertices.subSet(new Vertex("1"), new Vertex("17"))));
    }

    void printGraph(Graph g) {
        for (Vertex v: g.vertices()) {
            System.out.printf("<%s>: ", v);
            for (Edge e: g.incidentEdges(v)) {
                System.out.printf("(%s, %s) ", e.a, e.b);
            }
            System.out.println();
        }
    }
    public static void main(String[] args) {
	    new Main().start();
    }
}
