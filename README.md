# Instituto · Vídeos de clase

Vídeos animados para explicar las Matemáticas de **1.º de ESO** (currículo de la Comunitat Valenciana),
hechos con [Manim](https://www.manim.community/). Explicaciones visuales, paso a paso, con ejercicios resueltos
al final de cada tema.

**▶ Ver los vídeos: <https://j0an2.github.io/Instituto/>**

## Temas de 1.º ESO · Matemáticas

| Tema | Vídeos |
|---|---|
| 1 · Divisibilidad | Múltiplos y divisores, primos y compuestos, criterios de divisibilidad, criba de Eratóstenes |
| 2 · Factores primos, M.C.D. y m.c.m. | Árbol de factores, divisiones sucesivas, múltiplos y divisores comunes, M.C.D. y m.c.m., problemas, ejercicios |
| 3 · Números enteros | Para qué sirven, la recta, opuesto y valor absoluto, comparar y ordenar, ejercicios |
| 4 · Operaciones con enteros | Sumar en la recta y con fichas, restar, sumas y restas combinadas, multiplicar (regla de los signos), dividir, ejercicios |
| 5 · Fracciones equivalentes | Qué es una fracción, equivalentes, amplificar y simplificar, comparar, ordenar, ejercicios |
| 6 · Números decimales | Décimas y centésimas, valor de cada cifra, decimales en la recta, comparar, ordenar, ejercicios |
| 7 · Operaciones con fracciones | Sumar y restar (mismo y distinto denominador), fracción de una cantidad, multiplicar, dividir, ejercicios |
| 8 · Operaciones con decimales | Sumar y restar, por 10, 100 y 1000, multiplicar, dividir, de fracción a decimal y redondeo, ejercicios |

Próximamente: potencias y raíces, jerarquía de las operaciones, álgebra, geometría, funciones y estadística.

## Cómo está organizado

La carpeta sigue la misma estructura que la web: **curso → asignatura → vídeos**.

```
index.html                    ← la web
assets/                       ← recursos de la web (mascotas, fórmulas del fondo)
1ESO/
├── mascota/                  ← Xola, la mascota del curso (imágenes finales + PROMPTS.txt)
└── Matematicas/
    ├── videos/<tema>/        ← vídeos finales (1080p)
    └── codigo/               ← escenas de Manim (un archivo por tema) y utilidades
```

## Generar los vídeos

Necesitas Python, `pip install manim` y una instalación de LaTeX (por ejemplo, MiKTeX). Desde `1ESO/Matematicas/codigo`:

```bash
python -m manim -pql t03_enteros.py RectaEnteros   # probar una escena en baja calidad
python publicar.py t03_enteros.py                  # renderizar en 1080p y actualizar la web
```

`publicar.py` deja los vídeos numerados en `videos/<tema>/` y reescribe la lista de vídeos de `index.html`.
