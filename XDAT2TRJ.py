from ase.io import read, write
import ase.io
# Read XDATCAR file
atoms_list = read('XDATCAR', index=':')
# Write to .trj file
with open('output.trj', 'w') as f:
    write('output.trj', atoms_list, format='traj')
traj = ase.io.read('output.trj', ':')
# Write the trajectory to an XYZ file
ase.io.write('your_traj_file.xyz', traj)
