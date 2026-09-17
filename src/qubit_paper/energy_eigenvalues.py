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
E_C = 1/2.0     # effective mass for the phi coordinate (used implicitly below)
# We use units with hbar = 1 and kinetic prefactor = -1/(2 m_eff) d^2/dphi^2

# E_C_values = [0, 0.05, 0.1, 0.5, 1]

b_values = [4.75]

# b_values = np.linspace(0, phi_c/np.sqrt(3* np.pi**2), 100)

# b_values = [1.05]

e_0 = []
e_1 = []
e_2 = []

d10 = []
d21 = []

a=0.54

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
    # temp.append(E[1] - E[0])
    # temp1.append(E[2] - E[1])
    # e_0.append(E[0])
    # e_1.append(E[1])
    # e_2.append(E[2])


    # # --- RESULTS ---
    # print(f"Parameters: I_c={I_c}, phi_c={phi_c}, b={b}")
    # for i, val in enumerate(E[:6]):
    #     print(f"E[{i}] = {val:.8f}")

    # # ground and first excited
    E0, E1, E2 = E[0], E[1], E[2]
    psi0 = V[:,0]
    psi1 = V[:,1]
    psi2 = V[:,2]
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dphi)
    psi1 = psi1 / np.sqrt(np.sum(np.abs(psi1)**2) * dphi)
    psi2 = psi2 / np.sqrt(np.sum(np.abs(psi2)**2) * dphi)
    plt.figure(figsize=(9,6))
    plt.plot(phi, U, linewidth=3)
    plt.plot(phi, psi0**2)
    plt.plot(phi, psi1**2)
    plt.plot(phi, psi2**2)
    # plt.plot(phi, E0 + psi0 * 0.5/np.sqrt(dphi), label=f'ground (shifted) E0={E0:.6f}')
    # plt.plot(phi, E1 + psi1 * 0.5/np.sqrt(dphi), label=f'1st excited (shifted) E1={E1:.6f}')
    plt.axhline(E0, linestyle='--', linewidth=2, label=f"E={E0}")
    plt.axhline(E1, linestyle='--', linewidth=2,label=f"E={E1}")
    plt.axhline(E2, linestyle='--', linewidth=2, label=f"E={E2}")
    plt.xlabel(r'$\phi$', fontsize=15)
    plt.xlabel(r'Energy', fontsize=15)
    # plt.title('Potential')
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(f"energies_b{np.round(b,2)}.png")
    plt.show()

    print(np.abs(E[2] - E[1] - (E[1] - E[0]))/(E[1] - E[0]))
    # d10.append(temp)
    # d21.append(temp1)

# d21 = np.array(d21)
# d10 = np.array(d10)

# for i in range(len(d10)):
#     arr1 = np.array(d10[i])
#     arr2 = np.array(d21[i])
#     plt.plot(b_values, np.log10(np.abs(arr1 - arr2)/arr1), linewidth = 3, label=f"E_c = {E_C_values[i]}")
# plt.plot(b_values,e_0, label=r"$E_{0}$")
# plt.plot(b_values,e_1, label=r"$E_{1}$")
# plt.plot(b_values,e_2, label=r"$E_{2}$")
# plt.grid()
# plt.legend(loc="upper right")
# plt.xlabel("Magnetic Field (b)")
# plt.ylabel(r"Energies")
# plt.savefig("energies_ec.png")
# plt.show()
# plt.close()


# Normalize for plotting convenience (they should already be normalized)
# Plot potential and shifted eigenfunctions
# plt.figure(figsize=(9,6))
# plt.plot(phi, U, linewidth=3, label="Potential")
# # plt.plot(phi, E0 + psi0 * 0.5/np.sqrt(dphi), label=f'ground (shifted) E0={E0:.6f}')
# # plt.plot(phi, E1 + psi1 * 0.5/np.sqrt(dphi), label=f'1st excited (shifted) E1={E1:.6f}')
# plt.axhline(E0, linestyle='--', linewidth=2)
# plt.axhline(E1, linestyle='--', linewidth=2)
# plt.axhline(E2, linestyle='--', linewidth=2)
# plt.xlabel(r'$\phi$')
# plt.xlabel(r'Energy')
# plt.title('Potential')
# plt.legend()
# plt.grid(alpha=0.25)
# plt.tight_layout()
# plt.show()

# # Probability densities
# plt.figure(figsize=(9,4))
# plt.plot(phi, psi0**2, label='|psi0|^2')
# plt.plot(phi, psi1**2, label='|psi1|^2')
# plt.xlim(-4, 4)
# plt.xlabel('phi')
# plt.ylabel('Probability density')
# plt.title('Probability densities of ground and first excited state')
# plt.legend()
# plt.grid(alpha=0.25)
# plt.tight_layout()
# plt.show()
