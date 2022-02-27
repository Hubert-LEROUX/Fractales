
from PIL import Image, ImageDraw, ImageFont
import numpy as np 
import random
import tools
import cmath
import sys
import os

def fractale_f(f, **kwargs):
    """
    Procédure traçant une fractale à l'aide de la fonction f (de signature (complex, complex) -> complex)
    On pose pour chaque pixel la suite:
    u_0 = coordonnées complexe du pixel
    u_{n+1} = f(u_n,u_0)
    Dès que la suite "converge suffisamment" ou qu'on a dépassé le nombre maximum d'itérations, on s'arrête, le rang du dernier terme fixe la couleur.
    "Converger suffisamment" peut signifier:
        1. Dépasser un certain module (on considère que le module des termes de la suite tend vers l'infini) N.B. Du coup la suite diverge grossièrement
        2. Converger vers un complexe fini

        Arguments:
    @param DX (tuple) = intervalle de l'axe des réelles
    @param DY (tuple) = intervalle de l'axe des imaginaires purs
    @param resolution (tuple) = nombre de pixels longueur/hauteur
        Par défaut (512,512)
    @param output_file (string) = nom_du_fichier_de_sortie
    @param cmap_file (string) = nom du fichier pour la palette de couleur
    @param maxIt = nombre maximum d'itérations 
        Par défaut la valeur est 30. Attention il doit y avoir plus de valeurs dans cmap que maxIt
    @param epsilon
        Par défaut la valeur est 1e-4
    @param limit_modulus
        Par défaut la valeur est 50
    @param show (bool): Vrai par défaut
    @param label (str) : label en bas à droite
    @param condition_arret (lambda (complex, complex) -> bool): prend en paramètres le dernier et l'avant dernier terme de la suite
    """
    # f"mandelbrot_images/m_{random.randint(100,1_000)}.png", cmap_file="dawn", maxIt = 256,

    #* On récupère les paramètres
    DX = kwargs.get("DX", (-1,1))
    DY = kwargs.get("DY", (-1,1))
    resolution = kwargs.get("resolution", (512,512))
    output_file = kwargs.get("output_file", None)
    cmap_file = kwargs.get("cmap_file", "fires")
    maxIt = kwargs.get("maxIt", 30)
    epsilon = kwargs.get("epsilon", 1e-4)
    limit_modulus = kwargs.get("limit_modulus", 50)
    show = kwargs.get("show", True)
    label = kwargs.get("label", None)
    condition_arret = kwargs.get("condition_arret", lambda z,last: abs(z) > limit_modulus or abs(z-last)<=epsilon)

    # print(condition_arret(0.5, 0.5))

    cmap = tools.load_cmap(cmap_file, maxIt+1)
    (longueur, hauteur) = resolution
    fontsize = 20
    font = ImageFont.truetype("arial.ttf", fontsize)

    X = np.linspace(DX[0], DX[1], longueur)
    Y = np.linspace(DY[0], DY[1], hauteur)

    image = Image.new("RGB", (longueur, hauteur), "white")

    draw = ImageDraw.Draw(image)

    def get_rank_diverge(c):
        """
        u_0 = c
        u_{n+1} = f(u_n, u_0)
        """
        z = c
        last = float("+inf")
        i = 0
        while not condition_arret(z, last) and i < maxIt:
            try:
                last, z = z, f(z, c)
            except ZeroDivisionError:
                return i
            i+=1
        return i

    for x, a in enumerate(X):
        for y, b in enumerate(Y):
            i = get_rank_diverge(complex(a, b))

            try:
                image.putpixel((x, y), cmap[i]) # On place le pixer avec la couleur correspondante
            except:
                print(i)
                sys.exit()

    if label:
        off_size_x = 300
        off_size_y = 20
        draw.text((longueur-off_size_x, hauteur-off_size_y), text=label, fill=(255,255,255), font=font)

    if show:
        image.show()
    if output_file:
        image.save(output_file, "PNG")

