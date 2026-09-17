import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator

def list_to_python_syntax(lst):
    result = "[" + ", ".join(str(item) for item in lst) + "]"
    return result

def plot_results(Ic_max, Ic_min, vorticity, MagField):

    colors = ['blue', 'red', 'black'] # Example Colors

    plt.figure(figsize=(10, 6))
    x_locator = MultipleLocator(1)  # X-axis ticks at integer multiples
    y_locator = MultipleLocator(1)  # Y-axis ticks at integer multiples
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_locator)
    ax.yaxis.set_major_locator(y_locator)
    for i in range(len(Ic_max)):
        if i == 1:
            print('her')
            plt.plot(MagField, Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)], linestyle="--")
            plt.plot(MagField, Ic_min[i], color=colors[i % len(colors)], linestyle="--")
            continue
        plt.plot(MagField, Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)])
        plt.plot(MagField, Ic_min[i], color=colors[i % len(colors)])
    # plt.legend(loc="upper right") # If the legend gets too long, comment the above line out
    plt.xlim(-4,4)
    plt.ylim(-8,8)
    plt.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=20)  # For major ticks
    plt.tick_params(axis='both', which='minor', labelsize=12)
    plt.xlabel("b", fontsize=30)
    plt.ylabel("j", fontsize=30)
    plt.show()
    
def plot_results_i(Ic_max, Ic_min, vorticity, MagField):

    colors = ['blue', 'red', 'black'] # Example Colors

    plt.figure(figsize=(10, 6))
    x_locator = MultipleLocator(1)  # X-axis ticks at integer multiples
    y_locator = MultipleLocator(1)  # Y-axis ticks at integer multiples
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_locator)
    ax.yaxis.set_major_locator(y_locator)
    for i in range(len(Ic_max)):
        if i == 1:
            print('her')
            plt.plot(MagField, Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)], linestyle="--")
            plt.plot(MagField, Ic_min[i], color=colors[i % len(colors)], linestyle="--")
            continue
        plt.plot(MagField, -1 * Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)])
        plt.plot(MagField, -1 * Ic_min[i], color=colors[i % len(colors)])
    # plt.legend(loc="upper right") # If the legend gets too long, comment the above line out
    plt.xlim(-4,4)
    plt.ylim(-8,8)
    plt.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=20)  # For major ticks
    plt.tick_params(axis='both', which='minor', labelsize=12)
    plt.xlabel("b", fontsize=30)
    plt.ylabel("j", fontsize=30)
    plt.show()
    
def plot_results_i_b(Ic_max, Ic_min, vorticity, MagField):

    colors = ['blue', 'red', 'black'] # Example Colors

    plt.figure(figsize=(10, 6))
    x_locator = MultipleLocator(1)  # X-axis ticks at integer multiples
    y_locator = MultipleLocator(1)  # Y-axis ticks at integer multiples
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_locator)
    ax.yaxis.set_major_locator(y_locator)
    for i in range(len(Ic_max)):
        if i == 1:
            print('her')
            plt.plot(-1 * MagField, -1 * Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)], linestyle="--", linewidth=3)
            plt.plot(-1 * MagField, -1 *Ic_min[i], color=colors[i % len(colors)], linestyle="--", linewidth=3)
            continue
        plt.plot(MagField, Ic_max[i], label=f"v_n = {list_to_python_syntax(vorticity[i])}", color=colors[i % len(colors)], linewidth=3)
        plt.plot(MagField, Ic_min[i], color=colors[i % len(colors)], linewidth=3)
    # plt.legend(loc="upper right") # If the legend gets too long, comment the above line out
    plt.xlim(-4,4)
    plt.ylim(-8,8)
    plt.grid(True)
    plt.tick_params(axis='both', which='major', labelsize=20)  # For major ticks
    plt.tick_params(axis='both', which='minor', labelsize=12)
    plt.xlabel("b", fontsize=30)
    plt.ylabel("j", fontsize=30)
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
    plot_results_i(Ic_max, Ic_min, vorticity, MagField)
    plot_results_i_b(Ic_max, Ic_min, vorticity, MagField)
    

if __name__ == "__main__":
    main()
