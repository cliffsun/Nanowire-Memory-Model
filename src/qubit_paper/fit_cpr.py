import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

true = np.array(pd.read_csv("data\\siddiqi1.csv"))

t_x = [arr[0] for arr in true]
t_y = [arr[1] for arr in true]

def cpr(phi, b, phic1, phic2, a,n):
    Is1 = (phi - np.pi * b)/phic1 -a *((phi - np.pi * b)/phic1)**(2*n+1)
    Is2 = (phi + np.pi * b)/phic2 - a * ((phi + np.pi * b)/phic2)**(2*n+1)
    return Is1 + Is2

phic = 2*np.pi

a = 0.7

n=2

I_c = 44

phi = np.linspace(-phic,phic,10000)

phi_exp = np.linspace(0,2*np.pi,len(t_y))


b=0

I_1 = cpr(phi,b=b,phic1=phic, phic2=phic, a=a, n=n)

I_1 = np.array([I_1[i] if I_1[i] * phi[i] >= 0 else np.nan for i in range(len(I_1))])
# I_1 = [I_1[i] if I_1[i] * phi[i] > 0 else np.nan for i in range(len(I_1))]

I_1 = I_1[~np.isnan(I_1)]

I_1 = I_c*I_1

phi_norm = np.linspace(-phic/2,phic/2,len(I_1))
phi_norm1 = np.linspace(phic/2,phic/2 * 3,len(I_1))


plt.plot(phi_exp,t_y, linewidth=4, color='black')
plt.plot(phi_norm, I_1, linewidth=4, linestyle='--', color='red')
plt.plot(phi_norm1,I_1, linewidth=4, linestyle='--', color='red')
plt.grid()
plt.xlabel(r'Global Phase ($\phi$)', fontsize=16)
plt.ylabel(r'Supercurrent ($I_{s}$)', fontsize=16)
plt.savefig('imgs\\siddiqi_cpr_fit.png')
plt.show()
plt.close()