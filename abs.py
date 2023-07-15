# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:38:43 2014

@author: DIGIT
"""
import tigraphs2 as tig
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import time

class Simplex(tig.BasicNode, object):
    def __init__(self, vertices, **kwargs):
        super(Simplex, self).__init__(**kwargs)
        
        self.vertices = vertices
        self.faces=[]
        self.cofaces=[]
        self.dimension = len(self.vertices)-1
        #These are used for initialising the complex:
        self._cfaces =[]
        self._children={}
        self.__parent = None
        

        
class SimplicialComplex(tig.return_tree_class(), object):
    def __init__(self, maximal_simplices, Vertex=Simplex, **kwargs):
        super(SimplicialComplex, self).__init__(Vertex=Vertex, **kwargs)
        self.maximal_simplices = maximal_simplices
        self.dimension = max(map(len,self.maximal_simplices))-1
        self.n_simplex_dict={} #Keeps track of simplexes by dimension.
        for i in range(-1,self.dimension+1):
            self.n_simplex_dict[i]=[]
        #Create the empty set 'root' of the structure.
        self.create_simplex([])
        self.set_root(self.vertices[0])
        self.vertices[0].label=str([])
        #Initialize complex from maximal simplices
        for ms in self.maximal_simplices:
            self.add_maximal_simplex(ms)
        
    def create_simplex(self, vertices):
        self.create_vertex(vertices)
        vertex = self.vertices[-1]    
        self.n_simplex_dict[vertex.dimension].append(self.vertices[-1])
        #It is convienient for the simplex to know its index for later on
        #when we create 'vectors' of simplices.
        index = len(self.n_simplex_dict[vertex.dimension])-1
        vertex.index=index
        vertex.label=str(vertices)

        
    def create_child(self, simplex, vertex):
        if vertex in simplex._cfaces:
            return
        simplex._cfaces.append(vertex)
        child_vertices=[v for v in simplex.vertices]
        child_vertices.append(vertex)
        self.create_simplex(child_vertices)
        child=self.vertices[-1]
        child._parent=simplex
        simplex._children[vertex]=child
        self.leaves.add(child)
        self.create_edge(ends=[simplex, child])
        simplex.cofaces.append(child)
        child.faces.append(simplex)
        
        
    def add_maximal_simplex(self, vertices, simplex=None, first=True):
        if first:
            simplex = self.get_root()
        
        if len(vertices) >= 1:
            for index in range(len(vertices)):
                vertex = vertices[index]
                self.create_child(simplex, vertex)
                self.add_maximal_simplex(simplex=simplex._children[vertex], vertices=vertices[index+1:], first=False)
                                        
    def get_simplex(self, address, first=True, simplex=None):
        if first:
            simplex = self.get_root()
        if len(address)==0:
            return simplex
        if address[0] not in simplex._cfaces:
            return None
        return self.get_simplex(address=address[1:], first=False, simplex=simplex._children[address[0]])
        
    def _boundary(self,simplex):
        vertices = simplex.vertices
        n = len(vertices)
        boundary=[]
        for index in range(n):
            boundary.append(vertices[:index]+vertices[index+1:])
        return boundary
    
    def add_face_coface(self, face, coface):
        if coface._parent != face:
            self.create_edge([face, coface])
            face.cofaces.append(coface)
            coface.faces.append(face)
    
    def update_adjacency_simplex(self, simplex):
        boundary_faces = self._boundary(simplex)
        boundary_faces = map(self.get_simplex, boundary_faces)
        for face in boundary_faces:
            self.add_face_coface(face,simplex)
        
    def update_adjacency(self):
        for i in range(self.dimension+1):
            for simplex in self.n_simplex_dict[i]:
                self.update_adjacency_simplex(simplex)
                       
    def plot(self,margin=60):
        A = self.get_adjacency_matrix_as_list()        
        g = ig.Graph.Adjacency(A, mode='undirected')
        for vertex in self.vertices:
            if vertex.label != None:
                index=self.vertices.index(vertex)
                g.vs[index]['label']=vertex.label
        layout = g.layout_reingold_tilford(root=[0])
        fig, ax = plt.subplots()
        ig.plot(g, layout=layout, target=ax)  
        plt.show()
           


#TEST
n = 4
maximal_simplices = [range(n)]
Sn = SimplicialComplex(maximal_simplices)
Sn.plot()
Sn.update_adjacency()
Sn.plot()