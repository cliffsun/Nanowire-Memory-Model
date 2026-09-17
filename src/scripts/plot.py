import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator
from scipy.stats import binned_statistic_2d
from matplotlib.colors import LogNorm

def list_to_python_syntax(lst):
    result = "[" + ", ".join(str(item) for item in lst) + "]"
    return result

def read_tuple(filename):
    data = []
    with open(filename) as f:
        for line in f:
            row = []
            for cell in line.strip().split(","):
                if "|" in cell:
                    a, b = map(float, cell.split("|"))
                    row.append((a, b))
                else:
                    row.append((float(cell), float('nan')))
            data.append(row)
    return np.array(data, dtype=object)

def plot_results(Ic_max, Ic_min, vorticity, MagField):

    colors = ['blue', 'red', 'black'] # Example Colors

    plt.figure(figsize=(10, 6))
    x_locator = MultipleLocator(1)  # X-axis ticks at integer multiples
    y_locator = MultipleLocator(1)  # Y-axis ticks at integer multiples
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_locator)
    ax.yaxis.set_major_locator(y_locator)
    for i in range(len(Ic_max)):
        plt.plot(MagField, Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)])
        plt.plot(MagField, Ic_min[i], color=colors[i % len(colors)])
    # plt.legend(loc="upper right") # If the legend gets too long, comment the above line out
    plt.xlim(-10,10)
    plt.ylim(-3,3)
    plt.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=20)  # For major ticks
    plt.tick_params(axis='both', which='minor', labelsize=12)
    plt.xlabel("b", fontsize=30)
    plt.ylabel("j", fontsize=30)
    plt.show()


def main():
    print("started plotting....")
    MagField = np.linspace(0, 10, 10000)
    ic_max_path = r"src\csv\Ic_max.csv"
    ic_min_path = r"src\csv\Ic_min.csv"
    vorticity_path = r"src\csv\vorticies.csv"
    KI_path = r"src\csv\KI_0.csv"
    KI_I_array = read_tuple(KI_path)

    KI_arr = np.array([[t[0] for t in row] for row in KI_I_array])
    I_arr = np.array([[t[1] for t in row] for row in KI_I_array])

    # KI_arr_clean = np.nan_to_num(KI_arr, nan=-10.0, posinf=0.0, neginf=0.0)
    # I_arr_clean = np.nan_to_num(I_arr, nan=-10.0, posinf=0.0, neginf=0.0)

    B_flat = np.array([MagField for i in range(10000)]).T    # repeats each B for all columns

    B_flat = B_flat.flatten()
    I_flat = I_arr.flatten()
    KI_flat = KI_arr.flatten()

    Ic_max = np.array(pd.read_csv(ic_max_path, header=None))
    Ic_min = np.array(pd.read_csv(ic_min_path, header=None))

    # Mask out NaNs
    mask = ~np.isnan(B_flat) & ~np.isnan(I_flat) & ~np.isnan(KI_flat)
    B_flat = B_flat[mask]
    I_flat = I_flat[mask]
    KI_flat = np.abs(KI_flat[mask])

    per_point = 2
    B_flat = B_flat[::per_point]
    I_flat = I_flat[::per_point]
    KI_flat = KI_flat[::per_point]

    print(KI_flat)

    threshold = np.percentile(KI_flat, 95)

    # Create masks for top 3% and the rest
    top_mask = KI_flat >= threshold
    rest_mask = ~top_mask

    # Create scatter plot
    plt.figure(figsize=(8,6))
    # sc = plt.scatter(B_flat[rest_mask], I_flat[rest_mask], c=KI_flat[rest_mask], cmap='RdBu', s=1, norm=LogNorm(np.min(KI_flat[rest_mask]), np.max(KI_flat[rest_mask])))
    sc = plt.scatter(B_flat, I_flat, c=KI_flat, cmap='RdBu', s=1, norm=LogNorm(np.min(KI_flat), np.max(KI_flat)))
    # plt.scatter(B_flat[top_mask], I_flat[top_mask], 
            # c='blue', s=0.1, label='Top 5% KI')
    # plt.plot(MagField, Ic_max[0], linewidth=1, linestyle='--', color='blue')
    # plt.plot(MagField, Ic_min[0], linewidth=1, linestyle='--', color='red')
    plt.colorbar(sc, label="Kinetic Inductance (KI)")
    plt.xlabel("B (Magnetic Field)")
    plt.ylabel("I (Current)")
    plt.title("KI Heat Map")
    plt.grid()
    plt.savefig('KI_map.png')
    plt.show()
  
if __name__ == "__main__":
    main()
