import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plus_func(phic, b):
    return np.sqrt((phic**2)/3.0 - np.pi**2*b**2)

def negative_func(phic, b):
    return -1 * np.sqrt((phic**2)/3.0 - np.pi**2*b**2)

def plus_func_bruh(phic, b):
    return np.sqrt((phic**2)/1.0 - 3*np.pi**2*b**2)

def negative_func_bruh(phic, b):
    return -1 * np.sqrt((phic**2)/1.0 - 3*np.pi**2*b**2)

phics = [10*np.pi]
colors = ['blue', 'red', 'green']

for i in range(len(phics)):
    phic = phics[i]
    color = colors[i]
    b_bound = np.sqrt(phic**2/(3*np.pi**2))
    b_values = np.linspace(-b_bound,b_bound,10000)
    global_phi_plus = [plus_func(phic, b) for b in b_values]
    global_phi_negative = [negative_func(phic, b) for b in b_values]
    plt.plot(b_values, global_phi_plus, linewidth=3, color=color)
    plt.plot(b_values, global_phi_negative, linewidth=3, color=color)
    bruh1 = [plus_func_bruh(phic, b) for b in b_values]
    bruh2 = [negative_func_bruh(phic, b) for b in b_values]
    plt.plot(b_values, bruh1, linewidth=3, color='red')
    plt.plot(b_values, bruh2, linewidth=3, color='red')

plt.grid()
plt.ylabel(r"Global Phase $(\phi)$", fontsize=15)
plt.xlabel(r"Magnetic Field $(b)$", fontsize=15)
plt.savefig('imgs\\phi_v_I.png')
plt.show()
plt.close()