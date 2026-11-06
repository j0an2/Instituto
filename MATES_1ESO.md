# Animacions Manim · Matemàtiques 1r ESO

Animacions per a explicar els continguts de 1r d'ESO de la Comunitat Valenciana,
a partir de `1ESO/Matematicas/Matemáticas (1º-2º ESO).pdf` (currículum LOMCE, Decret 87/2015).

- **Llengua dels textos:** castellà (de moment; després es traduiran al valencià).
- **Estat:** ✅ fet · 🟡 en curs · ⬜ pendent

## Instal·lació (ja feta)

| Peça | Versió | Notes |
|---|---|---|
| Python | 3.13.8 | |
| Manim Community | 0.22.1 | `pip install manim` (porta ffmpeg integrat via PyAV) |
| MiKTeX | via winget | Necessari per a `MathTex`. Instal·lació automàtica de paquets activada |

Si una terminal no troba `latex`, cal obrir-ne una de nova (o afegir
`%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64` al PATH).

## Estructura

Organitzada igual que la web: **curs → assignatura → vídeos** (des del 06/11/2026).

```
Manim/
├── index.html                     ← la web (obrir amb doble clic)
├── MATES_1ESO.md                  ← aquest fitxer
└── 1ESO/
    └── Matematicas/
        ├── Matemáticas (1º-2º ESO).pdf   ← currículum
        ├── videos/                       ← VÍDEOS FINALS, una carpeta per tema
        │   ├── t01_divisibilidad/        (1.Divisores.mp4, 2.PrimosCompuestos.mp4...)
        │   ├── t02_factores_mcd_mcm/
        │   └── ...
        └── codigo/                       ← tot el que fa falta per a crear-los
            ├── estilo.py                 ← colors, fons i funcions comunes
            ├── t01_divisibilidad.py ...  ← un fitxer per tema (tNN_nom.py)
            ├── publicar.py               ← renderitza en 1080p, porta els vídeos a videos/ i actualitza la web
            ├── revisar.py                ← trau fotogrames d'un vídeo per a revisar-lo
            └── media/                    ← memòria cau de Manim (proves 480p, fitxers temporals)
```

Un curs o assignatura nova seguiria el mateix patró (`2ESO/Matematicas/...`, `1ESO/FisicaQuimica/...`).

## Flux de treball

Des de `1ESO/Matematicas/codigo`, amb el Python de l'entorn de Manim:

1. **Provar** una escena en qualitat baixa:
   ```powershell
   ~\venvs\manim\Scripts\python.exe -m manim -pql t01_divisibilidad.py Divisores
   ```
2. **Publicar** quan estiga bé (renderitza en 1080p, deixa els vídeos numerats a `videos/<tema>/` i actualitza la web):
   ```powershell
   ~\venvs\manim\Scripts\python.exe publicar.py t01_divisibilidad.py   # un tema
   ~\venvs\manim\Scripts\python.exe publicar.py --todos                # tots
   ~\venvs\manim\Scripts\python.exe publicar.py --solo-web             # només la llista de la web
   ```
3. Obrir `Manim/index.html` al navegador.

`publicar.py` posa MiKTeX al PATH ell sol, així que funciona des de qualsevol terminal.

## La web (`index.html`)

- Inici → curs (1r ESO ... 2n Batx.) → assignatura (Mates, FiQ, BiG) → reproductor amb llista per temes.
- En acabar un vídeo passa al següent automàticament. URL directa a un vídeo: `index.html#/1eso/mat/3`.
- **La llista de vídeos de 1r ESO Mates es genera sola** entre els marcadors `// <<AUTO` i `// AUTO>>`.
  No s'ha d'editar a mà: es torna a escriure cada vegada que s'executa `publicar.py`.
- Altres cursos/assignatures es poden afegir a mà a `VIDEOS`, fora dels marcadors.

### Requisits de cada fitxer de tema

Perquè `publicar.py` el trobe i el pose a la web, cada `tNN_*.py` ha de tindre:

```python
TEMA = "Tema 3 · Números enteros"
TITULOS = {
    "NombreEscena": "Título del vídeo",
    ...
}
```

