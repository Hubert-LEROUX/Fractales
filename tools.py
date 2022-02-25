import os
from math import ceil


def filter_cmap(cmap, max_size):
    pas = (len(cmap)//max_size) if len(cmap) > max_size else 1
    return cmap[::pas]

def save_cmap(cmap, name):
    file = os.path.join("cmaps", name)
    with open(file, "w") as f:
        for c in cmap:
            f.write(f"{' '.join(map(str, list(c)))}\n")

def load_cmap(name, max_size=30):
    file = os.path.join("cmaps", name)
    cmap = []
    with open(file, "r") as cmap_file:
        cmap=[tuple(map(int, line.strip().split(" "))) for line in cmap_file.readlines()]
    return filter_cmap(cmap, max_size) 

if __name__ == "__main__":
    print(load_cmap("fire"))