import numpy as np
import matplotlib.pyplot as plt

def plus_func(phic, b):
    return np.sqrt((phic**2)/3.0 - np.pi**2*b**2)

def negative_func(phic, b):
    return -1 * np.sqrt((phic**2)/3.0 - np.pi**2*b**2)

def icb(phi, phic, b, m, n, a):
    return 2 * phi/phic - a * (phi - np.pi * (b - n))**(2*m+1)/(phic**(2*m+1)) - a * (phi + np.pi * (b - n))**(2*m+1)/(phic**(2*m+1))

# NOTE: The program only works for m = 1

phic_values = [10*np.pi]

m=1
n=0
a=1

m_values = [1]
colors=['blue', 'red', 'green', 'black']

for k in range(len(phic_values)):
    phic = phic_values[k]

    b_bound = np.sqrt(phic**2/(3*np.pi**2))
    b_values = np.linspace(-b_bound+1e-4,b_bound-1e-4,10000)

    global_phi_plus = [plus_func(phic, b) for b in b_values]
    global_phi_negative = [negative_func(phic, b) for b in b_values]

    for i in range(len(m_values)):
        m = m_values[i]
        color=colors[k]
        icb_plus = [icb(plus_func(phic, b), phic=phic, b=b, m=m, n=n, a=a) for b in b_values]
        icb_negative = [icb(negative_func(phic, b), phic=phic, b=b, m=m, n=n, a=a) for b in b_values]
        plt.plot(b_values, icb_plus, linewidth=4, color=color)
        plt.plot(b_values, icb_negative, linewidth=4, color=color)
plt.grid()
plt.xlabel(r"Magnetic Field $(b)$", fontsize=15)
plt.ylabel(r"Normalized Supercurrent $(I_s)$", fontsize=15)
plt.savefig(f'imgs\\icb_m{m}_n{n}_a{a}_phic{np.round(phic_values[0],2)}.png')
plt.show()
plt.close()