- L'**ordre dels vídeos** és l'ordre de les classes `Scene` dins del fitxer.
- Una escena sense entrada a `TITULOS` apareix amb el nom de la classe.
- Si s'afegeix o es reordena una escena, `publicar.py` renumera i esborra les numeracions velles.

## Estil comú (`estilo.py`)

- Fons fosc `#1e1e2e`, text blanc, accent groc.
- Verd = correcte / primer · Roig = error · Blau = múltiple / compost.
- Colors fixos per primers: 2 blau, 3 verd, 5 taronja, 7 morat.
- Cada escena comença amb `titulo(...)`: títol gran al centre i després es queda xicotet a dalt a l'esquerra.

## Temes

### Bloc 2 · Nombres i àlgebra

| # | Tema | Fitxer | Escenes | Estat |
|---|---|---|---|---|
| 1 | Divisibilitat, primers i compostos | `t01_divisibilidad.py` | `Divisores`, `PrimosCompuestos`, `Criterios`, `CribaEratostenes` | 🟡 primera versió |
| 2–3 | Factors primers, comuns, MCD i mcm | `t02_factores_mcd_mcm.py` | `ArbolFactores`, `DivisionesSucesivas`, `ComunesRecta`, `McdMcmFactores`, `ProblemasMcdMcm`, `EjerciciosEjemplo`, `EjerciciosResueltos` | 🟡 primera versió |
| 4 | Nombres enters (tema 3) | `t03_enteros.py` | `NegativosVidaReal`, `RectaEnteros`, `OpuestoValorAbsoluto`, `OrdenarEnteros`, `EjerciciosEjemplo`, `EjerciciosResueltos` | 🟡 primera versió |
| 5 | Operacions amb enters (tema 4) | `t04_operaciones_enteros.py` | `SumaRecta`, `SumaFichas`, `Resta`, `SumasRestasCombinadas`, `Multiplicacion`, `Division`, `EjerciciosEjemplo`, `EjerciciosResueltos` | 🟡 primera versió |
| 6 | Fraccions equivalents, comparar i ordenar (tema 5) | `t05_fracciones.py` | `QueEsUnaFraccion`, `FraccionesEquivalentes`, `AmplificarSimplificar`, `CompararFracciones`, `OrdenarFracciones`, `EjerciciosEjemplo`, `EjerciciosResueltos` | 🟡 primera versió |
| 7 | Operacions amb fraccions | | Comú denominador visual | ⬜ |
| 8 | Nombres decimals (tema 6) | `t06_decimales.py` | `QueEsUnDecimal`, `ValorPosicional`, `DecimalesEnLaRecta`, `CompararDecimales`, `OrdenarDecimales`, `EjerciciosEjemplo`, `EjerciciosResueltos` | 🟡 primera versió |
| 9 | Potències i arrels quadrades | | Quadrats perfectes amb blocs | ⬜ |
| 10 | Jerarquia de les operacions | | Expressió resolta pas a pas | ⬜ |
| 11 | Llenguatge algebraic i equacions | | Balança | ⬜ |

### Bloc 3 · Geometria

| # | Tema | Escenes | Estat |
|---|---|---|---|
| 12 | Angles i relacions | Transportador, complementaris/suplementaris | ⬜ |
| 13 | Mediatriu i bisectriu | Construcció amb compàs | ⬜ |
| 14 | Triangles i quadrilàters | Classificació, suma d'angles = 180° | ⬜ |
| 15 | Àrees i perímetres | Paral·lelogram → rectangle, triangle = ½ rectangle | ⬜ |
| 16 | Circumferència i cercle | Desenrotllar π, cercle → "rectangle" | ⬜ |

### Bloc 4 · Funcions

| # | Tema | Escenes | Estat |
|---|---|---|---|
| 17 | Coordenades cartesianes | Punt que viatja a (x, y) | ⬜ |
| 18 | Concepte de funció | Màquina → taula → gràfica | ⬜ |

### Bloc 5 · Estadística i probabilitat

| # | Tema | Escenes | Estat |
|---|---|---|---|
| 19 | Freqüències i gràfics | Taula → barres → sectors | ⬜ |
| 20 | Probabilitat i Laplace | Simulació de daus | ⬜ |

## Tema 1 · Divisibilidad (detall)

