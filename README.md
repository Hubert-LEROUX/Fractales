# Fractales

[Alt text](https://raw.githubusercontent.com/Hubert-LEROUX/Fractales/master/best_pictures/exponential_1_4096_4096_reds.png "Fractal complex exponential")

## Colormaps

color = (i % 4 * 64, i % 8 * 32, i % 16 *16)
https://jdherman.github.io/colormap/    
http://fractalforums.com/programming/newbie-how-to-map-colors-in-the-mandelbrot-set/
https://en.wikipedia.org/wiki/Monotone_cubic_interpolation
https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
https://colordesigner.io/gradient-generator
https://colorgradient.dev/
https://stackoverflow.com/questions/369438/smooth-spectrum-for-mandelbrot-set-rendering


## Fonctions

    1. _
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


## For a C++ implementation
https://learncplusplus.org/tutorial-easily-learn-to-draw-mandelbrot-in-c-on-windows/
https://www.geeksforgeeks.org/mandlebrot-set-in-c-c-using-graphics/

## Create gif file
https://ostechnix.com/create-animated-gif-ubuntu-16-04/

## Interesting points mandelbrot set

For exploration
http://davidbau.com/mandelbrot/
https://mathr.co.uk/blog/2013-02-01_navigating_by_spokes_in_the_mandelbrot_set.html
 -0.22817920780250860271229 +
  1.11515676722969926888287 i

  -0.8005751794227
  +0.1707571631678 i

@ 3.32e-21
