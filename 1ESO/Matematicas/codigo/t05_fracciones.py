"""Tema 5 · Fracciones equivalentes. Comparación y ordenación (1º ESO)

Escenas:
    QueEsUnaFraccion        – partes iguales de un todo: barra, pizza, recta
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
TEMA = "Tema 5 · Fracciones equivalentes, comparar y ordenar"
TITULOS = {
    "QueEsUnaFraccion": "¿Qué es una fracción?",
    "FraccionesEquivalentes": "Fracciones equivalentes",
    "AmplificarSimplificar": "Amplificar y simplificar",
    "CompararFracciones": "Comparar fracciones",
    "OrdenarFracciones": "Ordenar fracciones",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
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
        limpiar(self, cab)

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
        limpiar(self, cab)

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
        limpiar(self, cab)

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
        limpiar(self, cab)

        # Productos cruzados
        sub = subtitulo(self, cab, "¿Cómo saber si dos fracciones son equivalentes?")
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
        subtitulo(self, cab, "Amplificar: multiplicar arriba y abajo por el mismo número")
        datos = [(2, 3), (4, 6), (8, 12)]
        self.cadena_ops(datos, "x", [2, 2], xs)
        resumen = texto("Cortamos más fino: hay más trozos, pero la parte pintada es la misma", 24, GREY_B)
        resumen.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(resumen))
        self.wait(2.5)
        limpiar(self, cab)

        # Simplificar
        subtitulo(self, cab, "Simplificar: dividir arriba y abajo por el mismo número")
        datos = [(12, 18), (6, 9), (2, 3)]
        self.cadena_ops(datos, ":", [2, 3], xs)
        resumen = texto("Juntamos trozos: hay menos trozos, pero la parte pintada es la misma", 24, GREY_B)
        resumen.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(resumen))
        self.wait(2.5)
        limpiar(self, cab)

        # Irreducible con el M.C.D.
        subtitulo(self, cab, "De una vez: dividimos por el M.C.D.")
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
        subtitulo(self, cab, nombre)
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
        limpiar(self, cab)

    def idea_comun(self, cab):
        """Por qué hace falta el común denominador."""
        subtitulo(self, cab, "Distinto denominador")
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
        limpiar(self, cab)

    def caso_comun(self, cab, a, b, nombre):
        (na, da), (nb, db) = a, b
        m = da * db // np.gcd(da, db)
        subtitulo(self, cab, f"{nombre}: ¿cuál es mayor?")
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
        limpiar(self, cab)

    def resumen(self, cab):
        subtitulo(self, cab, "Resumen")
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


def mcm(*ds):
    m = 1
    for d in ds:
        m = m * d // gcd(m, d)
    return m


def fr_txt(n, d):
    return f"{n}/{d}"


def dibujo(tipo, n, d, escala=1.0):
    return barra(d, n, ancho=3.0 * escala, alto=0.8 * escala) if tipo == "barra" else pizza(d, n, r=1.0 * escala)


def pagina_enunciados(scene, cab, bloques):
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
    limpiar(scene, cab)


def mini_dibujos():
    g = VGroup()
    for l, (tipo, n, d) in zip("abcd", DIBUJOS):
        g.add(VGroup(texto(f"{l})", 24), dibujo(tipo, n, d, 0.5)).arrange(RIGHT, buff=0.2))
    return g.arrange(RIGHT, buff=0.8)


def enunciados_1():
    return [
        ("1. Escribe la fracción que representa cada dibujo:", mini_dibujos()),
        ("2. Fracciones equivalentes:",
         "a) ¿Son equivalentes?   " + "    ".join(f"{fr_txt(*p)} y {fr_txt(*q)}" for p, q in EQUIVALENTES) + "\n"
         "b) Completa:   " + "    ".join(f"{fr_txt(*p)} = {fr_txt(*q)}" for p, q in COMPLETA)),
        ("3. Simplifica hasta la fracción irreducible:", "    ".join(fr_txt(*f) for f in SIMPLIFICA)),
    ]


def enunciados_2():
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
    m = mcm(da, db)
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
    m = mcm(*[d for _, d in fracs])
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
    m = mcm(da, db)
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
    m = mcm(*[d for _, _, d in LECTORES])
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


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Fracciones equivalentes, comparar y ordenar")
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        resolver_dibujos(self, DIBUJOS[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a): ¿son equivalentes?")
        resolver_cruzados(self, EQUIVALENTES[:1], "a")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 b): completa")
        resolver_completa(self, COMPLETA[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        resolver_simplifica(self, SIMPLIFICA[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 a)")
        resolver_compara(self, *COMPARA[0], "a")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 b)")
        resolver_compara(self, *COMPARA[1], "b", detalle=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 a)")
        resolver_ordena(self, *ORDENA[0], "a")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        problema_dos(self, "Ana se come 3/8 de una pizza y Luis 1/4 de otra igual. ¿Quién come más?",
                     (3, 8), (1, 4), ("Ana", "Luis"), "pizza", "Ana come más pizza")
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Fracciones equivalentes, comparar y ordenar")

        subtitulo(self, cab, "Ejercicio 1: b), c) y d)")
        resolver_dibujos(self, DIBUJOS[1:], "bcd")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a): b) y c)")
        resolver_cruzados(self, EQUIVALENTES[1:], "bc")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 b): b) y c)")
        resolver_completa(self, COMPLETA[1:], "bc")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        resolver_simplifica(self, SIMPLIFICA[1:], "bcd")
        limpiar(self, cab)
        for letra, (a, b) in zip("cde", COMPARA[2:]):
            subtitulo(self, cab, f"Ejercicio 4 {letra})")
            resolver_compara(self, a, b, letra)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 b)")
        resolver_ordena(self, *ORDENA[1], "b")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 b)")
        problema_dos(self, "En una clase, 2/5 del alumnado va en autobús y 3/10 andando.\n¿Qué grupo es mayor?",
                     (2, 5), (3, 10), ("Autobús", "Andando"), "barra", "Son más los que van en autobús")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 c)")
        problema_lectores(self)
        limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes trabajar con fracciones equivalentes.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
