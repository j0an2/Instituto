# Instituto · Vídeos de clase

Vídeos animados para explicar las Matemáticas de **1.º y 2.º de ESO** (currículo de la Comunitat Valenciana),
hechos con [Manim](https://www.manim.community/). Explicaciones visuales, paso a paso, con ejercicios resueltos
al final de cada tema.

**▶ Ver los vídeos: <https://j0an2.github.io/Instituto/>**

## Temas de 1.º ESO · Matemáticas

| Tema | Vídeos |
|---|---|
| 1 · Números naturales y potencias | Sistemas de numeración, el número natural, propiedades de las operaciones, potencias, cuadrados perfectos y raíz, redondear y estimar, ejercicios |
| 2 · Divisibilidad | Múltiplos y divisores, criterios de divisibilidad, primos y compuestos, criba de Eratóstenes, árbol de factores, divisiones sucesivas, múltiplos y divisores comunes, M.C.D. y m.c.m., problemas, ejercicios y una actividad interactiva para practicar con tus propios números |
| 3 · Números enteros | Para qué sirven, la recta, opuesto y valor absoluto, comparar y ordenar, sumar en la recta y con fichas, restar, sumas y restas combinadas, multiplicar (regla de los signos), dividir, ejercicios |
| 4 · Jerarquía de las operaciones | Por qué hace falta un orden, mismo nivel de izquierda a derecha, paréntesis y corchetes, resolver paso a paso, potencias de números negativos, errores típicos, ejercicios |
| 5 · Fracciones | Qué es una fracción, propias, impropias y números mixtos, equivalentes, amplificar y simplificar, comparar, ordenar, sumar y restar, fracción de una cantidad, multiplicar, dividir, operaciones combinadas, ejercicios |
| 6 · Números decimales | Décimas y centésimas, valor de cada cifra, decimales en la recta, comparar, ordenar, sumar y restar, por 10, 100 y 1000, multiplicar, dividir, de fracción a decimal y redondeo, decimales periódicos, ejercicios |
| 7 · Proporcionalidad | Razón, proporción, magnitudes directamente e inversamente proporcionales, regla de tres directa e inversa, porcentajes, aumentos y descuentos, ejercicios, extra (escalas) y una actividad interactiva (¿directa o inversa?) |
| 8 · Lenguaje algebraico | Expresiones algebraicas, monomios, polinomios, suma y resta de polinomios, qué es una ecuación, ecuaciones equivalentes con la balanza, ecuaciones de primer grado, ejercicios |
| 9 · Magnitudes y medida | Magnitudes, el Sistema Métrico Decimal (la escalera), longitud, masa y capacidad, superficie, volumen (¿dónde cabe 1 litro?), el tiempo (sistema sexagesimal), euros y céntimos, forma compleja e incompleja, operaciones, ejercicios |

Próximamente: geometría, perímetros y áreas, funciones y estadística.

## Temas de 2.º ESO · Matemáticas

| Tema | Vídeos |
|---|---|
| 1 · Números enteros | Naturales y divisibilidad (repaso), positivos y negativos, suma y resta, multiplicación y división, potencias y raíces cuadradas, operaciones con potencias, operaciones combinadas, ejercicios |
| 2 · Fracciones y números decimales | Fracciones (repaso), suma y resta, multiplicación y división, potencias, operaciones combinadas, fracciones y decimales, ¿por qué sale exacto o periódico? (extra), de decimal periódico a fracción, operaciones combinadas con decimales, raíces cuadradas con decimales, notación científica, ejercicios y una actividad interactiva (M.C.D. y m.c.m.) |
| 3 · Lenguaje algebraico | Expresiones algebraicas, monomios, polinomios, suma y resta, multiplicación, identidades notables con áreas, ejercicios y actividades interactivas (multiplicar polinomios, identidades notables) |
| 4 · Ecuaciones | Qué es una ecuación, ecuaciones equivalentes con la balanza, primer grado con paréntesis y con denominadores, segundo grado incompletas y la fórmula, problemas, ejercicios, extras (de dónde sale la fórmula, interpretación gráfica, suma y producto) y una actividad interactiva (resolver con la fórmula) |
| 5 · Sistemas de ecuaciones | Qué es un sistema, método gráfico, sustitución, reducción, igualación, tipos de sistemas, problemas, ejercicios, extras (los tres métodos, número de soluciones) y una actividad interactiva (dos rectas) |
| 6 · Proporcionalidad numérica | Razón y proporción, proporcionalidad directa e inversa, regla de tres, proporcionalidad compuesta, porcentajes, aumentos y disminuciones, ejercicios, extra (interés simple) y actividades interactivas (¿directa o inversa?, ofertas) |
| 7 · Funciones y gráficas | Coordenadas, concepto de función, gráficas, dominio y recorrido, continuidad y crecimiento, interpretar gráficas, ejercicios |

Próximamente: más temas de 2.º ESO.

## Cómo está organizado

La carpeta sigue la misma estructura que la web: **curso → asignatura → vídeos**.

```
index.html                    ← la web
assets/                       ← recursos de la web (fórmulas del fondo)
└── mascota/                  ← Xola, la mascota de 1.º: imágenes de la web, poses de los vídeos, asignaturas y PROMPTS.txt
1ESO/
└── Matematicas/
    ├── videos/<tema>/        ← vídeos finales (1080p)
    ├── interactivos/         ← actividades interactivas (HTML) que aparecen en la lista de vídeos
    └── codigo/               ← escenas de Manim (un archivo por tema) y utilidades; potencias_raices.py
                                no tiene tema propio: sus vídeos van dentro del tema 4
2ESO/
└── Matematicas/
    ├── videos/<tema>/        ← vídeos finales (1080p)
    └── codigo/               ← escenas de 2.º (reutilizan estilo.py y utilidades de 1.º)
```

## Generar los vídeos

Necesitas Python, `pip install manim` y una instalación de LaTeX (por ejemplo, MiKTeX). Desde `1ESO/Matematicas/codigo`:

```bash
python -m manim -pql t02_divisibilidad.py Divisores   # probar una escena en baja calidad
python publicar.py t02_divisibilidad.py                 # renderizar en 1080p y actualizar la web
```

`publicar.py` deja los vídeos numerados en `videos/<tema>/` y reescribe la lista de vídeos de `index.html`.
Para 2.º ESO se hace igual desde `2ESO/Matematicas/codigo` (su `publicar.py` llama al de 1.º).