| Escena | Què mostra | Durada aprox. |
|---|---|---|
| `Divisores` | 12 fitxes en rectangles 1×12, 2×6, 3×4 → divisors de 12; definició de divisor/múltiple | ~33 s |
| `PrimosCompuestos` | 7 fitxes: amb 2 i 3 files sobren buits → només 1×7; primer vs compost; l'1 no és cap | ~27 s |
| `Criterios` | Taula de criteris per 2, 3, 5, 10 i exemple 471 → 4+7+1 = 12 | ~21 s |
| `CribaEratostenes` | Graella 1–100, es ratllen múltiples de 2, 3, 5, 7 amb colors → 25 primers | ~34 s |

## Tema 2 · Factores primos, M.C.D. y m.c.m. (detall)

Fil conductor: la descomposició en factors primers és l'eina; MCD i mcm són dues lectures d'ella.
Les fitxes de colors dels primers (`pieza()` a `estilo.py`) es reutilitzen a totes les escenes.

| Escena | Què mostra | Durada aprox. |
|---|---|---|
| `ArbolFactores` | Primers = «ladrillos»; arbre de 60 per 6×10 i per 4×15 → mateix resultat 2²·3·5 | ~38 s |
| `DivisionesSucesivas` | Mètode de la columna amb 60 i 84, justificant cada pas amb els criteris | ~23 s |
| `ComunesRecta` | Granotes de 4 en 4 i de 6 en 6 → mcm(4,6) = 12; Venn de divisors → MCD(12,18) = 6 | ~40 s |
| `McdMcmFactores` | 12 i 18 amb fitxes: comunes al menor → 6; totes al major → 36; targetes resum | ~36 s |
| `ProblemasMcdMcm` | Cintes i rajoles (MCD), autobusos (mcm) i regla «¿repartir? / ¿coincidir?» | ~62 s |
| `EjerciciosEjemplo` | Enunciats a)–h) + «pausa el vídeo». Resol a) 60 y 90: el 60 per **dos camins** (començant per 2 i per 5) → mateixos factors; després 90, MCD = 30 i mcm = 180 | ~50 s |
| `EjerciciosResueltos` | Resol b)–h) d'una sola manera: columnes, factorització, MCD i mcm (h és de tres nombres) | ~1 min 50 s |

**Exercicis** (llista `PROBLEMAS` al fitxer; els resultats es calculen sols):

| | Nombres | Factoritzacions | MCD | mcm |
|---|---|---|---|---|
| a | 60 y 90 | 2²·3·5 · 2·3²·5 | 30 | 180 |
| b | 24 y 36 | 2³·3 · 2²·3² | 12 | 72 |
| c | 18 y 30 | 2·3² · 2·3·5 | 6 | 90 |
| d | 20 y 50 | 2²·5 · 2·5² | 10 | 100 |
| e | 28 y 42 | 2²·7 · 2·3·7 | 14 | 84 |
| f | 45 y 75 | 3²·5 · 3·5² | 15 | 225 |
| g | 16 y 40 | 2⁴ · 2³·5 | 8 | 80 |
| h | 12, 18 y 30 | 2²·3 · 2·3² · 2·3·5 | 6 | 180 |

Per a canviar els exercicis, n'hi ha prou amb editar `PROBLEMAS`: les columnes, les factoritzacions i els resultats
es generen automàticament (funcions `descomponer`, `mcd_mcm`, `columna`, `resolver_mcd_mcm`).

## Tema 3 · Números enteros (detall)

Colors fixos per als enters (a `estilo.py`): **positius taronja** `POSITIVO`, **negatius blau** `NEGATIVO`, 0 blanc.
Funcions comunes: `color_entero(n)`, `fmt_entero(n)` (amb el signe − tipogràfic per a `Text`).
Es reutilitzaran al tema 4 (operacions).

