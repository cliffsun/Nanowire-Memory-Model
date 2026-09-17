import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.linalg import eigh
from scipy.integrate import quad
from scipy.optimize import root_scalar
from scipy.optimize import brentq

I_c = 1
phi_c = 10 * np.pi 
b=6.64
E_C = 1e-4
pi = np.pi
a=1

# b = phi_c/(np.sqrt(3 * np.pi**2))

def turning_points(E, V, phi):
    f = lambda x: E - V(x)
    roots = []
    for i in range(len(phi) - 1):
        if f(phi[i]) * f(phi[i+1]) < 0:
            roots.append(brentq(f, phi[i], phi[i+1]))
    if len(roots) < 2:
        raise ValueError("Not enough turning points")
    return roots[0], roots[-1]

def potential(phi):
    return phi**2/phi_c - a * ((phi - pi * b)**6 + (phi + pi * b)**6)/ (6 * phi_c**5) 

def WKB_action(E, V, phi):
    phi1, phi2 = turning_points(E, V, phi)
    integrand = lambda x: np.sqrt((E - V(x))/(4*E_C))
    return quad(integrand, phi1, phi2, limit=200)[0]

def WKB_quantization(E, n, V, phi):
    return WKB_action(E, V, phi) - (n + 0.5)*np.pi


def normalize_wavefunction(psi, x):
    dx = x[1] - x[0]
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx)
    return psi / norm

def expectation_value(operator, psi, x):
    dx = x[1] - x[0]
    return np.sum(np.conjugate(psi) * operator * psi) * dx

def zero_point_fluctuation_x(psi, x):
    psi = normalize_wavefunction(psi, x)
    
    x_operator = x
    x2_operator = x**2
    
    x_mean = expectation_value(x_operator, psi, x)
    x2_mean = expectation_value(x2_operator, psi, x)
    
    variance = x2_mean - x_mean**2
    return np.real(variance)

# gamma = -1/(2 * phi_c**3)
# beta =  (phi_c**2 - 3*np.pi**2*b**2)/phi_c**3

# print(r"E_C * gamma/beta = ", E_C * gamma/beta)

b_values = [b]

