
from PIL import Image, ImageDraw, ImageFont
import numpy as np 
import random
import tools
import cmath
import sys

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

    cmap = tools.load_cmap(cmap_file, maxIt+1)
    (longueur, hauteur) = resolution
    fontsize = 15
    font = ImageFont.truetype("arial.ttf", fontsize)

    X = np.linspace(DX[0], DX[1], longueur)
    Y = np.linspace(DY[0], DY[1], hauteur)

    image = Image.new("RGB", (longueur, hauteur), "white")

    draw = ImageDraw.Draw(image)

    def get_rank_diverge(c):
        z = c
        last = float("+inf")
        i = 0
        while abs(z) <= limit_modulus and abs(z-last)>epsilon and i <= maxIt:
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

def zoom_fractal_f_one_point(f, point, nb_images=20, folder="zoom_one_point", rapport = 1/2):
    X, Y = point
    for k in range(nb_images):
        mandelbrot(f, [X-rapport**k, X+rapport**k], [Y-rapport**k, Y+rapport**k], 512, 512, f"{folder}/Point_{str(X).replace('.', '-')}_{str(Y).replace('.','-')}_rapport_{str(rapport).replace('.', '-')}_zoom_{k+1}.png")
        print(f"Done with image #{k+1}")


if __name__ == "__main__":
    # zoom_mandelbrot()
    # zoom_mandelbrot_one_point((0.38, 0.13))

   

    size_x = size_y = 4096
    function_name = "f(z,c) = exp(z)+c"
    f = lambda z,c: cmath.exp(z) + c
    scale_coef = 1
    cmap_name = "reds"
    fractale_f(f, 
        DX = (-2*scale_coef,2*scale_coef), 
        DY = (-2 * scale_coef,2 * scale_coef),
        resolution = (size_x, size_y), 
        output_file = f"best_pictures/exponential_1_{size_x}_{size_y}_{cmap_name}.png", 
        cmap_file = cmap_name, 
        maxIt = 35, 
        label = function_name)


"""
Colormaps:
https://jdherman.github.io/colormap/
http://fractalforums.com/programming/newbie-how-to-map-colors-in-the-mandelbrot-set/
https://en.wikipedia.org/wiki/Monotone_cubic_interpolation
https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
https://colordesigner.io/gradient-generator
https://colorgradient.dev/

Fonctions:
    2. f = lambda z,c : (z**3 + c)/z
    3. f = lambda z,c : (z**3 + z**2 + c)/z
    4. f = lambda z,c : (z**3 + z**2 + c)/(z*z)
    5. f = lambda z,c : z - (z**4+3*z+1)/(5*z**2-6*z+1)
    6. f = lambda z,c: cmath.exp(z)+c
    7. Cos complexe https://fr.wikipedia.org/wiki/Cosinus
    8. Tan -> nul
    9. Sqrt -> Continu
    10. acos
    11. f = lambda z,c: cmath.sin(z**2+3*z)-cmath.sin(z)
    12. f = lambda z,c: z-(cmath.exp(z)-2)/(cmath.exp(z))
    13. f = lambda z,c: z-cmath.tan(z)
    14. f = lambda z,c: z-(cmath.exp(z)-2)/(cmath.exp(z))
    15. f = lambda z,c: (z-(cmath.tan(z)-2)/(1+cmath.tan(z)**2))
    16. f = lambda z,c: z- z * (cmath.log(z)+4)

        SUPER_MANDELBROT
    17. f = lambda z,c: z**5+c
    18. f = lambda z,c: z**5+z**4+z**3+c
    19. f = z+c
    20. f = zẑ+c
    20. f = zẑ
    22. f = z**2 - ()/()
    23. f = lambda z,c: z - (z**2+1)**2/(z**3+12)
    25. f = lambda z,c: z**2+1/(z**8) + c
    26. f = lambda z,c: (z+1)/(z**8) + c
    

    
  Système de couleur actuel...
# color = (i % 4 * 64, i % 8 * 32, i % 16 *16)
# tools.save_cmap([(i % 4 * 64, i % 8 * 32, i % 16 *16) for i in range(256)], "regular_mandelbrot")

"""