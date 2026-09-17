import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.sparse import diags
from scipy.linalg import eigh
from scipy.integrate import quad
from scipy.optimize import root_scalar
from scipy.optimize import brentq
import seaborn as sns

I_c = 1
phi_c = 10 * np.pi 
b=5.6
E_C = 1e-4
pi = np.pi

# b = phi_c/(np.sqrt(3 * np.pi**2))

def set_origin_style(
    font_size=20,
    axes_linewidth=2.2,
    tick_width=2.0,
    tick_length_major=8,
    tick_length_minor=4,
    ticks_direction="in",
    show_box=True,          # True = Origin-like box around plot
    use_minor_ticks=True,
    legend_frame=False
):
    mpl.rcParams.update({
        # Fonts
        "font.size": font_size,
        "axes.labelsize": font_size,
        "axes.titlesize": font_size,
        "legend.fontsize": font_size * 0.75,

        # Axes appearance
        "axes.linewidth": axes_linewidth,

        # Ticks
        "xtick.direction": ticks_direction,
        "ytick.direction": ticks_direction,
        "xtick.major.width": tick_width,
        "ytick.major.width": tick_width,
        "xtick.minor.width": tick_width * 0.9,
        "ytick.minor.width": tick_width * 0.9,
        "xtick.major.size": tick_length_major,
        "ytick.major.size": tick_length_major,
        "xtick.minor.size": tick_length_minor,
        "ytick.minor.size": tick_length_minor,

        # Figure export (Origin-like clean export)
        "savefig.dpi": 300,
        "figure.dpi": 120,
        "savefig.bbox": "tight",
    })

    # Apply to current axes when you call it
    ax = plt.gca()
    if use_minor_ticks:
        ax.minorticks_on()

    if show_box:
        # Origin often shows a full box around plot
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_linewidth(axes_linewidth)
    else:
        # “Scientific Matplotlib” style (no top/right)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    leg = ax.get_legend()
    if leg is not None:
        leg.set_frame_on(legend_frame)

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
    return I_c * ( (phi**2 + (pi*b)**2)/phi_c
            - (phi**4 + 6*phi**2*(pi*b)**2 + (pi*b)**4)/(2*phi_c**3) )

def WKB_action(E, V, phi):
    phi1, phi2 = turning_points(E, V, phi)
    integrand = lambda x: np.sqrt((E - V(x))/(4*E_C))
    return quad(integrand, phi1, phi2, limit=200)[0]

def WKB_quantization(E, n, V, phi):
    return WKB_action(E, V, phi) - (n + 0.5)*np.pi

gamma = -1/(2 * phi_c**3)
beta =  (phi_c**2 - 3*np.pi**2*b**2)/phi_c**3

def bracket_wkb_root(n, Vfun, phi, ngrid=2000, eps=1e-12):
    Vvals = Vfun(phi)
    Vmin, Vmax = np.min(Vvals), np.max(Vvals)

    # energies strictly inside (Vmin, Vmax) so turning points exist
    Es = Vmin + (Vmax - Vmin) * np.linspace(eps, 1 - eps, ngrid)

    fvals = []
    for E in Es:
        try:
            fvals.append(WKB_quantization(E, n, Vfun, phi))
        except ValueError:
            fvals.append(np.nan)

    fvals = np.array(fvals)

    # find first adjacent pair with opposite signs
    for i in range(len(Es) - 1):
        if np.isfinite(fvals[i]) and np.isfinite(fvals[i+1]):
            if fvals[i] * fvals[i+1] < 0:
                return Es[i], Es[i+1]

    raise RuntimeError(f"No sign change found for n={n}. Try increasing ngrid or check potential/turning points.")

# print(r"E_C * gamma/beta = ", E_C * gamma/beta)

b_values = [0,5.7]

