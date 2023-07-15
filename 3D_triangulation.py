import numpy as np
import gudhi as gd
import matplotlib.pyplot as plt
import time

time_start = time.perf_counter()

# Generate the 2D grid points
Nx = 5
Ny = 5
Nt = 5

x_periodic = True
y_periodic = True
t_periodic = False

def generate_simplices(Nx, Ny, Nt):
    x = np.arange(0, Nx)
    y = np.arange(0, Ny)
    t = np.arange(0, Nt)

    grid_points = np.array(np.meshgrid(x, y, t)).T.reshape(-1, 3)

    # Create an AlphaComplex for the 2D grid
    ac = gd.AlphaComplex(points=grid_points)

    # Compute the 2D triangulation
    st = ac.create_simplex_tree(default_filtration_value=True)

    # Get the list of simplices in the tessellation
    skeleton_gen = st.get_skeleton(3)

    skeleton = []
    for simplex in skeleton_gen:
        skeleton.append(simplex[0])
    
    return grid_points, skeleton


grid_points, skeleton = generate_simplices(Nx, Ny, Nt)

# Plotting the triangles
fig = plt.subplots()
ax = plt.axes(projection ="3d")

# Hide grid
#ax.axis('off')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('T')

#extract 0-simplices (vertices) from gudhi triangulation, returns point labels and labels before periodicization
def verteces(skeleton):
    points = []
    non_periodic_labels = []
    for simplex in skeleton:
        if len(simplex) == 1:
            
            non_periodic_labels.append(simplex[0])

            point_coords = grid_points[simplex[0]]

            #print(point_coords)
            
            if x_periodic:
                #impose periodicity in the labelling on x
                if point_coords[0] == Nx-1:
                    simplex[0] -= Ny*(Nx-1)
            if y_periodic:
                #impose periodicity in the labelling on y
                if point_coords[1] == Ny-1:
                    simplex[0] -= (Ny-1)
            if t_periodic:
                #impose periodicity in the labelling on t            
                if point_coords[2] == Nt-1:
                    simplex[0] -= Nx*Ny*(Nt-1)

            point_coords = grid_points[simplex[0]]

            points.append(simplex[0])

            #plotting
            ax.scatter3D(point_coords[0], point_coords[1], point_coords[2], color='black')
            ax.text(point_coords[0], point_coords[1], point_coords[2], f'{simplex[0]}')
    return points, non_periodic_labels

points, non_periodic_labels = verteces(skeleton)

print(points)

def edges(skeleton):
    edges = []
    edge_causality = []
    for simplex in skeleton:
        if len(simplex) == 2:
            
            #impose label periodicity
            for i, label in enumerate(simplex):
                for j, old_label in enumerate(non_periodic_labels):
                    if label == old_label:
                        simplex[i] = points[j]

            edges.append(simplex)

            #plotting and coloring spacelike/timelike edges
            point1_coords = grid_points[simplex[0]]
            point2_coords = grid_points[simplex[1]]

            col = 0
            if point1_coords[2] != point2_coords[2]:
                edge_causality.append('t')
                col = 'red'
            else:
                edge_causality.append('s')
                col = 'blue'

            ax.plot([point1_coords[0], point2_coords[0]], [point1_coords[1], point2_coords[1]], [point1_coords[2], point2_coords[2]], color=col)
    return edges


edges_with_redundancies = edges(skeleton)


#delete redundant edges
def uniquify_edges(edges):
    unique_edges = []
    for edge in edges:
        flipped_edge = [edge[1], edge[0]]
        if edge not in unique_edges:
            if flipped_edge not in unique_edges:
                unique_edges.append(edge)
    return unique_edges


edges = uniquify_edges(edges_with_redundancies)

print(edges)

def triangles(skeleton):
    triangles = []
    for simplex in skeleton:
        if len(simplex) == 3:
            
            #impose label periodicity
            for i, label in enumerate(simplex):
                for j, old_label in enumerate(non_periodic_labels):
                    if label == old_label:
                        simplex[i] = points[j]

            triangles.append(simplex)
    return triangles

triangles = triangles(skeleton)
print(triangles)

def tetrahedra(skeleton):
    tetrahedra = []
    for simplex in skeleton:
        if len(simplex) == 4:

            #impose label periodicity
            for i, label in enumerate(simplex):
                for j, old_label in enumerate(non_periodic_labels):
                    if label == old_label:
                        simplex[i] = points[j]

            tetrahedra.append(simplex)
    return tetrahedra
    
tetrahedra = tetrahedra(skeleton)
print(tetrahedra)

time_elapsed = (time.perf_counter() - time_start)
print ("checkpoint %5.1f secs" % (time_elapsed))

plt.show()