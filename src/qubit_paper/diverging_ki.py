import numpy as np
import matplotlib.pyplot as plt

# Calculate inductance

def ki(phic, phi, b):
    return phic**3/(2 * phic**2 - 3 * (phi - np.pi * b)**2 - 3 * (phi + np.pi * b)**2)

phic = 10*np.pi

b_values = [0, 3, 5.7]

print(b_values)
colors=['blue', 'red', 'green', 'black']

for i in range(len(b_values)):
    b=b_values[i]
    phi_values = np.linspace(-0.9 * np.sqrt(phic**2/3 - np.pi**2 * b**2), 0.9 * np.sqrt(phic**2/3 - np.pi**2 * b**2), 1000)
    color = colors[i]
    temp = ki(phic, phi_values, b)
    plt.plot(phi_values, np.log10(temp), linewidth=4, color=color)
plt.grid()
plt.xlabel(r"Global Phase $(\phi)$", fontsize=15)
plt.ylabel(r"$\log_{10}\left(\frac{2\pi}{\Phi_0}L_k\right)$", fontsize=15)
plt.savefig(f'imgs\\inductance_phic{np.round(phic,2)}.png')
plt.show()
plt.close()