| Escena | Què mostra | Durada aprox. |
|---|---|---|
| `NegativosVidaReal` | Tres panells: termòmetre (escala −20…+30; +25 → 0 → −3 °C), ascensor (planta 3 → baixa → 2n soterrani) i diners (20 € − 30 € = −10 €) | ~34 s |
| `RectaEnteros` | El termòmetre es «tomba» i es fa recta; origen, positius/negatius, el 0 no és cap; salts fins a +4 i −3; ℤ = {…} | ~26 s |
| `OpuestoValorAbsoluto` | Oposat com a reflex en el 0 (+4 ↔ −4, +2 ↔ −2, mateixa distància); valor absolut com a distància: \|−5\| = 5, \|+3\| = 3, \|0\| = 0 | ~41 s |
| `OrdenarEnteros` | «Més a la dreta = major»; +2 > −5 i −1 > −4 (amb el termòmetre); ordenar 3, −2, 0, −5, 1, −1 posant-los a la recta | ~38 s |

| `EjerciciosEjemplo` | Enunciats (2 pàgines) + resol el 1r apartat de cada tipus: 1a, 2 (−4), 3 (−7), 4a, 5a | ~1 min 15 s |
| `EjerciciosResueltos` | La resta: 1 b–f, 2, 3, 4 b–e, 5b (de major a menor) i 6 (ciutats amb termòmetres) | ~1 min 45 s |

**Exercicis** (llistes `EXPRESA`, `REPRESENTA`, `OPUESTOS`, `COMPARA`, `ORDENA_MENOR`, `ORDENA_MAYOR`, `CIUDADES`
al fitxer; les solucions es calculen soles):

1. Expressa amb un enter: 5 graus sota zero, planta 4, deute de 20 €, bussejar a 10 m, guanyar 15 €, tercer soterrani
2. Representa: −4, +2, 0, −1, +5
3. Oposat i valor absolut: −7, +3, −12, 0, +9
4. < o >: −3 ? +1 · −6 ? −2 · 0 ? −5 · −10 ? −1 · +4 ? −8
5. Ordena: a) menor→major 4, −3, 0, −7, 2, −1 · b) major→menor −5, 6, −2, 1, −9, 3
6. Ciutats: Madrid 2, Moscou −15, València 12, Oslo −6, Terol −3 °C → més freda, més càlida, ordenar

## Tema 4 · Operaciones con números enteros (detall)

Reutilitza de `estilo.py`: `recta_enteros`, `tex_entero`, `expr_enteros` (expressions amb parèntesis i colors),
`salto` (salts a la recta amb rastre) i `ficha_entero` (fitxes + taronja / − blau).

| Escena | Què mostra | Durada aprox. |
|---|---|---|
| `SumaRecta` | Sumar positiu = dreta, negatiu = esquerra; 4 exemples (un per combinació de signes) + context de temperatura | ~50 s |
| `SumaFichas` | «Pareja cero» (+1)+(−1)=0; (+5)+(−3), (−4)+(−2), (−6)+(+2) amb fitxes; targetes de la regla | ~45 s |
| `Resta` | Restar = sumar l'oposat: (+3)−(+5), (−2)−(−6); de 12 °C a −3 °C → 15 graus; taula per a llevar parèntesis | ~60 s |
| `SumasRestasCombinadas` | −3+7−5+2−4 agrupant positius i negatius en caixes; 5−(−3)+(−8) llevant parèntesis → 0 | ~40 s |
| `Multiplicacion` | (+3)·(−2) com a suma repetida; multiplicar per (−1) = donar la volta (reflex en el 0, lliga amb el tema 3); (−3)·(−2) = oposat de [(+3)·(−2)] = oposat de (−6) = +6; taula de signes | ~60 s |
| `Division` | (−12):(+3) = ? → «¿qué número por (+3) da −12?»; 4 casos amb la comprovació; mateixa regla | ~35 s |

