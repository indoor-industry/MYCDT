# -*- coding: utf-8 -*-
import tigraphs2 as tig


def iterate_triangles(graph):
    G=graph
    V=G.vertices
    V.sort(key=lambda x: G.get_degree(x), reverse=True)
    n=len(V)
    A={}
    for i in range(n):
        V[i].index=i
        A[V[i]]=set()
    for first_vertex in V:
        for second_vertex in G.get_vertex_neighbors(first_vertex):
            if first_vertex.index < second_vertex.index:
                for third_vertex in A[first_vertex].intersection(A[second_vertex]):
                    yield [first_vertex.index, second_vertex.index, third_vertex.index]
                A[second_vertex].add(first_vertex)

import time
times ={}
for i in range(3,20):
    print(i)
    G=tig.Complete(i)
    start= time.perf_counter()
    for j in range(10000):
        count=0
        for triangle in iterate_triangles(G):
            count+=1
    timer = (time.perf_counter() - start)
    times[i]=timer
print(times)
    
import matplotlib.pyplot as plt
no_vertices=range(3,20)
def foo(x):
    x=float(x)
    return x*(x-1)/2
no_edges = [foo(x) for x in no_vertices]
run_time=[times[i] for i in no_vertices]
plt.plot(no_edges, run_time)
plt.xlabel('Number of edges in Complete Graph')
plt.ylabel('Runtime in secs for 10000 triangle iterations')
plt.show()