def zoom_fractal_f(f, hauteur=512, longeur=512):
    xMin, xMax, yMin, yMax = -2.0,1.0,-3/2,3/2
    while True:
        mandelbrot(f, (xMin, xMax), (yMin, yMax))
        NB_DIVISIONS = 3
        print(f"xMin:\t{xMin:5f}\txMax:\t{xMax:5f}")
        print(f"yMin:\t{yMin:5f}\tyMax:\t{yMax:5f}")
        print("Sur quelle partie zoomer ?")
        print("""
            | 0 | 1 | 2 |
            | 3 | 4 | 5 |
            | 6 | 7 | 8 |
            Entrer -1 pour sortir
        """)
        subdivision = int(input())

        deltaX = (xMax-xMin)
        deltaY = (yMax-yMin )

        iCol = subdivision % NB_DIVISIONS
        iLigne = subdivision // NB_DIVISIONS

        print(f"Ligne: {iLigne}")
        print(f"Colonne: {iCol}")
        print(f"deltaX:{deltaX}\tdeltaY:{deltaY}")

        if not 0 <= subdivision <= NB_DIVISIONS**2:
            break 

        taille_sub_division_x = deltaX / NB_DIVISIONS
        taille_sub_division_y = deltaY / NB_DIVISIONS

        print(f"TailleX={taille_sub_division_x}")
        print(f"TailleY={taille_sub_division_y}")

        # On recalcule xMin et xMax
        xMax = xMin + (iCol+1) * taille_sub_division_x # Attention à placer cette ligne en premier !
        xMin = xMin + iCol * taille_sub_division_x 

        # On recalcule yMin et yMax
        yMax = yMin + (iLigne+1)*taille_sub_division_y
        yMin = yMin + iLigne*taille_sub_division_y

def zoom_fractal_f_one_point(f, point, nb_images=20, folder="zoom_one_point", rapport = 1/2, prefix_label="Zoom", **kwargs):
    X, Y = point
    folder = os.path.join("zooms", folder)
    if not os.path.exists(folder):
        # print("Hello")
        os.makedirs(folder)

    delta = 2
    for k in range(nb_images):
        fractale_f(f, 
            DX=(X-delta, X+delta), 
            DY=(Y-delta, Y+delta), 
            label = prefix_label + str(k+1),
            output_file=f"{folder}/zoom_{k+1}.png", 
            **kwargs)
        print(f"Done with image #{k+1} - {(X-delta, X+delta)} - {(Y-delta, Y+delta)}")
        delta *= rapport


if __name__ == "__main__":
    # zoom_mandelbrot()
    # zoom_mandelbrot_one_point((0.38, 0.13))

   

    # size_x = size_y = 1024
    # for d in range(100):
    #     print(d)
    #     function_name = f"Racines z^{d}-1"
    #     f = lambda z,c: z - (z**d-1)/(d*(z**(d-1)))
    #     # scale_coef = 1
    #     cmap_name = "regular_cmap_2"
    #     # condition_arret = lambda z, previous: abs(z)>2 # Infinite
    #     condition_arret = lambda z, previous: abs(z-previous) <= 1e-4
    #     fractale_f(f, 
    #         DX = (-2, 2), 
    #         DY = (-2, 2),
    #         resolution = (size_x, size_y), 
    #         output_file = f"racines_unite/regular_cmap_2/Racines_{str(d).replace('.','_')}_{size_x}_{size_y}_{cmap_name}.png", 
    #         cmap_file = cmap_name, 
    #         maxIt = 37, 
    #         label = function_name,
    #         show = False,
    #         condition_arret=condition_arret
    #         )
    
    #*Zone zoom
    point = (-0.22817920780250860271229, 1.11515676722969926888287)
    size_x = size_y = 1024
    nb_images = 120
    rapport = 3/4
    prefix_label = f"Mandelbrot zoom {point[0]}+{point[1]} i"

    f = lambda z,c: z*z + c
    # scale_coef = 1
    cmap_name = "cmap_wiki"
    # condition_arret = lambda z, previous: abs(z)>2 # Infinite
    condition_arret = lambda z, previous: abs(z) > 10
    zoom_fractal_f_one_point(f, 
        point,
        nb_images,
        "zoom_mandelbrot_2",
        rapport = rapport,
        prefix_label=prefix_label,
        resolution = (size_x, size_y), 
        cmap_file = cmap_name, 
        maxIt = 70, 
        show = False,
        condition_arret=condition_arret)