for b in b_values:
    temp = []
    temp1 = []
        # --- GRID ---
    phi_min, phi_max = -np.sqrt((phi_c**2)/3 - np.pi**2*b**2),np.sqrt((phi_c**2)/3 - np.pi**2*b**2)


    # phi_min, phi_max = -700,700
    N = 2400
    phi = np.linspace(phi_min, phi_max, N)
    dphi = phi[1] - phi[0]
    U = I_c * ( (phi**2 + (pi*b)**2)/phi_c
            - (phi**4 + 6*phi**2*(pi*b)**2 + (pi*b)**4)/(2*phi_c**3) )

    kinetic = diags([np.full(N-1, 1.0), np.full(N, -2.0), np.full(N-1, 1.0)],
                    offsets=[-1,0,1]).toarray() * ( -4.0 * E_C / (dphi**2) )
    
    # U_total = U + soft_wall(phi, phi_min, phi_max)
    U_total = U

    # print("Maximum of potential:", np.max(U) - np.min(U))

    H = kinetic + np.diag(U_total)
    
    # H = kinetic + np.diag(U)
    num_eig = 3
    E, V = eigh(H, subset_by_index=(0, num_eig-1))

    E0, E1, E2 = E[0], E[1], E[2]

    # a0, b0 = bracket_wkb_root(0, potential, phi)
    # E0_WKB = brentq(lambda E: WKB_quantization(E, 0, potential, phi), a0, b0)

    # a1, b1 = bracket_wkb_root(1, potential, phi)
    # E1_WKB = brentq(lambda E: WKB_quantization(E, 1, potential, phi), a1, b1)

    # a2, b2 = bracket_wkb_root(2, potential, phi)
    # E2_WKB = brentq(lambda E: WKB_quantization(E, 2, potential, phi), a2, b2)

    digits = 5

    # print(f"{np.round(E0 - np.min(U),digits)} & {np.round(E1 - np.min(U),digits)} & {np.round(E2 - np.min(U),digits)}")
    # print(f"{np.round(E0_WKB - np.min(U),digits)} & {np.round(E1_WKB - np.min(U),digits)} & {np.round(E2_WKB - np.min(U),digits)}")

    box_state = 1/(2*phi_max)**2

    # print(f"Comparison of ground state {E0} versus box state {box_state}")

    E10 = E1 - E0
    E21 = E2 - E1

    # print("Energy transition 0 to 1", E10)
    # print("Energy transition 1 to 2", E21)

    # E21_WKB = E2_WKB - E1_WKB
    # E10_WKB = E1_WKB - E0_WKB

    # print("Absolute Anharmonicity:", E21 - E10)
    # print("Relative Anharmonicity:", (E21-E10)/E10)

    # print("Semi-classical estimate Absolute Anharmonicity:", E21_WKB - E10_WKB)
    # print("Semi-classical estimate Relative Anharmonicity:", (E21_WKB - E10_WKB)/E10_WKB)


    psi0 = V[:,0]
    psi1 = V[:,1]
    psi2 = V[:,2]

    edge_prob = (
        np.sum(np.abs(psi0[:10])**2) +
        np.sum(np.abs(psi0[-10:])**2)
    ) * dphi

    phi_range = np.linspace(-np.sqrt((phi_c**2) - 3*np.pi**2*b**2), np.sqrt((phi_c**2) - 3*np.pi**2*b**2), 1000)

    def U_function(phi):
        return  I_c * ( (phi**2 + (pi*b)**2)/phi_c
            - (phi**4 + 6*phi**2*(pi*b)**2 + (pi*b)**4)/(2*phi_c**3) )

    # print("Edge probability:", edge_prob)
    c= 0.001
    # colors = sns.color_palette("colorblind")
    psi0 = psi0 / np.sqrt(np.sum(np.abs(psi0)**2) * dphi)
    psi1 = psi1 / np.sqrt(np.sum(np.abs(psi1)**2) * dphi)
    psi2 = psi2 / np.sqrt(np.sum(np.abs(psi2)**2) * dphi)
    # print(np.max(U_function(phi_range) - np.min(U))) 
    
    sns.set_theme(
        style="ticks",
        context="paper",
        palette="colorblind",
        font_scale=1.8
    )

    colors = sns.color_palette("colorblind")

    fig, ax = plt.subplots(figsize=(9,6))

    # potential
    ax.plot(
        phi_range,
        U_function(phi_range) - np.min(U),
        linewidth=4
    )

    # wavefunctions
    ax.plot(
        phi,
        c * psi0**2 + E0 - np.min(U),
        linewidth=2.5,
        color=colors[0]
    )

    ax.plot(
        phi,
        c * psi1**2 + E1 - np.min(U),
        linewidth=2.5,
        color=colors[1]
    )

    ax.plot(
        phi,
        c * psi2**2 + E2 - np.min(U),
        linewidth=2.5,
        color=colors[2]
    )

    # energy levels
    ax.axhline(E0 - np.min(U), linestyle="--", linewidth=2, color=colors[0])
    ax.axhline(E1 - np.min(U), linestyle="--", linewidth=2, color=colors[1])
    ax.axhline(E2 - np.min(U), linestyle="--", linewidth=2, color=colors[2])

    # axis limits
    ax.set_xlim(-2,2)
    ax.set_ylim(0,0.06)

    # labels
    ax.set_xlabel(r"Global Phase ($\phi$)")
    ax.set_ylabel(r"$2eE/(\hbar I_0)$")

    # ticks
    ax.tick_params(axis="both", which="major", length=7, width=1.5)
    ax.tick_params(axis="both", which="minor", length=4, width=1)

    # grid
    ax.grid(alpha=0.25)

    # remove top/right spines (seaborn style)
    sns.despine(ax=ax)

    # legend
    ax.legend(frameon=False)

    fig.tight_layout()

    fig.savefig(
        f"imgs/energies_b{np.round(b,2)}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    # plt.close()