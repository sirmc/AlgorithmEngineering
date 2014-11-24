package steinertree;


public class Edge implements Comparable<Edge> {
    Vertex a;
    Vertex b;

    public Edge(Vertex a, Vertex b) {
        this.a = a;
        this.b = b;
    }

    public boolean equals(Edge e) {
        return (a.equals(e.a) && b.equals(e.b)) || (a.equals(e.b) && b.equals(e.a));
    }

    public boolean incidesWith(Vertex v) {
        return a.equals(v) || b.equals(v);
    }

    @Override
    public int compareTo(Edge e) {
        if (this.equals(e)) {
            return 0;
        }
        if (a.compareTo(e.a) != 0) {
            return a.compareTo(e.a);
        } else {
            return b.compareTo(e.b);
        }
    }
}