| `EjerciciosEjemplo` | Enunciats (2 pàgines) + 1a (recta), 2a (sumar l'oposat), 3a (parèntesis), 4a (caixes), 5a (taula de signes), 6a (termòmetre) | ~1 min 40 s |
| `EjerciciosResueltos` | La resta, amb pista de la regla al costat de cada resultat; 6b (barra del compte bancari) i 6c (recta del temps d'Arquimedes) | ~2 min 30 s |

**Exercicis** (llistes `SUMAS`, `RESTAS`, `PARENTESIS`, `COMBINADAS`, `MULDIV` al fitxer; resultats i pistes automàtics):

1. Sumes: (+4)+(−7), (−3)+(−5), (−8)+(+8), (+6)+(−2), (−9)+(+4), (−1)+(−6)
2. Restes: (+2)−(+7), (−4)−(−9), (+5)−(−3), (−6)−(+2), (−1)−(−1)
3. Parèntesis: 8−(+3)+(−6) · −5−(−2)+(+4) · 7+(−10)−(−1)
4. Combinades: −4+9−3−7+2 · 12−5−8+1 · −6−2+10−4
5. Mult./div.: (−6)·(+4), (−7)·(−3), (+5)·(−8), (−24):(−6), (+36):(−9), (−45):(+5)
6. Problemes: temperatura −4+11−9 = −2 °C · compte 50+3·(−20) = −10 € · Arquimedes −212−(−287) = 75 anys

**Ordre dels pròxims temes** (segons el currículum): fraccions equivalents i ordre → decimals →
operacions amb fraccions → operacions amb decimals → potències i arrels → jerarquia de les operacions.

## Tema 5 · Fracciones equivalentes, comparar y ordenar (detall)

Colors fixos (a `estilo.py`): **numerador verd** `NUMERADOR`, **denominador lila** `DENOMINADOR`,
part presa **groga**, resta gris `VACIO`. Funcions: `fraccion(n, d)`, `cadena(...)`, `barra(parts, preses)`, `pizza(parts, preses)`.

| Escena | Què mostra | Durada aprox. |
|---|---|---|
| `QueEsUnaFraccion` | Tableta tallada en 4 → 3/4 (numerador/denominador); pizza 5/8; contraexemple de parts desiguals; 3/4 a la recta | ~45 s |
| `FraccionesEquivalentes` | Barres 1/2 → 2/4 → 4/8 tallant per la meitat, mateixa part pintada; productes creuats (1/2 = 2/4 sí, 2/3 i 3/4 no) | ~45 s |
| `AmplificarSimplificar` | 2/3 → 4/6 → 8/12 (×2); 12/18 → 6/9 → 2/3 (:2, :3); d'una vegada amb el M.C.D.(12,18) = 6 → irreductible | ~45 s |
| `CompararFracciones` | Mateix denominador (3/7 < 5/7); per què cal el comú denominador; 2 exemples pas a pas (3/4 vs 5/6 i 2/3 vs 3/5): 1) mcm amb llistes de múltiples, 2) quant multiplica cada fracció (12 : 4 = 3...) i les barres es tornen a tallar, 3) comparar numeradors; resum dels 3 passos | 1 min 44 s |
| `OrdenarFracciones` | 1/2, 3/8, 3/4, 5/8 → passar a vuitens → col·locar a la recta → 3/8 < 1/2 < 5/8 < 3/4 | ~35 s |

| `EjerciciosEjemplo` | Enunciats (2 pàgines) + 1a, 2a, 2b, 3a, 4a, 4b (amb els 3 passos), 5a i 6a (pizzes) | 1 min 56 s |
| `EjerciciosResueltos` | La resta; als 4c i 4e la fracció que ja té el denominador comú es queda igual (×1); 6b amb barres i 6c amb barres per persona | 2 min 42 s |

**Exercicis** (llistes `DIBUJOS`, `EQUIVALENTES`, `COMPLETA`, `SIMPLIFICA`, `COMPARA`, `ORDENA`, `LECTORES` al fitxer;
mcm, MCD i resultats automàtics):

1. Escriu la fracció (dibuixos): 3/5, 5/8, 2/6 (= 1/3), 7/10
2. a) Equivalents? 2/3 i 8/12 (sí) · 3/5 i 6/9 (no) · 1/3 i 3/9 (sí) — b) Completa: 3/4 = ?/12 · 2/5 = 6/? · 10/15 = ?/3
3. Simplifica: 8/12, 15/25, 18/24, 20/30
4. Compara: 4/9 ? 7/9 · 2/3 ? 3/4 · 3/10 ? 2/5 · 5/6 ? 7/9 · 4/6 ? 2/3 (= , la trampa)
5. Ordena: a) menor→major 1/2, 2/3, 5/12, 3/4 · b) major→menor 3/5, 7/10, 1/2, 4/5
6. Problemes: pizzes Ana 3/8 vs Lluís 1/4 · bus 2/5 vs a peu 3/10 · llibre Marta 2/3, Pablo 5/6, Sara 3/4

