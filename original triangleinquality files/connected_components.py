# -*- coding: utf-8 -*-

import tigraphs as tig

def get_connected_components(graph):
    vertices = graph.vertices
    edges=graph.edges
    for vertex in vertices:
        vertex.seen_before=False
    for edge in edges:
        edge.seen_before=False
    components=[]
    for vertex in vertices:
        component=get_component(graph, vertex)
        if component:
            components.append(component)
    return components
    
def get_component(graph, vertex): #assumes vertices .seen_before initiated
    component=tig.UnDirGraph()
    check=True 
    def get_component_recursive(graph, vertex, first=False):
        if vertex.seen_before:
            if first:
                return False
            return
        else:
            component.add_vertex(vertex)
            vertex.seen_before=True
        for incident_edge in graph.get_incident_edges(vertex):
            if not incident_edge.seen_before:
                incident_edge.seen_before=True
                for target in incident_edge.ends:
                    if target != vertex:
                        component.create_edge([vertex, target])
                        get_component_recursive(graph, target)
    check=get_component_recursive(graph, vertex, first=True)
    if check==False:
        return check
    else:
        return component
    
G=tig.Complete(5)
H=tig.create_linear(number_vertices=5)
GunionH=tig.UnDirGraph(vertices=G.vertices+H.vertices, edges=G.edges.union(H.edges))
GunionH.plot()
get_connected_components(GunionH)[0].plot()
get_connected_components(GunionH)[1].plot()