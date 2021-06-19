# PP_ImageJ

## Repositorio para el trabajo de prácticas profesionales Verano 2021.

[ImageJ](https://imagej.net/) es un software abierto para el procesamiento de imágenes.  

Paquete de python: https://anaconda.org/conda-forge/pyimagej , para instalar en anaconda se requiere usar el prompt con el comando:

```py
conda install -c conda-forge pyimagej
```

Para exportar el ambiente:
```py
conda env export > environment.yml
```

PyimageJ gestiona una version del software en python, de modo que de acuerdo a la configuración que le indiquemos podemos acceder a diferentes versiones
de ImageJ (1-2) o bien acceder al launcher y sus plugins a los cuales accedemos con [Fiji](https://imagej.net/software/fiji/downloads). En el [repositorio](https://github.com/imagej/pyimagej) de pyimagej podemos encontrar los metodos de inicialización antes mencionados.

En la pagina de [lenguajes compatibles](https://imagej.net/scripting/python) de ImageJ se menciona que el modulo de python tiene algunos errores con ImageJ1.x y es más estable con ImageJ2.

[Matlab](https://imagej.net/scripting/matlab) tambien es compatible de forma bidireccional y es compatible con ambas versiones.

Solicitud de acceso de Francisco

