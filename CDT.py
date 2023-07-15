import tigraphs2 as tig
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import time

time_start = time.perf_counter()

points = np.load('triangulation_data_2D/points.npy')
edges = np.load('triangulation_data_2D/edges.npy')

#create graph with a number of vertices
no_vertices = len(points)
G = tig.UnDirGraph()
tig.UnDirGraph.create_vertices(G, no_vertices)

#label vertices with integers
i = 0
for node in G.vertices:
    tig.BasicNode.add_label(node, points[i])
    print(node.label)
    i+=1

#add edges from file
for edge in edges:
    ends = [0, 0]
    for node in G.vertices:
        if edge[0] == node.label:
            ends[0] = node
        if edge[1] == node.label:
            ends[1] = node

    tig.UnDirGraph.create_edge(G, ends)

G.plot()


time_elapsed = (time.perf_counter() - time_start)
print ("checkpoint %5.1f secs" % (time_elapsed))