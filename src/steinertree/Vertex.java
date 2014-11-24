package steinertree;

import java.util.Comparator;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Vertex implements Comparable<Vertex> {
    String identifier;

    public Vertex(String identifier) {
        this.identifier = identifier;
    }
    public boolean equals(Vertex o) {
        return identifier.equals(o.identifier);
    }


    public String toString() {
        return identifier;
    }

    @Override
    public int compareTo(Vertex o) {
        return this.identifier.compareTo(o.identifier);
    }
}
