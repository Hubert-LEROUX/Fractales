
from PIL import Image, ImageDraw
import numpy as np 
import random
import tools
import cmath
import sys

def fractale_f(f, X, Y, hauteur=256, longueur = 256, output_file=f"mandelbrot_images/m_{random.randint(100,1_000)}.png", cmap_file="dawn", maxIt = 256):

    cmap = tools.load_cmap(cmap_file, maxIt+1)

    epsilon = 1e-6
    limit_modulus = 50

    X = np.linspace(X[0], X[1], longueur)
    Y = np.linspace(Y[0], Y[1], hauteur)

    image = Image.new("RGB", (longueur, hauteur), "white")
    # image.putpixel((500,200), black)

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

    image.show()
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

   

    size_x = size_y = 1024
    newton = lambda z,c : z-(z**5-1)/(5*z**4)
    f = lambda z,c: cmath.exp(z)
    scale_coef = 1
    cmap_name = "purples"
    fractale_f(f, [-2*scale_coef,2*scale_coef], [-2 * scale_coef,2 * scale_coef], size_x, size_y, f"images/exp_2_{scale_coef}_{size_x}_{size_y}_{cmap_name}.png", cmap_name, 30)


"""
Colormaps:
https://jdherman.github.io/colormap/
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