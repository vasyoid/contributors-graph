from random import random
from math import sqrt


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}
        self.forces = {}
        self.vertices_ids = {}
        self.labels_ids = {}
        self.edges_ids = {}

    def add_vertex(self, vertex):
        self.vertices[vertex] = (random(), random())
        self.forces[vertex] = (0, 0)

    def add_edge(self, u, v, weight):
        self.edges[u, v] = weight

    def normalise_edges(self):
        max_weight = 0
        for weight in self.edges.values():
            max_weight = max(max_weight, weight)
        for edge in self.edges.keys():
            self.edges[edge] /= max_weight

    def update(self, dt, threshold):
        for (u, v), weight in self.edges.items():
            uv = sub(self.vertices[v], self.vertices[u])
            expected = (1 - weight) * 3 + 1 if weight > threshold else 5
            actual = length(uv)
            delta = actual - expected
            k = 0.3
            if weight <= threshold and delta > 0:
                continue
            uv = mul(uv, k / actual * delta)
            self.forces[v] = sub(self.forces[v], uv)
            self.forces[u] = add(self.forces[u], uv)
        for k in self.vertices.keys():
            f = mul(self.forces[k], dt)
            self.vertices[k] = add(self.vertices[k], f)
            self.forces[k] = (0, 0)


def mul(a, x):
    return a[0] * x, a[1] * x


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def length(a):
    return sqrt(a[0] * a[0] + a[1] * a[1])
