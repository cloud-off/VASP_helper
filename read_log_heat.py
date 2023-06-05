import numpy as np
from math import ceil


# Открытие файла CHGCAR и чтение блока данных плотности
with open('CHGCAR', 'r') as f:
    lines = f.readlines()
    num_atoms = sum([int(x) for x in lines[6].split()])
    dead_lines = 10
    nx, ny, nz = [int(x) for x in lines[num_atoms+9].split()]
    num_density_lines = ceil((nx*ny*nz) / 5)
    end_index = num_atoms + dead_lines + num_density_lines
    
    data = np.array([float(x) for x in ' '.join(lines[num_atoms+dead_lines:end_index]).split()])

# Извлечение размеров сетки плотности


# Преобразование массива значений плотности в массив координат X, Y, Z
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



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import matplotlib 
from matplotlib.colors import LogNorm
import matplotlib.colors as colors

# def on_mouse_move(event):
#     if event.button == 'down':
#         ax.view_init(azim=ax.azim + event.dx, elev=ax.elev + event.dy)
#         plt.pause(1)
#         plt.draw()


# def on_scroll(event):
#     # Получаем текущие пределы осей x, y и z
#     xlim = ax.get_xlim3d()
#     ylim = ax.get_ylim3d()
#     zlim = ax.get_zlim3d()
#     # Вычисляем текущие размеры графика
#     xsize = xlim[1] - xlim[0]
#     ysize = ylim[1] - ylim[0]
#     zsize = zlim[1] - zlim[0]
#     # Вычисляем новые размеры графика в соответствии с направлением прокрутки
#     if event.button == 'up':
#         k = 0.9  # коэффициент масштабирования при приближении
#     elif event.button == 'down':
#         k = 1.1  # коэффициент масштабирования при отдалении
#     xsize_new = xsize * k
#     ysize_new = ysize * k
#     zsize_new = zsize * k
#     # Вычисляем новые пределы осей в соответствии с новыми размерами графика
#     xcenter = (xlim[0] + xlim[1]) / 2
#     ycenter = (ylim[0] + ylim[1]) / 2
#     zcenter = (zlim[0] + zlim[1]) / 2
#     xlim_new = (xcenter - xsize_new / 2, xcenter + xsize_new / 2)
#     ylim_new = (ycenter - ysize_new / 2, ycenter + ysize_new / 2)
#     zlim_new = (zcenter - zsize_new / 2, zcenter + zsize_new / 2)
#     # Устанавливаем новые пределы для осей x, y и z
#     ax.set_xlim3d(xlim_new)
#     ax.set_ylim3d(ylim_new)
#     ax.set_zlim3d(zlim_new)
#     fig.canvas.draw_idle()
    
    
    
# plt.ion()


# matplotlib.use('TkAgg')  # или 'Qt5Agg'
data = np.loadtxt('density.dat', skiprows=1)

indices = np.random.choice(data.shape[0], size=int(data.shape[0] * 1), replace=False)
data = data[indices, :]

x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
value = data[:, 3]

unique_z = np.unique(z)  # получаем уникальные значения Z


for curr_z in unique_z:
    if curr_z < 8:
        curr_indices = np.where(z == curr_z)  
        curr_x = x[curr_indices]
        curr_y = y[curr_indices]
        curr_value = value[curr_indices]
        curr_vmax = max(curr_value.max(), 1) if curr_value.max() >= 1 else 1
    
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        norm = colors.LogNorm(vmin=0.1, vmax=10)  # определяем логарифмическую шкалу
        surf = ax.scatter(curr_x, curr_y, curr_z, c=curr_value, cmap='jet', norm=norm, s=1.8)

        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.view_init(elev=90, azim=0)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Value')
        # Remove the grid lines while keeping the axes and ticks
        ax.grid(False)
        ax.set_zticks([])
        ax.set_zticklabels([])
        
        # fig.canvas.callbacks.connect('scroll_event', on_scroll)
        # fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)
        
        
        ax.set_title(f'Z = {curr_z:.2f}')  # добавляем заголовок с текущим значением Z

plt.show()
# run = True
# while run:
#     plt.show()
#     plt.pause(0.1)
