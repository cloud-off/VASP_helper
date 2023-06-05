# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:21:29 2023

@author: vladi
"""

import os
import matplotlib.pyplot as plt
import numpy as np

EDIFFG = 0.02

result_lines = []  # список для хранения строк, которые будут записаны в файл results.txt

# находим все папки в текущей директории
folders = [folder for folder in os.listdir() if os.path.isdir(folder)]

for folder in folders:
    # находим файл OUTCAR в каждой папке
    outcar_path = os.path.join(folder, "OUTCAR")
    if os.path.exists(outcar_path):
        with open(outcar_path, "r") as file:
            data = file.readlines()
            
        dF_list = []
        energy_list = []
        
        for line in data:
            if "FORCES: max atom" in line:
                dF = float(line.split()[4])
                dF_list.append(dF)
                
            if "free  energy   TOTEN" in line:
                energy = float(line.split()[4])
                energy_list.append(energy)
                
        # создаем список номеров итераций
        iter_list = list(range(1, len(dF_list) + 1))
        
        # строим график
        fig, ax1 = plt.subplots()
        color = 'tab:blue'
        ax1.set_xlabel('Iteration number')
        ax1.set_ylabel('Max force', color=color)
        ax1.semilogy(iter_list, dF_list, 'b.-', label='Max force')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.axhline(EDIFFG, color='blue', linestyle='--', label='EDIFFG param')
        
        ax2 = ax1.twinx()  # создаем вторую ось
        color = 'tab:red'
        ax2.set_ylabel('Energy, eV', color=color)
        ax2.plot(iter_list, energy_list, 'r.-', label='Energy')
        ax2.tick_params(axis='y', labelcolor=color)
        fig.tight_layout()  # автоматически подгоняет расположение графиков
        plt.title(f'{folder}')
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='best')
        
        # сохраняем график с соответствующим названием
        fig.savefig(f"{folder}_convergence.png")
        
        # добавляем строку в список результатов для файла results.txt
        last_iter = len(dF_list)
        result_lines.append(f"{folder}: dF={dF_list[last_iter-1]}, energy={energy_list[last_iter-1]}")
        
# записываем результаты в файл results.txt
with open("results.txt", "w") as file:
    file.write("\n".join(result_lines))


# открываем файл results.txt и считываем данные
with open("results.txt", "r") as file:
    data = file.readlines()

# создаем списки для значений силы и энергии
dF_list = []

# проходим по каждой строке в файле и извлекаем значения силы и энергии
for line in data:
    # разбиваем строку на части по разделителю ":"
    parts = line.split(": ")
    # извлекаем название файла
    filename = parts[0]
    # извлекаем значение силы
    dF = float(parts[1].split(", ")[0].split("=")[1])
    dF_list.append(dF)
# создаем список меток для оси X (название файлов)
labels = []
for line in data:
    labels.append(line.split(": ")[0])

# создаем фигуру и оси для гистограммы
fig, ax = plt.subplots()

# создаем два столбика для каждого файла
bar_width = 0.35
index = list(range(len(labels)))
ax.bar(index, dF_list, bar_width, label='Max force')

# добавляем линию на уровне EDIFFG
ax.axhline(y=0.02, linestyle='--', color='black')

# настраиваем метки и заголовки графика
ax.set_ylabel('Value')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(labels)
ax.set_title('Values from results.txt')
ax.set_yscale("log")
plt.xticks(rotation=75)
# добавляем легенду
ax.legend()

# показываем гистограмму
plt.show()