for b in b_values:
    temp = []
    temp1 = []
        # --- GRID ---
    phi_range = np.linspace(-100,100,100)
    phi_max = np.abs(phi_range[np.argmax(potential(phi_range))])
    # phi_max = 31.313131313131308
    print("phi_max", phi_max)
    phi_min = -phi_max
    # phi_max = 17.66
    # phi_min = -phi_max
    # phi_max = np.sqrt(((phi_c**4 - 5*a*(np.pi*b)**4)/phi_c**5)/ (2 * 5*a*(np.pi * b)**2/phi_c**5))
    # phi_min = -np.sqrt(((phi_c**4 - 5*a*(np.pi*b)**4)/phi_c**5)/ (2 * 5*a*(np.pi * b)**2/phi_c**5))
    # phi_min, phi_max = -np.sqrt((phi_c**2)/3 - np.pi**2*b**2),np.sqrt((phi_c**2)/3 - np.pi**2*b**2)


    # phi_min, phi_max = -700,700
    N = 5000
    phi = np.linspace(phi_min, phi_max, N)
    dphi = phi[1] - phi[0]
    U = phi**2/phi_c - a * ((phi - pi * b)**6 + (phi + pi * b)**6)/ (6 * phi_c**5) 
    # U = I_c * ( (phi**2 + (pi*b)**2)/phi_c
            # - (phi**4 + 6*phi**2*(pi*b)**2 + (pi*b)**4)/(2*phi_c**3) )

    kinetic = diags([np.full(N-1, 1.0), np.full(N, -2.0), np.full(N-1, 1.0)],
                    offsets=[-1,0,1]).toarray() * ( -4.0 * E_C / (dphi**2) )
    
    # U_total = U + soft_wall(phi, phi_min, phi_max)
    U_total = U

    print("Minimum", np.min(U))

    H = kinetic + np.diag(U_total)
    
    # H = kinetic + np.diag(U)
    num_eig = 3
    E, V = eigh(H, subset_by_index=(0, num_eig-1))

    E0, E1, E2 = E[0], E[1], E[2]

    # E0_WKB = root_scalar(
    #     WKB_quantization,
    #     args=(0, potential, phi),
    #     bracket=[min(potential(phi)) + 1e-3, max(potential(phi)) - 1e-3]
    # ).root
    # E1_WKB = root_scalar(
    #     WKB_quantization,
    #     args=(1, potential, phi),
    #     bracket=[min(potential(phi)) + 1e-3, max(potential(phi)) - 1e-3]
    # ).root
    # E2_WKB = root_scalar(
    #     WKB_quantization,
    #     args=(2, potential, phi),
    #     bracket=[min(potential(phi)) + 1e-3, max(potential(phi)) - 1e-3]
    # ).root

    print(E0 - np.min(U), E1- np.min(U), E2-np.min(U))
    # print(E0_WKB, E1_WKB, E2_WKB)

    # box_state = 1/(2*phi_max)**2

    # print(f"Comparison of ground state {E0} versus box state {box_state}")

    E10 = E1 - E0
    E21 = E2 - E1

    print("Energy transition 0 to 1", E10)
    print("Energy transition 1 to 2", E21)

    # E21_WKB = E2_WKB - E1_WKB
    # E10_WKB = E1_WKB - E0_WKB

    print("Absolute Anharmonicity:", E21 - E10)
    print("Relative Anharmonicity:", (E21-E10)/E10)

    # print("Semi-classical estimate Absolute Anharmonicity:", E21_WKB - E10_WKB)
    # print("Semi-classical estimate Relative Anharmonicity:", (E21_WKB - E10_WKB)/E10_WKB)


    psi0 = V[:,0]
    psi1 = V[:,1]
    psi2 = V[:,2]

    psi0 = normalize_wavefunction(psi=psi0, x=phi)
    psi1 = normalize_wavefunction(psi=psi1, x=phi)
    psi2 = normalize_wavefunction(psi=psi2, x=phi)


    phi6 = phi**6
    dE0 = -(1/(3*phi_c**5)) * np.sum(np.abs(psi0)**2 * phi6) * dphi
    dE1 = -(1/(3*phi_c**5)) * np.sum(np.abs(psi1)**2 * phi6) * dphi
    dE2 = -(1/(3*phi_c**5)) * np.sum(np.abs(psi2)**2 * phi6) * dphi
    alpha_pt = ((dE2 - dE1) - (dE1 - dE0))
    print("PT alpha (1st order) =", alpha_pt)

    edge_prob = (
        np.sum(np.abs(psi0[:10])**2) +
        np.sum(np.abs(psi0[-10:])**2)
    ) * dphi
    
    variance_x = zero_point_fluctuation_x(psi0, phi)
    print("Zero-point fluctuation =", variance_x)

    print("AB Calculation:", -180 * 1/(3 * phi_c**5) * variance_x**3 * 497e9/(E10 * 497e9))
    # print("AB Calculation:", -12 * (5 * pi**2 * b**2)/(phi_c**5) * variance_x**2 * 497e9/(E10 * 497e9))

    # print("Δx =", np.sqrt(variance_x))

    # phi_range = np.linspace(-np.sqrt(((phi_c**4 - 5*a*(np.pi*b)**4)/phi_c**5)/ (2 * 5*a*(np.pi * b)**2/phi_c**5)), np.sqrt(((phi_c**4 - 5*a*(np.pi*b)**4)/phi_c**5)/ (2 * 5*a*(np.pi * b)**2/phi_c**5)), 1000)

    phi_range = np.linspace(phi_min,phi_max,N)

    print("Edge probability:", edge_prob)
    c= 0.001
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dphi)
    psi1 = psi1 / np.sqrt(np.sum(np.abs(psi1)**2) * dphi)
    psi2 = psi2 / np.sqrt(np.sum(np.abs(psi2)**2) * dphi)
    print(np.max(U - np.min(U))) 
    plt.figure(figsize=(9,6))
    plt.plot(phi_range, U - np.min(U), linewidth=5)
    plt.plot(phi, c * psi0**2 + E0 - np.min(U), linewidth=3,color='blue')
    plt.plot(phi, c * psi1**2 + E1 - np.min(U), linewidth=3, color='red')
    plt.plot(phi, c * psi2**2 + E2 - np.min(U), linewidth=3, color='green')
    plt.tick_params(axis='both', labelsize=20)
    # plt.xticks(np.linspace(-1, 1, 5)) 
    # plt.yticks(np.linspace(0,0.03, 4))
    plt.axhline(E0- np.min(U), linestyle='--', linewidth=2, color='blue')
    plt.axhline(E1- np.min(U), linestyle='--', linewidth=2, color='red')
    plt.axhline(E2- np.min(U), linestyle='--', linewidth=2, color='green')

    # plt.axhline(E0_WKB, linestyle='-.', linewidth=2, color='blue')
    # plt.axhline(E1_WKB, linestyle='-.', linewidth=2, color='red')
    # plt.axhline(E2_WKB, linestyle='-.', linewidth=2, color='green')
    # plt.xlim(-1,1)
    # plt.ylim(0,0.03)
    plt.xlabel(r'Global Phase ($\phi$)', fontsize=20)
    plt.ylabel(r'$2eE/(\hbar I_0)$', fontsize=20)
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(f"imgs\\5_energies_b{np.round(b,2)}.png")
    plt.show()
    plt.close()