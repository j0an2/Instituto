"""Tema 5 · Fracciones (1º ESO) — unidad 4 del libro (antes temas 5 y 7)

Escenas:
    QueEsUnaFraccion        – partes iguales de un todo: barra, pizza, recta
    FraccionesImpropias     – (extra E1) propias e impropias, números mixtos y en la recta
    FraccionesEquivalentes  – 1/2 = 2/4 = 4/8 (misma parte pintada) y productos cruzados
    AmplificarSimplificar   – multiplicar/dividir arriba y abajo; irreducible con el M.C.D.
    CompararFracciones      – mismo denominador, mismo numerador, común denominador (m.c.m.)
    OrdenarFracciones       – reducir a común denominador y colocar en la recta

Renderizar (desde esta carpeta):
    python -m manim -pql t05_fracciones.py QueEsUnaFraccion
    python publicar.py t05_fracciones.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 5 · Fracciones"
TITULOS = {
    "QueEsUnaFraccion": "¿Qué es una fracción?",
    "FraccionesImpropias": "Fracciones propias, impropias y números mixtos",
    "FraccionesEquivalentes": "Fracciones equivalentes",
    "AmplificarSimplificar": "Amplificar y simplificar",
    "CompararFracciones": "Comparar fracciones",
    "OrdenarFracciones": "Ordenar fracciones",
    "EjerciciosFraccionesEjemplo": "Ejercicios (fracciones): enunciados y ejemplos resueltos",
    "EjerciciosFraccionesResueltos": "Ejercicios (fracciones) resueltos",
    "SumaRestaMismoDenominador": "Sumar y restar con el mismo denominador",
    "SumaRestaDistintoDenominador": "Sumar y restar con distinto denominador",
    "FraccionDeUnaCantidad": "Fracción de una cantidad",
    "MultiplicarFracciones": "Multiplicar fracciones",
    "DividirFracciones": "Dividir fracciones",
    "OperacionesCombinadas": "Operaciones combinadas con fracciones",
    "EjerciciosEjemplo": "Ejercicios (operaciones): enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios (operaciones) resueltos",
}
EXTRAS = {"FraccionesImpropias": "E1", "OperacionesCombinadas": "E2"}


def limpiar_a(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo_a(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def flecha_op(f1, f2, op, k, color=ACENTO):
    """Flechas entre dos fracciones (arriba entre numeradores, abajo entre denominadores) con '×k' o ':k'."""
    s = (r"\times " if op == "x" else r": ") + str(k)
    g = VGroup()
    for i, lado in ((0, UP), (2, DOWN)):
        a = Arrow(f1[i].get_right() + RIGHT * 0.15, f2[i].get_left() + LEFT * 0.15, buff=0, color=color,
                  stroke_width=3, max_tip_length_to_length_ratio=0.2)
        lab = MathTex(s, font_size=30, color=color).next_to(a, lado, buff=0.08)
        g.add(VGroup(a, lab))
    return g


# ---------------------------------------------------------------------------
class QueEsUnaFraccion(Scene):
    def construct(self):
        cab = titulo(self, "¿Qué es una fracción?", "Partes iguales de un todo")

        # Tableta de chocolate: 3/4
        ancho, x0, y0 = 5.0, -3.2, 0.6
        entera = Rectangle(width=ancho, height=1.3, stroke_color=WHITE, fill_color=VACIO, fill_opacity=1)
        entera.move_to([x0, y0, 0])
        t0 = texto("Una tableta de chocolate", 28, GREY_B).next_to(entera, UP, buff=0.35)
        self.play(FadeIn(entera), FadeIn(t0))
        cortes = VGroup(*[Line(entera.get_corner(UL) + RIGHT * ancho * k / 4, entera.get_corner(DL) + RIGHT * ancho * k / 4,
                               stroke_width=3) for k in (1, 2, 3)])
        f = fraccion(3, 4, size=96).move_to([1.0, y0, 0])
        den_lab = texto("denominador: en cuántas\npartes IGUALES dividimos", 24, DENOMINADOR).next_to(f[2], RIGHT, buff=0.5)
        num_lab = texto("numerador: cuántas\npartes tomamos", 24, NUMERADOR).next_to(f[0], RIGHT, buff=0.5)
        self.play(Create(cortes), run_time=1.2)
        self.play(Write(f[1]), Write(f[2]), FadeIn(den_lab))
        b = barra(4, 0, ancho=ancho, alto=1.3).move_to(entera)
        self.add(b)
        self.remove(entera, cortes)
        for i in range(3):
            self.play(b[i].animate.set_fill(ACENTO), run_time=0.45)
        self.play(Write(f[0]), FadeIn(num_lab))
        lee = texto("Se lee: «tres cuartos»", 30, ACENTO).move_to([0, -1.6, 0])
        self.play(FadeIn(lee))
        self.wait(2.5)
        limpiar_a(self, cab)

        # Pizza: 5/8
        p = pizza(8, 0, r=1.6).move_to([-3, -0.2, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in p], lag_ratio=0.08))
        f = fraccion(5, 8, size=96).move_to([1.0, -0.2, 0])
        self.play(Write(f[1]), Write(f[2]))
        self.play(LaggedStart(*[p[i].animate.set_fill(ACENTO) for i in range(5)], lag_ratio=0.25))
        self.play(Write(f[0]))
        lee = texto("«cinco octavos»", 30, ACENTO).next_to(f, RIGHT, buff=0.8)
        self.play(FadeIn(lee))
        self.wait(2)
        limpiar_a(self, cab)

        # Partes iguales: contraejemplo
        anchos = [0.8, 2.2, 1.3, 0.7]
        mal = VGroup(*[Rectangle(width=w, height=1.2, stroke_color=WHITE, stroke_width=2,
                                 fill_color=ACENTO if i == 1 else VACIO, fill_opacity=1)
                       for i, w in enumerate(anchos)]).arrange(RIGHT, buff=0).move_to([-2.0, 0.5, 0])
        preg = cadena(texto("¿Es", 34), fraccion(1, 4, 60), texto("?", 34), buff=0.25).next_to(mal, RIGHT, buff=0.8)
        self.play(FadeIn(mal), FadeIn(preg))
        cruz = Cross(mal, stroke_color=MAL, stroke_width=8)
        no = texto("¡No! Las partes tienen que ser IGUALES", 32, MAL).move_to([0, -1.3, 0])
        self.play(Create(cruz), Write(no))
        self.wait(2)
        limpiar_a(self, cab)

        # En la recta
        sub = texto("Una fracción también es un número: tiene su sitio en la recta", 28, ACENTO)
        sub.next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        self.play(FadeIn(sub))
        recta = NumberLine(x_range=[0, 1, 0.25], length=10, include_tip=False, stroke_width=3,
                           tick_size=0.12).move_to([0, -0.5, 0])
        extremos = VGroup(MathTex("0", font_size=40).next_to(recta.n2p(0), DOWN, buff=0.25),
                          MathTex("1", font_size=40).next_to(recta.n2p(1), DOWN, buff=0.25))
        self.play(Create(recta), FadeIn(extremos))
        cuartos = VGroup(*[fraccion(k, 4, size=28).next_to(recta.n2p(k / 4), DOWN, buff=0.2) for k in (1, 2, 3)])
        exp = texto("Dividimos el trozo de 0 a 1 en 4 partes iguales y avanzamos 3", 26, GREY_B)
        exp.move_to([0, 1.2, 0])
        self.play(FadeIn(cuartos), FadeIn(exp))
        punto = Dot(recta.n2p(0) + UP * 0.25, radius=0.13, color=ACENTO)
        self.play(FadeIn(punto, scale=2))
        for k in range(3):
            arco = ArcBetweenPoints(recta.n2p(k / 4) + UP * 0.25, recta.n2p((k + 1) / 4) + UP * 0.25, angle=-PI / 1.6)
            self.play(MoveAlongPath(punto, arco), Create(DashedVMobject(arco.copy().set_stroke(ACENTO, 3))),
                      run_time=0.5, rate_func=linear)
        self.play(punto.animate.move_to(recta.n2p(0.75)))
        et = fraccion(3, 4, size=48).next_to(punto, UP, buff=0.3)
        self.play(Write(et), Flash(punto, color=ACENTO))
        self.wait(2.5)


# ---------------------------------------------------------------------------
def mixto(e, n, d, size=48, color=ACENTO):
    """Número mixto: entero grande + fracción."""
    return VGroup(MathTex(str(e), font_size=size * 1.4, color=color), fraccion(n, d, size)).arrange(RIGHT, buff=0.1)


def division_caja(dividendo, divisor, size=48):
    """División a la española: VGroup(dividendo, divisor, cociente, resto, rayas)."""
    q, r = divmod(dividendo, divisor)
    dv = MathTex(str(dividendo), font_size=size)
    ds = MathTex(str(divisor), font_size=size, color=DENOMINADOR).next_to(dv, RIGHT, buff=0.45)
    v = Line(ds.get_corner(UL) + LEFT * 0.18 + UP * 0.08, ds.get_corner(DL) + LEFT * 0.18 + DOWN * 0.1, stroke_width=3)
    h = Line(v.get_end(), v.get_end() + RIGHT * (ds.width + 0.45), stroke_width=3)
    co = MathTex(str(q), font_size=size, color=ACENTO).next_to(h, DOWN, buff=0.15).align_to(ds, LEFT)
    re = MathTex(str(r), font_size=size, color=NUMERADOR).next_to(dv, DOWN, buff=0.35).align_to(dv, RIGHT)
    return VGroup(dv, ds, co, re, VGroup(v, h))


class FraccionesImpropias(Scene):
    def construct(self):
        cab = titulo(self, "Fracciones propias e impropias", "y números mixtos")
        w = 3.6  # ancho de una unidad

        # 1. Propia, igual a 1, impropia
        b1 = barra(4, 0, ancho=w, alto=0.7).move_to([-3.6, 2.0, 0])
        f1 = fraccion(3, 4, 44).next_to(b1, LEFT, buff=0.4)
        self.play(FadeIn(b1), Write(f1))
        self.play(LaggedStart(*[b1[i].animate.set_fill(ACENTO) for i in range(3)], lag_ratio=0.3))
        t1 = texto("PROPIA: numerador < denominador\nno llega a la unidad", 24, OK).next_to(b1, RIGHT, buff=0.5)
        self.play(FadeIn(t1))
        self.wait(1.5)

        b2 = barra(4, 0, ancho=w, alto=0.7).move_to([-3.6, 0.6, 0])
        f2 = fraccion(4, 4, 44).next_to(b2, LEFT, buff=0.4)
        self.play(FadeIn(b2), Write(f2))
        self.play(LaggedStart(*[b2[i].animate.set_fill(ACENTO) for i in range(4)], lag_ratio=0.3))
        t2 = texto("4/4 = 1: la unidad entera", 24, GREY_B).next_to(b2, RIGHT, buff=0.5)
        self.play(FadeIn(t2))
        self.wait(1.2)

        b3a = barra(4, 0, ancho=w, alto=0.7).move_to([-3.6, -0.9, 0])
        b3b = barra(4, 0, ancho=w, alto=0.7).next_to(b3a, RIGHT, buff=0.35)
        f3 = fraccion(7, 4, 44).next_to(b3a, LEFT, buff=0.4)
        self.play(FadeIn(b3a), Write(f3))
        q = texto("¿7 cuartos? ¡Con una unidad no hay bastante!", 24, ACENTO).move_to([0, -2.0, 0])
        piezas = list(b3a) + list(b3b[:3])
        nums = VGroup()
        for k, pz in enumerate(piezas):
            if k == 4:
                self.play(FadeIn(b3b), FadeIn(q))
            n = MathTex(str(k + 1), font_size=28, color=BLACK).move_to(pz)
            self.play(pz.animate.set_fill(ACENTO), FadeIn(n), run_time=0.3)
            nums.add(n)
        t3 = texto("IMPROPIA: numerador > denominador → es mayor que 1", 26, POSITIVO).move_to([0, -2.0, 0])
        self.play(FadeOut(q), FadeIn(t3))
        self.wait(2.5)
        limpiar_a(self, cab)

        # 2. Número mixto con las barras
        sub = subtitulo_a(self, cab, "Número mixto: unidades enteras + una fracción")
        b3a = barra(4, 4, ancho=w, alto=0.7).move_to([-2.0, 1.3, 0])
        b3b = barra(4, 3, ancho=w, alto=0.7).next_to(b3a, RIGHT, buff=0.35)
        f3 = fraccion(7, 4, 52).next_to(b3a, LEFT, buff=0.5)
        self.play(FadeIn(b3a), FadeIn(b3b), FadeIn(f3))
        ll1 = Brace(b3a, DOWN, buff=0.1)
        ll2 = Brace(b3b[:3], DOWN, buff=0.1)
        e1 = texto("1 unidad", 24, ACENTO).next_to(ll1, DOWN, buff=0.1)
        e2 = fraccion(3, 4, 32).next_to(ll2, DOWN, buff=0.1)
        self.play(GrowFromCenter(ll1), FadeIn(e1))
        self.play(GrowFromCenter(ll2), FadeIn(e2))
        ec = VGroup(fraccion(7, 4, 56), MathTex("=", font_size=56), MathTex("1", font_size=56, color=ACENTO),
                    MathTex("+", font_size=56), fraccion(3, 4, 56), MathTex("=", font_size=56),
                    mixto(1, 3, 4, 56)).arrange(RIGHT, buff=0.3).move_to([0, -1.2, 0])
        self.play(Write(ec[:5]))
        self.play(Write(ec[5:]))
        lee = texto("Se lee: «uno y tres cuartos»", 26, ACENTO).next_to(ec, DOWN, buff=0.4)
        self.play(FadeIn(lee), Circumscribe(ec[6], color=ACENTO))
        self.wait(2.5)
        limpiar_a(self, cab)

        # 3. Impropia -> mixto dividiendo
        subtitulo_a(self, cab, "De impropia a mixto: dividimos")
        for (n, d), x in (((7, 4), -3.3), ((11, 3), 3.3)):
            f = fraccion(n, d, 60).move_to([x - 2.2, 1.0, 0])
            self.play(Write(f))
            dc = division_caja(n, d, 52).move_to([x, 1.0, 0])
            self.play(TransformFromCopy(f[0], dc[0]), TransformFromCopy(f[2], dc[1]), Create(dc[4]))
            self.play(Write(dc[2]), Write(dc[3]))
            q_, r_ = divmod(n, d)
            m = mixto(q_, r_, d, 60).move_to([x, -1.4, 0])
            self.play(TransformFromCopy(dc[2], m[0]), TransformFromCopy(dc[3], m[1][0]),
                      TransformFromCopy(dc[1], m[1][2]), FadeIn(m[1][1]))
            self.wait(0.8)
        regla = texto("cociente → unidades enteras   ·   resto → numerador   ·   el denominador no cambia",
                      22, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(regla))
        self.wait(3)
        limpiar_a(self, cab)

        # 4. Mixto -> impropia
        subtitulo_a(self, cab, "De mixto a impropia")
        m = mixto(2, 2, 3, 60).move_to([-5.2, 1.4, 0])
        self.play(Write(m))
        ws = 2.6
        bs = VGroup(barra(3, 3, ancho=ws, alto=0.65), barra(3, 3, ancho=ws, alto=0.65),
                    barra(3, 2, ancho=ws, alto=0.65)).arrange(RIGHT, buff=0.3).move_to([1.2, 1.4, 0])
        self.play(FadeIn(bs))
        cont = VGroup()
        k = 0
        for bb in bs:
            for pz in bb:
                if pz.get_fill_color().to_hex().upper() != VACIO.upper():
                    k += 1
                    n_ = MathTex(str(k), font_size=26, color=BLACK).move_to(pz)
                    cont.add(n_)
                    self.play(FadeIn(n_), run_time=0.22)
        t = texto("8 tercios", 26, ACENTO).next_to(bs, DOWN, buff=0.3)
        self.play(FadeIn(t))
        cal = VGroup(mixto(2, 2, 3, 56), MathTex("=", font_size=56),
                     fraccion(r"2 \cdot 3 + 2", "3", 56), MathTex("=", font_size=56),
                     fraccion(8, 3, 56)).arrange(RIGHT, buff=0.3).move_to([0, -0.9, 0])
        self.play(Write(cal[:3]))
        self.play(Write(cal[3:]))
        regla = texto("unidades × denominador + numerador  ·  el denominador no cambia", 24, GREY_B)
        regla.next_to(cal, DOWN, buff=0.5)
        self.play(FadeIn(regla))
        self.wait(3)
        limpiar_a(self, cab)

        # 5. En la recta
        subtitulo_a(self, cab, "En la recta: las impropias están después del 1")
        recta = NumberLine(x_range=[0, 3, 1], length=11, include_tip=False, stroke_width=3,
                           tick_size=0.14).move_to([0, -0.4, 0])
        nums = VGroup(*[MathTex(str(k), font_size=40).next_to(recta.n2p(k), DOWN, buff=0.25) for k in range(4)])
        self.play(Create(recta), FadeIn(nums))
        zona = Line(recta.n2p(0), recta.n2p(1), stroke_width=10, color=OK).set_opacity(0.6)
        zt = texto("propias", 24, OK).next_to(zona, DOWN, buff=0.75)
        self.play(Create(zona), FadeIn(zt))
        for (n, d, col, mx) in ((3, 4, OK, None), (7, 4, POSITIVO, (1, 3, 4)), (8, 3, POSITIVO, (2, 2, 3))):
            pnt = Dot(recta.n2p(n / d), radius=0.12, color=col)
            et = fraccion(n, d, 36).next_to(pnt, UP, buff=0.3)
            g = VGroup(et)
            if mx:
                igual = MathTex("=", font_size=36).next_to(et, RIGHT, buff=0.15)
                mm = mixto(*mx, 36).next_to(igual, RIGHT, buff=0.15)
                g.add(igual, mm)
                g.next_to(pnt, UP, buff=0.3)
            self.play(FadeIn(pnt, scale=2), FadeIn(g))
        fin = texto("7/4 = 1 y 3/4: está entre el 1 y el 2", 26, ACENTO).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(fin))
        self.wait(3)


# ---------------------------------------------------------------------------
class FraccionesEquivalentes(Scene):
    def construct(self):
        cab = titulo(self, "Fracciones equivalentes", "El mismo trozo con distinto nombre")

        ancho, xb = 7.0, 0.9
        filas = [(2, 1, 1.6), (4, 2, 0.1), (8, 4, -1.4)]
        barras, fracs = [], []
        for idx, (p, k, y) in enumerate(filas):
            b = barra(p, k, ancho=ancho, alto=0.9).move_to([xb, y, 0])
            f = fraccion(k, p, size=56).move_to([-4.6, y, 0])
            if idx == 0:
                self.play(FadeIn(b), Write(f))
            else:
                prev = barras[-1].copy()
                self.play(prev.animate.move_to(b))
                nota = texto("cortamos cada trozo por la mitad", 22, GREY_B).next_to(b, DOWN, buff=0.12)
                self.play(ReplacementTransform(prev, b), FadeIn(nota), run_time=1.2)
                self.play(Write(f), FadeOut(nota))
            barras.append(b)
            fracs.append(f)
            self.wait(0.4)

        x_borde = barras[0][0].get_right()[0]
        guia = DashedLine([x_borde, 2.3, 0], [x_borde, -2.1, 0], color=ACENTO)
        misma = texto("¡La parte pintada es siempre la misma!", 28, ACENTO).move_to([0, -2.5, 0])
        self.play(Create(guia), Write(misma))
        self.wait(1.5)
        fila = cadena((1, 2), "=", (2, 4), "=", (4, 8), size=56).move_to([0, -2.6, 0])
        self.play(FadeOut(misma), *[TransformFromCopy(f, fila[2 * i]) for i, f in enumerate(fracs)],
                  FadeIn(fila[1]), FadeIn(fila[3]))
        defi = texto("Son fracciones EQUIVALENTES: representan la misma cantidad", 26, ACENTO).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(defi))
        self.wait(2.5)
        limpiar_a(self, cab)

        # Productos cruzados
        sub = subtitulo_a(self, cab, "¿Cómo saber si dos fracciones son equivalentes?")
        for (a, b, c, d), y in (((1, 2, 2, 4), 1.0), ((2, 3, 3, 4), -1.6)):
            f1 = fraccion(a, b, size=72).move_to([-4.2, y, 0])
            f2 = fraccion(c, d, size=72).move_to([-1.8, y, 0])
            sig = MathTex("=" if a * d == b * c else r"\neq", font_size=72).move_to([-3.0, y, 0])
            self.play(Write(f1), Write(f2))
            l1 = Line(f1[0].get_center(), f2[2].get_center(), color=NUMERADOR, stroke_width=4)
            l2 = Line(f1[2].get_center(), f2[0].get_center(), color=DENOMINADOR, stroke_width=4)
            self.play(Create(l1), Create(l2))
            p1 = MathTex(f"{a} \\cdot {d} = {a * d}", font_size=44, color=NUMERADOR).move_to([0.6, y + 0.4, 0])
            p2 = MathTex(f"{b} \\cdot {c} = {b * c}", font_size=44, color=DENOMINADOR).move_to([0.6, y - 0.4, 0])
            self.play(Write(p1), Write(p2))
            ok = a * d == b * c
            res = texto("iguales →\nequivalentes" if ok else "distintos →\nNO son equivalentes", 28, OK if ok else MAL)
            res.move_to([2.3, y, 0], aligned_edge=LEFT)
            self.play(FadeOut(VGroup(l1, l2)), FadeIn(sig), Write(res))
            self.wait(1.5)
        regla = texto("Productos cruzados: si son iguales, las fracciones son equivalentes", 26, ACENTO)
        regla.to_edge(DOWN, buff=0.3)
        self.play(Write(regla))
        self.wait(3)


# ---------------------------------------------------------------------------
class AmplificarSimplificar(Scene):
    def construct(self):
        cab = titulo(self, "Amplificar y simplificar")
        xs = [-4.6, 0, 4.6]

        # Amplificar
        subtitulo_a(self, cab, "Amplificar: multiplicar arriba y abajo por el mismo número")
        datos = [(2, 3), (4, 6), (8, 12)]
        self.cadena_ops(datos, "x", [2, 2], xs)
        resumen = texto("Cortamos más fino: hay más trozos, pero la parte pintada es la misma", 24, GREY_B)
        resumen.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(resumen))
        self.wait(2.5)
        limpiar_a(self, cab)

        # Simplificar
        subtitulo_a(self, cab, "Simplificar: dividir arriba y abajo por el mismo número")
        datos = [(12, 18), (6, 9), (2, 3)]
        self.cadena_ops(datos, ":", [2, 3], xs)
        resumen = texto("Juntamos trozos: hay menos trozos, pero la parte pintada es la misma", 24, GREY_B)
        resumen.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(resumen))
        self.wait(2.5)
        limpiar_a(self, cab)

        # Irreducible con el M.C.D.
        subtitulo_a(self, cab, "De una vez: dividimos por el M.C.D.")
        l1 = VGroup(MathTex(r"12 = 2^2 \cdot 3", font_size=44), MathTex(r"18 = 2 \cdot 3^2", font_size=44))
        l1.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-3.6, 1.5, 0])
        for m in l1:
            m.set_color_by_tex("2", COLOR_PRIMO[2])
        mcd = MathTex(r"\text{M.C.D.}(12, 18) = 2 \cdot 3 = 6", font_size=44, color=ACENTO).next_to(l1, RIGHT, buff=0.8)
        recuerda = texto("(lo aprendimos en el tema 2)", 22, GREY_B).next_to(mcd, DOWN, buff=0.15)
        self.play(Write(l1))
        self.play(Write(mcd), FadeIn(recuerda))
        f1 = fraccion(12, 18, size=80).move_to([-2.2, -1.2, 0])
        f2 = fraccion(2, 3, size=80).move_to([2.2, -1.2, 0])
        self.play(Write(f1))
        ops = flecha_op(f1, f2, ":", 6)
        self.play(Create(ops))
        self.play(TransformFromCopy(f1, f2))
        irr = texto("2/3 es IRREDUCIBLE: ya no se puede simplificar más", 26, ACENTO).to_edge(DOWN, buff=0.35)
        self.play(Circumscribe(f2, color=ACENTO), FadeIn(irr))
        self.wait(3)

    def cadena_ops(self, datos, op, ks, xs):
        fracs = [fraccion(n, d, size=72).move_to([x, 1.3, 0]) for (n, d), x in zip(datos, xs)]
        barras = [barra(d, n, ancho=3.4, alto=0.7).move_to([x, -0.9, 0]) for (n, d), x in zip(datos, xs)]
        self.play(Write(fracs[0]), FadeIn(barras[0]))
        for i in range(1, len(datos)):
            ops = flecha_op(fracs[i - 1], fracs[i], op, ks[i - 1])
            self.play(Create(ops))
            self.play(TransformFromCopy(fracs[i - 1], fracs[i]))
            self.play(ReplacementTransform(barras[i - 1].copy(), barras[i]), run_time=1.2)
            self.wait(0.4)
        iguales = VGroup(*[MathTex("=", font_size=60).move_to([(xs[i] + xs[i + 1]) / 2, -0.9, 0])
                           for i in range(len(xs) - 1)])
        self.play(FadeIn(iguales))


# ---------------------------------------------------------------------------
class CompararFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Comparar fracciones", "¿Cuál es mayor?")

        self.caso(cab, "Mismo denominador", (3, 7), (5, 7),
                  "Trozos del mismo tamaño: es mayor la que tiene más trozos")
        self.idea_comun(cab)
        self.caso_comun(cab, (3, 4), (5, 6), "Ejemplo 1")
        self.caso_comun(cab, (2, 3), (3, 5), "Ejemplo 2")
        self.resumen(cab)

    def mostrar(self, a, b, ancho=6.5):
        filas = []
        for (n, d), y in ((a, 1.0), (b, -0.4)):
            f = fraccion(n, d, size=56).move_to([-4.8, y, 0])
            br = barra(d, n, ancho=ancho, alto=0.8).move_to([0.9, y, 0])
            self.play(Write(f), FadeIn(br))
            filas.append((f, br))
        return filas

    def resultado(self, a, b, y=-1.8):
        sig = ">" if a[0] / a[1] > b[0] / b[1] else "<"
        r = cadena(a, sig, b, size=60).move_to([0, y, 0])
        r[1].set_color(ACENTO)
        self.play(Write(r))
        return r

    def caso(self, cab, nombre, a, b, explicacion):
        subtitulo_a(self, cab, nombre)
        filas = self.mostrar(a, b)
        x_a = filas[0][1][a[0] - 1].get_right()[0]
        x_b = filas[1][1][b[0] - 1].get_right()[0]
        guias = VGroup(DashedLine([x_a, 1.5, 0], [x_a, -0.9, 0], color=ACENTO),
                       DashedLine([x_b, 1.5, 0], [x_b, -0.9, 0], color=ACENTO))
        self.play(Create(guias))
        r = self.resultado(a, b)
        if a[1] != b[1]:
            trampa = texto("¡Cuidado! 5 es mayor que 3, pero un quinto es MÁS PEQUEÑO que un tercio", 24, MAL)
            trampa.next_to(r, DOWN, buff=0.25)
            self.play(Indicate(filas[0][1][0], scale_factor=1.15), Indicate(filas[1][1][0], scale_factor=1.15))
            self.play(FadeIn(trampa))
        exp = texto(explicacion, 24, GREY_B).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(exp))
        self.wait(2.5)
        limpiar_a(self, cab)

    def idea_comun(self, cab):
        """Por qué hace falta el común denominador."""
        subtitulo_a(self, cab, "Distinto denominador")
        a, b = (3, 4), (5, 6)
        filas = self.mostrar(a, b)
        p1 = texto("Los trozos son de distinto tamaño (cuartos y sextos)...", 26, GREY_B).move_to([0, -1.5, 0])
        self.play(Indicate(filas[0][1][0], scale_factor=1.15), Indicate(filas[1][1][0], scale_factor=1.15), FadeIn(p1))
        self.wait(1)
        p2 = texto("¡Así no podemos comparar! Necesitamos trozos del MISMO tamaño", 28, MAL).move_to([0, -2.2, 0])
        self.play(FadeIn(p2))
        self.wait(1)
        p3 = texto("Truco: las pasamos a fracciones equivalentes con el MISMO denominador", 26, ACENTO)
        p3.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(p3))
        self.wait(2.5)
        limpiar_a(self, cab)

    def caso_comun(self, cab, a, b, nombre):
        (na, da), (nb, db) = a, b
        m = da * db // np.gcd(da, db)
        subtitulo_a(self, cab, f"{nombre}: ¿cuál es mayor?")
        ya, yb, xf, xe, xb = 1.75, -0.25, -5.6, -3.0, 2.0
        fa = fraccion(na, da, size=56).move_to([xf, ya, 0])
        fb = fraccion(nb, db, size=56).move_to([xf, yb, 0])
        ba = barra(da, na, ancho=6.4, alto=0.75).move_to([xb, ya, 0])
        bb = barra(db, nb, ancho=6.4, alto=0.75).move_to([xb, yb, 0])
        self.play(Write(fa), Write(fb), FadeIn(ba), FadeIn(bb))
        self.wait(0.5)

        # Paso 1: el m.c.m. de los denominadores con las listas de múltiplos
        paso = texto(f"1.º  Buscamos el m.c.m. de los denominadores {da} y {db}", 26, ACENTO).move_to([0, -1.4, 0])
        self.play(FadeIn(paso), Indicate(fa[2], color=DENOMINADOR), Indicate(fb[2], color=DENOMINADOR))
        listas, aros = VGroup(), VGroup()
        for d, y in ((da, -2.05), (db, -2.7)):
            mult = [d * k for k in range(1, m // d + 2)]
            lab = texto(f"Múltiplos de {d}:", 26, DENOMINADOR)
            nums = VGroup(*[MathTex(str(v), font_size=38) for v in mult]).arrange(RIGHT, buff=0.4)
            fila = VGroup(lab, nums, MathTex(r"\dots", font_size=40)).arrange(RIGHT, buff=0.35)
            fila.move_to([-0.6, y, 0], aligned_edge=ORIGIN).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(lab), LaggedStart(*[FadeIn(n_, shift=RIGHT * 0.1) for n_ in nums], lag_ratio=0.15),
                      FadeIn(fila[2]), run_time=1.4)
            aros.add(Circle(radius=0.32, color=ACENTO, stroke_width=4).move_to(nums[mult.index(m)]))
            listas.add(fila)
        self.play(Create(aros))
        res_mcm = MathTex(rf"\text{{m.c.m.}}({da}, {db}) = {m}", font_size=46, color=ACENTO)
        res_mcm.next_to(listas, RIGHT, buff=0.6)
        nuevo = texto(f"→ el nuevo denominador será {m}", 22, ACENTO).next_to(res_mcm, DOWN, buff=0.15)
        VGroup(res_mcm, nuevo).to_edge(RIGHT, buff=0.4)
        self.play(Write(res_mcm), FadeIn(nuevo))
        self.wait(2)
        self.play(FadeOut(VGroup(listas, aros, paso, nuevo)), res_mcm.animate.scale(0.75).move_to([-0.5, 2.75, 0]))

        # Paso 2: ¿por cuánto multiplicamos cada fracción?
        paso = texto("2.º  ¿Por cuánto multiplicamos cada fracción para llegar a ese denominador?", 24, ACENTO)
        paso.move_to([0, -1.4, 0])
        self.play(FadeIn(paso))
        nuevas_f, nuevas_b = [], []
        for (n, d), f, br, y, yc in ((a, fa, ba, ya, -2.05), (b, fb, bb, yb, -2.7)):
            k = m // d
            cuenta = MathTex(f"{m} : {d} = {k}", font_size=40).move_to([-3.6, yc, 0])
            expl = texto(f"multiplicamos arriba y abajo por {k}", 24, GREY_B).next_to(cuenta, RIGHT, buff=0.5)
            self.play(Write(cuenta), FadeIn(expl))
            f2 = fraccion(n * k, m, size=56).move_to([xe, y, 0])
            ops = flecha_op(f, f2, "x", k)
            self.play(Create(ops))
            self.play(TransformFromCopy(f, f2))
            # Paso 3 (visual): la barra se vuelve a cortar
            br2 = barra(m, n * k, ancho=6.4, alto=0.75).move_to(br)
            corte = texto(f"cada trozo se corta en {k}", 20, GREY_B).next_to(br, UP, buff=0.08)
            self.play(FadeIn(corte), ReplacementTransform(br, br2), run_time=1.3)
            self.play(FadeOut(corte))
            nuevas_f.append(f2)
            nuevas_b.append(br2)
            self.play(FadeOut(VGroup(cuenta, expl)))
        self.play(FadeOut(paso))

        # Paso 3: comparar numeradores
        paso = texto("3.º  Ahora los trozos son iguales: comparamos los numeradores", 26, ACENTO).move_to([0, -1.4, 0])
        self.play(FadeIn(paso))
        ka, kb = na * (m // da), nb * (m // db)
        guias = VGroup(*[DashedLine([br[k - 1].get_right()[0], 2.3, 0], [br[k - 1].get_right()[0], -0.8, 0], color=ACENTO)
                         for br, k in zip(nuevas_b, (ka, kb))])
        self.play(Create(guias), Indicate(nuevas_f[0][0], color=NUMERADOR, scale_factor=1.4),
                  Indicate(nuevas_f[1][0], color=NUMERADOR, scale_factor=1.4))
        sig = ">" if ka > kb else "<"
        r = cadena((ka, m), sig, (kb, m), "\\Rightarrow", a, sig, b, size=54).move_to([0, -2.55, 0])
        r[1].set_color(ACENTO)
        r[5].set_color(ACENTO)
        self.play(Write(r), run_time=1.8)
        self.play(Circumscribe(r[4:], color=ACENTO))
        self.wait(2.5)
        limpiar_a(self, cab)

    def resumen(self, cab):
        subtitulo_a(self, cab, "Resumen")
        pasos = VGroup(
            texto("1.  Buscamos el m.c.m. de los denominadores", 32),
            texto("2.  Pasamos cada fracción a ese denominador\n     (multiplicando arriba y abajo por el mismo número)", 32),
            texto("3.  Con el mismo denominador, es mayor\n     la que tiene el numerador mayor", 32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        for p in pasos:
            self.play(FadeIn(p, shift=RIGHT * 0.2))
            self.wait(0.8)
        self.wait(3)


# ---------------------------------------------------------------------------
class OrdenarFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Ordenar fracciones")
        enun = texto("Ordena de menor a mayor:", 30, ACENTO).next_to(cab, DOWN, buff=0.35).to_edge(LEFT)
        datos = [(1, 2), (3, 8), (3, 4), (5, 8)]
        xs = [-3.6, -1.2, 1.2, 3.6]
        orig = [fraccion(n, d, size=60).move_to([x, 1.6, 0]) for (n, d), x in zip(datos, xs)]
        self.play(FadeIn(enun), LaggedStart(*[Write(f) for f in orig], lag_ratio=0.2))

        # 1) Común denominador 8
        paso = texto("1.º  Común denominador: m.c.m.(2, 8, 4) = 8", 26, GREY_B).move_to([0, 0.5, 0])
        self.play(FadeIn(paso))
        eq = []
        for (n, d), f, x in zip(datos, orig, xs):
            k = 8 // d
            g = cadena("=", (n * k, 8), size=48, buff=0.15)
            g.next_to(f, RIGHT, buff=0.12)
            if k > 1:
                nota = MathTex(rf"\times {k}", font_size=26, color=ACENTO).next_to(g[1], DOWN, buff=0.08)
                g.add(nota)
            eq.append(g)
        # Reajustamos para que quepan las parejas
        for f, g, x in zip(orig, eq, xs):
            VGroup(f, g).move_to([x, 1.6, 0])
        self.play(*[f.animate.move_to([x - 0.45, 1.6, 0]) for f, x in zip(orig, xs)])
        for f, g in zip(orig, eq):
            g.next_to(f, RIGHT, buff=0.12)
            self.play(FadeIn(g), run_time=0.6)
        self.wait(1)

        # 2) A la recta
        self.play(FadeOut(paso))
        paso2 = texto("2.º  Las colocamos en la recta (dividida en octavos)", 26, GREY_B).move_to([0, 0.5, 0])
        self.play(FadeIn(paso2))
        recta = NumberLine(x_range=[0, 1, 1 / 8], length=11, include_tip=False, stroke_width=3,
                           tick_size=0.1).move_to([0, -1.2, 0])
        marcas = VGroup(MathTex("0", font_size=36).next_to(recta.n2p(0), DOWN, buff=0.2),
                        MathTex("1", font_size=36).next_to(recta.n2p(1), DOWN, buff=0.2),
                        *[fraccion(k, 8, size=24, colores=False).set_opacity(0.6).next_to(recta.n2p(k / 8), DOWN, buff=0.15)
                          for k in range(1, 8)])
        self.play(Create(recta), FadeIn(marcas))
        sobre = []
        for (n, d), f in zip(datos, orig):
            v = n / d
            dot = Dot(recta.n2p(v), radius=0.11, color=ACENTO)
            c = f.copy()
            self.play(c.animate.scale(0.7).next_to(recta.n2p(v), UP, buff=0.3), FadeIn(dot, scale=2), run_time=0.8)
            sobre.append((v, c))
        self.wait(1)

        # 3) Resultado
        orden = sorted(zip(datos, sobre), key=lambda t: t[0][0] / t[0][1])
        items = []
        for i, ((n, d), _) in enumerate(orden):
            if i:
                items.append("<")
            items.append((n, d))
        fila = cadena(*items, size=52).to_edge(DOWN, buff=0.35)
        self.play(FadeOut(paso2))
        self.play(LaggedStart(*[TransformFromCopy(s[1], fila[2 * i]) for i, (_, s) in enumerate(orden)], lag_ratio=0.2),
                  *[FadeIn(fila[2 * i + 1]) for i in range(len(orden) - 1)], run_time=2)
        truco = texto("Ordenar de menor a mayor = leer la recta de izquierda a derecha", 24, ACENTO)
        truco.move_to([0, 0.4, 0])
        self.play(FadeIn(truco), Circumscribe(fila, color=ACENTO))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
from math import gcd  # noqa: E402

DIBUJOS = [("barra", 3, 5), ("pizza", 5, 8), ("barra", 2, 6), ("pizza", 7, 10)]
EQUIVALENTES = [((2, 3), (8, 12)), ((3, 5), (6, 9)), ((1, 3), (3, 9))]
COMPLETA = [((3, 4), ("?", 12)), ((2, 5), (6, "?")), ((10, 15), ("?", 3))]
SIMPLIFICA = [(8, 12), (15, 25), (18, 24), (20, 30)]
COMPARA = [((4, 9), (7, 9)), ((2, 3), (3, 4)), ((3, 10), (2, 5)), ((5, 6), (7, 9)), ((4, 6), (2, 3))]
ORDENA = [([(1, 2), (2, 3), (5, 12), (3, 4)], True), ([(3, 5), (7, 10), (1, 2), (4, 5)], False)]
LECTORES = [("Marta", 2, 3), ("Pablo", 5, 6), ("Sara", 3, 4)]


def mcm_a(*ds):
    m = 1
    for d in ds:
        m = m * d // gcd(m, d)
    return m


def fr_txt(n, d):
    return f"{n}/{d}"


def dibujo(tipo, n, d, escala=1.0):
    return barra(d, n, ancho=3.0 * escala, alto=0.8 * escala) if tipo == "barra" else pizza(d, n, r=1.0 * escala)


def pagina_enunciados_a(scene, cab, bloques):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        c = texto(cuerpo, 23) if isinstance(cuerpo, str) else cuerpo
        b = VGroup(texto(cabecera, 28, ACENTO), c).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cab, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar_a(scene, cab)


def mini_dibujos():
    g = VGroup()
    for l, (tipo, n, d) in zip("abcd", DIBUJOS):
        g.add(VGroup(texto(f"{l})", 24), dibujo(tipo, n, d, 0.5)).arrange(RIGHT, buff=0.2))
    return g.arrange(RIGHT, buff=0.8)


def enunciados_1_a():
    return [
        ("1. Escribe la fracción que representa cada dibujo:", mini_dibujos()),
        ("2. Fracciones equivalentes:",
         "a) ¿Son equivalentes?   " + "    ".join(f"{fr_txt(*p)} y {fr_txt(*q)}" for p, q in EQUIVALENTES) + "\n"
         "b) Completa:   " + "    ".join(f"{fr_txt(*p)} = {fr_txt(*q)}" for p, q in COMPLETA)),
        ("3. Simplifica hasta la fracción irreducible:", "    ".join(fr_txt(*f) for f in SIMPLIFICA)),
    ]


def enunciados_2_a():
    return [
        ("4. Compara con <, > o =:",
         "    ".join(f"{l}) {fr_txt(*p)}  ?  {fr_txt(*q)}" for l, (p, q) in zip("abcde", COMPARA))),
        ("5. Ordena:",
         "a) De menor a mayor:  " + ",  ".join(fr_txt(*f) for f in ORDENA[0][0]) + "\n"
         "b) De mayor a menor:  " + ",  ".join(fr_txt(*f) for f in ORDENA[1][0])),
        ("6. Problemas:",
         "a) Ana se come 3/8 de una pizza y Luis 1/4 de otra igual. ¿Quién come más?\n"
         "b) En una clase, 2/5 del alumnado va en autobús y 3/10 andando.\n"
         "     ¿Qué grupo es mayor?\n"
         "c) Marta ha leído 2/3 de un libro, Pablo 5/6 y Sara 3/4.\n"
         "     Ordénalos de quien ha leído más a quien ha leído menos."),
    ]


def flecha_una(m1, m2, s, lado, color=ACENTO):
    a = Arrow(m1.get_right() + RIGHT * 0.15, m2.get_left() + LEFT * 0.15, buff=0, color=color,
              stroke_width=3, max_tip_length_to_length_ratio=0.2)
    return VGroup(a, MathTex(s, font_size=30, color=color).next_to(a, lado, buff=0.08))


# --- 1. Escribe la fracción
def resolver_dibujos(scene, items, letras, ejemplo=False):
    xs = [0.0] if len(items) == 1 else [-4.5, 0.0, 4.5][:len(items)]
    for (tipo, n, d), l, x in zip(items, letras, xs):
        esc = 1.6 if ejemplo else 1.0
        dib = dibujo(tipo, n, d, esc).move_to([x - (2.2 if ejemplo else 0), 0.7, 0])
        lab = texto(f"{l})", 30).next_to(dib, LEFT, buff=0.3)
        scene.play(FadeIn(lab), FadeIn(dib))
        if ejemplo:
            f = fraccion(n, d, size=90).move_to([x + 2.8, 0.7, 0])
            e1 = texto(f"{d} partes iguales  →  denominador", 26, DENOMINADOR).move_to([0, -1.3, 0])
            e2 = texto(f"{n} partes pintadas  →  numerador", 26, NUMERADOR).next_to(e1, DOWN, buff=0.25)
            scene.play(LaggedStart(*[Indicate(p, scale_factor=1.1) for p in dib], lag_ratio=0.05), FadeIn(e1),
                       Write(f[1]), Write(f[2]))
            scene.play(LaggedStart(*[Indicate(p, scale_factor=1.2) for p in dib[:n]], lag_ratio=0.1), FadeIn(e2),
                       Write(f[0]))
        else:
            f = fraccion(n, d, size=64).move_to([x, -1.2, 0])
            scene.play(Write(f))
            g = gcd(n, d)
            if g > 1:
                s = cadena("=", (n // g, d // g), size=44, buff=0.15).next_to(f, RIGHT, buff=0.2)
                scene.play(FadeIn(s))
                nota = texto("(simplificada)", 20, GREY_B).next_to(s, DOWN, buff=0.1)
                scene.play(FadeIn(nota))
    scene.wait(2.5)


# --- 2a. ¿Son equivalentes?
def resolver_cruzados(scene, pares, letras):
    ys = [0.9] if len(pares) == 1 else [1.3, -1.0]
    for ((a, b), (c, d)), l, y in zip(pares, letras, ys):
        lab = texto(f"{l})", 30).move_to([-6.2, y, 0])
        f1 = fraccion(a, b, size=68).move_to([-4.8, y, 0])
        f2 = fraccion(c, d, size=68).move_to([-2.6, y, 0])
        scene.play(FadeIn(lab), Write(f1), Write(f2))
        l1 = Line(f1[0].get_center(), f2[2].get_center(), color=NUMERADOR, stroke_width=4)
        l2 = Line(f1[2].get_center(), f2[0].get_center(), color=DENOMINADOR, stroke_width=4)
        p1 = MathTex(f"{a} \\cdot {d} = {a * d}", font_size=42, color=NUMERADOR).move_to([0.2, y + 0.38, 0])
        p2 = MathTex(f"{b} \\cdot {c} = {b * c}", font_size=42, color=DENOMINADOR).move_to([0.2, y - 0.38, 0])
        scene.play(Create(l1), Write(p1))
        scene.play(Create(l2), Write(p2))
        ok = a * d == b * c
        sig = MathTex("=" if ok else r"\neq", font_size=68).move_to([-3.7, y, 0])
        res = texto("iguales →\nSÍ son equivalentes" if ok else "distintos →\nNO son equivalentes", 26,
                    OK if ok else MAL).move_to([2.0, y, 0], aligned_edge=LEFT)
        scene.play(FadeOut(VGroup(l1, l2)), FadeIn(sig), Write(res))
        scene.wait(1)
    scene.wait(1.5)


# --- 2b. Completa
def resolver_completa(scene, items, letras, ejemplo=False):
    ys = [0.6] if len(items) == 1 else [1.3, -1.0]
    for ((a, b), (c, d)), l, y in zip(items, letras, ys):
        lab = texto(f"{l})", 30).move_to([-6.2, y, 0])
        f1 = fraccion(a, b, size=72).move_to([-4.6, y, 0])
        f2 = fraccion(c, d, size=72).move_to([-1.4, y, 0])
        for k in (0, 2):
            if f2[k].get_tex_string() == "?":
                f2[k].set_color(ACENTO)
        scene.play(FadeIn(lab), Write(f1), Write(f2))
        # Pareja conocida: de ahí sale el número por el que se multiplica o divide
        conocido = 2 if c == "?" else 0
        desconocido = 2 - conocido
        x0, x1 = (b, d) if conocido == 2 else (a, c)
        if x1 > x0:
            op, k, s = "x", x1 // x0, rf"\times {x1 // x0}"
        else:
            op, k, s = ":", x0 // x1, rf": {x0 // x1}"
        lado = DOWN if conocido == 2 else UP
        f_con = flecha_una(f1[conocido], f2[conocido], s, lado)
        scene.play(Create(f_con))
        if ejemplo:
            exp = texto(f"{x0} → {x1}: hemos {'multiplicado' if op == 'x' else 'dividido'} por {k}", 26, ACENTO)
            exp.move_to([0, y - 1.6, 0])
            scene.play(FadeIn(exp))
        f_des = flecha_una(f1[desconocido], f2[desconocido], s, UP if lado is DOWN else DOWN)
        scene.play(Create(f_des))
        v = (a if desconocido == 0 else b)
        v = v * k if op == "x" else v // k
        nuevo = MathTex(str(v), font_size=72, color=NUMERADOR if desconocido == 0 else DENOMINADOR)
        nuevo.move_to(f2[desconocido])
        scene.play(Transform(f2[desconocido], nuevo), Flash(nuevo, color=ACENTO))
        if ejemplo:
            regla = texto("Lo que hacemos abajo, lo hacemos arriba (y al revés)", 26, ACENTO).to_edge(DOWN, buff=0.5)
            scene.play(FadeIn(regla))
        scene.wait(1)
    scene.wait(1.5)


# --- 3. Simplificar
def resolver_simplifica(scene, items, letras, ejemplo=False):
    ys = [0.8] if len(items) == 1 else [1.9, 0.0, -1.9]
    for (n, d), l, y in zip(items, letras, ys):
        g = gcd(n, d)
        lab = texto(f"{l})", 30).move_to([-6.2, y, 0])
        f1 = fraccion(n, d, size=56).move_to([-4.9, y, 0])
        scene.play(FadeIn(lab), Write(f1))
        m = MathTex(rf"\text{{M.C.D.}}({n}, {d}) = {g}", font_size=40, color=ACENTO).move_to([-1.8, y, 0])
        scene.play(Write(m))
        f2 = fraccion(n // g, d // g, size=56).move_to([3.3, y, 0])
        ops = flecha_op(VGroup(m[0][-1:]).copy().move_to([0.4, y + 0.38, 0]),
                        f2, ":", g) if False else None
        fl = VGroup(flecha_una(Dot([0.4, y + 0.38, 0], radius=0.01), f2[0], f": {g}", UP),
                    flecha_una(Dot([0.4, y - 0.38, 0], radius=0.01), f2[2], f": {g}", DOWN))
        scene.play(Create(fl))
        scene.play(Write(f2))
        if ejemplo:
            irr = texto(f"{n // g}/{d // g} es irreducible: el M.C.D. de {n // g} y {d // g} es 1", 26, GREY_B)
            irr.to_edge(DOWN, buff=0.6)
            scene.play(FadeIn(irr), Circumscribe(f2, color=ACENTO))
        scene.wait(0.6)
    scene.wait(2)


# --- 4. Comparar
def resolver_compara(scene, a, b, letra, detalle=False):
    (na, da), (nb, db) = a, b
    m = mcm_a(da, db)
    ya, yb, xf, xe = 1.2, -1.05, -5.0, -2.2
    lab = texto(f"{letra})", 32).move_to([-6.4, (ya + yb) / 2, 0])
    fa = fraccion(na, da, size=60).move_to([xf, ya, 0])
    fb = fraccion(nb, db, size=60).move_to([xf, yb, 0])
    scene.play(FadeIn(lab), Write(fa), Write(fb))
    if da == db:
        nota = texto(f"Mismo denominador: comparamos los numeradores ({na} y {nb})", 26, ACENTO).move_to([1.6, 2.2, 0])
        scene.play(FadeIn(nota), Indicate(fa[0], color=NUMERADOR, scale_factor=1.4),
                   Indicate(fb[0], color=NUMERADOR, scale_factor=1.4))
        conv = [(na, fa), (nb, fb)]
    else:
        t = MathTex(rf"\text{{m.c.m.}}({da}, {db}) = {m}", font_size=44, color=ACENTO).move_to([-3.6, 2.4, 0])
        if detalle:
            p1 = texto(f"1.º  m.c.m. de los denominadores", 24, ACENTO).move_to([2.4, 2.4, 0])
            scene.play(FadeIn(p1), Indicate(fa[2], color=DENOMINADOR), Indicate(fb[2], color=DENOMINADOR))
        scene.play(Write(t))
        if detalle:
            p2 = texto("2.º  pasamos las dos a denominador " + str(m), 24, ACENTO).move_to(p1, aligned_edge=LEFT)
            scene.play(Transform(p1, p2))
        conv = []
        for (n, d), f, y in ((a, fa, ya), (b, fb, yb)):
            k = m // d
            f2 = fraccion(n * k, m, size=60).move_to([xe, y, 0])
            scene.play(Create(flecha_op(f, f2, "x", k)))
            scene.play(TransformFromCopy(f, f2))
            if k == 1:
                ya_ = texto(f"{fr_txt(n, d)} ya tiene denominador {m}: se queda igual (×1)", 22, GREY_B)
                ya_.to_edge(DOWN, buff=0.4)
                scene.play(FadeIn(ya_))
            conv.append((n * k, f2))
        if detalle:
            p3 = texto("3.º  comparamos los numeradores", 24, ACENTO).move_to(p1, aligned_edge=LEFT)
            scene.play(Transform(p1, p3), Indicate(conv[0][1][0], color=NUMERADOR, scale_factor=1.4),
                       Indicate(conv[1][1][0], color=NUMERADOR, scale_factor=1.4))
    ka, kb = conv[0][0], conv[1][0]
    sig = ">" if ka > kb else "<" if ka < kb else "="
    items = [(na, da), sig, (nb, db)] if da == db else [(ka, m), sig, (kb, m), r"\Rightarrow", (na, da), sig, (nb, db)]
    r = cadena(*items, size=56).move_to([2.6, 0.1, 0])
    for i, it in enumerate(items):
        if it == sig:
            r[i].set_color(ACENTO)
    scene.play(Write(r), run_time=1.5)
    if sig == "=":
        eq = texto("¡Son equivalentes: representan la misma cantidad!", 26, OK).move_to([1.6, -2.2, 0])
        scene.play(FadeIn(eq))
    scene.play(Circumscribe(r[-3:], color=ACENTO))
    scene.wait(2)


# --- 5. Ordenar
def resolver_ordena(scene, fracs, creciente, letra):
    m = mcm_a(*[d for _, d in fracs])
    modo = "De menor a mayor" if creciente else "De mayor a menor"
    enun = texto(f"{letra}) {modo}", 28, ACENTO).move_to([-4.6, 2.55, 0])
    xs = [-4.4, -1.5, 1.4, 4.3]
    orig = [fraccion(n, d, size=54).move_to([x - 0.5, 1.4, 0]) for (n, d), x in zip(fracs, xs)]
    scene.play(FadeIn(enun), LaggedStart(*[Write(f) for f in orig], lag_ratio=0.15))
    t = MathTex(rf"\text{{m.c.m.}}({', '.join(str(d) for _, d in fracs)}) = {m}", font_size=38, color=ACENTO)
    t.move_to([2.6, 2.55, 0])
    scene.play(Write(t))
    for (n, d), f in zip(fracs, orig):
        k = m // d
        g = cadena("=", (n * k, m), size=44, buff=0.12).next_to(f, RIGHT, buff=0.12)
        if k > 1:
            g.add(MathTex(rf"\times {k}", font_size=24, color=ACENTO).next_to(g[1], DOWN, buff=0.06))
        scene.play(FadeIn(g), run_time=0.6)
    recta = NumberLine(x_range=[0, 1, 1 / m], length=11.5, include_tip=False, stroke_width=3,
                       tick_size=0.08).move_to([0, -1.3, 0])
    marcas = VGroup(MathTex("0", font_size=32).next_to(recta.n2p(0), DOWN, buff=0.2),
                    MathTex("1", font_size=32).next_to(recta.n2p(1), DOWN, buff=0.2))
    scene.play(Create(recta), FadeIn(marcas))
    sobre = []
    for (n, d), f in zip(fracs, orig):
        v = n / d
        dot = Dot(recta.n2p(v), radius=0.1, color=ACENTO)
        c = f.copy()
        scene.play(c.animate.scale(0.65).next_to(recta.n2p(v), UP, buff=0.25), FadeIn(dot, scale=2), run_time=0.7)
        sobre.append(c)
    orden = sorted(range(len(fracs)), key=lambda i: fracs[i][0] / fracs[i][1], reverse=not creciente)
    items = []
    for j, i in enumerate(orden):
        if j:
            items.append("<" if creciente else ">")
        items.append(fracs[i])
    fila = cadena(*items, size=50).to_edge(DOWN, buff=0.3)
    lect = texto("leemos la recta de " + ("izquierda a derecha →" if creciente else "← derecha a izquierda"), 22,
                 GREY_B).move_to([0, 0.35, 0])
    scene.play(FadeIn(lect))
    scene.play(LaggedStart(*[TransformFromCopy(sobre[i], fila[2 * j]) for j, i in enumerate(orden)], lag_ratio=0.2),
               *[FadeIn(fila[2 * j + 1]) for j in range(len(orden) - 1)], run_time=2)
    scene.play(Circumscribe(fila, color=ACENTO))
    scene.wait(2.5)


# --- 6. Problemas
def problema_dos(scene, enunciado, a, b, nombres, tipo, conclusion):
    """Compara dos fracciones de un problema con dibujos y común denominador."""
    (na, da), (nb, db) = a, b
    m = mcm_a(da, db)
    enun = texto(enunciado, 26).move_to([0, 2.45, 0])
    scene.play(Write(enun), run_time=1.5)
    xs = [-3.2, 3.2]
    filas = []
    for (n, d), nombre, x in zip((a, b), nombres, xs):
        dib = dibujo(tipo, n, d, 1.25).move_to([x - 1.1, 0.35, 0])
        f = fraccion(n, d, size=60).next_to(dib, RIGHT, buff=0.5)
        nm = texto(nombre, 26, ACENTO).next_to(dib, UP, buff=0.2)
        scene.play(FadeIn(nm), FadeIn(dib), Write(f))
        filas.append((dib, f))
    t = MathTex(rf"\text{{m.c.m.}}({da}, {db}) = {m}", font_size=42, color=ACENTO).move_to([0, -1.2, 0])
    scene.play(Write(t))
    nuevos = []
    for (n, d), (dib, f) in zip((a, b), filas):
        k = m // d
        if k > 1:
            dib2 = dibujo(tipo, n * k, m, 1.25).move_to(dib)
            f2 = fraccion(n * k, m, size=60).move_to(f)
            scene.play(ReplacementTransform(dib, dib2), Transform(f, f2), run_time=1.3)
        nuevos.append(n * k)
    sig = ">" if nuevos[0] > nuevos[1] else "<"
    r = cadena((nuevos[0], m), sig, (nuevos[1], m), r"\Rightarrow", a, sig, b, size=50).move_to([0, -2.1, 0])
    r[1].set_color(ACENTO)
    r[5].set_color(ACENTO)
    scene.play(Write(r), run_time=1.5)
    sol = texto(conclusion, 30, OK).to_edge(DOWN, buff=0.25)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_lectores(scene):
    enun = texto("Marta ha leído 2/3 de un libro, Pablo 5/6 y Sara 3/4.\nOrdénalos de quien ha leído más a quien menos.",
                 26).move_to([0, 2.45, 0])
    scene.play(Write(enun), run_time=1.5)
    m = mcm_a(*[d for _, _, d in LECTORES])
    t = MathTex(rf"\text{{m.c.m.}}(3, 6, 4) = {m}", font_size=40, color=ACENTO).move_to([4.4, 1.3, 0])
    filas = []
    for i, (nombre, n, d) in enumerate(LECTORES):
        y = 1.2 - i * 1.15
        nm = texto(nombre, 28, ACENTO).move_to([-5.6, y, 0])
        f = fraccion(n, d, size=50).move_to([-4.2, y, 0])
        b = barra(d, n, ancho=4.8, alto=0.65).move_to([-0.4, y, 0])
        scene.play(FadeIn(nm), Write(f), FadeIn(b), run_time=0.8)
        filas.append([nombre, n, d, nm, f, b, y])
    scene.play(Write(t))
    for fila in filas:
        nombre, n, d, nm, f, b, y = fila
        k = m // d
        b2 = barra(m, n * k, ancho=4.8, alto=0.65).move_to(b)
        f2 = fraccion(n * k, m, size=50).move_to(f)
        scene.play(ReplacementTransform(b, b2), Transform(f, f2), run_time=1)
        fila[5] = b2
        fila.append(n * k)
    orden = sorted(filas, key=lambda r: -r[7])
    texto_orden = "  >  ".join(f"{r[0]} ({r[7]}/{m})" for r in orden)
    sol = texto(texto_orden, 28, OK).to_edge(DOWN, buff=0.9)
    sol2 = texto(f"Ha leído más {orden[0][0]} y menos {orden[-1][0]}", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(*[Indicate(r[5], scale_factor=1.05) for r in orden])
    scene.play(Write(sol))
    scene.play(FadeIn(sol2))
    scene.wait(3)


class EjerciciosFraccionesEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Fracciones equivalentes, comparar y ordenar")
        pagina_enunciados_a(self, cab, enunciados_1_a())
        pagina_enunciados_a(self, cab, enunciados_2_a())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo_a(self, cab, "Ejercicio 1 a)")
        resolver_dibujos(self, DIBUJOS[:1], "a", ejemplo=True)
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 2 a): ¿son equivalentes?")
        resolver_cruzados(self, EQUIVALENTES[:1], "a")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 2 b): completa")
        resolver_completa(self, COMPLETA[:1], "a", ejemplo=True)
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 3 a)")
        resolver_simplifica(self, SIMPLIFICA[:1], "a", ejemplo=True)
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 4 a)")
        resolver_compara(self, *COMPARA[0], "a")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 4 b)")
        resolver_compara(self, *COMPARA[1], "b", detalle=True)
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 5 a)")
        resolver_ordena(self, *ORDENA[0], "a")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 6 a)")
        problema_dos(self, "Ana se come 3/8 de una pizza y Luis 1/4 de otra igual. ¿Quién come más?",
                     (3, 8), (1, 4), ("Ana", "Luis"), "pizza", "Ana come más pizza")
        limpiar_a(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosFraccionesResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Fracciones equivalentes, comparar y ordenar")

        subtitulo_a(self, cab, "Ejercicio 1: b), c) y d)")
        resolver_dibujos(self, DIBUJOS[1:], "bcd")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 2 a): b) y c)")
        resolver_cruzados(self, EQUIVALENTES[1:], "bc")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 2 b): b) y c)")
        resolver_completa(self, COMPLETA[1:], "bc")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 3: b), c) y d)")
        resolver_simplifica(self, SIMPLIFICA[1:], "bcd")
        limpiar_a(self, cab)
        for letra, (a, b) in zip("cde", COMPARA[2:]):
            subtitulo_a(self, cab, f"Ejercicio 4 {letra})")
            resolver_compara(self, a, b, letra)
            limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 5 b)")
        resolver_ordena(self, *ORDENA[1], "b")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 6 b)")
        problema_dos(self, "En una clase, 2/5 del alumnado va en autobús y 3/10 andando.\n¿Qué grupo es mayor?",
                     (2, 5), (3, 10), ("Autobús", "Andando"), "barra", "Son más los que van en autobús")
        limpiar_a(self, cab)
        subtitulo_a(self, cab, "Ejercicio 6 c)")
        problema_lectores(self)
        limpiar_a(self, cab)

        fin = texto("¡Muy bien! Ya sabes trabajar con fracciones equivalentes.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)


# ===========================================================================
# Antes t07_operaciones_fracciones.py
from math import gcd



ROSA = "#FF79C6"
AZUL = "#5DADE2"


def mcm(a, b):
    return a * b // gcd(a, b)


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def nota_op(f_ini, f_fin, s, color=ACENTO, size=26):
    """Etiquetas '×k' arriba y abajo entre dos fracciones."""
    g = VGroup()
    for i, lado in ((0, UP), (2, DOWN)):
        p = (f_ini[i].get_right() + f_fin[i].get_left()) / 2
        g.add(MathTex(s, font_size=size, color=color).move_to(p))
    return g


def juntar(scene, origenes, destino, inicio=0, rt=0.35):
    """Mueve copias de los trozos 'origenes' a las casillas de la barra 'destino' a partir de 'inicio'."""
    copias = []
    for k, pieza in enumerate(origenes):
        c = pieza.copy()
        scene.play(c.animate.move_to(destino[inicio + k]), run_time=rt)
        copias.append(c)
    return copias


# ---------------------------------------------------------------------------
class SumaRestaMismoDenominador(Scene):
    def construct(self):
        cab = titulo(self, "Sumar y restar fracciones", "Con el mismo denominador")

        e = cadena((2, 7), "+", (3, 7), "=", size=64).move_to([-0.6, 2.0, 0])
        self.play(Write(e))
        ancho, xb = 7.0, 1.0
        b1 = barra(7, 2, ancho=ancho, alto=0.7).move_to([xb, 0.6, 0])
        b2 = barra(7, 3, ancho=ancho, alto=0.7, color=ROSA).move_to([xb, -0.4, 0])
        br = barra(7, 0, ancho=ancho, alto=0.7).move_to([xb, -1.8, 0])
        l1 = fraccion(2, 7, 40).next_to(b1, LEFT, buff=0.5)
        l2 = fraccion(3, 7, 40).next_to(b2, LEFT, buff=0.5)
        self.play(FadeIn(b1), FadeIn(l1))
        self.play(FadeIn(b2), FadeIn(l2))
        tam = texto("Los trozos son del mismo tamaño (séptimos): solo hay que juntarlos", 24, GREY_B)
        tam.move_to([0, -1.0, 0])
        self.play(FadeIn(tam), FadeIn(br))
        juntar(self, list(b1[:2]), br, 0)
        juntar(self, list(b2[:3]), br, 2)
        res = fraccion(5, 7, 64).next_to(e, RIGHT, buff=0.3)
        lr = fraccion(5, 7, 40).next_to(br, LEFT, buff=0.5)
        self.play(Write(res), FadeIn(lr))
        regla = texto("Se suman los numeradores y se deja el mismo denominador", 28, ACENTO).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(regla), Indicate(VGroup(e[0][0], e[2][0], res[0]), color=NUMERADOR))
        self.wait(2.5)
        limpiar(self, cab)

        # Error típico
        subtitulo(self, cab, "¡Cuidado con este error!")
        mal = cadena((2, 7), "+", (3, 7), r"\neq", (5, 14), size=64).move_to([0, 1.9, 0])
        self.play(Write(mal))
        cruz = Cross(mal[4], stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        b7 = barra(7, 5, ancho=8, alto=0.6).move_to([0.9, 0.2, 0])
        b14 = barra(14, 5, ancho=8, alto=0.6).move_to([0.9, -0.8, 0])
        self.play(FadeIn(b7), FadeIn(fraccion(5, 7, 36).next_to(b7, LEFT, buff=0.4)))
        self.play(FadeIn(b14), FadeIn(fraccion(5, 14, 36).next_to(b14, LEFT, buff=0.4)))
        exp = texto("Los denominadores NO se suman: los trozos siguen siendo séptimos.\n"
                    "5/14 es mucho menos de lo que tenemos.", 26, MAL).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(exp))
        self.wait(3)
        limpiar(self, cab)

        # Resta
        subtitulo(self, cab, "Restar: quitamos trozos")
        e = cadena((5, 8), "-", (2, 8), "=", size=64).move_to([-0.6, 1.8, 0])
        b = barra(8, 5, ancho=8, alto=0.8).move_to([0.6, 0.0, 0])
        self.play(Write(e), FadeIn(b))
        self.play(*[b[i].animate.set_fill(MAL) for i in (3, 4)])
        quita = texto("quitamos 2 octavos", 24, MAL).next_to(VGroup(b[3], b[4]), DOWN, buff=0.25)
        self.play(FadeIn(quita))
        self.play(*[b[i].animate.set_fill(VACIO) for i in (3, 4)], FadeOut(quita))
        res = fraccion(3, 8, 64).next_to(e, RIGHT, buff=0.3)
        self.play(Write(res), Indicate(VGroup(*b[:3]), scale_factor=1.05))
        regla = texto("Se restan los numeradores y se deja el mismo denominador", 28, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(regla))
        self.wait(2.5)


# ---------------------------------------------------------------------------
class SumaRestaDistintoDenominador(Scene):
    def construct(self):
        cab = titulo(self, "Sumar y restar fracciones", "Con distinto denominador")
        self.suma_visual(cab)
        self.resta(cab)
        self.simplificar(cab)
        self.entero(cab)

    def suma_visual(self, cab):
        e = cadena((1, 2), "+", (1, 3), "=", size=60).move_to([-0.8, 2.3, 0])
        self.play(Write(e))
        ancho, xb = 6.0, 1.6
        b1 = barra(2, 1, ancho=ancho, alto=0.65).move_to([xb, 1.1, 0])
        b2 = barra(3, 1, ancho=ancho, alto=0.65, color=ROSA).move_to([xb, 0.2, 0])
        f1 = fraccion(1, 2, 40).move_to([-5.4, 1.1, 0])
        f2 = fraccion(1, 3, 40).move_to([-5.4, 0.2, 0])
        self.play(FadeIn(b1), FadeIn(f1), FadeIn(b2), FadeIn(f2))
        p = texto("Trozos de distinto tamaño: así no los podemos juntar", 24, MAL).move_to([0, -0.6, 0])
        self.play(FadeIn(p))
        self.wait(1)

        paso1 = texto("1.º  m.c.m. de los denominadores:", 24, ACENTO)
        m = MathTex(r"\text{m.c.m.}(2, 3) = 6", font_size=40, color=ACENTO)
        g1 = VGroup(paso1, m).arrange(RIGHT, buff=0.3).move_to([0, -0.6, 0])
        self.play(ReplacementTransform(p, g1))
        self.wait(1)
        paso2 = texto("2.º  Pasamos las dos a sextos (fracciones equivalentes)", 24, ACENTO).move_to(g1)
        self.play(ReplacementTransform(g1, paso2))
        nuevas = []
        for f, b, (n, d), col in ((f1, b1, (1, 2), ACENTO), (f2, b2, (1, 3), ROSA)):
            k = 6 // d
            f_new = fraccion(n * k, 6, 40).move_to(f.get_center() + RIGHT * 2.4)
            ops = nota_op(f, f_new, rf"\times {k}", size=24)
            b_new = barra(6, n * k, ancho=ancho, alto=0.65, color=col).move_to(b)
            self.play(FadeIn(ops), TransformFromCopy(f, f_new), ReplacementTransform(b, b_new), run_time=1.3)
            nuevas.append(b_new)
        b1, b2 = nuevas
        self.wait(0.5)
        paso3 = texto("3.º  Ya son trozos iguales: los juntamos", 24, ACENTO).move_to(paso2)
        self.play(ReplacementTransform(paso2, paso3))
        br = barra(6, 0, ancho=ancho, alto=0.65).move_to([xb, -1.5, 0])
        self.play(FadeIn(br))
        juntar(self, list(b1[:3]), br, 0)
        juntar(self, list(b2[:2]), br, 3)
        res = fraccion(5, 6, 60).next_to(e, RIGHT, buff=0.3)
        self.play(Write(res), FadeIn(fraccion(5, 6, 40).move_to([-3.0, -1.5, 0])))
        cuenta = cadena((1, 2), "+", (1, 3), "=", (3, 6), "+", (2, 6), "=", (5, 6), size=44).to_edge(DOWN, buff=0.3)
        self.play(Write(cuenta))
        self.wait(3)
        limpiar(self, cab)

    def lineas(self, filas, x=-5.8, y0=1.7, dy=1.25, size=56):
        objs = []
        for i, items in enumerate(filas):
            l = cadena(*items, size=size).move_to([x, y0 - i * dy, 0], aligned_edge=LEFT)
            self.play(Write(l), run_time=1.2)
            objs.append(l)
        return objs

    def resta(self, cab):
        subtitulo(self, cab, "Restar: igual, pero quitando")
        filas = self.lineas([[(3, 4), "-", (1, 6)]])
        m = MathTex(r"\text{m.c.m.}(4, 6) = 12", font_size=40, color=ACENTO).move_to([2.8, 1.7, 0])
        self.play(Write(m))
        filas += self.lineas([["=", (9, 12), "-", (2, 12)], ["=", (7, 12)]], y0=0.45)
        n = texto("3/4 = 9/12  (×3)      1/6 = 2/12  (×2)", 22, GREY_B).next_to(filas[1], RIGHT, buff=0.6)
        self.play(FadeIn(n))
        self.play(Circumscribe(filas[2][1], color=ACENTO))
        self.wait(2.5)
        limpiar(self, cab)

    def simplificar(self, cab):
        subtitulo(self, cab, "Al final, simplificamos si se puede")
        filas = self.lineas([[(1, 4), "+", (1, 12)], ["=", (3, 12), "+", (1, 12)], ["=", (4, 12)]], dy=1.15)
        f2 = cadena("=", (1, 3), size=56).next_to(filas[2], RIGHT, buff=0.3)
        mcd = texto("dividimos arriba y abajo\npor el M.C.D.(4, 12) = 4", 24, ACENTO).next_to(f2, RIGHT, buff=0.7)
        self.play(Write(mcd))
        self.play(Write(f2))
        irr = texto("1/3 es irreducible: el resultado se da siempre simplificado", 26, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(irr), Circumscribe(f2[1], color=ACENTO))
        self.wait(2.5)
        limpiar(self, cab)

    def entero(self, cab):
        subtitulo(self, cab, "Un número entero más una fracción")
        e = cadena("2", "+", (1, 3), "=", size=64).move_to([-1.0, 1.5, 0])
        self.play(Write(e))
        bs = VGroup(barra(3, 3, ancho=3, alto=0.7), barra(3, 3, ancho=3, alto=0.7),
                    barra(3, 1, ancho=3, alto=0.7, color=ROSA)).arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        self.play(FadeIn(bs[0]), FadeIn(bs[1]))
        dos = texto("2 unidades = 6 tercios", 26, ACENTO).next_to(VGroup(bs[0], bs[1]), DOWN, buff=0.3)
        self.play(FadeIn(dos))
        self.play(FadeIn(bs[2]), FadeIn(fraccion(1, 3, 36).next_to(bs[2], DOWN, buff=0.3)))
        l = cadena("2", "+", (1, 3), "=", (6, 3), "+", (1, 3), "=", (7, 3), size=52).move_to([0, -1.7, 0])
        self.play(Write(l))
        truco = texto("El entero se escribe con el mismo denominador: 2 = 6/3", 26, GREY_B).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(truco), Write(fraccion(7, 3, 64).next_to(e, RIGHT, buff=0.3)))
        self.wait(3)


# ---------------------------------------------------------------------------
class FraccionDeUnaCantidad(Scene):
    def construct(self):
        cab = titulo(self, "Fracción de una cantidad", "¿Cuánto son 3/4 de 20?")
        caramelos = VGroup(*[Circle(radius=0.17, color=ROSA, fill_color=ROSA, fill_opacity=0.85) for _ in range(20)])
        caramelos.arrange(RIGHT, buff=0.15).move_to([0, 1.6, 0])
        t = texto("Tenemos 20 caramelos", 28).next_to(caramelos, UP, buff=0.3)
        self.play(FadeIn(t), LaggedStart(*[GrowFromCenter(c) for c in caramelos], lag_ratio=0.04))
        self.wait(0.5)

        # Paso 1: repartir en 4 grupos
        grupos = VGroup(*[VGroup(*caramelos[5 * g:5 * g + 5]) for g in range(4)])
        destino = VGroup(*[VGroup(*[c.copy() for c in gr]).arrange(DOWN, buff=0.12) for gr in grupos])
        destino.arrange(RIGHT, buff=1.0).move_to([-2.0, -0.4, 0])
        p1 = texto("1.º  El denominador (4) dice en cuántos grupos iguales repartimos", 24, DENOMINADOR)
        p1.move_to([0, 2.65, 0])
        self.play(FadeOut(t), FadeIn(p1))
        self.play(*[c.animate.move_to(d) for gr, dg in zip(grupos, destino) for c, d in zip(gr, dg)], run_time=1.5)
        cajas = VGroup(*[SurroundingRectangle(gr, color=GREY_B, buff=0.12) for gr in grupos])
        self.play(Create(cajas))
        c1 = MathTex("20 : 4 = 5", font_size=48, color=DENOMINADOR).move_to([4.2, 0.6, 0])
        c1n = texto("caramelos en cada grupo", 22, GREY_B).next_to(c1, DOWN, buff=0.15)
        self.play(Write(c1), FadeIn(c1n))
        self.wait(1)

        # Paso 2: tomar 3 grupos
        p2 = texto("2.º  El numerador (3) dice cuántos grupos tomamos", 24, NUMERADOR).move_to(p1)
        self.play(ReplacementTransform(p1, p2))
        self.play(*[cajas[g].animate.set_stroke(ACENTO, 5) for g in range(3)],
                  *[c.animate.set_fill(ACENTO) .set_stroke(ACENTO) for g in range(3) for c in grupos[g]])
        c2 = MathTex(r"5 \cdot 3 = 15", font_size=48, color=NUMERADOR).move_to([4.2, -0.9, 0])
        self.play(Write(c2))
        res = VGroup(fraccion(3, 4, 56), MathTex(r"\text{de } 20 = 15", font_size=56)).arrange(RIGHT, buff=0.25)
        res.to_edge(DOWN, buff=0.5)
        self.play(Write(res), Circumscribe(res, color=ACENTO))
        regla = texto("Dividimos por el denominador y multiplicamos por el numerador", 26, ACENTO)
        regla.next_to(res, UP, buff=0.3)
        self.play(FadeIn(regla))
        self.wait(3)
        limpiar(self, cab)

        # Dinero
        subtitulo(self, cab, "Otro ejemplo: 2/5 de 30 €")
        b = barra(5, 0, ancho=10, alto=0.9).move_to([0, 0.8, 0])
        llave = Brace(b, UP)
        total = texto("30 €", 30).next_to(llave, UP, buff=0.1)
        self.play(FadeIn(b), GrowFromCenter(llave), FadeIn(total))
        c1 = MathTex(r"30 : 5 = 6", font_size=48, color=DENOMINADOR).move_to([-3.0, -0.8, 0])
        self.play(Write(c1))
        seis = VGroup(*[Text("6 €", font_size=26).move_to(p) for p in b])
        self.play(LaggedStart(*[FadeIn(s) for s in seis], lag_ratio=0.15))
        self.play(*[b[i].animate.set_fill(ACENTO) for i in range(2)], *[seis[i].animate.set_color(BLACK) for i in range(2)])
        c2 = MathTex(r"6 \cdot 2 = 12", font_size=48, color=NUMERADOR).move_to([3.0, -0.8, 0])
        self.play(Write(c2))
        res = VGroup(fraccion(2, 5, 56), Text("de 30 € = 12 €", font_size=40)).arrange(RIGHT, buff=0.25)
        res.to_edge(DOWN, buff=0.6)
        self.play(Write(res), Circumscribe(res, color=ACENTO))
        self.wait(3)


# ---------------------------------------------------------------------------
class MultiplicarFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicar fracciones", "El truco del rectángulo")
        lado, c0 = 4.2, np.array([-3.4, -0.4, 0])
        cuadro = Square(lado, stroke_color=WHITE, fill_color=VACIO, fill_opacity=1).move_to(c0)
        e = cadena((2, 3), r"\cdot", (4, 5), "=", size=64).move_to([3.0, 2.0, 0])
        self.play(Write(e), FadeIn(cuadro))
        izq, arr = cuadro.get_left()[0], cuadro.get_top()[1]

        # 2/3: columnas
        cols = VGroup(*[Line([izq + lado * k / 3, arr, 0], [izq + lado * k / 3, arr - lado, 0], stroke_width=2)
                        for k in (1, 2)])
        f_col = Rectangle(width=lado * 2 / 3, height=lado, stroke_width=0, fill_color=AZUL, fill_opacity=0.45)
        f_col.move_to([izq + lado / 3, c0[1], 0])
        t1 = VGroup(fraccion(2, 3, 36), texto("de las columnas", 24, AZUL)).arrange(RIGHT, buff=0.2)
        t1.next_to(cuadro, UP, buff=0.3)
        self.play(Create(cols), Indicate(e[0], color=AZUL))
        self.play(FadeIn(f_col), FadeIn(t1))
        self.wait(0.6)

        # 4/5: filas
        filas = VGroup(*[Line([izq, arr - lado * k / 5, 0], [izq + lado, arr - lado * k / 5, 0], stroke_width=2)
                         for k in range(1, 5)])
        f_fil = Rectangle(width=lado, height=lado * 4 / 5, stroke_width=0, fill_color=ACENTO, fill_opacity=0.35)
        f_fil.move_to([c0[0], arr - lado * 2 / 5, 0])
        t2 = VGroup(fraccion(4, 5, 36), texto("de las filas", 24, ACENTO)).arrange(RIGHT, buff=0.2)
        t2.next_to(cuadro, DOWN, buff=0.3)
        self.play(Create(filas), Indicate(e[2], color=ACENTO))
        self.play(FadeIn(f_fil), FadeIn(t2))
        self.wait(0.6)

        # Cruce
        w, h = lado / 3, lado / 5
        celdas = VGroup(*[Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=2, fill_color=VERDE_CRUCE,
                                    fill_opacity=0.95).move_to([izq + w * (c + 0.5), arr - h * (r + 0.5), 0])
                          for r in range(4) for c in range(2)])
        cruce = texto("Donde se cruzan: 8 cuadraditos", 26, VERDE_CRUCE).move_to([3.0, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in celdas], lag_ratio=0.1), FadeIn(cruce))
        total = texto("En total hay 3 · 5 = 15 cuadraditos", 26, GREY_B).next_to(cruce, DOWN, buff=0.3)
        self.play(FadeIn(total))
        res = fraccion(8, 15, 64).next_to(e, RIGHT, buff=0.3)
        self.play(Write(res))
        formula = MathTex(r"\frac{2}{3}\cdot\frac{4}{5}=\frac{2\cdot 4}{3\cdot 5}=\frac{8}{15}", font_size=52)
        formula.move_to([3.0, -1.4, 0])
        self.play(Write(formula))
        regla = texto("Numerador por numerador\ny denominador por denominador", 28, ACENTO).move_to([3.0, -2.8, 0])
        self.play(FadeIn(regla))
        self.wait(3)
        limpiar(self, cab)

        # «de» = por, y simplificar
        subtitulo(self, cab, "Más ejemplos")
        l1 = VGroup(texto("«2/3 de 4/5» es lo mismo que", 30), cadena((2, 3), r"\cdot", (4, 5), size=52))
        l1.arrange(RIGHT, buff=0.3).move_to([0, 1.8, 0])
        self.play(FadeIn(l1))
        l2 = cadena((3, 4), r"\cdot", (2, 9), "=", (6, 36), "=", (1, 6), size=52).move_to([0, 0.3, 0])
        self.play(Write(l2))
        n2 = texto("simplificamos al final (M.C.D. = 6)", 22, GREY_B).next_to(l2, DOWN, buff=0.2)
        self.play(FadeIn(n2))
        l3 = cadena("3", r"\cdot", (2, 5), "=", (3, 1), r"\cdot", (2, 5), "=", (6, 5), size=52).move_to([0, -1.6, 0])
        self.play(Write(l3))
        n3 = texto("un entero es una fracción con denominador 1", 22, GREY_B).next_to(l3, DOWN, buff=0.2)
        self.play(FadeIn(n3))
        self.wait(3)


VERDE_CRUCE = "#58D68D"


# ---------------------------------------------------------------------------
class DividirFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Dividir fracciones", "¿Cuántas veces cabe?")
        e = cadena((3, 4), ":", (1, 8), "=", size=64).move_to([-0.6, 2.2, 0])
        q = texto("¿Cuántos octavos caben en 3/4?", 30, ACENTO).move_to([0, 1.2, 0])
        self.play(Write(e), FadeIn(q))
        ancho = 10.0
        b4 = barra(4, 3, ancho=ancho, alto=0.8).move_to([0, 0.0, 0])
        b8 = barra(8, 0, ancho=ancho, alto=0.8).move_to([0, -1.1, 0])
        self.play(FadeIn(b4), FadeIn(fraccion(3, 4, 32).next_to(b4, LEFT, buff=0.25)))
        self.play(FadeIn(b8), FadeIn(fraccion(1, 8, 32).next_to(b8, LEFT, buff=0.25)))
        guia = DashedLine(b4[2].get_corner(UR) + UP * 0.1, b8[5].get_corner(DR) + DOWN * 0.1, color=ACENTO)
        self.play(Create(guia))
        nums = VGroup()
        for k in range(6):
            n = MathTex(str(k + 1), font_size=36, color=BLACK).move_to(b8[k])
            self.play(b8[k].animate.set_fill(ROSA), FadeIn(n), run_time=0.35)
            nums.add(n)
        r = MathTex("6", font_size=64, color=ACENTO).next_to(e, RIGHT, buff=0.3)
        self.play(Write(r), FadeIn(texto("¡Caben 6!", 30, ACENTO).to_edge(DOWN, buff=0.6)))
        self.wait(2.5)
        limpiar(self, cab)

        # La inversa
        subtitulo(self, cab, "La fracción inversa: le damos la vuelta")
        ejemplos = [(1, 8), (2, 3), (5, 1)]
        xs = [-4.0, 0.0, 4.0]
        for (n, d), x in zip(ejemplos, xs):
            f = fraccion(n, d, 72).move_to([x, 0.8, 0])
            self.play(Write(f), run_time=0.7)
            self.play(Swap(f[0], f[2]), run_time=1.0)
            self.play(f[0].animate.set_color(NUMERADOR), f[2].animate.set_color(DENOMINADOR), run_time=0.3)
            if d == 1:
                nota = texto("5 = 5/1  →  1/5", 24, GREY_B).next_to(f, DOWN, buff=0.4)
            else:
                nota = texto(f"{n}/{d}  →  {d}/{n}", 24, GREY_B).next_to(f, DOWN, buff=0.4)
            self.play(FadeIn(nota))
        self.wait(2)
        limpiar(self, cab)

        # Regla
        subtitulo(self, cab, "Dividir es multiplicar por la inversa")
        regla = MathTex(r"\frac{a}{b} : \frac{c}{d} = \frac{a}{b}\cdot\frac{d}{c}", font_size=64, color=ACENTO)
        regla.move_to([0, 1.9, 0])
        self.play(Write(regla))
        l1 = cadena((3, 4), ":", (1, 8), "=", (3, 4), r"\cdot", (8, 1), "=", (24, 4), "=", "6", size=52).move_to([0, 0.3, 0])
        self.play(Write(l1), run_time=2)
        ok = texto("¡Igual que en el dibujo! ✓", 26, OK).next_to(l1, DOWN, buff=0.2)
        self.play(FadeIn(ok))
        l2 = cadena((2, 3), ":", (4, 5), "=", (2, 3), r"\cdot", (5, 4), "=", (10, 12), "=", (5, 6), size=52)
        l2.move_to([0, -1.6, 0])
        self.play(Write(l2), run_time=2)
        n2 = texto("y simplificamos al final", 22, GREY_B).next_to(l2, DOWN, buff=0.2)
        self.play(FadeIn(n2), Circumscribe(l2[-1], color=ACENTO))
        self.wait(3)


# ---------------------------------------------------------------------------
def orden_ops(size=22):
    """Recuadro pequeño con el orden de las operaciones (como en el tema 10)."""
    filas = VGroup(*[texto(t, size, c) for t, c in (("1.º Paréntesis", "#FF79C6"), ("2.º Potencias", "#5DADE2"),
                                                       ("3.º · y :  (izq. → dcha.)", "#FF9F43"),
                                                       ("4.º + y −  (izq. → dcha.)", "#7BD88F"))])
    filas.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    caja = SurroundingRectangle(filas, color=GREY_B, buff=0.2, corner_radius=0.1, stroke_width=2)
    return VGroup(caja, filas)


def paso_comb(scene, fila_ant, idx, lado, nueva, nota, x=-6.4, y=None):
    """Marca con caja amarilla los trozos idx de fila_ant, hace la cuenta 'lado' a la derecha y escribe 'nueva' debajo."""
    caja = SurroundingRectangle(VGroup(*[fila_ant[i] for i in idx]), color=ACENTO, buff=0.1, stroke_width=3)
    n = texto(nota, 26, ACENTO).to_edge(DOWN, buff=0.35)
    scene.play(Create(caja), FadeIn(n))
    lado.next_to(fila_ant, RIGHT, buff=0.9)
    if lado.get_right()[0] > 6.9:
        lado.scale_to_fit_width(6.9 - lado.get_left()[0])
    lado.set_color(ACENTO)
    flecha = Arrow(fila_ant.get_right(), lado.get_left(), buff=0.1, color=ACENTO, stroke_width=3,
                   max_tip_length_to_length_ratio=0.25)
    scene.play(GrowArrow(flecha), Write(lado), run_time=1.3)
    scene.wait(1.2)
    nueva.next_to(fila_ant, DOWN, buff=0.45).align_to([x, 0, 0], LEFT)
    scene.play(Write(nueva), FadeOut(n), run_time=1.2)
    scene.wait(0.8)
    return caja, flecha


class OperacionesCombinadas(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones combinadas", "con fracciones")
        orden = orden_ops().to_corner(UR, buff=0.3)
        intro = texto("El orden es el mismo que con los números enteros", 28, ACENTO).move_to([0, 0.3, 0])
        self.play(FadeIn(intro))
        self.play(FadeIn(orden, shift=LEFT * 0.3))
        self.wait(2)
        self.play(FadeOut(intro))

        # Ejemplo 1: sin paréntesis
        f1 = cadena((1, 2), "+", (3, 4), r"\cdot", (2, 3), size=52).move_to([0, 1.3, 0]).align_to([-6.4, 0, 0], LEFT)
        self.play(Write(f1))
        lado = cadena((3, 4), r"\cdot", (2, 3), "=", (6, 12), "=", (1, 2), size=40, buff=0.2)
        f2 = cadena("=", (1, 2), "+", (1, 2), size=52)
        paso_comb(self, f1, [2, 3, 4], lado, f2, "1.º la multiplicación (va antes que la suma)")
        f3 = cadena("=", (2, 2), "=", "1", size=52)
        caja = SurroundingRectangle(f2[1:], color=ACENTO, buff=0.1, stroke_width=3)
        n = texto("2.º la suma: mismo denominador", 26, ACENTO).to_edge(DOWN, buff=0.35)
        self.play(Create(caja), FadeIn(n))
        f3.next_to(f2, DOWN, buff=0.45).align_to([-6.4, 0, 0], LEFT)
        self.play(Write(f3), FadeOut(n))
        self.play(Circumscribe(f3[-1], color=ACENTO))
        self.wait(2)

        # El error típico
        mal = VGroup(texto("Si sumamos primero:", 24, MAL),
                     cadena((5, 4), r"\cdot", (2, 3), "=", (10, 12), "=", (5, 6), size=36, buff=0.2))
        mal.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(mal))
        cruz = Cross(mal[1][-1], stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        self.play(FadeIn(texto("¡Otro resultado! Por eso hay que respetar el orden", 24, MAL).next_to(mal, UP, buff=0.2)))
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (cab, orden)])

        # Ejemplo 2: con paréntesis
        f1 = cadena("(", (2, 3), "-", (1, 4), ")", r"\cdot", (6, 5), size=52).move_to([0, 1.3, 0]).align_to([-6.4, 0, 0], LEFT)
        self.play(Write(f1))
        lado = cadena((8, 12), "-", (3, 12), "=", (5, 12), size=40, buff=0.2)
        f2 = cadena("=", (5, 12), r"\cdot", (6, 5), size=52)
        paso_comb(self, f1, [0, 1, 2, 3, 4], lado, f2, "1.º el paréntesis: m.c.m.(3, 4) = 12")
        lado2 = cadena((5, 12), r"\cdot", (6, 5), "=", (30, 60), "=", (1, 2), size=40, buff=0.2)
        f3 = cadena("=", (1, 2), size=52)
        paso_comb(self, f2, [1, 2, 3], lado2, f3, "2.º la multiplicación y simplificamos")
        self.play(Circumscribe(f3[-1], color=ACENTO))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (cab, orden)])

        # Ejemplo 3: entero, división y resta
        f1 = cadena("2", "-", (1, 3), ":", (2, 9), "+", (1, 2), size=52).move_to([0, 1.3, 0]).align_to([-6.4, 0, 0], LEFT)
        self.play(Write(f1))
        lado = cadena((1, 3), r"\cdot", (9, 2), "=", (9, 6), "=", (3, 2), size=40, buff=0.2)
        f2 = cadena("=", "2", "-", (3, 2), "+", (1, 2), size=52)
        paso_comb(self, f1, [2, 3, 4], lado, f2, "1.º la división: multiplicamos por la inversa")
        lado2 = cadena((4, 2), "-", (3, 2), "+", (1, 2), "=", (2, 2), size=40, buff=0.2)
        f3 = cadena("=", (2, 2), "=", "1", size=52)
        paso_comb(self, f2, [1, 2, 3, 4, 5], lado2, f3, "2.º sumas y restas de izquierda a derecha (2 = 4/2)")
        self.play(Circumscribe(f3[-1], color=ACENTO))
        resumen = texto("Primero se decide QUÉ toca y después se opera como siempre", 26, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(resumen))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
from fractions import Fraction  # noqa: E402

# Las operaciones se escriben como (a, op, b): a y b son enteros o tuplas (n, d); op es "+", "-", "x" o ":".
MISMO_DEN = [((3, 8), "+", (2, 8)), ((7, 9), "-", (4, 9)), ((2, 5), "+", (4, 5)), ((5, 6), "-", (1, 6))]
DISTINTO_DEN = [((1, 2), "+", (1, 4)), ((2, 3), "+", (1, 6)), ((3, 4), "-", (2, 3)),
                ((5, 6), "+", (3, 8)), (1, "-", (3, 5)), (2, "+", (3, 4))]
DE_CANTIDAD = [(2, 3, 18), (3, 5, 40), (5, 8, 72), (3, 10, 250)]
MULTIPLICA = [((2, 5), "x", (3, 7)), ((4, 9), "x", (3, 8)), (5, "x", (2, 15)), ((6, 5), "x", (10, 3))]
DIVIDE = [((3, 5), ":", (2, 7)), ((4, 9), ":", (2, 3)), (6, ":", (3, 4)), ((5, 8), ":", 10)]
PROBLEMAS = [
    "a) Un depósito de 60 L está lleno en sus 3/4 partes. ¿Cuántos litros tiene?",
    "b) Juan se come 1/3 de una pizza y Marta 1/4.\n"
    "     ¿Qué fracción se comen entre los dos? ¿Cuánta pizza queda?",
    "c) ¿Cuántos vasos de 1/4 L se llenan con una botella de 3/2 L?",
    "d) Laura tiene 30 €. Gasta 2/5 en un libro y 1/3 de lo que le queda en el cine.\n"
    "     ¿Cuánto dinero le queda?",
]

SIMB_TEX = {"+": "+", "-": "-", "x": r"\cdot", ":": ":"}
SIMB_TXT = {"+": "+", "-": MENOS, "x": "·", ":": ":"}


def como_frac(x):
    """Entero -> (x, 1); tupla -> la misma tupla."""
    return (x, 1) if isinstance(x, int) else x


def item(x):
    """Lo que se dibuja: los enteros como número, las fracciones como fracción."""
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else (x.numerator, x.denominator)
    return str(x) if isinstance(x, int) else x


def op_txt(a, op, b):
    def t(x):
        return str(x) if isinstance(x, int) else f"{x[0]}/{x[1]}"
    return f"{t(a)} {SIMB_TXT[op]} {t(b)}"


def pasos_op(a, op, b, ejemplo=False):
    """Pasos de 'a op b': lista de (elementos de la cadena, nota). Los resultados salen de Fraction."""
    (na, da), (nb, db) = como_frac(a), como_frac(b)
    segs = [([item(a), SIMB_TEX[op], item(b)], None)]
    if op in "+-":
        signo = 1 if op == "+" else -1
        verbo = "suman" if op == "+" else "restan"
        if da == db:
            raw = (na + signo * nb, da)
            segs.append((["=", raw], f"Mismo denominador: se {verbo} los numeradores y se deja el {da}"))
        else:
            m = mcm(da, db)
            a2, b2 = (na * m // da, m), (nb * m // db, m)
            if isinstance(a, int):
                nota = f"El entero con denominador {m}: {a} = {a2[0]}/{m}"
            elif ejemplo:
                nota = f"1.º m.c.m.({da}, {db}) = {m}: pasamos las dos a denominador {m}"
            else:
                nota = f"m.c.m.({da}, {db}) = {m}"
            segs.append((["=", a2, SIMB_TEX[op], b2], nota))
            raw = (a2[0] + signo * b2[0], m)
            segs.append((["=", raw], ("2.º " if ejemplo else "") + f"Mismo denominador: se {verbo} los numeradores"))
    else:
        A = (na, da)
        B = (nb, db) if op == "x" else (db, nb)
        if op == "x" and (isinstance(a, int) or isinstance(b, int)):
            segs.append((["=", A, r"\cdot", B], "Un entero es una fracción con denominador 1"))
        if op == ":":
            nota = f"La inversa de {nb}/{db} es {db}/{nb}" if db != 1 else f"La inversa de {nb} es 1/{nb}"
            segs.append((["=", A, r"\cdot", B], "Dividir es multiplicar por la inversa. " + nota))
        segs.append((["=", (rf"{A[0]} \cdot {B[0]}", rf"{A[1]} \cdot {B[1]}")],
                     "Numerador por numerador y denominador por denominador"))
        raw = (A[0] * B[0], A[1] * B[1])
        segs.append((["=", raw], None))
    r = Fraction(*raw)
    if (r.numerator, r.denominator) != raw:
        segs.append((["=", item(r)], f"Simplificamos: M.C.D.({raw[0]}, {raw[1]}) = {gcd(*raw)}"))
    return segs


def resolver_cadena(scene, segs, etiqueta, y, x=-6.5, size=50, ejemplo=False, ancho_max=13.0):
    """Escribe la cadena de pasos de izquierda a derecha, con la nota de cada paso abajo."""
    elementos = [e for s, _ in segs for e in s]
    fila = cadena(*elementos, size=size)
    partes = [texto(etiqueta, 30)] if etiqueta else []
    grupo = VGroup(*partes, fila).arrange(RIGHT, buff=0.4)
    if grupo.width > ancho_max:
        grupo.scale_to_fit_width(ancho_max)
    grupo.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    k, nota_vieja = 0, None
    for i, (s, nota) in enumerate(segs):
        trozo = fila[k:k + len(s)]
        k += len(s)
        anims = [Write(trozo)]
        if i == 0 and partes:
            anims.append(FadeIn(partes[0]))
        if nota_vieja:
            anims.append(FadeOut(nota_vieja))
            nota_vieja = None
        if nota:
            nota_vieja = texto(nota, 28 if ejemplo else 24, ACENTO).to_edge(DOWN, buff=0.4)
            anims.append(FadeIn(nota_vieja))
        scene.play(*anims, run_time=1.2 if ejemplo else 0.9)
        scene.wait(1.6 if ejemplo else 0.7)
    if nota_vieja:
        scene.play(FadeOut(nota_vieja))
    scene.play(Circumscribe(fila[-1], color=ACENTO))
    return grupo


def resolver_ops(scene, ops, letras, ejemplo=False):
    """Varias operaciones en filas (1, 2 o 3 por pantalla)."""
    ys = {1: [0.6], 2: [1.2, -1.1], 3: [1.7, 0.0, -1.7]}[len(ops)]
    for (a, op, b), l, y in zip(ops, letras, ys):
        resolver_cadena(scene, pasos_op(a, op, b, ejemplo), f"{l})", y, size=60 if ejemplo else 50, ejemplo=ejemplo)
    scene.wait(1.5)


def resolver_cantidad(scene, n, d, total, etiqueta, y, unidad="", ejemplo=False):
    """«n/d de total» con una barra de d partes: total : d en cada parte y tomamos n partes."""
    parte = total // d
    res = parte * n
    u = rf"\text{{ {unidad}}}" if unidad else ""
    frac = fraccion(n, d, 44)
    lab = VGroup(*([texto(etiqueta, 30)] if etiqueta else []), frac,
                 MathTex(rf"\text{{de }} {total}" + u, font_size=44)).arrange(RIGHT, buff=0.2)
    lab.move_to([-4.9, y, 0])
    b = barra(d, 0, ancho=5.0, alto=0.7).move_to([0.8, y, 0])
    llave = Brace(b, UP, buff=0.08)
    tot = MathTex(str(total) + u, font_size=30).next_to(llave, UP, buff=0.05)
    scene.play(FadeIn(lab), FadeIn(b), GrowFromCenter(llave), FadeIn(tot))
    nota = None
    if ejemplo:
        nota = texto(f"1.º Dividimos entre el denominador: {d} partes iguales", 28, DENOMINADOR)
        nota.to_edge(DOWN, buff=0.4)
        scene.play(FadeIn(nota), Indicate(frac[2], color=DENOMINADOR, scale_factor=1.4))
    c1 = MathTex(f"{total} : {d} = {parte}", font_size=38, color=DENOMINADOR).move_to([5.5, y + 0.35, 0])
    vals = VGroup(*[MathTex(str(parte), font_size=26 if d <= 8 else 20).move_to(p) for p in b])
    scene.play(Write(c1))
    scene.play(LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.08))
    if ejemplo:
        scene.wait(1)
        nota2 = texto(f"2.º Multiplicamos por el numerador: tomamos {n} partes", 28, NUMERADOR)
        nota2.to_edge(DOWN, buff=0.4)
        scene.play(ReplacementTransform(nota, nota2), Indicate(frac[0], color=NUMERADOR, scale_factor=1.4))
        nota = nota2
    c2 = MathTex(rf"{parte} \cdot {n} = {res}", font_size=38, color=NUMERADOR).move_to([5.5, y - 0.35, 0])
    scene.play(*[b[i].animate.set_fill(ACENTO) for i in range(n)],
               *[vals[i].animate.set_color(BLACK) for i in range(n)], Write(c2))
    r = MathTex(rf"= {res}" + u, font_size=48, color=ACENTO).next_to(lab, DOWN, buff=0.25).align_to(frac, LEFT)
    scene.play(Write(r), Circumscribe(r, color=ACENTO))
    scene.wait(1.5 if ejemplo else 0.8)
    if nota:
        scene.play(FadeOut(nota))


def resolver_cantidades(scene, items, letras):
    ys = {1: [0.4], 2: [1.2, -1.3], 3: [1.6, -0.35, -2.3]}[len(items)]
    for (n, d, total), l, y in zip(items, letras, ys):
        resolver_cantidad(scene, n, d, total, f"{l})", y)
    scene.wait(1.5)


def pagina_enunciados(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 28, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cab, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def lista_ops(ops, por_linea=4):
    trozos = [f"{l}) {op_txt(*o)}" for l, o in zip("abcdef", ops)]
    return "\n".join("     ".join(trozos[i:i + por_linea]) for i in range(0, len(trozos), por_linea))


def enunciados_1():
    return [
        ("1. Suma o resta (mismo denominador) y simplifica:", lista_ops(MISMO_DEN)),
        ("2. Suma o resta (distinto denominador) y simplifica:", lista_ops(DISTINTO_DEN, 3)),
        ("3. Calcula:", "     ".join(f"{l}) {n}/{d} de {t}" for l, (n, d, t) in zip("abcd", DE_CANTIDAD))),
    ]


def enunciados_2():
    return [
        ("4. Multiplica y simplifica:", lista_ops(MULTIPLICA)),
        ("5. Divide y simplifica:", lista_ops(DIVIDE)),
        ("6. Problemas:", "\n".join(PROBLEMAS)),
    ]


# --- 6. Problemas
def enunciado(scene, i):
    e = texto(PROBLEMAS[i][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    return e


def problema_deposito(scene):
    enunciado(scene, 0)
    resolver_cantidad(scene, 3, 4, 60, "", 0.2, unidad="L", ejemplo=True)
    sol = texto("El depósito tiene 45 litros", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_pizza(scene):
    enunciado(scene, 1)
    p = pizza(12, 0, r=1.35).move_to([-5.2, -0.2, 0])
    scene.play(FadeIn(p))
    resolver_cadena(scene, pasos_op((1, 3), "+", (1, 4)), "Comen:", 0.8, x=-3.3, size=46, ancho_max=10)
    nj = texto("Juan: 4/12", 24, ACENTO).next_to(p, DOWN, buff=0.25)
    nm = texto("Marta: 3/12", 24, ROSA).next_to(nj, DOWN, buff=0.12)
    scene.play(*[p[i].animate.set_fill(ACENTO) for i in range(4)], FadeIn(nj))
    scene.play(*[p[i].animate.set_fill(ROSA) for i in range(4, 7)], FadeIn(nm))
    resolver_cadena(scene, pasos_op(1, "-", (7, 12)), "Queda:", -1.1, x=-3.3, size=46, ancho_max=10)
    scene.play(LaggedStart(*[Indicate(p[i], scale_factor=1.1) for i in range(7, 12)], lag_ratio=0.1))
    sol = texto("Se comen 7/12 de la pizza y queda 5/12", 30, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_vasos(scene):
    enunciado(scene, 2)
    resolver_cadena(scene, pasos_op((3, 2), ":", (1, 4)), "", 1.0, x=-4.5, size=50)
    bs = VGroup(barra(4, 4, ancho=4.0, alto=0.75), barra(4, 2, ancho=4.0, alto=0.75)).arrange(RIGHT, buff=0.5)
    bs.move_to([0, -1.0, 0])
    litros = VGroup(*[texto("1 L", 22, GREY_B).next_to(b, DOWN, buff=0.15) for b in bs])
    bot = texto("3/2 L = una botella y media", 24, GREY_B).next_to(bs, UP, buff=0.2)
    scene.play(FadeIn(bs), FadeIn(litros), FadeIn(bot))
    trozos = list(bs[0]) + list(bs[1][:2])
    nums = VGroup(*[MathTex(str(i + 1), font_size=34, color=BLACK).move_to(t) for i, t in enumerate(trozos)])
    scene.play(LaggedStart(*[FadeIn(n, scale=1.5) for n in nums], lag_ratio=0.2))
    sol = texto("Cada trozo es un vaso de 1/4 L: se llenan 6 vasos", 30, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_laura(scene):
    enunciado(scene, 3)
    b = barra(5, 0, ancho=10, alto=0.8).move_to([0, 0.85, 0])
    llave = Brace(b, UP, buff=0.08)
    tot = texto("30 €", 26).next_to(llave, UP, buff=0.05)
    seis = VGroup(*[texto("6 €", 24).move_to(p) for p in b])
    scene.play(FadeIn(b), GrowFromCenter(llave), FadeIn(tot))
    scene.play(LaggedStart(*[FadeIn(s) for s in seis], lag_ratio=0.15))
    l1 = texto("Libro: 2/5 de 30 € = 12 €   →   le quedan 30 − 12 = 18 €", 28).move_to([0, -0.9, 0])
    scene.play(*[b[i].animate.set_fill(ACENTO) for i in range(2)], *[seis[i].animate.set_color(BLACK) for i in range(2)],
               FadeIn(l1))
    queda = Brace(VGroup(*b[2:]), DOWN, buff=0.08, color=GREY_B)
    tq = texto("quedan 18 €", 22, GREY_B).next_to(queda, DOWN, buff=0.05)
    scene.play(GrowFromCenter(queda), FadeIn(tq))
    scene.wait(1)
    trampa = texto("¡Ojo! Es 1/3 de lo que le queda (18 €), no de los 30 €", 24, ACENTO).move_to([0, -1.6, 0])
    scene.play(FadeIn(trampa))
    scene.wait(1.5)
    l2 = texto("Cine: 1/3 de 18 € = 6 €", 28).move_to([0, -1.6, 0])
    scene.play(ReplacementTransform(trampa, l2), b[2].animate.set_fill(ROSA), seis[2].animate.set_color(BLACK))
    sol = texto("Le quedan 18 − 6 = 12 €", 32, OK).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(sol), Indicate(VGroup(*b[3:]), scale_factor=1.05))
    scene.wait(3)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Operaciones con fracciones")
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2(), size=22)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        for sub, ops, letra in (("Ejercicio 1 a)", MISMO_DEN[:1], "a"), ("Ejercicio 2 a)", DISTINTO_DEN[:1], "a"),
                                ("Ejercicio 2 f): un entero más una fracción", DISTINTO_DEN[5:], "f")):
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, letra, ejemplo=True)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        resolver_cantidad(self, *DE_CANTIDAD[0], "a)", 0.4, ejemplo=True)
        limpiar(self, cab)
        for sub, ops in (("Ejercicio 4 a)", MULTIPLICA[:1]), ("Ejercicio 5 a)", DIVIDE[:1])):
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, "a", ejemplo=True)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        problema_deposito(self)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Operaciones con fracciones")
        pantallas = [
            ("Ejercicio 1: b), c) y d)", MISMO_DEN[1:], "bcd"),
            ("Ejercicio 2: b) y c)", DISTINTO_DEN[1:3], "bc"),
            ("Ejercicio 2: d) y e)", DISTINTO_DEN[3:5], "de"),
        ]
        for sub, ops, letras in pantallas:
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, letras)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        resolver_cantidades(self, DE_CANTIDAD[1:], "bcd")
        limpiar(self, cab)
        for sub, ops in (("Ejercicio 4: b), c) y d)", MULTIPLICA[1:]), ("Ejercicio 5: b), c) y d)", DIVIDE[1:])):
            subtitulo(self, cab, sub)
            resolver_ops(self, ops, "bcd")
            limpiar(self, cab)
        for sub, f in (("Ejercicio 6 b)", problema_pizza), ("Ejercicio 6 c)", problema_vasos),
                       ("Ejercicio 6 d)", problema_laura)):
            subtitulo(self, cab, sub)
            f(self)
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes operar con fracciones.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
