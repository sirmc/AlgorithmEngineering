package steinertree;

import java.util.Collection;
import java.util.Iterator;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;


public class Graph {

    private TreeSet<Edge> edges;
    private TreeSet<Vertex> vertices;

    public Graph() {
        edges = new TreeSet<Edge>();
        vertices = new TreeSet<Vertex>();
    }

    public Graph(Set<Vertex> vertices, Set<Edge> edges) {
        this.edges = (TreeSet<Edge>)edges;
        this.vertices = (TreeSet<Vertex>)vertices;
    }

    public boolean contains(Vertex v) {
        return vertices.contains(v);
    }

    public boolean contains(Edge e) {
        return edges.contains(e);
    }

    public void add(Vertex v) {
        vertices.add(v);
    }

    public void add(Edge e) {
        edges.add(e);
    }

    public void remove(Vertex v) {
        vertices.remove(v);
        edges.removeAll(incidentEdges(v));
    }

    public void remove(Edge e) {
        edges.remove(e);
    }

    public Set<Edge> edges(){
        return (Set)edges.clone();
    }

    public Set<Vertex> vertices() {
        return (Set)vertices.clone();
    }

    public Set<Edge> incidentEdges(Vertex v) {

        Stream<Edge> result = edges.stream().filter(e -> e.incidesWith(v));
        return result.collect(Collectors.toCollection(TreeSet::new));
    }

    public Set<Vertex> neighbors(Vertex v) {
        TreeSet<Vertex> result = new TreeSet<>();

        for (Edge e: incidentEdges(v)) {
            result.add(e.a);
            result.add(e.b);
        }
        return result;
    }

    public Graph subGraph(Set<Vertex> vertices) {
        TreeSet<Edge> edges = new TreeSet<>();
        for (Vertex v: vertices) {
            for (Edge e: incidentEdges(v)) {
                if (vertices.contains(e.a) && vertices.contains(e.b)) {
                    edges.add(e);
                }
            }

        }
        return new Graph((Set)vertices, (Set)edges);
    }

}
