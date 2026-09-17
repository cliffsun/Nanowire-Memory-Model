# nanowire_eigens.py
# Run with: python nanowire_eigens.py
# Requires: numpy, scipy, matplotlib, pandas (optional)
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.linalg import eigh

# --- PARAMETERS (edit these if you want different values) ---
I_c = 1.0       # critical current scale
phi_c = 10 * np.pi    # characteristic phase scale
b = 1.2        # bias parameter (phase offset)
E_C = 1e-3     # effective mass for the phi coordinate (used implicitly below)
# We use units with hbar = 1 and kinetic prefactor = -1/(2 m_eff) d^2/dphi^2

b_values = np.linspace(0, phi_c/np.sqrt(3* np.pi**2) - 1e-1, 50)

anharmon = []
rel_anharmon = []

a=1

for b in b_values:
    temp = []
    temp1 = []
        # --- GRID ---
    phi_min, phi_max = -50.0, 50.0
    N = 2400
    phi = np.linspace(phi_min, phi_max, N)
    dphi = phi[1] - phi[0]

    pi = np.pi
    U = I_c * ( (phi**2 + (pi*b)**2)/phi_c
            - a * (phi**4 + 6*phi**2*(pi*b)**2 + (pi*b)**4)/(2*phi_c**3) )

    kinetic = diags([np.full(N-1, 1.0), np.full(N, -2.0), np.full(N-1, 1.0)],
                    offsets=[-1,0,1]).toarray() * ( -4.0 * E_C / (dphi**2) )

    # --- HAMILTONIAN and DIAGONALIZATION ---
    H = kinetic + np.diag(U)
    num_eig = 3
    E, V = eigh(H, subset_by_index=(0, num_eig-1))

    # # ground and first excited
    E0, E1, E2 = E[0], E[1], E[2]

    print(E0)
    print(E1)
    print(E2)

    E10 = E1 - E0
    E21 = E2 - E1

    anharmon.append(E21 - E10)
    
    if np.abs(E10) == 0:
        rel_anharmon.append(np.nan)
        continue 
    rel_anharmon.append((E21-E10)/E10)

print(anharmon)
print(rel_anharmon) 

plt.plot(b_values, anharmon,linewidth=3, color='blue')
plt.plot(b_values, rel_anharmon,linewidth=3, color='red')
plt.xlabel("Magnetic Field (b)", fontsize=15)
plt.grid()
plt.savefig(r'imgs\anharmonicities.png')
plt.close()