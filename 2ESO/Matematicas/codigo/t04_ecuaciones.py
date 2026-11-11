"""Tema 4 · Ecuaciones (2º ESO)

Sigue el índice del libro: igualdades y ecuaciones · ecuaciones equivalentes · ecuaciones de primer grado
(con paréntesis y con denominadores) · ecuaciones de segundo grado (incompletas y fórmula) · problemas.

Escenas:
    QueEsEcuacion          – igualdad, identidad y ecuación; miembros, términos, incógnita, grado; solución
    EcuacionesEquivalentes – la balanza (quitar lo mismo de los dos lados, repartir) y la transposición
    PrimerGrado            – receta, con paréntesis, el menos delante del paréntesis, sin solución / infinitas
    ConDenominadores       – multiplicar todo por el m.c.m.; el menos delante de una fracción
    SegundoGradoIncompletas– a, b y c; x² = 25 (±5), sin solución, x² − 3x = 0 sacando factor común
    FormulaSegundoGrado    – la fórmula, dos ejemplos y el discriminante (2, 1 o 0 soluciones)
    DemostracionFormula    – (extra E1) completar el cuadrado: x² + 6x = 16 con áreas y la deducción general
    InterpretacionGrafica  – (extra E2) parábolas: cortes con y = 0 = soluciones; 2, 1 o 0 según Δ; c que sube
    Problemas              – pasos; números consecutivos, edades (tabla) y un rectángulo (2.º grado)
    EjerciciosEjemplo      – enunciados de los 10 ejercicios y el apartado a) de cada uno
    EjerciciosResueltos1/2 – el resto de apartados

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t04_ecuaciones.py EcuacionesEquivalentes
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t04_ecuaciones.py
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
COMUN = os.path.normpath(os.path.join(AQUI, "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from t09_potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t03_lenguaje_algebraico import X, cuenta, lista, pagina_enunciados, tarjeta, ROSA, LETRA  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 4 · Ecuaciones"
TITULOS = {
    "QueEsEcuacion": "¿Qué es una ecuación?",
    "EcuacionesEquivalentes": "Ecuaciones equivalentes: la balanza",
    "PrimerGrado": "Ecuaciones de primer grado con paréntesis",
    "ConDenominadores": "Ecuaciones con denominadores",
    "SegundoGradoIncompletas": "Ecuaciones de segundo grado incompletas",
    "FormulaSegundoGrado": "La fórmula de segundo grado",
    "DemostracionFormula": "¿De dónde sale la fórmula? Completar el cuadrado",
    "InterpretacionGrafica": "Las soluciones en un dibujo: la parábola",
    "Problemas": "Problemas con ecuaciones",
    "EjerciciosEjemplo": "Ejercicios: enunciados y un ejemplo de cada",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 a 4)",
    "EjerciciosResueltos2": "Ejercicios resueltos (5 a 10)",
}

EXTRAS = {"DemostracionFormula": "E1", "InterpretacionGrafica": "E2"}
INTERACTIVOS = [("E3", "Pruébalo tú: la fórmula paso a paso", "interactivos/formula_segundo_grado.html",
                 "InterpretacionGrafica")]

MIEMBRO_I, MIEMBRO_D = "#5DADE2", ROSA     # primer y segundo miembro
A_C, B_C, C_C = "#5DADE2", ROSA, "#7BD88F"  # a, b, c de segundo grado
MUEVE = ROSA                                # términos que cambian de miembro


def XC(s, size=48, col=None):
    """MathTex con la x amarilla y algunos trozos de otro color: col = {trozo: color}."""
    col = col or {}
    t = MathTex(s, font_size=size, substrings_to_isolate=list(col) + ["x"])
    t.set_color_by_tex("x", LETRA)
    for k, c in col.items():
        t.set_color_by_tex(k, c)
    return t


def comprobar(scene, filas, x, y, size=40, dy=0.7):
    """Comprobación: filas de tex; la última con ✓."""
    g = VGroup(texto("Comprobación:", 26, GREY_B).move_to([x, y, 0], aligned_edge=LEFT))
    scene.play(FadeIn(g[0]))
    for i, f in enumerate(filas):
        m = MathTex(f, font_size=size).move_to([x, y - 0.6 - i * dy, 0], aligned_edge=LEFT)
        scene.play(Write(m), run_time=0.8)
        g.add(m)
    ok = MathTex("\\checkmark", font_size=size + 8, color=OK).next_to(g[-1], RIGHT, buff=0.3)
    scene.play(FadeIn(ok, scale=1.5))
    g.add(ok)
    return g


# ---------------------------------------------------------------------------
# Balanza
def ficha_x():
    return VGroup(Square(0.55, color=LETRA, fill_color=LETRA, fill_opacity=0.3),
                  MathTex("x", font_size=34, color=LETRA))


def pesa():
    return VGroup(Circle(0.2, color=GREY_B, fill_color="#555566", fill_opacity=0.9), MathTex("1", font_size=24))


def menos1():
    """Ficha de −1 (rosa): con una pesa de +1 se anula."""
    return VGroup(Circle(0.2, color=ROSA, fill_color=ROSA, fill_opacity=0.55), MathTex("-1", font_size=20))


def pila(n):
    """n pesas en filas de 4, de abajo arriba."""
    filas = [VGroup(*[pesa() for _ in range(min(4, n - 4 * k))]).arrange(RIGHT, buff=0.06)
             for k in range((n + 3) // 4)]
    return VGroup(*filas).arrange(UP, buff=0.06, aligned_edge=LEFT)


def carga(nx, n1):
    g = VGroup()
    if nx:
        g.add(VGroup(*[ficha_x() for _ in range(nx)]).arrange(RIGHT, buff=0.08))
    if n1:
        g.add(pila(n1))
    return g.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)


def balanza(cx=0.0, y=-1.5, L=3.4, pw=1.4):
    piv = np.array([cx, y, 0])
    base = Polygon(piv, piv + [-0.6, -1.1, 0], piv + [0.6, -1.1, 0], color=GREY_B,
                   fill_color="#44475a", fill_opacity=1)
    brazo = Line(piv + [-L, 0, 0], piv + [L, 0, 0], stroke_width=8, color=GREY_B)
    platos = VGroup()
    for s in (-1, 1):
        poste = Line(piv + [s * L, 0, 0], piv + [s * L, 0.3, 0], stroke_width=5, color=GREY_B)
        plato = Line(piv + [s * L - pw, 0.3, 0], piv + [s * L + pw, 0.3, 0], stroke_width=8, color=GREY_B)
        platos.add(VGroup(poste, plato))
    return base, VGroup(brazo, platos), piv


def poner(c, mov, lado):
    c.next_to(mov[1][lado][1], UP, buff=0.04)
    return c


# ---------------------------------------------------------------------------
class QueEsEcuacion(Scene):
    def construct(self):
        cab = titulo(self, "¿Qué es una ecuación?")
        notas = Notas(self)

        # --- Igualdades
        subtitulo(self, cab, "Igualdades")
        g = VGroup(MathTex("3+5=8", font_size=60), MathTex("2+2=5", font_size=60)).arrange(RIGHT, buff=2.5)
        g.move_to([0, 1.4, 0])
        self.play(Write(g[0]))
        ok = MathTex("\\checkmark", color=OK, font_size=60).next_to(g[0], RIGHT, buff=0.3)
        self.play(Write(g[1]))
        no = MathTex("\\times", color=MAL, font_size=60).next_to(g[1], RIGHT, buff=0.3)
        notas("Una igualdad son dos expresiones unidas por el signo =. Puede ser cierta o falsa")
        self.play(FadeIn(ok), FadeIn(no))
        self.wait(2)
        idn = X("2(x+1)=2x+2", 60).move_to([0, -0.2, 0])
        self.play(Write(idn))
        notas("Con letras: esta es cierta para CUALQUIER valor de x. Se llama identidad")
        prue = VGroup(MathTex("x=1:\\ 4=4", font_size=42), MathTex("x=5:\\ 12=12", font_size=42)).arrange(RIGHT, buff=1.2)
        prue.next_to(idn, DOWN, buff=0.5)
        self.play(FadeIn(prue[0]))
        self.play(FadeIn(prue[1]))
        self.wait(2)
        ec = X("2x+3=11", 60).move_to([0, -2.2, 0])
        self.play(Write(ec))
        notas("Y esta solo es cierta para algunos valores de x: es una ECUACIÓN", color=ROSA)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Partes
        subtitulo(self, cab, "Partes de una ecuación")
        izq = X("2x+3", 80)
        igual = MathTex("=", font_size=80)
        der = MathTex("11", font_size=80)
        e = VGroup(izq, igual, der).arrange(RIGHT, buff=0.3).move_to([0, 0.8, 0])
        self.play(Write(e))
        bi = Brace(izq, DOWN, color=MIEMBRO_I)
        ti = texto("1.er miembro", 28, MIEMBRO_I).next_to(bi, DOWN, buff=0.1)
        bd = Brace(der, DOWN, color=MIEMBRO_D)
        td = texto("2.º miembro", 28, MIEMBRO_D).next_to(bd, DOWN, buff=0.1)
        notas("Lo que hay a cada lado del = son los miembros")
        self.play(GrowFromCenter(bi), FadeIn(ti), GrowFromCenter(bd), FadeIn(td))
        self.wait(1.5)
        notas("Cada sumando es un término: 2x, 3 y 11")
        for m in (izq[0][0:2], izq[0][2:], der):
            self.play(Indicate(m, scale_factor=1.25), run_time=0.7)
        flecha = Arrow(izq[0][1].get_top() + UP * 1.3 + LEFT * 0.6, izq[0][1].get_top() + UP * 0.1, color=LETRA)
        tinc = texto("incógnita", 28, LETRA).next_to(flecha.get_start(), UP, buff=0.1)
        notas("La letra es la incógnita: el número que no conocemos")
        self.play(GrowArrow(flecha), FadeIn(tinc))
        self.wait(1.5)
        notas("El grado es el mayor exponente de la x: aquí x = x¹, así que es de primer grado")
        self.wait(2.5)
        e2 = X("x^{2}-5x+6=0", 56).move_to([0, -2.3, 0])
        self.play(Write(e2))
        notas("Esta es de segundo grado, porque aparece x²")
        self.play(Indicate(e2[0][0:2], color=ROSA))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Solución
        subtitulo(self, cab, "La solución")
        e = X("2x+3=11", 64).move_to([0, 2.0, 0])
        self.play(Write(e))
        notas("La solución es el valor de x que hace cierta la igualdad. ¿Será x = 3?")
        p1 = MathTex("x=3:", "\\quad 2\\cdot 3+3=9", "\\neq 11", font_size=48).move_to([0, 0.6, 0])
        p1[2].set_color(MAL)
        self.play(Write(p1))
        self.wait(1.5)
        notas("No sale 11. Probamos con x = 4")
        p2 = MathTex("x=4:", "\\quad 2\\cdot 4+3=11", "\\ \\checkmark", font_size=48).move_to([0, -0.6, 0])
        p2[2].set_color(OK)
        self.play(Write(p2))
        notas("¡Sí! x = 4 es la solución. Sustituir así se llama comprobar")
        self.play(Circumscribe(p2, color=OK))
        self.wait(2)
        notas("Probar números a ciegas es lento. En los siguientes vídeos aprendemos a resolverlas")
        self.wait(3)
        notas.fin()


class EcuacionesEquivalentes(Scene):
    def construct(self):
        cab = titulo(self, "Ecuaciones equivalentes")
        notas = Notas(self)
        subtitulo(self, cab, "La balanza")
        base, mov, piv = balanza()
        ci = poner(carga(2, 3), mov, 0)
        cd = poner(carga(0, 11), mov, 1)
        e = X("2x+3=11", 64).move_to([0, 2.2, 0])
        self.play(Write(e))
        self.play(FadeIn(base), Create(mov))
        self.play(LaggedStart(FadeIn(ci, shift=DOWN * 0.3), FadeIn(cd, shift=DOWN * 0.3), lag_ratio=0.4))
        notas("Una ecuación es como una balanza en equilibrio: los dos lados pesan lo mismo")
        self.wait(2.5)

        # Desequilibrio
        notas("Si quitamos 3 solo de un lado...")
        tres = ci[1]
        self.play(tres.animate.shift(UP * 1.4 + LEFT * 0.4).set_opacity(0.25))
        resto = VGroup(mov, ci[0], cd)
        self.play(Rotate(resto, angle=-0.12, about_point=piv), run_time=1.2)
        notas("... ¡se desequilibra! Lo que hagamos, hay que hacerlo en los dos lados", color=MAL)
        self.wait(2)
        self.play(Rotate(resto, angle=0.12, about_point=piv), run_time=1.0)
        self.play(tres.animate.shift(DOWN * 1.4 + RIGHT * 0.4).set_opacity(1))

        # Quitar 3 de los dos lados
        notas("Quitamos 3 de los DOS lados")
        tres_d = cd[0][2]
        self.play(Indicate(tres, color=ROSA), Indicate(tres_d, color=ROSA))
        e1 = XC("2x+3-3=11-3", 64, {"-3": ROSA}).move_to(e)
        self.play(TransformMatchingShapes(e, e1))
        self.play(FadeOut(tres, shift=UP), FadeOut(tres_d, shift=UP))
        e2 = X("2x=8", 64).move_to(e1)
        self.play(TransformMatchingShapes(e1, e2))
        self.wait(1.5)

        # Repartir entre 2
        notas("Ahora dividimos los dos lados entre 2: nos quedamos con la mitad de cada uno")
        xs, filas = ci[0], cd[0][:2]
        mitad_i = SurroundingRectangle(xs[0], color=ACENTO, buff=0.06)
        mitad_d = SurroundingRectangle(filas[0], color=ACENTO, buff=0.06)
        self.play(Create(mitad_i), Create(mitad_d))
        self.wait(1)
        self.play(FadeOut(xs[1], shift=UP), FadeOut(filas[1], shift=UP), FadeOut(mitad_i), FadeOut(mitad_d))
        e3 = X("x=4", 72).move_to(e2)
        self.play(TransformMatchingShapes(e2, e3))
        self.play(Circumscribe(e3, color=ACENTO))
        notas("Una x pesa lo mismo que 4: la solución es x = 4")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Equivalentes
        subtitulo(self, cab, "Ecuaciones equivalentes")
        g = VGroup(X("2x+3=11", 56), X("2x=8", 56), X("x=4", 56)).arrange(DOWN, buff=0.6).move_to([-2.5, 0.4, 0])
        for m in g:
            self.play(Write(m), run_time=0.8)
        llave = Brace(g, RIGHT, color=ACENTO)
        t = texto("misma solución:\nson equivalentes", 30, ACENTO).next_to(llave, RIGHT, buff=0.3)
        self.play(GrowFromCenter(llave), FadeIn(t))
        notas("Sumar, restar, multiplicar o dividir los dos miembros por el mismo número (≠ 0) no cambia la solución")
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)

        # --- Transposición
        subtitulo(self, cab, "El atajo: transponer")
        notas("En la práctica no escribimos «− 3» en los dos lados: el término cambia de lado y de operación")
        a = XC("2x+3=11", 60, {"+3": MUEVE}).move_to([-5.6, 1.6, 0], aligned_edge=LEFT)
        self.play(Write(a))
        self.wait(1.5)
        b = XC("2x=11-3", 60, {"-3": MUEVE}).move_to([-5.6, 0.5, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(a, b), run_time=1.5)
        r1 = texto("Lo que SUMA pasa RESTANDO", 28, MUEVE).move_to([-0.4, b.get_center()[1], 0], aligned_edge=LEFT)
        self.play(FadeIn(r1))
        self.wait(1.5)
        c = X("2x=8", 60).move_to([-5.6, -0.6, 0], aligned_edge=LEFT)
        self.play(Write(c))
        d = XC("x=\\frac{8}{2}", 60, {"2": MUEVE}).move_to([-5.6, -1.9, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(c, d), run_time=1.5)
        r2 = texto("Lo que MULTIPLICA pasa DIVIDIENDO", 28, MUEVE).move_to([-0.4, d.get_center()[1], 0], aligned_edge=LEFT)
        self.play(FadeIn(r2))
        f = MathTex("=4", font_size=60).next_to(d, RIGHT, buff=0.2)
        self.play(Write(f))
        self.play(Circumscribe(VGroup(d, f), color=ACENTO))
        notas("Es lo mismo que hacíamos con la balanza, pero más rápido")
        self.wait(3)
        notas.fin()


class PrimerGrado(Scene):
    def construct(self):
        cab = titulo(self, "Ecuaciones de primer grado")
        notas = Notas(self)
        subtitulo(self, cab, "La receta")
        pasos = VGroup(*[texto(t, 30) for t in (
            "1. Quitar paréntesis",
            "2. Términos con x a un lado y números al otro (transponer)",
            "3. Reducir (juntar los términos semejantes)",
            "4. Despejar la x",
            "5. Comprobar la solución")]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        card = tarjeta(pasos).move_to([0, 0.2, 0])
        self.play(Create(card[0]))
        for p in pasos:
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(3)
        limpiar(self, cab)

        # --- Ejemplo 1
        subtitulo(self, cab, "Con paréntesis")
        pas = [
            (XC("3x-6+4=2x+5", 52), "1. Quitamos el paréntesis: 3 · x − 3 · 2"),
            (XC("3x-2x=5+6-4", 52, {"-2x": MUEVE, "+6": MUEVE, "-4": MUEVE}),
             "2. El 2x pasa restando; el −6 pasa sumando y el +4, restando"),
            (XC("x=7", 52), "3. Reducimos: 3x − 2x = x   y   5 + 6 − 4 = 7"),
        ]
        cuenta(self, "3(x-2)+4=2x+5", pas, -6.0, 1.6, notas, None, True, 52, dy=1.0)
        c = comprobar(self, ["3\\cdot(7-2)+4=19", "2\\cdot 7+5=19"], 1.8, 1.6)
        notas("Los dos miembros dan lo mismo: x = 7 es correcta", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- El mismo ejemplo con la balanza
        st = subtitulo(self, cab, "Con la balanza")
        e = X("3(x-2)+4=2x+5", 60).move_to([0, 2.3, 0])
        self.play(Write(e))
        notas("Primero quitamos el paréntesis y juntamos los números: −6 + 4 = −2")
        e1 = X("3x-2=2x+5", 60).move_to(e)
        self.play(TransformMatchingShapes(e, e1))
        self.wait(1)
        base, mov, piv = balanza(L=3.6, pw=1.75)
        xs_i = VGroup(*[ficha_x() for _ in range(3)]).arrange(RIGHT, buff=0.08)
        neg = VGroup(*[menos1() for _ in range(2)]).arrange(RIGHT, buff=0.06)
        ci = poner(VGroup(xs_i, neg).arrange(RIGHT, buff=0.3, aligned_edge=DOWN), mov, 0)
        xs_d = VGroup(*[ficha_x() for _ in range(2)]).arrange(RIGHT, buff=0.08)
        pd = pila(5)
        cd = poner(VGroup(xs_d, pd).arrange(RIGHT, buff=0.3, aligned_edge=DOWN), mov, 1)
        self.play(FadeIn(base), Create(mov))
        self.play(LaggedStart(FadeIn(ci, shift=DOWN * 0.3), FadeIn(cd, shift=DOWN * 0.3), lag_ratio=0.4))
        notas("Las fichas rosas valen −1. Una de −1 y una de +1 juntas valen 0: se anulan")
        self.wait(2.5)

        # Paso 1: añadir 2 a los dos lados
        notas("Para quitar el −2, AÑADIMOS 2 a los dos lados")
        nuevas_i = VGroup(*[pesa() for _ in range(2)]).arrange(RIGHT, buff=0.06).next_to(neg, UP, buff=0.9)
        pd7 = pila(7).move_to(pd, aligned_edge=DL)
        nuevas_d = VGroup(*[pesa() for _ in range(2)]).move_to(pd7[1][1]).shift(UP * 0.9)
        nuevas_d[1].move_to(pd7[1][2]).shift(UP * 0.9)
        self.play(FadeIn(nuevas_i, shift=DOWN * 0.3), FadeIn(nuevas_d, shift=DOWN * 0.3))
        e2 = XC("3x-2+2=2x+5+2", 60, {"+2": ROSA}).move_to(e1)
        self.play(TransformMatchingShapes(e1, e2))
        self.play(nuevas_i.animate.move_to(neg), nuevas_d[0].animate.move_to(pd7[1][1]),
                  nuevas_d[1].animate.move_to(pd7[1][2]))
        self.play(*[Flash(m, color=ACENTO, flash_radius=0.3) for m in neg])
        notas("A la izquierda, −2 + 2 = 0: desaparecen. A la derecha, 5 + 2 = 7")
        self.play(FadeOut(neg, scale=0.3), FadeOut(nuevas_i, scale=0.3))
        e3 = X("3x=2x+7", 60).move_to(e2)
        self.play(TransformMatchingShapes(e2, e3))
        self.wait(1.5)

        # Paso 2: quitar 2x de los dos lados
        notas("Ahora QUITAMOS 2x de los dos lados")
        self.play(Indicate(xs_i[1:], color=ROSA), Indicate(xs_d, color=ROSA))
        e4 = XC("3x-2x=2x+7-2x", 60, {"-2x": ROSA}).move_to(e3)
        self.play(TransformMatchingShapes(e3, e4))
        self.play(FadeOut(xs_i[1:], shift=UP), FadeOut(xs_d, shift=UP))
        e5 = X("x=7", 72).move_to(e4)
        self.play(TransformMatchingShapes(e4, e5))
        self.play(Circumscribe(e5, color=ACENTO))
        notas("Una x pesa lo mismo que 7: x = 7, igual que antes", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Ejemplo 2
        subtitulo(self, cab, "Cuidado con el menos")
        pas = [
            (XC("5-2x-2=x-6", 48), "El −2 multiplica a los DOS términos: −2 · x  y  −2 · (+1) = −2"),
            (XC("-2x-x=-6-5+2", 48, {"-x": MUEVE, "-5": MUEVE, "+2": MUEVE}),
             "La x pasa restando; el 5 y el −2 pasan con el signo cambiado"),
            (XC("-3x=-9", 48), "Reducimos"),
            (XC("x=\\frac{-9}{-3}", 48, {"-3": MUEVE}), "El −3 multiplica a la x: pasa dividiendo, ¡con su signo!"),
            (XC("x=3", 48), None),
        ]
        cuenta(self, "5-2(x+1)=x-6", pas, -6.0, 2.0, notas, None, True, 48, dy=0.85)
        comprobar(self, ["5-2\\cdot(3+1)=-3", "3-6=-3"], 1.8, 1.6)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Casos especiales
        subtitulo(self, cab, "Casos especiales")
        g1 = cuenta(self, "2x+1=2x+5", [("2x-2x=5-1", None), ("0x=4", None)], -6.0, 1.6, None, None, False, 48)
        t1 = texto("Ningún número por 0 da 4:\nSIN SOLUCIÓN", 28, MAL).next_to(g1, DOWN, buff=0.4).align_to(g1, LEFT)
        self.play(FadeIn(t1))
        notas("Si las x desaparecen y queda algo falso, la ecuación no tiene solución")
        self.wait(2)
        g2 = cuenta(self, "3(x+1)=3x+3", [("3x+3=3x+3", None), ("0x=0", None)], 1.0, 1.6, None, None, False, 48)
        t2 = texto("Cualquier número vale:\nINFINITAS SOLUCIONES", 28, OK).next_to(g2, DOWN, buff=0.4).align_to(g2, LEFT)
        self.play(FadeIn(t2))
        notas("Si queda algo siempre cierto, todas las x son solución: es una identidad")
        self.wait(3)
        notas.fin()


class ConDenominadores(Scene):
    def construct(self):
        cab = titulo(self, "Ecuaciones con denominadores")
        notas = Notas(self)
        subtitulo(self, cab, "Quitar denominadores")
        notas("Truco: multiplicamos TODOS los términos por el m.c.m. de los denominadores")
        pas = [
            (XC("6\\cdot\\frac{x}{2}+6\\cdot\\frac{x}{3}=6\\cdot 10", 50, {"6\\cdot": MUEVE}),
             "m.c.m.(2, 3) = 6: multiplicamos todo por 6"),
            (XC("3x+2x=60", 50), "6 : 2 = 3  y  6 : 3 = 2. ¡Ya no hay fracciones!"),
            (XC("5x=60", 50), None),
            (XC("x=12", 50), "El 5 pasa dividiendo: 60 : 5 = 12"),
        ]
        cuenta(self, "\\frac{x}{2}+\\frac{x}{3}=10", pas, -6.0, 1.7, notas, None, True, 50, dy=1.05)
        comprobar(self, ["\\frac{12}{2}+\\frac{12}{3}=6+4=10"], 1.5, 1.4)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        subtitulo(self, cab, "El menos delante de una fracción")
        pas = [
            (XC("3(x-1)-2(x+2)=12", 48), "m.c.m.(4, 6) = 12;  12 : 4 = 3  y  12 : 6 = 2. Los numeradores, entre paréntesis"),
            (XC("3x-3-2x-4=12", 48, {"-4": MUEVE}), "¡El menos afecta a todo el numerador!  −2 · (+2) = −4"),
            (XC("3x-2x=12+3+4", 48), "Transponemos"),
            (XC("x=19", 48), None),
        ]
        cuenta(self, "\\frac{x-1}{4}-\\frac{x+2}{6}=1", pas, -6.0, 1.6, notas, None, True, 46, dy=0.95)
        mal = VGroup(texto("Error típico:", 26, MAL), XC("-2x+4", 40)).arrange(RIGHT, buff=0.3)
        tach = Line(mal[1].get_left(), mal[1].get_right(), color=MAL, stroke_width=4)
        mal.add(tach).move_to([3.6, 0.6, 0])
        self.play(FadeIn(mal[:2]), Create(tach))
        notas("Si olvidas el paréntesis, solo cambias el signo del primer término", color=MAL)
        self.wait(2.5)
        comprobar(self, ["\\frac{18}{4}-\\frac{21}{6}=4{,}5-3{,}5=1"], 1.2, -0.6, size=38)
        self.wait(2.5)
        notas.fin()


class SegundoGradoIncompletas(Scene):
    def construct(self):
        cab = titulo(self, "Ecuaciones de segundo grado")
        notas = Notas(self)
        subtitulo(self, cab, "La forma general")
        f = MathTex("a", "x^{2}", "+", "b", "x", "+", "c", "=0", font_size=80).move_to([0, 1.6, 0])
        f[0].set_color(A_C)
        f[3].set_color(B_C)
        f[6].set_color(C_C)
        f[1].set_color(LETRA)
        f[4].set_color(LETRA)
        self.play(Write(f))
        notas("Todo en un miembro e igualado a 0. La a no puede ser 0 (si no, no habría x²)")
        self.wait(2)
        ejs = [("2x^{2}-3x+1=0", "a=2", "b=-3", "c=1"),
               ("x^{2}-9=0", "a=1", "b=0", "c=-9"),
               ("x^{2}+4x=0", "a=1", "b=4", "c=0")]
        filas = VGroup()
        for i, (e, a, b, c) in enumerate(ejs):
            fila = VGroup(X(e, 44), MathTex(a, font_size=40, color=A_C), MathTex(b, font_size=40, color=B_C),
                          MathTex(c, font_size=40, color=C_C))
            for m, x in zip(fila, (-3.6, 0.6, 2.4, 4.2)):
                m.move_to([x, 0.1 - i * 0.9, 0])
            fila[0].move_to([-3.6, 0.1 - i * 0.9, 0])
            self.play(Write(fila[0]))
            self.play(LaggedStart(*[FadeIn(m) for m in fila[1:]], lag_ratio=0.3))
            filas.add(fila)
        notas("Si b = 0 o c = 0, la ecuación es incompleta: hay trucos para hacerlo rápido", color=ROSA)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- b = 0
        subtitulo(self, cab, "Sin término en x (b = 0)")
        pas = [("x=\\pm\\sqrt{25}", "Buscamos un número que al cuadrado dé 25"),
               ("x=\\pm 5", None)]
        g = cuenta(self, "x^{2}=25", pas, -6.0, 1.6, notas, None, True, 56, dy=1.1)
        sq = Square(2.2, color=A_C, fill_color=A_C, fill_opacity=0.25).move_to([3.6, 0.6, 0])
        ta = MathTex("25", font_size=48).move_to(sq)
        lado = MathTex("5", font_size=40).next_to(sq, DOWN, buff=0.15)
        self.play(Create(sq), FadeIn(ta))
        self.play(FadeIn(lado))
        notas("Un cuadrado de área 25 tiene lado 5... pero también (−5)² = 25")
        dos = MathTex("5^{2}=25", "\\qquad", "(-5)^{2}=25", font_size=42).move_to([0, -1.9, 0])
        self.play(Write(dos))
        notas("Por eso hay DOS soluciones: x = 5 y x = −5. ¡No olvides el ±!", color=ROSA)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        pas = [("2x^{2}=18", "Primero dejamos la x² sola: el −18 pasa sumando..."),
               ("x^{2}=9", "... y el 2 pasa dividiendo"),
               ("x=\\pm 3", None)]
        cuenta(self, "2x^{2}-18=0", pas, -6.0, 1.7, notas, None, False, 50, dy=1.0)
        pas = [("x^{2}=-4", None)]
        g = cuenta(self, "x^{2}+4=0", pas, 1.2, 1.7, notas, None, False, 50, dy=1.0)
        t = texto("Ningún cuadrado es negativo:\nSIN SOLUCIÓN", 28, MAL).next_to(g, DOWN, buff=0.5).align_to(g, LEFT)
        self.play(FadeIn(t))
        notas("x² nunca es negativo: 2² = 4 y (−2)² = 4", color=MAL)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- c = 0
        subtitulo(self, cab, "Sin término independiente (c = 0)")
        e = X("x^{2}-3x=0", 60).move_to([-6.0, 1.7, 0], aligned_edge=LEFT)
        self.play(Write(e))
        notas("Sacamos factor común la x")
        e2 = XC("x\\cdot(x-3)=0", 60).move_to([-5.5, 0.6, 0], aligned_edge=LEFT)
        self.play(Write(e2))
        notas("Si un producto da 0, uno de los factores tiene que ser 0")
        r1 = X("x=0", 56).move_to([-5.0, -0.8, 0], aligned_edge=LEFT)
        r2 = X("x-3=0\\ \\Rightarrow\\ x=3", 56).move_to([-1.8, -0.8, 0], aligned_edge=LEFT)
        self.play(TransformFromCopy(e2[0][0], r1))
        self.play(Write(r2))
        self.play(Circumscribe(VGroup(r1, r2), color=ACENTO))
        self.wait(1.5)
        notas("Error típico: dividir entre x. Así se pierde la solución x = 0", color=MAL)
        mal = X("x^{2}=3x\\ \\Rightarrow\\ x=3", 44).move_to([0, -2.1, 0])
        cruz = Cross(mal, stroke_color=MAL, stroke_width=4)
        self.play(FadeIn(mal), Create(cruz))
        self.wait(3)
        notas.fin()


class FormulaSegundoGrado(Scene):
    def construct(self):
        cab = titulo(self, "La fórmula de segundo grado")
        notas = Notas(self)
        subtitulo(self, cab, "La fórmula")
        f = MathTex("x", "=", "\\frac{-", "b", "\\pm\\sqrt{", "b", "^{2}-4", "a", "c", "}}{2", "a", "}", font_size=84)
        for i, c in ((0, LETRA), (3, B_C), (5, B_C), (7, A_C), (8, C_C), (10, A_C)):
            f[i].set_color(c)
        card = tarjeta(f, buff=0.4).move_to([0, 0.5, 0])
        gen = MathTex("a", "x^{2}", "+", "b", "x", "+", "c", "=0", font_size=52).next_to(card, UP, buff=0.5)
        for i, c in ((0, A_C), (3, B_C), (6, C_C), (1, LETRA), (4, LETRA)):
            gen[i].set_color(c)
        self.play(Write(gen))
        self.play(Create(card[0]), Write(f), run_time=2)
        notas("Sirve para TODAS las ecuaciones de segundo grado. El ± da (normalmente) dos soluciones")
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)

        # --- Ejemplo 1
        subtitulo(self, cab, "Ejemplo")
        e = X("x^{2}-5x+6=0", 56).move_to([-6.0, 2.1, 0], aligned_edge=LEFT)
        self.play(Write(e))
        abc = VGroup(MathTex("a=1", font_size=42, color=A_C), MathTex("b=-5", font_size=42, color=B_C),
                     MathTex("c=6", font_size=42, color=C_C)).arrange(RIGHT, buff=0.6).next_to(e, RIGHT, buff=1.0)
        notas("Primero escribimos a, b y c (¡con su signo!)")
        self.play(LaggedStart(*[FadeIn(m) for m in abc], lag_ratio=0.3))
        s1 = MathTex("x=\\frac{-(", "-5", ")\\pm\\sqrt{(", "-5", ")^{2}-4\\cdot", "1", "\\cdot", "6",
                     "}}{2\\cdot", "1", "}", font_size=50)
        for i, c in ((1, B_C), (3, B_C), (5, A_C), (7, C_C), (9, A_C)):
            s1[i].set_color(c)
        s1[0][0].set_color(LETRA)
        s1.move_to([-5.5, 0.8, 0], aligned_edge=LEFT)
        notas("Sustituimos en la fórmula")
        self.play(Write(s1), run_time=2)
        s2 = MathTex("=\\frac{5\\pm\\sqrt{25-24}}{2}=\\frac{5\\pm 1}{2}", font_size=50)
        s2.move_to([-5.0, -0.5, 0], aligned_edge=LEFT)
        notas("−(−5) = 5,  (−5)² = 25  y  4 · 1 · 6 = 24")
        self.play(Write(s2), run_time=1.5)
        self.wait(1)
        r1 = X("x_{1}=\\frac{5+1}{2}=3", 50).move_to([-4.6, -2.1, 0], aligned_edge=LEFT)
        r2 = X("x_{2}=\\frac{5-1}{2}=2", 50).move_to([1.2, -2.1, 0], aligned_edge=LEFT)
        notas("Una solución con el + y otra con el −")
        self.play(Write(r1))
        self.play(Write(r2))
        self.play(Circumscribe(VGroup(r1, r2), color=ACENTO))
        notas("Comprobamos x = 3:  9 − 15 + 6 = 0 ✓   y   x = 2:  4 − 10 + 6 = 0 ✓", color=OK)
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Ejemplo 2
        subtitulo(self, cab, "Otro ejemplo")
        pas = [("x=\\frac{-1\\pm\\sqrt{1^{2}-4\\cdot 2\\cdot(-3)}}{2\\cdot 2}", "a = 2,  b = 1,  c = −3"),
               ("x=\\frac{-1\\pm\\sqrt{25}}{4}=\\frac{-1\\pm 5}{4}", "1 + 24 = 25, y √25 = 5"),
               ("x_{1}=1,\\qquad x_{2}=\\frac{-6}{4}=-\\frac{3}{2}", "(−1 + 5) : 4 = 1   y   (−1 − 5) : 4 = −6/4")]
        cuenta(self, "2x^{2}+x-3=0", pas, -6.0, 2.0, notas, None, False, 46, dy=1.25)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Discriminante
        subtitulo(self, cab, "¿Cuántas soluciones?")
        d = MathTex("\\Delta", "=", "b^{2}-4ac", font_size=60).move_to([0, 2.0, 0])
        d[0].set_color(ACENTO)
        self.play(Write(d))
        notas("Lo de dentro de la raíz se llama discriminante (Δ) y decide cuántas soluciones hay")
        self.wait(1.5)
        filas = [("x^{2}-5x+6=0", "\\Delta=25-24=1>0", "2 soluciones", OK),
                 ("x^{2}-6x+9=0", "\\Delta=36-36=0", "1 solución (x = 3)", ACENTO),
                 ("x^{2}+2x+5=0", "\\Delta=4-20=-16<0", "sin solución", MAL)]
        for i, (e, dd, t, c) in enumerate(filas):
            y = 0.7 - i * 1.0
            m1 = X(e, 42).move_to([-4.2, y, 0])
            m2 = MathTex(dd, font_size=42).move_to([0.4, y, 0])
            m3 = texto(t, 28, c).move_to([4.6, y, 0])
            self.play(Write(m1))
            self.play(Write(m2))
            self.play(FadeIn(m3, shift=LEFT * 0.2))
            self.wait(0.8)
        notas("Si Δ < 0 tendríamos la raíz de un número negativo: no existe", color=MAL)
        self.wait(3.5)
        notas.fin()


class DemostracionFormula(Scene):
    def construct(self):
        cab = titulo(self, "¿De dónde sale la fórmula?", "Completar el cuadrado")
        notas = Notas(self)

        # --- 1. Con números: x² + 6x = 16
        st = subtitulo(self, cab, "Con números")
        XL, T = 2.6, 1.3                     # longitud dibujada de x y de 3
        O = np.array([-6.0, -1.8, 0])

        def caja(x0, y0, w, h, col, lab, op=0.45, size=40):
            r = Rectangle(width=w, height=h, color=WHITE, stroke_width=2, fill_color=col, fill_opacity=op)
            r.move_to(O + [x0 + w / 2, y0 + h / 2, 0])
            t = MathTex(lab, font_size=size).move_to(r)
            return VGroup(r, t)

        e0 = X("x^{2}+6x=16", 56).move_to([3.0, 2.2, 0])
        self.play(Write(e0))
        notas("Al-Juarismi (siglo IX) lo pensaba con áreas: x² es un cuadrado de lado x")
        cuad = caja(0, 0, XL, XL, A_C, "x^{2}", size=48)
        self.play(FadeIn(cuad))
        rect = caja(XL + 0.6, 0, 2 * T, XL, C_C, "6x")
        self.play(FadeIn(rect))
        notas("y 6x es un rectángulo de lados 6 y x")
        self.wait(1.5)
        notas("Lo partimos en dos tiras iguales de 3x...")
        t1 = caja(XL + 0.6, 0, T, XL, C_C, "3x")
        t2 = caja(XL + 0.6 + T, 0, T, XL, C_C, "3x")
        self.play(FadeOut(rect), FadeIn(t1), FadeIn(t2))
        self.play(t2.animate.shift(RIGHT * 0.3))
        self.wait(0.8)
        notas("... y ponemos una a la derecha del cuadrado y la otra encima")
        d1 = caja(XL, 0, T, XL, C_C, "3x")
        d2 = caja(0, XL, XL, T, C_C, "3x")
        self.play(Transform(t1, d1), run_time=1.2)
        self.play(Rotate(t2, PI / 2), run_time=0.8)
        self.play(Transform(t2, d2), run_time=1.2)
        self.wait(1)
        hueco = DashedVMobject(Square(T, color=ROSA)).move_to(O + [XL + T / 2, XL + T / 2, 0])
        self.play(Create(hueco))
        notas("¡Casi es un cuadrado! Le falta la esquina: un cuadradito de 3 × 3 = 9", color=ROSA)
        self.wait(2)
        esq = caja(XL, XL, T, T, ROSA, "9", op=0.6)
        self.play(FadeIn(esq, scale=1.3), FadeOut(hueco))
        notas("Si la añadimos a un lado, hay que añadirla también al otro")
        pasos = [(XC("x^{2}+6x+9=16+9", 52, {"+9": ROSA}), None),
                 (X("(x+3)^{2}=25", 52), "Ahora es un cuadrado de lado x + 3, y su área es 25"),
                 (X("x+3=5", 52), "Su lado mide 5..."),
                 (X("x=2", 52), "... así que x = 2")]
        b1 = Brace(VGroup(cuad, t1), DOWN, color=GREY_B)
        l1 = X("x+3", 40).next_to(b1, DOWN, buff=0.1)
        g = VGroup()
        prev = e0
        for i, (m, nota) in enumerate(pasos):
            if nota:
                notas(nota)
            m.next_to(prev, DOWN, buff=0.45).align_to(e0, LEFT).shift(RIGHT * 0.3 * (i > 0))
            self.play(Write(m))
            if i == 1:
                self.play(GrowFromCenter(b1), FadeIn(l1))
            self.wait(1)
            g.add(m)
            prev = m
        self.play(Circumscribe(g[-1], color=ACENTO))
        notas("(Con números también vale x + 3 = −5, o sea x = −8, pero un lado no puede ser negativo)", color=GREY_B)
        self.wait(3.5)
        notas.fin()
        limpiar(self, cab)

        # --- 2. En general
        st_g = subtitulo(self, cab, "En general")
        f0 = X("ax^{2}+bx+c=0", 50).move_to([2.6, 2.2, 0])
        self.play(Write(f0))
        notas("Dividimos entre a y pasamos el término independiente al otro lado")
        f = X("x^{2}+\\frac{b}{a}x=-\\frac{c}{a}", 50).move_to(f0)
        self.play(TransformMatchingShapes(f0, f))
        notas("A la izquierda: un cuadrado x² y un rectángulo (b/a) · x, como antes")
        cuad = caja(0, 0, XL, XL, A_C, "x^{2}", size=48)
        d1 = caja(XL, 0, T, XL, C_C, "\\frac{b}{2a}x", size=34)
        d2 = caja(0, XL, XL, T, C_C, "\\frac{b}{2a}x", size=34)
        self.play(FadeIn(cuad), FadeIn(d1), FadeIn(d2))
        notas("Lo partimos igual: dos tiras de ancho b/2a")
        self.wait(1.5)
        esq = caja(XL, XL, T, T, ROSA, "\\left(\\frac{b}{2a}\\right)^{2}", op=0.6, size=26)
        self.play(FadeIn(esq, scale=1.3))
        notas("La esquina que falta es (b/2a)²: la sumamos a los DOS lados")
        f2 = XC("x^{2}+\\frac{b}{a}x+\\left(\\frac{b}{2a}\\right)^{2}=-\\frac{c}{a}+\\left(\\frac{b}{2a}\\right)^{2}", 38,
                {"+\\left(\\frac{b}{2a}\\right)^{2}": ROSA}).next_to(f, DOWN, buff=0.6)
        self.play(Write(f2))
        self.wait(1.5)
        notas("La izquierda ya es un cuadrado de lado x + b/2a")
        lado = Brace(VGroup(cuad, d1), DOWN, color=GREY_B)
        ll = MathTex("x+\\frac{b}{2a}", font_size=38).next_to(lado, DOWN, buff=0.1)
        self.play(GrowFromCenter(lado), FadeIn(ll))
        f3 = XC("\\left(x+\\frac{b}{2a}\\right)^{2}=-\\frac{c}{a}+\\left(\\frac{b}{2a}\\right)^{2}", 38,
                {"\\left(\\frac{b}{2a}\\right)^{2}": ROSA}).next_to(f2, DOWN, buff=0.6)
        self.play(Write(f3))
        notas("Ya casi está: seguimos desde aquí")
        self.wait(1.5)

        # --- 3. El álgebra, enganchada a la última línea
        self.play(FadeOut(VGroup(cuad, d1, d2, esq, lado, ll, f, f2, st_g)),
                  f3.animate.scale(42 / 38).move_to([-6.2, 2.0, 0], aligned_edge=LEFT), run_time=1.2)
        subtitulo(self, cab, "Paso a paso")
        pas = [
            ("\\left(x+\\frac{b}{2a}\\right)^{2}=\\frac{b^{2}-4ac}{4a^{2}}",
             "A la derecha, común denominador 4a²:  b²/4a² − 4ac/4a²"),
            ("x+\\frac{b}{2a}=\\pm\\frac{\\sqrt{b^{2}-4ac}}{2a}", "Raíz cuadrada en los dos lados (¡el ±!), y √(4a²) = 2a"),
            ("x=\\frac{-b\\pm\\sqrt{b^{2}-4ac}}{2a}", "Pasamos b/2a restando... ¡y ya está!"),
        ]
        g = VGroup(f3)
        ultimo = f3
        for tex, nota in pas:
            m = X(tex, 42)
            yy = min(ultimo.get_center()[1] - 1.0, ultimo.get_bottom()[1] - 0.3 - m.height / 2)
            m.move_to([-5.7, yy, 0], aligned_edge=LEFT)
            notas(nota)
            self.wait(1.2)
            self.play(Write(m), run_time=1.2)
            self.wait(0.8)
            g.add(m)
            ultimo = m
        caja_f = SurroundingRectangle(g[-1], color=ACENTO, buff=0.15, corner_radius=0.1)
        self.play(Create(caja_f))
        notas("La fórmula no es magia: es completar el cuadrado de al-Juarismi", color=ACENTO)
        self.wait(3.5)
        notas.fin()


class InterpretacionGrafica(Scene):
    def construct(self):
        cab = titulo(self, "Las soluciones, en un dibujo", "Interpretación gráfica")
        notas = Notas(self)
        ax = Axes(x_range=[-2, 6, 1], y_range=[-5, 8, 1], x_length=7.4, y_length=5.0, tips=False,
                  axis_config={"include_numbers": True, "font_size": 22, "color": GREY_B})
        ax.move_to([2.9, -0.3, 0])
        lx = MathTex("x", font_size=34).next_to(ax.x_axis.get_right(), UR, buff=0.1)
        ly = MathTex("y", font_size=34).next_to(ax.y_axis.get_top(), RIGHT, buff=0.15)
        XI = -6.6                                     # columna de la izquierda

        def izq(m, y):
            return m.move_to([XI, y, 0], aligned_edge=LEFT)

        st = [None]

        def sub(t):
            if st[0]:
                self.play(FadeOut(st[0]), run_time=0.4)
            st[0] = subtitulo(self, cab, t)

        # --- 1. Tabla y puntos
        sub("Dos soluciones")
        e = izq(X("y=x^{2}-5x+6", 48), 2.1)
        self.play(Write(e))
        notas("Cambiamos el 0 por una y: para cada x sale un valor de y, y lo dibujamos como un punto")
        self.play(Create(ax), FadeIn(lx), FadeIn(ly))
        f = lambda x: x * x - 5 * x + 6
        tabla = VGroup()
        cabx = MathTex("x", font_size=34, color=LETRA)
        caby = MathTex("y", font_size=34)
        tabla.add(VGroup(cabx, caby).arrange(RIGHT, buff=1.0))
        puntos = VGroup()
        for i, x in enumerate(range(0, 6)):
            fila = VGroup(MathTex(str(x), font_size=32), MathTex(str(f(x)), font_size=32))
            fila[0].move_to(cabx.get_center() + DOWN * 0.42 * (i + 1))
            fila[1].move_to(caby.get_center() + DOWN * 0.42 * (i + 1))
            tabla.add(fila)
        tabla.move_to([XI + 1.0, -0.4, 0], aligned_edge=LEFT)
        raya = Line(tabla[0].get_corner(DL) + DOWN * 0.08 + LEFT * 0.2, tabla[0].get_corner(DR) + DOWN * 0.08 + RIGHT * 0.2,
                    color=GREY_B, stroke_width=2)
        self.play(FadeIn(tabla[0]), Create(raya))
        for i, x in enumerate(range(0, 6)):
            d = Dot(ax.c2p(x, f(x)), color=ACENTO, radius=0.07)
            self.play(FadeIn(tabla[i + 1]), FadeIn(d, scale=1.6), run_time=0.45)
            puntos.add(d)
        curva = ax.plot(f, x_range=[-0.3, 5.3], color=A_C, stroke_width=4)
        notas("Uniendo los puntos sale una curva: una parábola (la estudiaréis en el tema de funciones)")
        self.play(Create(curva), run_time=1.5)
        self.wait(1.5)
        notas("La ecuación x² − 5x + 6 = 0 pregunta: ¿dónde vale y = 0? ¡Donde la curva corta el eje x!", color=ROSA)
        self.play(ax.x_axis.animate.set_color(ROSA), run_time=0.8)
        self.play(*[Indicate(tabla[k][1], color=ROSA, scale_factor=1.5) for k in (3, 4)])
        cortes = VGroup(*[Dot(ax.c2p(r, 0), color=ROSA, radius=0.11) for r in (2, 3)])
        self.play(*[Flash(c, color=ROSA) for c in cortes], FadeIn(cortes))
        self.wait(1)
        self.play(FadeOut(tabla), FadeOut(raya))
        notas("En el dibujo: corta en x = 2 y en x = 3. ¿Lo confirma la fórmula?")
        self.wait(1.5)

        def formula(lineas, res, col_res, ds, nota_ok, y0=1.15):
            """Aplica la fórmula en la columna izquierda y comprueba con los puntos del dibujo."""
            g = VGroup()
            for k, tex in enumerate(lineas):
                m = MathTex(tex, font_size=40)
                if k == 0:
                    izq(m, y0)
                else:
                    m.next_to(g[-1], DOWN, buff=0.4).align_to(g[-1], LEFT)
                self.play(Write(m), run_time=1.2)
                self.wait(0.6)
                g.add(m)
            r = X(res, 44, color=LETRA) if res.startswith("x") else MathTex(res, font_size=40, color=col_res)
            r.next_to(g[-1], DOWN, buff=0.45).align_to(g[-1], LEFT)
            self.play(Write(r))
            g.add(r)
            if len(ds):
                self.play(Indicate(r, color=col_res, scale_factor=1.15),
                          *[Indicate(p, color=ACENTO, scale_factor=1.8) for p in ds], run_time=1.2)
            notas(nota_ok, color=col_res)
            self.wait(3)
            return g

        g = formula(["x=\\frac{5\\pm\\sqrt{25-24}}{2}=\\frac{5\\pm 1}{2}"], "x_{1}=3,\\quad x_{2}=2", OK, cortes,
                    "¡Coinciden! La fórmula da 3 y 2, justo donde la parábola corta el eje x")
        notas.fin()
        self.play(FadeOut(VGroup(e, g, curva, puntos, cortes)), ax.x_axis.animate.set_color(GREY_B))

        def caso(tex, func, rango, raices, nota_dibujo, lineas, res, color_sol, nota_ok):
            e = izq(X(tex, 48), 2.1)
            self.play(Write(e))
            c = ax.plot(func, x_range=rango, color=A_C, stroke_width=4)
            self.play(Create(c), run_time=1.5)
            ds = VGroup(*[Dot(ax.c2p(r, 0), color=ROSA, radius=0.11) for r in raices])
            if raices:
                self.play(*[Flash(p, color=ROSA) for p in ds], FadeIn(ds))
            notas(nota_dibujo)
            self.wait(2)
            g = formula(lineas, res, color_sol, ds, nota_ok)
            notas.fin()
            self.play(FadeOut(VGroup(e, c, ds, g)))

        caso("y=x^{2}-2x-3", lambda x: x * x - 2 * x - 3, [-1.9, 3.9], [-1, 3],
             "En el dibujo: corta en x = −1 y en x = 3. Ahora, con la fórmula (a = 1, b = −2, c = −3)",
             ["\\Delta=4+12=16>0", "x=\\frac{2\\pm\\sqrt{16}}{2}=\\frac{2\\pm 4}{2}"], "x_{1}=3,\\quad x_{2}=-1", OK,
             "¡Coinciden! Δ > 0: dos soluciones, dos puntos de corte")

        sub("Una solución")
        caso("y=x^{2}-4x+4", lambda x: x * x - 4 * x + 4, [-0.8, 4.8], [2],
             "En el dibujo: la parábola solo TOCA el eje x, en x = 2",
             ["\\Delta=16-16=0", "x=\\frac{4\\pm\\sqrt{0}}{2}=\\frac{4}{2}"], "x=2", ACENTO,
             "¡Coincide! Con Δ = 0, el + y el − dan lo mismo: una solución doble")

        sub("Ninguna solución")
        caso("y=x^{2}-4x+5", lambda x: x * x - 4 * x + 5, [-0.6, 4.6], [],
             "En el dibujo: la parábola queda por encima y nunca llega a y = 0",
             ["\\Delta=16-20=-4<0", "x=\\frac{4\\pm\\sqrt{-4}}{2}"], "\\sqrt{-4}\\ \\text{no existe}", MAL,
             "¡Coincide! Con Δ < 0 la fórmula no da solución, y la parábola no corta")

        # --- 5. La parábola que sube
        sub("Todo junto")
        c = ValueTracker(0.0)
        e = izq(MathTex("y=x^{2}-4x+", "c", font_size=48), 2.1)
        e[0][1].set_color(LETRA)
        e[0][4].set_color(LETRA)
        e[1].set_color(ROSA)
        self.play(Write(e))
        def media(): return min(2.6, np.sqrt(12 - c.get_value()))   # sin pasar de y = 8
        curva = always_redraw(lambda: ax.plot(lambda x: x * x - 4 * x + c.get_value(),
                                              x_range=[2 - media(), 2 + media()], color=A_C, stroke_width=4))

        def raices():
            dl = 16 - 4 * c.get_value()
            if dl < -1e-6:
                return []
            r = np.sqrt(max(dl, 0)) / 2
            return [2 - r, 2 + r] if r > 1e-3 else [2.0]

        puntos = always_redraw(lambda: VGroup(*[Dot(ax.c2p(r, 0), color=ROSA, radius=0.11) for r in raices()]))

        def lectura():
            v = c.get_value()
            dl = 16 - 4 * v
            col = OK if dl > 0.05 else (ACENTO if dl > -0.05 else MAL)
            txt = "2 soluciones" if dl > 0.05 else ("1 solución" if dl > -0.05 else "ninguna")
            g = VGroup(MathTex(f"c={v:.1f}".replace(".", "{,}"), font_size=40, color=ROSA),
                       MathTex(f"\\Delta=16-4c={dl:.1f}".replace(".", "{,}"), font_size=40),
                       texto(txt, 30, col)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
            return g.move_to([XI, 0.3, 0], aligned_edge=LEFT)

        lec = always_redraw(lectura)
        self.play(Create(curva), FadeIn(puntos), FadeIn(lec))
        notas("Si cambiamos el número c, la parábola sube o baja. Mira los puntos de corte...")
        self.wait(1.5)
        self.play(c.animate.set_value(4), run_time=5, rate_func=linear)
        notas("Con c = 4 (Δ = 0) los dos puntos se juntan en uno", color=ACENTO)
        self.wait(2)
        self.play(c.animate.set_value(6), run_time=3, rate_func=linear)
        notas("Y si sigue subiendo (Δ < 0), ya no corta: no hay solución", color=MAL)
        self.wait(2)
        self.play(c.animate.set_value(0), run_time=4, rate_func=smooth)
        notas("El discriminante dice cuántas veces corta la parábola al eje x: 2, 1 o 0")
        self.wait(3.5)
        notas.fin()


class Problemas(Scene):
    def construct(self):
        cab = titulo(self, "Problemas con ecuaciones")
        notas = Notas(self)
        subtitulo(self, cab, "Los pasos")
        pasos = VGroup(*[texto(t, 30) for t in (
            "1. Leer bien y decidir qué es la x",
            "2. Plantear: escribir la ecuación",
            "3. Resolver la ecuación",
            "4. Responder y comprobar (¿tiene sentido?)")]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        card = tarjeta(pasos).move_to([0, 0.2, 0])
        self.play(Create(card[0]))
        for p in pasos:
            self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(3)
        limpiar(self, cab)

        # --- Consecutivos
        subtitulo(self, cab, "Números consecutivos")
        enun = texto("La suma de tres números consecutivos es 72. ¿Cuáles son?", 30).move_to([0, 2.2, 0])
        self.play(FadeIn(enun))
        notas("Llamamos x al primero: los otros son x + 1 y x + 2")
        pas = [("3x+3=72", "Juntamos los semejantes"), ("3x=69", None), ("x=23", "69 : 3 = 23")]
        cuenta(self, "x+(x+1)+(x+2)=72", pas, -6.0, 1.1, notas, None, True, 48, dy=0.9)
        sol = texto("Los números son 23, 24 y 25", 32, OK).move_to([3.0, -0.6, 0])
        self.play(FadeIn(sol))
        notas("Comprobamos: 23 + 24 + 25 = 72 ✓", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Edades
        subtitulo(self, cab, "Edades")
        enun = texto("Un padre tiene el triple de edad que su hijo.\nDentro de 10 años tendrá el doble. ¿Qué edad tienen?",
                     28).move_to([0, 2.1, 0])
        self.play(FadeIn(enun))
        notas("Una tabla ayuda a ordenar los datos")
        t = VGroup(*[texto(s, 26, GREY_B) for s in ("", "Hoy", "Dentro de 10 años")],
                   texto("Hijo", 28), X("x", 40), X("x+10", 40),
                   texto("Padre", 28), X("3x", 40), X("3x+10", 40))
        for k, m in enumerate(t):
            m.move_to([(-6.0, -4.6, -2.6)[k % 3], 0.9 - (k // 3) * 0.75, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in t], lag_ratio=0.12), run_time=2)
        notas("Dentro de 10 años, la edad del padre = el doble de la del hijo")
        pas = [("3x+10=2x+20", None), ("3x-2x=20-10", None), ("x=10", None)]
        cuenta(self, "3x+10=2(x+10)", pas, 0.8, 1.1, notas, None, False, 46, dy=0.9)
        sol = texto("Hijo: 10 años · Padre: 30 años", 30, OK).move_to([0, -2.4, 0])
        self.play(FadeIn(sol))
        notas("Comprobamos: dentro de 10 años, 40 = 2 · 20 ✓", color=OK)
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Rectángulo (2.º grado)
        subtitulo(self, cab, "Un problema de segundo grado")
        enun = texto("Un rectángulo mide 3 cm más de largo que de ancho y su área es 40 cm².", 28).move_to([0, 2.2, 0])
        self.play(FadeIn(enun))
        r = Rectangle(width=3.2, height=2.0, color=C_C, fill_color=C_C, fill_opacity=0.25).move_to([4.2, 0.2, 0])
        bx = Brace(r, LEFT, color=GREY_B)
        lx = X("x", 40).next_to(bx, LEFT, buff=0.1)
        by = Brace(r, DOWN, color=GREY_B)
        ly = X("x+3", 40).next_to(by, DOWN, buff=0.1)
        self.play(Create(r), FadeIn(VGroup(bx, lx, by, ly)))
        notas("Ancho = x, largo = x + 3. Área = largo · ancho")
        pas = [("x^{2}+3x-40=0", "Quitamos el paréntesis y lo pasamos todo a un miembro"),
               ("x=\\frac{-3\\pm\\sqrt{9+160}}{2}=\\frac{-3\\pm 13}{2}", "Fórmula: a = 1, b = 3, c = −40"),
               ("x_{1}=5,\\qquad x_{2}=-8", None)]
        cuenta(self, "x(x+3)=40", pas, -6.2, 1.3, notas, None, False, 44, dy=1.05)
        notas("Un lado no puede medir −8: esa solución no sirve para el problema", color=MAL)
        self.wait(2.5)
        sol = texto("El rectángulo mide 5 cm × 8 cm  (5 · 8 = 40 ✓)", 30, OK).move_to([0, -2.6, 0])
        self.play(FadeIn(sol))
        self.wait(3)
        notas.fin()


# ---------------------------------------------------------------------------
# Ejercicios
def enunciados_1():
    return [
        ("1. Comprueba si x = 3 es solución:", lista(["2x + 1 = 7", "5x − 4 = 3x + 1", "x² − x = 6"], 3)),
        ("2. Resuelve:", lista(["3x + 5 = 20", "7x − 4 = 5x + 8", "2 − 3x = x + 14", "4x + 3 = 4x − 1"])),
        ("3. Resuelve (con paréntesis):", lista(["2(x + 3) = 14", "4(x − 1) − 3 = 2x + 3", "3 − (x − 5) = 2(x + 1)"], 3)),
        ("4. Resuelve (con denominadores):",
         lista(["x/3 + x/6 = 5", "(x + 1)/2 = (x + 4)/3", "(x − 2)/3 − (x − 3)/4 = 1"], 3)),
    ]


def enunciados_2():
    return [
        ("5. Resuelve (incompletas):", lista(["x² − 49 = 0", "3x² = 48", "x² + 5x = 0", "x² + 9 = 0"])),
        ("6. Resuelve con la fórmula:", lista(["x² − 7x + 10 = 0", "x² + 2x − 8 = 0", "2x² − 5x + 2 = 0"], 3)),
        ("7. Sin resolverlas, ¿cuántas soluciones tienen?",
         lista(["x² − 4x + 4 = 0", "x² + x + 1 = 0", "3x² − 2x − 1 = 0"], 3)),
    ]


def enunciados_3():
    return [
        ("8. Si al doble de un número le restas 7, obtienes 25. ¿Qué número es?", ""),
        ("9. Ana tiene 12 € más que Luis y entre los dos tienen 50 €. ¿Cuánto tiene cada uno?", ""),
        ("10. El cuadrado de un número menos su doble es 15. ¿Qué número puede ser?", ""),
    ]


SOLUCION = {"si": ("Sí es solución", OK), "no": ("No es solución", MAL)}
COMPRUEBA = [
    ("2x+1=7", ["2\\cdot 3+1=7"], "si"),
    ("5x-4=3x+1", ["5\\cdot 3-4=11", "3\\cdot 3+1=10", "11\\neq 10"], "no"),
    ("x^{2}-x=6", ["3^{2}-3=9-3=6"], "si"),
]


def ej_comprueba(scene, i, x, y, notas, ejemplo=False, size=48):
    e, filas, v = COMPRUEBA[i]
    if ejemplo:
        notas("Sustituimos x por 3 y miramos si los dos miembros dan lo mismo")
    g = cuenta(scene, e, [(MathTex(f, font_size=size), None) for f in filas], x, y, None, f"{'abc'[i]})",
               ejemplo, size, dy=0.85)
    t = texto(SOLUCION[v][0], 28, SOLUCION[v][1]).next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
    scene.play(FadeIn(t))
    scene.wait(1.2 if ejemplo else 0.6)
    return VGroup(g, t)


# Resolver: (enunciado, [(paso, nota)])
RESUELVE = [
    ("3x+5=20", [("3x=20-5", "El 5 pasa restando"), ("3x=15", None), ("x=5", "El 3 pasa dividiendo")]),
    ("7x-4=5x+8", [("7x-5x=8+4", "x a la izquierda y números a la derecha"), ("2x=12", None), ("x=6", None)]),
    ("2-3x=x+14", [("-3x-x=14-2", None), ("-4x=12", None), ("x=\\frac{12}{-4}=-3", "El −4 pasa dividiendo con su signo")]),
    ("4x+3=4x-1", [("4x-4x=-1-3", None), ("0x=-4", "Ningún número por 0 da −4")]),
]
PARENTESIS = [
    ("2(x+3)=14", [("2x+6=14", "Quitamos el paréntesis"), ("2x=8", None), ("x=4", None)]),
    ("4(x-1)-3=2x+3", [("4x-4-3=2x+3", "Quitamos el paréntesis"), ("4x-2x=3+4+3", None), ("2x=10", None),
                       ("x=5", None)]),
    ("3-(x-5)=2(x+1)", [("3-x+5=2x+2", "El menos cambia el signo de TODO el paréntesis"), ("-x-2x=2-3-5", None),
                        ("-3x=-6", None), ("x=2", None)]),
]
DENOM = [
    ("\\frac{x}{3}+\\frac{x}{6}=5", [("2x+x=30", "m.c.m.(3, 6) = 6. Multiplicamos todo por 6"), ("3x=30", None),
                                     ("x=10", None)]),
    ("\\frac{x+1}{2}=\\frac{x+4}{3}", [("3(x+1)=2(x+4)", "m.c.m.(2, 3) = 6:  6 : 2 = 3  y  6 : 3 = 2"),
                                       ("3x+3=2x+8", None), ("x=5", None)]),
    ("\\frac{x-2}{3}-\\frac{x-3}{4}=1", [("4(x-2)-3(x-3)=12", "m.c.m.(3, 4) = 12. ¡Paréntesis en los numeradores!"),
                                         ("4x-8-3x+9=12", "−3 · (−3) = +9"), ("x=12+8-9", None), ("x=11", None)]),
]
INCOMPLETAS = [
    ("x^{2}-49=0", [("x^{2}=49", None), ("x=\\pm 7", "Dos soluciones: 7 y −7")]),
    ("3x^{2}=48", [("x^{2}=16", "El 3 pasa dividiendo"), ("x=\\pm 4", None)]),
    ("x^{2}+5x=0", [("x\\cdot(x+5)=0", "Factor común x"), ("x=0,\\qquad x=-5", "x = 0  o  x + 5 = 0")]),
    ("x^{2}+9=0", [("x^{2}=-9", "Ningún cuadrado es negativo: sin solución")]),
]
FORMULA = [
    ("x^{2}-7x+10=0", [("x=\\frac{7\\pm\\sqrt{49-40}}{2}", "a = 1,  b = −7,  c = 10"),
                       ("x=\\frac{7\\pm 3}{2}", None), ("x_{1}=5,\\qquad x_{2}=2", None)]),
    ("x^{2}+2x-8=0", [("x=\\frac{-2\\pm\\sqrt{4+32}}{2}", "a = 1,  b = 2,  c = −8:  −4 · 1 · (−8) = +32"),
                      ("x=\\frac{-2\\pm 6}{2}", None), ("x_{1}=2,\\qquad x_{2}=-4", None)]),
    ("2x^{2}-5x+2=0", [("x=\\frac{5\\pm\\sqrt{25-16}}{4}", "a = 2,  b = −5,  c = 2. Abajo, 2a = 4"),
                       ("x=\\frac{5\\pm 3}{4}", None), ("x_{1}=2,\\qquad x_{2}=\\frac{1}{2}", None)]),
]
DISCRIM = [
    ("x^{2}-4x+4=0", "\\Delta=16-16=0", "1 solución", ACENTO),
    ("x^{2}+x+1=0", "\\Delta=1-4=-3<0", "ninguna", MAL),
    ("3x^{2}-2x-1=0", "\\Delta=4+12=16>0", "2 soluciones", OK),
]


def ej_lista(scene, datos, i, x, y, notas, ejemplo=False, size=48, dy=None, sin_sol=None):
    enun, pasos = datos[i]
    g = cuenta(scene, enun, pasos, x, y, notas, f"{'abcd'[i]})", ejemplo, size, dy=dy)
    if sin_sol:
        t = texto(sin_sol, 28, MAL).next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        scene.play(FadeIn(t))
        g.add(t)
    return g


def ej_discrim(scene, idx, notas, ejemplo=False, y0=1.2):
    if ejemplo:
        notas("Solo hace falta el discriminante Δ = b² − 4ac")
    for k, i in enumerate(idx):
        e, d, t, c = DISCRIM[i]
        y = y0 - k * 1.1
        et = texto(f"{'abc'[i]})", 28).move_to([-6.3, y, 0])
        m1 = X(e, 46).next_to(et, RIGHT, buff=0.3)
        m2 = MathTex(d, font_size=46).move_to([1.0, y, 0])
        m3 = texto(t, 30, c).move_to([5.0, y, 0])
        scene.play(FadeIn(et), Write(m1))
        scene.play(Write(m2))
        scene.play(FadeIn(m3, shift=LEFT * 0.2))
        scene.wait(1.2 if ejemplo else 0.6)
    notas.fin()


def problema_8(scene, notas, ejemplo=True):
    enun = texto("Si al doble de un número le restas 7, obtienes 25. ¿Qué número es?", 30).move_to([0, 2.2, 0])
    scene.play(FadeIn(enun))
    notas("x = el número.  El doble: 2x.  Le restamos 7: 2x − 7")
    pas = [("2x=25+7", None), ("2x=32", None), ("x=16", None)]
    cuenta(scene, "2x-7=25", pas, -3.0, 1.1, notas, None, ejemplo, 54, dy=1.0)
    notas("El número es 16. Comprobamos: 2 · 16 − 7 = 32 − 7 = 25 ✓", color=OK)
    scene.wait(3)
    notas.fin()


def problema_9(scene, notas):
    enun = texto("Ana tiene 12 € más que Luis y entre los dos tienen 50 €. ¿Cuánto tiene cada uno?", 28)
    scene.play(FadeIn(enun.move_to([0, 2.2, 0])))
    notas("x = el dinero de Luis.  Ana tiene x + 12")
    pas = [("2x+12=50", None), ("2x=38", None), ("x=19", None)]
    cuenta(scene, "x+(x+12)=50", pas, -3.6, 1.1, notas, None, False, 52, dy=1.0)
    notas("Luis tiene 19 € y Ana 19 + 12 = 31 €.  Comprobamos: 19 + 31 = 50 ✓", color=OK)
    scene.wait(3)
    notas.fin()


def problema_10(scene, notas):
    enun = texto("El cuadrado de un número menos su doble es 15. ¿Qué número puede ser?", 28)
    scene.play(FadeIn(enun.move_to([0, 2.2, 0])))
    notas("x = el número.  Su cuadrado: x².  Su doble: 2x")
    pas = [("x^{2}-2x-15=0", "Todo a un miembro: es de segundo grado"),
           ("x=\\frac{2\\pm\\sqrt{4+60}}{2}=\\frac{2\\pm 8}{2}", "a = 1,  b = −2,  c = −15"),
           ("x_{1}=5,\\qquad x_{2}=-3", None)]
    cuenta(scene, "x^{2}-2x=15", pas, -4.6, 1.2, notas, None, False, 48, dy=1.1)
    notas("Las dos sirven: 5² − 2 · 5 = 15  y  (−3)² − 2 · (−3) = 9 + 6 = 15 ✓", color=OK)
    scene.wait(3)
    notas.fin()


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Ecuaciones")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        ej_comprueba(self, 0, -3.0, 1.2, notas, ejemplo=True, size=54)
        notas.fin()
        limpiar(self, cab)
        for n, datos, y in ((2, RESUELVE, 1.5), (3, PARENTESIS, 1.5), (4, DENOM, 1.6), (5, INCOMPLETAS, 1.4),
                            (6, FORMULA, 1.6)):
            subtitulo(self, cab, f"Ejercicio {n} a)")
            ej_lista(self, datos, 0, -3.4, y, notas, ejemplo=True, size=52, dy=1.05)
            self.wait(1)
            notas.fin()
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        ej_discrim(self, [0], notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 8")
        problema_8(self, notas)
        limpiar(self, cab)
        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 4")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1: b) y c)")
        ej_comprueba(self, 1, -5.8, 1.6, notas)
        ej_comprueba(self, 2, 1.2, 1.6, notas)
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2: b) y c)")
        ej_lista(self, RESUELVE, 1, -5.8, 1.5, notas, size=46)
        ej_lista(self, RESUELVE, 2, 0.8, 1.5, notas, size=46)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 d)")
        ej_lista(self, RESUELVE, 3, -3.0, 1.5, notas, size=52, sin_sol="Sin solución")
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3: b) y c)")
        ej_lista(self, PARENTESIS, 1, -6.0, 1.6, notas, size=44, dy=0.85)
        ej_lista(self, PARENTESIS, 2, 0.8, 1.6, notas, size=44, dy=0.85)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 4 b)")
        ej_lista(self, DENOM, 1, -3.4, 1.5, notas, size=50, dy=1.05)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 c)")
        ej_lista(self, DENOM, 2, -3.4, 1.7, notas, size=48, dy=1.0)
        comprobar(self, ["\\frac{9}{3}-\\frac{8}{4}=3-2=1"], 2.6, 0.2, size=38)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 5 a 10.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 5 a 10")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 5: b) y c)")
        ej_lista(self, INCOMPLETAS, 1, -5.8, 1.4, notas, size=50, dy=1.05)
        ej_lista(self, INCOMPLETAS, 2, 0.8, 1.4, notas, size=50, dy=1.05)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 d)")
        ej_lista(self, INCOMPLETAS, 3, -3.0, 1.4, notas, size=54, dy=1.1, sin_sol="Sin solución")
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        for i in (1, 2):
            subtitulo(self, cab, f"Ejercicio 6 {'abc'[i]})")
            ej_lista(self, FORMULA, i, -3.4, 1.6, notas, size=52, dy=1.05)
            self.wait(1)
            notas.fin()
            limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 7: b) y c)")
        ej_discrim(self, [1, 2], notas)
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 9")
        problema_9(self, notas)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 10")
        problema_10(self, notas)
        limpiar(self, cab)
        fin = texto("¡Enhorabuena! Has terminado los ejercicios del tema.", 32, ACENTO)
        self.play(FadeIn(fin))
        self.wait(2)
