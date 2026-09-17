import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def potential(phi, phi_c, b):
    return (phi**2 + (np.pi*b)**2)/phi_c - (phi**4 + 6*phi**2*(np.pi*b)**2 + (np.pi*b)**4)/(2*phi_c**3)

b_values = [0]

phi_c = 2*np.pi

phi_values = np.linspace(-phi_c*1.1, phi_c*1.1, 500)

all_potentials = []

for b in b_values:
    U_phi = [potential(phi, phi_c, b) for phi in phi_values]
    all_potentials.append(U_phi)

for i in range(len(all_potentials)):
    arr = all_potentials[i]
    plt.plot(phi_values, arr, linewidth=5,color='blue')
plt.grid()
plt.xlabel(r"Global Phase ($\varphi$)", fontsize=16)
plt.ylabel("Energy", fontsize=16)
# plt.legend(loc="upper right")
plt.savefig(f"imgs\\potentials_b{b_values[0]}.png")
plt.show()