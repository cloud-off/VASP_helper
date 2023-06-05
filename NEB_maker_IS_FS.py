import numpy as np
from scipy.spatial.distance import cdist

# Read IS.vasp file
with open('IS.vasp', 'r') as f:
    lines = f.readlines()
# Extract lattice vectors
lattice = np.array([[float(x) for x in lines[i].split()] for i in range(2, 5)])
# Extract atom types and their numbers from IS.vasp
atom_types = lines[5].split()
atom_numbers = [int(x) for x in lines[6].split()]
# Extract atomic coordinates from IS.vasp
is_coords = []
for i in range(8, len(lines)):
    is_coords.append([float(x) for x in lines[i].split()[0:3]])
is_coords = np.array(is_coords)
# Read FS.vasp file
with open('FS.vasp', 'r') as f:
    lines = f.readlines()
# Extract atomic coordinates from FS.vasp
fs_coords = []
for i in range(8, len(lines)):
    fs_coords.append([float(x) for x in lines[i].split()[0:3]])
fs_coords = np.array(fs_coords)
# Separate coordinates into different areas based on atom types in IS.vasp
is_areas = []
fs_areas = []
start_idx = 0
for num in atom_numbers:
    end_idx = start_idx + num
    is_areas.append(is_coords[start_idx:end_idx])
    fs_areas.append(fs_coords[start_idx:end_idx])
    start_idx = end_idx
# Function to calculate the distance between two sets of atomic coordinates
def calculate_distance(coords1, coords2, lattice):
    diff = coords1 - coords2
    return np.linalg.norm(np.dot(diff, lattice), axis=1)
# Calculate distances between atoms in same areas in IS.vasp and FS.vasp
distances = []
for i in range(len(atom_types)):
    is_area = is_areas[i]
    fs_area = fs_areas[i]
    distances_area = cdist(is_area, fs_area, metric='euclidean')
    distances.append(distances_area)
# Find the nearest atom in FS.vasp for each atom in IS.vasp for each area
nearest_indices = []
for i in range(len(atom_types)):
    nearest_indices_area = np.argmin(distances[i], axis=1)
    nearest_indices.append(nearest_indices_area)
# Reorder atoms in IS.vasp based on the nearest atoms in FS.vasp for each area
is_coords_reordered = []
for i in range(len(atom_types)):
    is_area = is_areas[i]
    nearest_indices_area = nearest_indices[i]
    is_coords_reordered_area = is_area[nearest_indices_area]
    is_coords_reordered.append(is_coords_reordered_area)
is_coords_reordered = np.concatenate(is_coords_reordered, axis=0)
# Write reordered IS.vasp coordinates to a new file
with open('IS_reordered.vasp', 'w') as f:
    for i in range(len(lines)):
        if i < 8:
            f.write(lines[i])
        else:
            f.write('{:.6f} {:.6f} {:.6f}\n'.format(is_coords_reordered[i-8][0], is_coords_reordered[i-8][1], is_coords_reordered[i-8][2]))
print("IS.vasp coordinates have been reordered and written to IS_reordered.vasp.")
