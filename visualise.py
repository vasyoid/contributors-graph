import sys

from collect import load_contributors_stats
from graph import Graph
from frame import run_frame


def main():
    contributors = load_contributors_stats(sys.argv[1])
    graph = Graph()

    for contributor in contributors:
        graph.add_vertex(contributor.name)

    for i in range(len(contributors)):
        for j in range(i):
            left = contributors[i]
            right = contributors[j]
            weight = len(left.files.intersection(right.files)) / len(left.files.union(right.files))
            graph.add_edge(left.name, right.name, weight)

    graph.normalise_edges()
    run_frame(graph)


if __name__ == '__main__':
    main()
