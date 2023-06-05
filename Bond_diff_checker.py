import numpy as np

# Read in the POSCAR file
with open('POSCAR', 'r') as f:
    lines = f.readlines()

# Extract the lattice vectors
a = np.array(lines[2].split(), dtype=float)
b = np.array(lines[3].split(), dtype=float)
c = np.array(lines[4].split(), dtype=float)

# Extract the atomic positions and species
num_atoms = np.sum([int(x) for x in lines[6].split()])
species = lines[5].split()
positions = np.zeros((num_atoms, 3))
for i in range(num_atoms):
    positions[i] = np.array(lines[8+i].split()[:3], dtype=float)

# Calculate the distances between each pair of atoms
distances_poscar = np.zeros((num_atoms, num_atoms))
for i in range(num_atoms):
    for j in range(i+1, num_atoms):
        separation = positions[j] - positions[i]
        separation -= np.round(separation)
        distance = np.linalg.norm(np.dot(separation, [a, b, c]))
        distances_poscar[i, j] = distance
        distances_poscar[j, i] = distance

# Calculate the sum of bond lengths restricted to 2.2 angstroms in POSCAR
bond_sum_poscar = 0.0
for i in range(num_atoms):
    for j in range(i+1, num_atoms):
        if distances_poscar[i, j] <= 2.2:
            bond_sum_poscar += distances_poscar[i, j]

# Read in the CONTCAR file
with open('CONTCAR', 'r') as f:
    lines = f.readlines()

# Extract the lattice vectors
a = np.array(lines[2].split(), dtype=float)
b = np.array(lines[3].split(), dtype=float)
c = np.array(lines[4].split(), dtype=float)

# Extract the atomic positions and species
num_atoms = np.sum([int(x) for x in lines[6].split()])
species = lines[5].split()
positions = np.zeros((num_atoms, 3))
for i in range(num_atoms):
    positions[i] = np.array(lines[8+i].split()[:3], dtype=float)

# Calculate the distances between each pair of atoms
distances_contcar = np.zeros((num_atoms, num_atoms))
for i in range(num_atoms):
    for j in range(i+1, num_atoms):
        separation = positions[j] - positions[i]
        separation -= np.round(separation)
        distance = np.linalg.norm(np.dot(separation, [a, b, c]))
        distances_contcar[i, j] = distance
        distances_contcar[j, i] = distance

# Calculate the sum of bond lengths restricted to 2.2 angstroms in CONTCAR
bond_sum_contcar = 0.0
for i in range(num_atoms):
    for j in range(i+1, num_atoms):
        if distances_contcar[i, j] <= 2.2:
            bond_sum_contcar += distances_contcar[i, j]

# Calculate the difference in bond sums
bond_diff = bond_sum_contcar - bond_sum_poscar

print("Sum of bond lengths restricted to 2.2 angstroms in POSCAR:", bond_sum_poscar)
print("Sum of bond lengths restricted to 2.2 angstroms in CONTCAR:", bond_sum_contcar)
print("Difference", bond_diff)