La fracció d'una quantitat i la fracció com a divisió van al tema d'operacions.

## Tema 6 · Números decimales (detall)

Colors per posició (a `estilo.py`, `COLOR_POS`): unitats blanc, **dècimes blau**, **centèsimes verd**, **mil·lèsimes taronja**.
Funcions: `tex_decimal("34,072")` (una peça per xifra, amb coma), `tabla_posiciones([...])`, `dec_txt(x, n)`.

| Escena | Què mostra | Durada |
|---|---|---|
| `QueEsUnDecimal` | Quadrat unitat → 10 tires (0,1 i 0,3) → 100 quadradets (0,01 i 0,25); decimal = fracció /10, /100...; 2,45 € amb monedes | 40 s |
| `ValorPosicional` | Taula C D U , d c m amb 34,072; «34 unidades y 72 milésimas»; 34,072 ≠ 34,72 (el 0 importa); descomposició 30 + 4 + 0,07 + 0,002 | 35 s |
| `DecimalesEnLaRecta` | Zoom: 0 a 1 en dècimes (0,3) → 0,3 a 0,4 en centèsimes (0,37) → 0,37 a 0,38 en mil·lèsimes (0,375) | 26 s |
| `CompararDecimales` | Columna a columna a la taula (3,47 < 3,52); trampa 0,5 vs 0,45 amb zero de farciment i graelles; 0,5 = 0,50 = 0,500 amb barres | 41 s |
| `OrdenarDecimales` | 2,3; 2,03; 2,33; 2,13 → igualar amb zeros → recta → 2,03 < 2,13 < 2,3 < 2,33 | 24 s |

| `EjerciciosEjemplo` | Enunciats (2 pàgines) + primer apartat de cada exercici (1a, 1b, 2a, 2b, 3a, 4a, 5a, 6a, 7a) | 2 min 3 s |
| `EjerciciosResueltos` | La resta; comparacions a la taula de posicions amb zeros grisos; ordenar igualant zeros | 2 min 55 s |

**Exercicis** (sense operacions; llistes al fitxer, solucions automàtiques amb `Decimal`):

1. a) Fracció → decimal: 7/10, 35/100, 8/100, 125/1000 · b) Decimal → fracció: 0,9; 0,47; 0,06; 1,3
2. a) Valor del 5 en 5,2; 0,5; 3,05; 1,205 · b) Escriu: «4 u. y 8 décimas», «2 u. y 35 centésimas», «7 centésimas», «12 u. y 9 milésimas»
3. Recta: 0,2; 0,5; 0,9 (entre 0 i 1) · 2,4; 2,75 (entre 2 i 3)
4. Compara: 4,7 ? 4,2 · 0,8 ? 0,75 · 3,06 ? 3,6 · 1,5 ? 1,50 · 0,099 ? 0,1
5. Ordena: menor→major 0,7; 0,07; 0,77; 0,707 · major→menor 5,1; 5,01; 5,11; 5,101
6. Intercala: entre 0,3 i 0,4 · 1,25 i 1,26 · 2 i 2,1
7. Problemes: 100 m (guanya el temps MENOR) · alçades · preus de dos llibres

Fracció → decimal dividint i arrodoniment van al tema 7 (operacions amb decimals).

## Entorn de Python (des del 05/11/2026)

Manim s'executa des de l'entorn virtual **`~\venvs\manim`**, no des del Python global:

```powershell
~\venvs\manim\Scripts\python.exe -m manim -pql t05_fracciones.py QueEsUnaFraccion
~\venvs\manim\Scripts\python.exe publicar.py t05_fracciones.py
```

Motiu: el paquet `dsts_extractor` (instal·lat al Python global) exigeix `click==8.1.7`, i Manim necessita `click>=8.5`.
Amb l'entorn separat, cada eina té la seua versió i no es trepitgen.

## Idees pendents / millores

- Traduir els textos al valencià (es pot fer amb un diccionari de textos a `estilo.py`).
- Afegir veu en off o subtítols.
- Escena final del tema 1 amb exercicis ràpids ("¿Es 3 divisor de 51?").
