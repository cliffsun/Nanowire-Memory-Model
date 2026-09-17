import numpy as np
import matplotlib.pyplot as plt


e = 1.602176634e-19          # electron charge
hbar = 1.054571817e-34       # reduced Planck constant


def supercurrents(phi, b,m,nv,a,phi0):

    I_wire = (
        -a*(np.pi * b)**(2*m+1)
        /phi0**(2*m+1)
    )


    I_linear = np.pi * b/phi0

    return I_linear, I_wire


# -----------------------------
# Frequency
# -----------------------------
def omega(I0, b, Ec):
    term = phi0**(2*m) - a*(2*m+1)*(np.pi*(b-nv))**(2*m)

    # if term < 0:
    #     return None

    term = np.where(term < 0, np.nan, term)

    return np.sqrt(8 * 
        (Ec*I0/(e*hbar)) * term / phi0**(2*m+1)
    )


# -----------------------------
# Relative anharmonicity
# -----------------------------
def alpha_r(I0, b, Ec):

    numerator = (
        np.sqrt(2*e*Ec/(hbar*I0))
        *
        a*(2*m+1)
        *m*(2*m-1)
        *(np.pi*(b-nv))**(2*(m-1))
        *phi0**(m+0.5)
    )

    denominator = ( 
        2*
        (
            phi0**(2*m)
            -
            a*(2*m+1)*(np.pi*(b-nv))**(2*m)
        )**(1.5)
    )
    # if denominator < 0:
    #     return None
    denominator =  np.where(denominator < 0, np.nan, denominator)

    return np.abs(numerator/denominator)


I0_fixed = 1e-5       # A
Ec_fixed = 0.25e10 * hbar * 2*np.pi      # J
print(Ec_fixed/(hbar * 2*np.pi * 1e9))
nv = 0
m = 2       
a = 1.0
phi0 = 3*np.pi

# i0,i1 = supercurrents(phi=0, b=b_fixed, m=m,nv=nv,a=a,phi0=phi0)

# print("supercurrent in wire 1", (i0+i1))

# * (3 * np.sqrt(3)/2)
# print("supercurrent in wire 2:", (i0+i2) * (3 * np.sqrt(3)/2))

b_vals = np.linspace(0,10,1000)

plt.figure(figsize=(7,5))

plt.plot(
    b_vals,
    omega(I0_fixed,b_vals,Ec_fixed)/(2*np.pi * 1e9), # plotted in GHz,
    label="Plasma Frequency [GHz]"
)
plt.plot(
    b_vals,
    alpha_r(I0_fixed,b_vals,Ec_fixed) * 1e2, # percent, 
    label='Relative Anharmonicity [%]'
)
# plt.yscale('log')
plt.xlabel(r"$b$")
plt.ylabel(r"$\omega/2\pi$ (GHz)")
plt.title("Frequency vs Flux Bias")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# extract values
omega_vals = omega(I0_fixed, b_vals, Ec_fixed)/(2*np.pi*1e9)
alpha_vals = alpha_r(I0_fixed, b_vals, Ec_fixed)

# find first instance where |alpha_r| >= 1e-2
target = 1e-2

idx = np.where(np.abs(alpha_vals) >= target)[0][0]

print("First occurrence:")
print("b =", b_vals[idx])
i0,i1 = supercurrents(phi=0, b=b_vals[idx], m=m,nv=nv,a=a,phi0=phi0)

print("supercurrent in wire 1", (i0+i1))
print("omega/2pi =", omega_vals[idx], "GHz")
print("alpha_r =", alpha_vals[idx])


# # =====================================================
# # 4) alpha vs b
# # =====================================================

# plt.figure(figsize=(7,5))

# plt.plot(
#     b_vals,
#     alpha_r(I0_fixed,b_vals,Ec_fixed)
# )

# plt.xlabel(r"$b$")
# plt.ylabel(r"$\alpha_r$")
# plt.title("Relative Anharmonicity vs Flux Bias")
# plt.grid(True)
# plt.tight_layout()
# plt.show()



# # =====================================================
# # 5) 2D heatmap omega(I0,b)
# # =====================================================

# I_grid, b_grid = np.meshgrid(
#     np.linspace(0.1e-6,5e-6,150),
#     np.linspace(-0.5,0.5,150)
# )

# W = omega(I_grid,b_grid,Ec_fixed)/(2*np.pi*1e9)

# plt.figure(figsize=(7,5))

# plt.imshow(
#     W,
#     extent=[
#         0.1,5,
#         -0.5,0.5
#     ],
#     aspect='auto',
#     origin='lower'
# )

# plt.xlabel(r"$I_0$ ($\mu A$)")
# plt.ylabel(r"$b$")
# plt.title(r"$\omega/2\pi$ (GHz)")
# plt.colorbar(label="GHz")
# plt.tight_layout()
# plt.show()



# # =====================================================
# # 6) 2D heatmap alpha(I0,b)
# # =====================================================

# A = alpha_r(I_grid,b_grid,Ec_fixed)

# plt.figure(figsize=(7,5))

# plt.imshow(
#     A,
#     extent=[
#         0.1,5,
#         -0.5,0.5
#     ],
#     aspect='auto',
#     origin='lower'
# )

# plt.xlabel(r"$I_0$ ($\mu A$)")
# plt.ylabel(r"$b$")
# plt.title(r"Relative Anharmonicity $\alpha_r$")
# plt.colorbar()
# plt.tight_layout()
# plt.show()



# # =====================================================
# # 7) omega and alpha vs charging energy
# # =====================================================

# Ec_vals = np.logspace(-25,-22,300)

# plt.figure(figsize=(7,5))

# plt.plot(
#     Ec_vals/e,
#     omega(I0_fixed,b_fixed,Ec_vals)/(2*np.pi*1e9)
# )

# plt.xlabel(r"$E_C/e$ (V)")
# plt.ylabel(r"$\omega/2\pi$ (GHz)")
# plt.xscale("log")
# plt.grid(True)
# plt.title("Frequency vs Charging Energy")
# plt.tight_layout()
# plt.show()


# plt.figure(figsize=(7,5))

# plt.plot(
#     Ec_vals/e,
#     alpha_r(I0_fixed,b_fixed,Ec_vals)
# )

# plt.xlabel(r"$E_C/e$ (V)")
# plt.ylabel(r"$\alpha_r$")
# plt.xscale("log")
# plt.grid(True)
# plt.title("Anharmonicity vs Charging Energy")
# plt.tight_layout()
# plt.show()