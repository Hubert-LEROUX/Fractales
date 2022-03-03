import os
from math import ceil
from matplotlib import pyplot as plt
from scipy.interpolate import pchip_interpolate # https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.pchip_interpolate.html
import numpy as np


def filter_cmap(cmap, max_size):
    pas = (len(cmap)//max_size) if len(cmap) > max_size else 1
    return cmap[::pas]

def save_cmap(cmap, name):
    file = os.path.join("cmaps", name)
    with open(file, "w") as f:
        for c in cmap:
            f.write(f"{' '.join(map(str, list(c)))}\n")

def create_cmap_throught_interpolation(x_observed, RGBs_observed, name="cmap_from_interpolation"):
    """
    https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
    Written by Andrew
    @param x_observed (list): abscisses des points de l'interpolation
    @param RGBs_observed (list of tuple): couleurs correspondantes
    """
    #set up the control points for your gradient
    # yR_observed = [0, 0,32,237, 255, 0, 0, 32]
    # yG_observed = [2, 7, 107, 255, 170, 2, 7, 107]
    # yB_observed = [0, 100, 203, 255, 0, 0, 100, 203]

    yR_observed, yG_observed, yB_observed = map(list, zip(*RGBs_observed))   

    x_observed = [-.1425, 0, .16, .42, .6425, .8575, 1, 1.16]

    #Create the arrays with the interpolated values
    x = np.linspace(min(x_observed), max(x_observed), num=1000)
    yR = pchip_interpolate(x_observed, yR_observed, x)
    yG = pchip_interpolate(x_observed, yG_observed, x)
    yB = pchip_interpolate(x_observed, yB_observed, x)

    #Convert them back to python lists
    x = list(x)
    yR = list(yR)
    yG = list(yG)
    yB = list(yB)

    #Find the indexs where x crosses 0 and crosses 1 for slicing
    start = 0
    end = 0
    for i in x:
        if i > 0:
            start = x.index(i)
            break

    for i in x:
        if i > 1:
            end = x.index(i)
            break

    #Slice away the helper data in the begining and end leaving just 0 to 1
    x = x[start:end]
    yR = yR[start:end]
    yG = yG[start:end]
    yB = yB[start:end]

    #Plot the values if you want

    plt.plot(x, yR, color = "red")
    plt.plot(x, yG, color = "green")
    plt.plot(x, yB, color = "blue")
    plt.show()

    # On enregistre
    save_cmap([(yR[i], yG[i], yB[i]) for i in range(len(yR))], name)


def load_cmap(name, max_size=30):
    file = os.path.join("cmaps", name)
    cmap = []
    with open(file, "r") as cmap_file:
        numerise = lambda x : int(float(x))
        cmap=[tuple(map(numerise, line.strip().split(" "))) for line in cmap_file.readlines()]
    return filter_cmap(cmap, max_size) 

if __name__ == "__main__":
    # print(load_cmap("fire"))
    x_observed = [-.1425, 0, .16, .42, .6425, .8575, 1, 1.16]
    RGBs = [(0,2,0), (0,7,100),(32,107,203), (237,255,255),(255,140,0), (0,2,0),(0,7,100),(32,107,203)]
    create_cmap_throught_interpolation(x_observed, RGBs, "cmap_wiki")