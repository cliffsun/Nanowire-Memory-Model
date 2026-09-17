import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cpr(phi, b, phic1, phic2,n):
    Is1 = (phi - np.pi * (b-n))/phic1 - ((phi - np.pi * (b-n))/phic1)**5
    Is2 = (phi + np.pi * (b-n))/phic2 - ((phi + np.pi * (b-n))/phic2)**5
    return Is1 + Is2

b_values = [0, 0.2, 0.4, 0.6, 0.8, 1]

phic1 = 2*np.pi
phic2 = 2*np.pi
n_values = [0]

is_tot_n = []
temp = []
temp1=[]

norm_values = np.linspace(0,1,400)
is_tot_nan_n = []

phi_values = np.linspace(-phic1, phic1, 400)

for n in n_values:
    for b in b_values:
        Is_tot = [cpr(phi, b, phic1, phic2,n) if cpr(phi, b, phic1, phic2,n) * (phi) > 0 else np.nan for phi in phi_values]
        Is_tot_nan = [val for val in Is_tot if not np.isnan(val)]
        temp.append(Is_tot)
        temp1.append(Is_tot_nan)
    is_tot_n.append(temp)
    is_tot_nan_n.append(temp1)
    temp=[]
    temp1=[]

colors = ['blue', 'red', 'black', 'green', 'purple', 'brown']

linestyles=['-']



# Plot the normalized cpr

# for i in range(len(is_tot_nan_n)):
#     all_is_tot_nan = is_tot_nan_n[i]
#     linestyle=linestyles[i]
#     for k in range(len(all_is_tot_nan)):
#         arr = all_is_tot_nan[k]
#         arr = arr/max(arr)
#         plt.plot(arr)
# plt.grid()
# plt.xlabel(r'Global Phase ($\phi$)', fontsize=15)
# plt.ylabel(r"Normalized Supercurrent", fontsize=15)
# plt.savefig(f'imgs\\Is_v_phi_n{n_values[0]}.png')
# plt.show()
# plt.close()

# Plot the cpr regularly
for k in range(len(is_tot_n)):
    all_is_tot = is_tot_n[k]
    linestyle=linestyles[k]
    for i in range(len(all_is_tot)):
        print(len(all_is_tot))
        arr = all_is_tot[i]
        plt.plot(phi_values, arr, color=colors[i], linewidth=3,linestyle=linestyle)
plt.grid()
plt.xlabel(r'Global Phase ($\phi$)', fontsize=15)
plt.ylabel(r"Normalized Supercurrent ($I$)", fontsize=15)
plt.savefig(f'imgs\\Is_v_phi_n{n_values[0]}.png')
plt.show()
plt.close()
