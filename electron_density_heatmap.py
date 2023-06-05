import numpy as np
from math import ceil
import matplotlib.pyplot as plt
import matplotlib 
from matplotlib.colors import LogNorm
import matplotlib.colors as colors

with open('CHGCAR', 'r') as f:
    lines = f.readlines()
    num_atoms = sum([int(x) for x in lines[6].split()])
    dead_lines = 10
    nx, ny, nz = [int(x) for x in lines[num_atoms+9].split()]
    num_density_lines = ceil((nx*ny*nz) / 5)
    end_index = num_atoms + dead_lines + num_density_lines
    data = np.array([float(x) for x in ' '.join(lines[num_atoms+dead_lines:end_index]).split()])
    
x = np.linspace(0, 1, nx, endpoint=False)
y = np.linspace(0, 1, ny, endpoint=False)
z = np.linspace(0, 1, nz, endpoint=False)
zz, yy, xx = np.meshgrid(z, y, x, indexing='ij')

a = np.array([float(x) for x in lines[2].split()])
b = np.array([float(x) for x in lines[3].split()])
c = np.array([float(x) for x in lines[4].split()])

V = abs(np.dot(a, np.cross(b, c)))
alpha = np.rad2deg(np.arccos(np.dot(b, c) / (np.linalg.norm(b) * np.linalg.norm(c))))
beta = np.rad2deg(np.arccos(np.dot(a, c) / (np.linalg.norm(a) * np.linalg.norm(c))))
gamma = np.rad2deg(np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))

xyzv = np.zeros((nx*ny*nz, 4))
xyzv[:, 0] = xx.flatten() * a[0] + yy.flatten() * b[0] + zz.flatten() * c[0]
xyzv[:, 1] = xx.flatten() * a[1] + yy.flatten() * b[1] + zz.flatten() * c[1]
xyzv[:, 2] = xx.flatten() * a[2] + yy.flatten() * b[2] + zz.flatten() * c[2]
xyzv[:, 3] = data.flatten() / V

np.savetxt('density.dat', xyzv, header=f'X Y Z Value alpha={alpha:.2f} beta={beta:.2f} gamma={gamma:.2f}', comments='', fmt='%12.6f')

data = np.loadtxt('density.dat', skiprows=1)
indices = np.random.choice(data.shape[0], size=int(data.shape[0] * 1), replace=False)
data = data[indices, :]
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
value = data[:, 3]
unique_z = np.unique(z)

for curr_z in unique_z:
    if curr_z < Z_Value_that_you_need:
        curr_indices = np.where(z == curr_z)  
        curr_x = x[curr_indices]
        curr_y = y[curr_indices]
        curr_value = value[curr_indices]
        curr_vmax = max(curr_value.max(), 1) if curr_value.max() >= 1 else 1
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        norm = colors.LogNorm(vmin=0.1, vmax=10)
        surf = ax.scatter(curr_x, curr_y, curr_z, c=curr_value, cmap='jet', norm=norm, s=1.8)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.view_init(elev=90, azim=0)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Value')
        ax.grid(False)
        ax.set_zticks([])
        ax.set_zticklabels([])
        ax.set_title(f'Z = {curr_z:.2f}')

plt.show()
