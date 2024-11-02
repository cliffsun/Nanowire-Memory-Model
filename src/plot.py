import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def list_to_python_syntax(lst):
    result = "[" + ", ".join(str(item) for item in lst) + "]"
    return result

def plot_results(Ic_max, Ic_min, vorticity, MagField):
    plt.figure(figsize=(10, 6))
    for i in range(len(Ic_max)):
        plot, = plt.plot(MagField, Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}")
        # plot, = plt.plot(MagField, Ic_max[i]) <--- If the legend gets too long, comment the above line out and uncomment this line
        plt.plot(MagField, Ic_min[i], color=plot.get_color())
    plt.title("Nanowire Critical Current Graph")
    plt.xlabel("Magnetic Field (B)")
    plt.ylabel("Critical Current (I_c)")
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

def main():
    MagField = np.linspace(-10, 10, 1000)
    ic_max_path = r"src\csv\Ic_max.csv"
    ic_min_path = r"src\csv\Ic_min.csv"
    vorticity_path = r"src\csv\vorticies.csv"
    Ic_max = np.array(pd.read_csv(ic_max_path, header=None))
    Ic_min = np.array(pd.read_csv(ic_min_path, header=None))
    vorticity = np.array(pd.read_csv(vorticity_path, header=None))
    plot_results(Ic_max, Ic_min, vorticity, MagField)

if __name__ == "__main__":
    main()
