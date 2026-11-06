"""Tema 4 · Operaciones con números enteros (1º ESO)

Escenas:
    SumaRecta               – sumar = moverse por la recta
    SumaFichas              – fichas + y −, «parejas cero» y la regla de la suma
    Resta                   – restar = sumar el opuesto; quitar paréntesis
    SumasRestasCombinadas   – agrupar positivos y negativos
    Multiplicacion          – suma repetida, patrón (−)·(−) = +, regla de los signos
    Division                – inversa de la multiplicación, misma regla

Renderizar (desde esta carpeta):
    python -m manim -pql t04_operaciones_enteros.py SumaRecta
    python publicar.py t04_operaciones_enteros.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 4 · Operaciones con números enteros"
TITULOS = {
    "SumaRecta": "Sumar enteros en la recta",
    "SumaFichas": "Sumar con fichas: la regla de la suma",
    "Resta": "Restar es sumar el opuesto",
    "SumasRestasCombinadas": "Sumas y restas combinadas",
    "Multiplicacion": "Multiplicar: la regla de los signos",
    "Division": "Dividir enteros",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}


def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena, color=ACENTO):
    t = texto(cadena, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:  # no cabe al lado: debajo
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


# ---------------------------------------------------------------------------
class SumaRecta(Scene):
    def construct(self):
        cab = titulo(self, "Sumar enteros", "Moverse por la recta")
        reglas = VGroup(texto("Sumar un positivo  →  avanzar hacia la derecha", 26, POSITIVO),
                        texto("Sumar un negativo  →  retroceder hacia la izquierda", 26, NEGATIVO))
        reglas.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(cab, DOWN, buff=0.3).to_edge(LEFT)
        self.play(FadeIn(reglas))
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.4, size=28)
        self.play(Create(linea), FadeIn(grupo[1]))

        slots = [np.array([x, -3.1, 0]) for x in (-4.9, -1.65, 1.65, 4.9)]
        for (a, b), slot in zip([(3, 2), (-2, -3), (5, -3), (-6, 4)], slots):
            e = expr_enteros(a, "+", b, "=", size=56).move_to([0, 0.5, 0])
            self.play(Write(e))
            p = Dot(linea.n2p(a) + UP * 0.25, radius=0.13, color=ACENTO)
            ini = texto(f"Empezamos en {fmt_entero(a)}", 24, color_entero(a)).next_to(e, DOWN, buff=0.25)
            self.play(Indicate(e[0], color=color_entero(a)), FadeIn(p, scale=2), FadeIn(ini))
            dir_ = "derecha" if b > 0 else "izquierda"
            mov = texto(f"{fmt_entero(b)}: {abs(b)} pasos a la {dir_}", 24, color_entero(b)).move_to(ini)
            self.play(Indicate(e[2], color=color_entero(b)), Transform(ini, mov))
            traza = salto(self, p, linea, a, a + b, color_entero(b))
            r = tex_entero(a + b, size=56).next_to(e, RIGHT, buff=0.25)
            self.play(Write(r), Flash(p, color=color_entero(a + b)))
            self.wait(1)
            g = VGroup(e, r)
            self.play(FadeOut(VGroup(p, traza, ini)), g.animate.scale(0.55).move_to(slot))

        self.wait(1)
        limpiar(self, cab)

        # Contexto: temperatura
        ctx = texto("A las 8 h estamos a −2 °C y la temperatura sube 5 grados.\n¿Qué temperatura hace?", 30)
        ctx.next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(ctx))
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.4, size=28)
        self.play(Create(linea), FadeIn(grupo[1]))
        e = expr_enteros(-2, "+", 5, "=", size=56).move_to([0, 0.4, 0])
        self.play(Write(e))
        p = Dot(linea.n2p(-2) + UP * 0.25, radius=0.13, color=ACENTO)
        self.play(FadeIn(p, scale=2))
        salto(self, p, linea, -2, 3, POSITIVO)
        r = VGroup(MathTex("+3", font_size=56, color=POSITIVO), Text("°C", font_size=40, color=POSITIVO))
        r.arrange(RIGHT, buff=0.12).next_to(e, RIGHT, buff=0.25)
        self.play(Write(r), Flash(p, color=POSITIVO))
        self.wait(3)


# ---------------------------------------------------------------------------
class SumaFichas(Scene):
    def construct(self):
        cab = titulo(self, "Sumar con fichas")

        # Pareja cero
        a, b = ficha_entero(1, 0.45).shift(LEFT * 1.5), ficha_entero(-1, 0.45).shift(RIGHT * 1.5)
        t1 = MathTex("(+1)", "+", "(-1)", "=", "0", font_size=56).shift(UP * 1.6)
        t1[0].set_color(POSITIVO)
        t1[2].set_color(NEGATIVO)
        self.play(GrowFromCenter(a), GrowFromCenter(b))
        self.play(Write(t1[:3]))
        self.play(a.animate.move_to(LEFT * 0.3), b.animate.move_to(RIGHT * 0.3))
        self.play(FadeOut(a, scale=0.2), FadeOut(b, scale=0.2), Flash(ORIGIN, color=WHITE), Write(t1[3:]))
        nombre = texto("Una ficha + y una ficha − se anulan: forman una «pareja cero»", 28, ACENTO)
        nombre.shift(DOWN * 1.3)
        self.play(FadeIn(nombre))
        self.wait(2)
        limpiar(self, cab)

        for a, b in [(5, -3), (-4, -2), (-6, 2)]:
            self.ejemplo(cab, a, b)

        # Reglas
        tarjetas = VGroup()
        for tit, l1, ej, col in (
            ("Mismo signo", "Se suman y se deja el signo", r"(-4)+(-2)=-6", ACENTO),
            ("Distinto signo", "Se restan y se pone el signo\ndel que tiene mayor valor absoluto",
             r"(+5)+(-3)=+2", ACENTO),
        ):
            caja = RoundedRectangle(width=6.4, height=3.2, corner_radius=0.3, color=col, fill_opacity=0.1)
            txt = VGroup(texto(tit, 38, col, weight=BOLD), texto(l1, 22), MathTex(ej, font_size=44))
            txt.arrange(DOWN, buff=0.3).move_to(caja)
            tarjetas.add(VGroup(caja, txt))
        tarjetas.arrange(RIGHT, buff=0.3).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.3) for t in tarjetas], lag_ratio=0.4))
        self.wait(4)

    def ejemplo(self, cab, a, b):
        e = expr_enteros(a, "+", b, "=", size=56).move_to([0, 2.3, 0])
        self.play(Write(e))
        x0 = -3.5

        def fila(n, y):
            g = VGroup(*[ficha_entero(1 if n > 0 else -1) for _ in range(abs(n))]).arrange(RIGHT, buff=0.25)
            return g.move_to([x0, y, 0], aligned_edge=LEFT)

        f1, f2 = fila(a, 0.9), fila(b, -0.3)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in f1], lag_ratio=0.1))
        self.play(LaggedStart(*[GrowFromCenter(f) for f in f2], lag_ratio=0.1))

        if (a > 0) != (b > 0):
            k = min(abs(a), abs(b))
            medios = [(f1[i].get_center() + f2[i].get_center()) / 2 for i in range(k)]
            exp = texto(f"Se anulan {k} parejas cero", 28, GREY_B).move_to([0, -1.6, 0])
            self.play(*[f1[i].animate.move_to(medios[i] + UP * 0.32) for i in range(k)],
                      *[f2[i].animate.move_to(medios[i] + DOWN * 0.32) for i in range(k)], FadeIn(exp))
            self.play(*[FadeOut(f1[i], scale=0.2) for i in range(k)], *[FadeOut(f2[i], scale=0.2) for i in range(k)],
                      *[Flash(m, color=WHITE) for m in medios])
            quedan = VGroup(*(f1[k:] if abs(a) > abs(b) else f2[k:]))
        else:
            exp = texto("Todas del mismo color: se juntan", 28, GREY_B).move_to([0, -1.6, 0])
            destino = [f1[-1].get_center() + RIGHT * 0.85 * (i + 1) for i in range(len(f2))]
            self.play(*[f.animate.move_to(d) for f, d in zip(f2, destino)], FadeIn(exp))
            quedan = VGroup(*f1, *f2)
        res = a + b
        self.play(Circumscribe(quedan, color=color_entero(res)))
        nombre_color = "naranjas" if res > 0 else "azules"
        fin = texto(f"Quedan {abs(res)} fichas {nombre_color}  →  {fmt_entero(res)}", 30, color_entero(res))
        fin.move_to([0, -2.4, 0])
        r = tex_entero(res, size=56).next_to(e, RIGHT, buff=0.25)
        self.play(Write(fin), Write(r))
        self.wait(2)
        limpiar(self, cab)


# ---------------------------------------------------------------------------
class Resta(Scene):
    def construct(self):
        cab = titulo(self, "Restar enteros", "Restar es sumar el opuesto")
        idea = MathTex(r"a - b", r"\;=\;", r"a + (\text{opuesto de } b)", font_size=56)
        idea[2].set_color(ACENTO)
        self.play(Write(idea))
        self.wait(2)
        self.play(idea.animate.scale(0.6).next_to(cab, RIGHT, buff=0.6))

        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.7, size=28)
        self.play(Create(linea), FadeIn(grupo[1]))
        for a, b in [(3, 5), (-2, -6)]:
            e1 = expr_enteros(a, "-", b, size=56).move_to([0, 1.9, 0])
            e2 = expr_enteros(a, "+", -b, "=", size=56).move_to([0, 0.6, 0])
            self.play(Write(e1))
            fl = Arrow(e1.get_bottom(), e2.get_top(), buff=0.1, color=GREY_B)
            n1 = texto("la resta pasa a suma", 22, ACENTO).next_to(e1, LEFT, buff=0.6)
            n2 = texto("y cambiamos por el opuesto", 22, ACENTO).next_to(e1, RIGHT, buff=0.6)
            self.play(GrowArrow(fl), FadeIn(n1), Indicate(e1[1], color=ACENTO))
            self.play(TransformFromCopy(e1[0], e2[0]), TransformFromCopy(e1[1], e2[1]))
            self.play(FadeIn(n2), Indicate(e1[2], color=ACENTO))
            self.play(TransformFromCopy(e1[2], e2[2]), FadeIn(e2[3]))
            p = Dot(linea.n2p(a) + UP * 0.25, radius=0.13, color=ACENTO)
            self.play(FadeIn(p, scale=2))
            traza = salto(self, p, linea, a, a - b, color_entero(-b), rt=0.25)
            r = tex_entero(a - b, size=56).next_to(e2, RIGHT, buff=0.25)
            self.play(Write(r), Flash(p, color=color_entero(a - b)))
            self.wait(1.5)
            self.play(FadeOut(VGroup(e1, e2, fl, n1, n2, p, traza, r)))
        limpiar(self, cab)

        # Contexto
        ctx = texto("De día hace 12 °C y de noche −3 °C.\n¿Cuántos grados ha bajado la temperatura?", 30)
        ctx.next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        self.play(Write(ctx))
        grupo, linea = recta_enteros(-4, 14, largo=13, y=-1.3, size=26)
        self.play(Create(linea), FadeIn(grupo[1]))
        d1 = Dot(linea.n2p(12), radius=0.13, color=POSITIVO)
        d2 = Dot(linea.n2p(-3), radius=0.13, color=NEGATIVO)
        self.play(FadeIn(d1, scale=2), FadeIn(d2, scale=2))
        br = BraceBetweenPoints(linea.n2p(-3), linea.n2p(12), UP).shift(UP * 0.15)
        bt = texto("15 grados", 26, ACENTO).next_to(br, UP, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(bt))
        e = expr_enteros(12, "-", -3, "=", 12, "+", 3, "=", size=48).to_edge(DOWN, buff=0.5).shift(LEFT * 0.6)
        r = MathTex("15", font_size=48, color=ACENTO).next_to(e, RIGHT, buff=0.2)
        self.play(Write(e), Write(r))
        self.wait(2.5)
        limpiar(self, cab)

        # Quitar paréntesis
        sub = texto("Para quitar paréntesis", 32, ACENTO).next_to(cab, DOWN, buff=0.4).to_edge(LEFT)
        self.play(FadeIn(sub))
        filas = VGroup()
        for signo, n in (("+", 3), ("+", -3), ("-", 3), ("-", -3)):
            res = n if signo == "+" else -n
            f = MathTex(signo, par_ent(n), "=", s_ent(res), font_size=56)
            f[1].set_color(color_entero(n))
            f[3].set_color(color_entero(res))
            filas.add(f)
        filas.arrange(DOWN, buff=0.4, aligned_edge=LEFT).shift(LEFT * 2.5 + DOWN * 0.3)
        for f in filas:
            self.play(Write(f), run_time=0.8)
        iguales = VGroup(SurroundingRectangle(filas[0], color=POSITIVO, buff=0.1),
                         SurroundingRectangle(filas[3], color=POSITIVO, buff=0.1))
        distintos = VGroup(SurroundingRectangle(filas[1], color=NEGATIVO, buff=0.1),
                           SurroundingRectangle(filas[2], color=NEGATIVO, buff=0.1))
        ti = texto("Signos iguales  →  +", 32, POSITIVO).move_to([3.3, 0.6, 0])
        td = texto(f"Signos distintos  →  {MENOS}", 32, NEGATIVO).move_to([3.3, -1.0, 0])
        self.play(Create(iguales), Write(ti))
        self.play(Create(distintos), Write(td))
        self.wait(3)


# ---------------------------------------------------------------------------
class SumasRestasCombinadas(Scene):
    def construct(self):
        cab = titulo(self, "Sumas y restas combinadas")
        sub = subtitulo(self, cab, "Agrupamos positivos y negativos")

        nums = [-3, 7, -5, 2, -4]
        toks = MathTex(*[str(n) if (i == 0 or n < 0) else f"+{n}" for i, n in enumerate(nums)], font_size=64)
        for t, n in zip(toks, nums):
            t.set_color(color_entero(n))
        toks.move_to([0, 1.75, 0])
        self.play(Write(toks))

        cajas = {}
        for signo, x, col, nombre in ((1, -3.4, POSITIVO, "Positivos"), (-1, 3.4, NEGATIVO, "Negativos")):
            caja = RoundedRectangle(width=5.2, height=1.6, corner_radius=0.25, color=col, fill_opacity=0.1)
            caja.move_to([x, 0.0, 0])
            lab = texto(nombre, 26, col).next_to(caja, UP, buff=0.1)
            cajas[signo] = caja
            self.play(Create(caja), FadeIn(lab), run_time=0.6)

        for signo in (1, -1):
            sel = [(t, n) for t, n in zip(toks, nums) if (n > 0) == (signo > 0)]
            copias = [t.copy() for t, _ in sel]
            destino = VGroup(*[c.copy() for c in copias]).arrange(RIGHT, buff=0.4).move_to(cajas[signo])
            self.play(*[c.animate.move_to(d) for c, d in zip(copias, destino)], run_time=1.2)
            vals = [abs(n) for _, n in sel]
            suma = MathTex(" + ".join(map(str, vals)), "=", str(sum(vals)), font_size=44,
                           color=POSITIVO if signo > 0 else NEGATIVO)
            suma.next_to(cajas[signo], DOWN, buff=0.3)
            self.play(Write(suma))

        fin = MathTex("+9", "-12", "=", "-3", font_size=64).move_to([0, -2.3, 0])
        fin[0].set_color(POSITIVO)
        fin[1].set_color(NEGATIVO)
        fin[3].set_color(NEGATIVO)
        self.play(Write(fin))
        exp = texto("Distinto signo: 12 − 9 = 3, con el signo del mayor (−)", 24, GREY_B).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(exp), Circumscribe(fin[3], color=ACENTO))
        self.wait(2.5)
        limpiar(self, cab)

        # Con paréntesis
        sub = subtitulo(self, cab, "Con paréntesis: primero los quitamos")
        l1 = MathTex("5", "-", "(-3)", "+", "(-8)", font_size=60).move_to([0, 1.7, 0])
        l1[2].set_color(NEGATIVO)
        l1[4].set_color(NEGATIVO)
        self.play(Write(l1))
        n1 = MathTex(r"-(-3) = +3", font_size=36, color=POSITIVO).next_to(l1, DOWN, buff=0.35).shift(LEFT * 1.0)
        n2 = MathTex(r"+(-8) = -8", font_size=36, color=NEGATIVO).next_to(l1, DOWN, buff=0.35).shift(RIGHT * 2.0)
        self.play(Indicate(VGroup(l1[1], l1[2])), FadeIn(n1))
        self.play(Indicate(VGroup(l1[3], l1[4])), FadeIn(n2))
        l2 = MathTex("5", "+3", "-8", font_size=60).move_to([0, 0.2, 0])
        l2[0].set_color(POSITIVO)
        l2[1].set_color(POSITIVO)
        l2[2].set_color(NEGATIVO)
        self.play(TransformFromCopy(l1[0], l2[0]), TransformFromCopy(VGroup(l1[1], l1[2]), l2[1]),
                  TransformFromCopy(VGroup(l1[3], l1[4]), l2[2]))
        l3 = MathTex("+8", "-8", "=", "0", font_size=60).move_to([0, -1.3, 0])
        l3[0].set_color(POSITIVO)
        l3[1].set_color(NEGATIVO)
        e3 = texto("positivos: 5 + 3 = 8   ·   negativos: 8", 24, GREY_B).next_to(l3, DOWN, buff=0.3)
        self.play(Write(l3), FadeIn(e3))
        self.play(Circumscribe(l3[3], color=ACENTO))
        self.wait(3)


# ---------------------------------------------------------------------------
class Multiplicacion(Scene):
    def reflejar(self, p, linea, n):
        """Lleva el punto de n a −n con un arco por encima (reflejo en el 0)."""
        arco = ArcBetweenPoints(linea.n2p(n), linea.n2p(-n), angle=PI / 2 if n > 0 else -PI / 2)
        c0, c1 = ManimColor(color_entero(n)), ManimColor(color_entero(-n))
        self.play(MoveAlongPath(p, arco),
                  UpdateFromAlphaFunc(p, lambda m, t: m.set_color(interpolate_color(c0, c1, t))), run_time=1.4)

    def construct(self):
        cab = titulo(self, "Multiplicar enteros")

        # Suma repetida
        sub = subtitulo(self, cab, "Multiplicar es sumar varias veces")
        e = expr_enteros(3, r"\cdot", -2, "=", size=56).move_to([0, 1.8, 0])
        self.play(Write(e))
        rep = expr_enteros(-2, "+", -2, "+", -2, size=48).next_to(e, DOWN, buff=0.4)
        veces = texto("3 veces (−2)", 24, GREY_B).next_to(rep, RIGHT, buff=0.4)
        self.play(Write(rep), FadeIn(veces))
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.6, size=28)
        self.play(Create(linea), FadeIn(grupo[1]))
        p = Dot(linea.n2p(0) + UP * 0.25, radius=0.13, color=ACENTO)
        self.play(FadeIn(p, scale=2))
        salto(self, p, linea, 0, -6, NEGATIVO, paso=2, rt=0.5)
        r = tex_entero(-6, size=56).next_to(e, RIGHT, buff=0.25)
        self.play(Write(r), Flash(p, color=NEGATIVO))
        self.wait(2)
        limpiar(self, cab)

        # El signo − da la vuelta (opuesto = reflejo en el 0, como en el tema 3)
        sub = subtitulo(self, cab, "Multiplicar por (−1) es dar la vuelta")
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.4, size=28)
        espejo = DashedLine(linea.n2p(0) + DOWN * 0.15, linea.n2p(0) + UP * 1.4, color=GREY_B)
        self.play(Create(linea), FadeIn(grupo[1]), Create(espejo))
        p = Dot(linea.n2p(4), radius=0.14, color=POSITIVO)
        self.play(FadeIn(p, scale=2))
        frases = [texto("El opuesto: el reflejo en el 0", 28, GREY_B),
                  texto("Dos vueltas: ¡volvemos a estar como al principio!", 28, ACENTO)]
        for k, (n, frase) in enumerate(zip((4, -4), frases)):
            e = VGroup(expr_enteros(-1, r"\cdot", n, "=", size=56), tex_entero(-n, size=56))
            e.arrange(RIGHT, buff=0.2).move_to([0, 1.6, 0])
            self.play(Write(e[0]))
            self.reflejar(p, linea, n)
            frase.move_to([0, 0.6, 0])
            self.play(Write(e[1]), FadeIn(frase), Flash(p, color=color_entero(-n)))
            self.wait(1.5)
            self.play(FadeOut(e), FadeOut(frase))
        limpiar(self, cab)

        # (−3)·(−2): primero (+3)·(−2), luego el − da la vuelta
        sub = subtitulo(self, cab, "¿Cuánto es (−3)·(−2)?")
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.6, size=28)
        espejo = DashedLine(linea.n2p(0) + DOWN * 0.15, linea.n2p(0) + UP * 1.4, color=GREY_B)
        self.play(Create(linea), FadeIn(grupo[1]))
        l1 = MathTex(par_ent(-3), r"\cdot", par_ent(-2), "=", r"\text{opuesto de }", r"\big[",
                     par_ent(3), r"\cdot", par_ent(-2), r"\big]", font_size=46).move_to([0, 2.0, 0])
        for i, n in ((0, -3), (2, -2), (6, 3), (8, -2)):
            l1[i].set_color(color_entero(n))
        l1[4].set_color(ACENTO)
        self.play(Write(l1[:4]))
        menos = texto("el − del −3 significa «y luego, el opuesto»", 24, ACENTO).next_to(l1, DOWN, buff=0.3)
        self.play(Indicate(l1[0], color=ACENTO), FadeIn(menos))
        self.play(Write(l1[4:]))
        self.wait(0.8)
        self.play(FadeOut(menos))

        # Paso 1: (+3)·(−2) = −6
        paso1 = texto("1.º  (+3)·(−2): tres saltos de 2 hacia la izquierda", 26, NEGATIVO).move_to([0, 0.9, 0])
        self.play(FadeIn(paso1), Indicate(VGroup(*l1[6:9]), color=NEGATIVO))
        p = Dot(linea.n2p(0) + UP * 0.25, radius=0.13, color=ACENTO)
        self.play(FadeIn(p, scale=2))
        traza = salto(self, p, linea, 0, -6, NEGATIVO, paso=2, rt=0.45)
        self.play(p.animate.move_to(linea.n2p(-6)).set_color(NEGATIVO), FadeOut(traza))
        lm6 = tex_entero(-6, size=44).next_to(p, UP, buff=0.3)
        self.play(Write(lm6))
        self.wait(0.5)

        # Paso 2: el − da la vuelta: −6 → +6
        paso2 = texto("2.º  El −: damos la vuelta  →  el opuesto de −6", 26, POSITIVO).move_to(paso1)
        self.play(Transform(paso1, paso2), Create(espejo))
        self.reflejar(p, linea, -6)
        lp6 = tex_entero(6, size=44).next_to(p, UP, buff=0.3)
        self.play(Write(lp6), Flash(p, color=POSITIVO))
        l2 = MathTex("=", r"\text{opuesto de }", "(-6)", "=", "+6", font_size=50).next_to(l1, DOWN, buff=0.35)
        l2.align_to(l1[3], LEFT)
        l2[2].set_color(NEGATIVO)
        l2[4].set_color(POSITIVO)
        self.play(FadeOut(paso1), Write(l2))
        self.play(Circumscribe(l2[4], color=POSITIVO))
        self.wait(1)
        concl = VGroup(MathTex(r"(-)\cdot(-) = +", font_size=56, color=POSITIVO),
                       texto("Un signo − da una vuelta. Dos signos − dan dos vueltas: volvemos a +", 24, ACENTO))
        concl.arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.2)
        self.play(FadeOut(VGroup(lm6, lp6)), FadeIn(concl, shift=UP * 0.2))
        self.wait(3)
        limpiar(self, cab)

        # Regla de los signos
        sub = subtitulo(self, cab, "La regla de los signos")
        tabla = VGroup()
        celdas = [[r"\cdot", "+", "-"], ["+", "+", "-"], ["-", "-", "+"]]
        for i, fila in enumerate(celdas):
            for j, s in enumerate(fila):
                sq = Square(1.1, stroke_color=GREY_B, stroke_width=2)
                sq.move_to([-4.2 + j * 1.1, 1.0 - i * 1.1, 0])
                if i and j:
                    col = POSITIVO if s == "+" else NEGATIVO
                    sq.set_fill(col, 0.25)
                else:
                    col = ACENTO
                m = MathTex(s, font_size=60, color=col).move_to(sq)
                tabla.add(VGroup(sq, m))
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in tabla], lag_ratio=0.08))
        frase = VGroup(texto("Signos iguales  →  +", 32, POSITIVO),
                       texto(f"Signos distintos  →  {MENOS}", 32, NEGATIVO)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        frase.move_to([2.8, 1.3, 0])
        self.play(FadeIn(frase, shift=LEFT * 0.2))
        ejemplos = VGroup()
        for a, b in ((-4, -5), (6, -3)):
            g = VGroup(expr_enteros(a, r"\cdot", b, "=", size=48), tex_entero(a * b, size=48)).arrange(RIGHT, buff=0.2)
            ejemplos.add(g)
        ejemplos.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([2.8, -1.4, 0])
        for g in ejemplos:
            self.play(Write(g))
            self.wait(0.5)
        self.wait(3)


# ---------------------------------------------------------------------------
class Division(Scene):
    def construct(self):
        cab = titulo(self, "Dividir enteros", "Lo contrario de multiplicar")

        e = expr_enteros(-12, ":", 3, "=", size=60).move_to([-0.5, 1.8, 0])
        q = MathTex("?", font_size=60, color=ACENTO).next_to(e, RIGHT, buff=0.25)
        self.play(Write(e), FadeIn(q))
        preg = texto("¿Qué número multiplicado por (+3) da −12?", 30).move_to([0, 0.6, 0])
        self.play(Write(preg))
        comp = VGroup(expr_enteros(-4, r"\cdot", 3, "=", size=56), tex_entero(-12, size=56)).arrange(RIGHT, buff=0.2)
        comp.move_to([0, -0.6, 0])
        self.play(Write(comp))
        self.play(Indicate(comp[0][0], color=NEGATIVO, scale_factor=1.4))
        sol = tex_entero(-4, size=60).move_to(q)
        self.play(ReplacementTransform(q, sol), Circumscribe(sol, color=ACENTO))
        self.wait(2)
        limpiar(self, cab)

        sub = subtitulo(self, cab, "La misma regla de los signos")
        casos = VGroup()
        for a, b in ((15, 5), (-15, -5), (15, -5), (-15, 5)):
            c = a // b
            linea = VGroup(expr_enteros(a, ":", b, "=", size=48), tex_entero(c, size=48)).arrange(RIGHT, buff=0.2)
            check = MathTex(r"\text{porque }", par_ent(c), r"\cdot", par_ent(b), "=", s_ent(a), font_size=30)
            check.set_color(GREY_B)
            g = VGroup(linea, check).arrange(DOWN, buff=0.15)
            casos.add(g)
        casos.arrange_in_grid(rows=2, cols=2, buff=(1.2, 0.8)).shift(DOWN * 0.2)
        for g in casos:
            self.play(Write(g[0]), run_time=0.9)
            self.play(FadeIn(g[1]), run_time=0.5)
        self.wait(1)
        regla = texto("Multiplicar y dividir:  signos iguales → +   ·   signos distintos → −", 28, ACENTO)
        regla.to_edge(DOWN, buff=0.4)
        self.play(Write(regla))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
SUMAS = [(4, -7), (-3, -5), (-8, 8), (6, -2), (-9, 4), (-1, -6)]
RESTAS = [(2, 7), (-4, -9), (5, -3), (-6, 2), (-1, -1)]
PARENTESIS = [  # primer término + lista de (operación, número entre paréntesis)
    (8, [("-", 3), ("+", -6)]),
    (-5, [("-", -2), ("+", 4)]),
    (7, [("+", -10), ("-", -1)]),
]
COMBINADAS = [[-4, 9, -3, -7, 2], [12, -5, -8, 1], [-6, -2, 10, -4]]
MULDIV = [(-6, "·", 4), (-7, "·", -3), (5, "·", -8), (-24, ":", -6), (36, ":", -9), (-45, ":", 5)]


def P(n):
    """'(+4)' / '(−7)' para Text."""
    return f"({fmt_entero(n)})"


def cadena_combinada(nums, mas_primero=False):
    s = fmt_entero(nums[0], mas_primero)
    for n in nums[1:]:
        s += f" + {n}" if n > 0 else f" {MENOS} {abs(n)}"
    return s


def cadena_parentesis(item):
    primero, resto = item
    s = fmt_entero(primero, False)
    for op, n in resto:
        s += f" {op.replace('-', MENOS)} {P(n)}"
    return s


ENUN_1 = [
    ("1. Calcula estas sumas:",
     "    ".join(f"{l}) {P(a)} + {P(b)}" for l, (a, b) in zip("abc", SUMAS[:3])) + "\n" +
     "    ".join(f"{l}) {P(a)} + {P(b)}" for l, (a, b) in zip("def", SUMAS[3:]))),
    ("2. Calcula estas restas:",
     "    ".join(f"{l}) {P(a)} {MENOS} {P(b)}" for l, (a, b) in zip("abc", RESTAS[:3])) + "\n" +
     "    ".join(f"{l}) {P(a)} {MENOS} {P(b)}" for l, (a, b) in zip("de", RESTAS[3:]))),
    ("3. Quita los paréntesis y calcula:",
     "    ".join(f"{l}) {cadena_parentesis(it)}" for l, it in zip("abc", PARENTESIS))),
]
ENUN_2 = [
    ("4. Calcula:", "    ".join(f"{l}) {cadena_combinada(c)}" for l, c in zip("abc", COMBINADAS))),
    ("5. Multiplica y divide:",
     "    ".join(f"{l}) {P(a)} {op} {P(b)}" for l, (a, op, b) in zip("abc", MULDIV[:3])) + "\n" +
     "    ".join(f"{l}) {P(a)} {op} {P(b)}" for l, (a, op, b) in zip("def", MULDIV[3:]))),
    ("6. Problemas:",
     f"a) A las 6 h hace {MENOS}4 °C. A mediodía sube 11 grados y por la noche baja 9.\n"
     "     ¿Qué temperatura hace por la noche?\n"
     "b) Tienes 50 € y pagas 3 cuotas de 20 €. ¿Cuánto dinero te queda?\n"
     "c) Arquímedes nació en el año 287 a.C. y murió en el 212 a.C.\n"
     "     ¿Cuántos años vivió?"),
]


def pagina_enunciados(scene, cab, bloques):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 28, ACENTO), texto(cuerpo, 23))
        b.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(cab, DOWN, buff=0.5).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.35)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def pista_suma(a, b):
    if a == -b:
        return "opuestos: se anulan"
    if (a > 0) == (b > 0):
        return f"mismo signo: {abs(a)} + {abs(b)} = {abs(a) + abs(b)}, signo {'+' if a > 0 else MENOS}"
    g = a if abs(a) > abs(b) else b
    return (f"distinto signo: {max(abs(a), abs(b))} {MENOS} {min(abs(a), abs(b))} = {abs(a + b)},"
            f" signo de {fmt_entero(g)}")


def pista_muldiv(a, op, b):
    signo = "+" if (a > 0) == (b > 0) else MENOS
    tipo = "signos iguales" if signo == "+" else "signos distintos"
    r = a * b if op == "·" else a // b
    return f"{tipo} → {signo};  {abs(a)} {op} {abs(b)} = {abs(r)}"


def filas_resultado(scene, filas, y0=2.0, dy=0.95, x_pista=None):
    """filas: lista de (MathTex de la operación, pista str). Las escribe una debajo de otra,
    con las pistas alineadas en una columna justo a la derecha de la fila más larga."""
    for i, (m, _) in enumerate(filas):
        m.move_to([-6.3, y0 - i * dy, 0], aligned_edge=LEFT)
    x = max(m.get_right()[0] for m, _ in filas) + 0.5
    for m, pista in filas:
        p = texto(pista, 20, GREY_B).move_to([x, m.get_y(), 0], aligned_edge=LEFT)
        if p.get_right()[0] > config.frame_width / 2 - 0.2:  # no cabe: debajo
            p.next_to(m, DOWN, buff=0.08).align_to(m, LEFT)
        scene.play(Write(m), run_time=1.1)
        scene.play(FadeIn(p, shift=LEFT * 0.2), run_time=0.5)
    scene.wait(2.5)


def tex_suma(a, b):
    return VGroup(expr_enteros(a, "+", b, "=", size=46), tex_entero(a + b, size=46)).arrange(RIGHT, buff=0.18)


def tex_resta(a, b):
    return VGroup(expr_enteros(a, "-", b, "=", a, "+", -b, "=", size=40),
                  tex_entero(a - b, size=40)).arrange(RIGHT, buff=0.16)


def tex_muldiv(a, op, b):
    r = a * b if op == "·" else a // b
    sim = r"\cdot" if op == "·" else ":"
    return VGroup(expr_enteros(a, sim, b, "=", size=46), tex_entero(r, size=46)).arrange(RIGHT, buff=0.18)


def tex_tokens(nums, size=56):
    t = MathTex(*[str(n) if (i == 0 or n < 0) else f"+{n}" for i, n in enumerate(nums)], font_size=size)
    for s, n in zip(t, nums):
        s.set_color(color_entero(n))
    return t


def tex_agrupado(nums, size=50):
    pos = sum(n for n in nums if n > 0)
    neg = -sum(n for n in nums if n < 0)
    r = pos - neg
    t = MathTex(f"+{pos}", f"-{neg}", "=", s_ent(r), font_size=size)
    t[0].set_color(POSITIVO)
    t[1].set_color(NEGATIVO)
    t[3].set_color(color_entero(r))
    return t, pos, neg


# --- 1. Sumas
def resolver_sumas(scene, items, letras, ejemplo=False):
    if ejemplo:
        a, b = items[0]
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.5, size=28)
        scene.play(Create(linea), FadeIn(grupo[1]))
        e = expr_enteros(a, "+", b, "=", size=56).move_to([0, 1.6, 0])
        scene.play(Write(e))
        p = Dot(linea.n2p(a) + UP * 0.25, radius=0.13, color=ACENTO)
        scene.play(FadeIn(p, scale=2))
        salto(scene, p, linea, a, a + b, color_entero(b), rt=0.28)
        r = tex_entero(a + b, size=56).next_to(e, RIGHT, buff=0.25)
        pista = texto("Con la regla → " + pista_suma(a, b), 26, ACENTO).move_to([0, 0.5, 0])
        scene.play(Write(r), Flash(p, color=color_entero(a + b)), FadeIn(pista))
        scene.wait(2.5)
        return
    filas = []
    for (a, b), l in zip(items, letras):
        m = VGroup(MathTex(rf"\text{{{l})}}", font_size=42), tex_suma(a, b)).arrange(RIGHT, buff=0.25)
        filas.append((m, pista_suma(a, b)))
    filas_resultado(scene, filas, y0=2.2, dy=1.0)


# --- 2. Restas
def resolver_restas(scene, items, letras, ejemplo=False):
    if ejemplo:
        a, b = items[0]
        e1 = expr_enteros(a, "-", b, size=56).move_to([0, 2.0, 0])
        e2 = expr_enteros(a, "+", -b, "=", size=56).move_to([0, 0.8, 0])
        scene.play(Write(e1))
        n1 = texto("restar = sumar el opuesto", 24, ACENTO).next_to(e1, RIGHT, buff=0.6)
        scene.play(FadeIn(n1))
        scene.play(TransformFromCopy(e1[0], e2[0]), TransformFromCopy(e1[1], e2[1]),
                   TransformFromCopy(e1[2], e2[2]), FadeIn(e2[3]))
        grupo, linea = recta_enteros(-8, 8, largo=13, y=-1.6, size=28)
        scene.play(Create(linea), FadeIn(grupo[1]))
        p = Dot(linea.n2p(a) + UP * 0.25, radius=0.13, color=ACENTO)
        scene.play(FadeIn(p, scale=2))
        salto(scene, p, linea, a, a - b, color_entero(-b), rt=0.25)
        r = tex_entero(a - b, size=56).next_to(e2, RIGHT, buff=0.25)
        scene.play(Write(r), Flash(p, color=color_entero(a - b)))
        scene.wait(2.5)
        return
    filas = []
    for (a, b), l in zip(items, letras):
        m = VGroup(MathTex(rf"\text{{{l})}}", font_size=42), tex_resta(a, b)).arrange(RIGHT, buff=0.25)
        filas.append((m, pista_suma(a, -b)))
    filas_resultado(scene, filas, y0=2.2, dy=1.05)


# --- 3. Paréntesis
def resolver_parentesis(scene, item, letra):
    primero, resto = item
    partes = [s_ent(primero, False)]
    for op, n in resto:
        partes += [op, par_ent(n)]
    l1 = MathTex(rf"\text{{{letra})}}\;", *partes, font_size=58).move_to([0, 2.0, 0])
    l1[1].set_color(color_entero(primero))
    for k, (op, n) in enumerate(resto):
        l1[3 + 2 * k].set_color(color_entero(n))
    scene.play(Write(l1))
    # Cada paréntesis se convierte con la tabla de signos
    limpios = [primero] + [n if op == "+" else -n for op, n in resto]
    notas = VGroup()
    for (op, n), v in zip(resto, limpios[1:]):
        nota = MathTex(op + par_ent(n), "=", s_ent(v), font_size=36)
        nota[2].set_color(color_entero(v))
        notas.add(nota)
    notas.arrange(RIGHT, buff=1.2).next_to(l1, DOWN, buff=0.35)
    for k, nota in enumerate(notas):
        scene.play(Indicate(VGroup(l1[2 + 2 * k], l1[3 + 2 * k]), color=ACENTO), FadeIn(nota), run_time=0.9)
    l2 = tex_tokens(limpios, 58).move_to([0, 0.1, 0])
    scene.play(Write(l2))
    l3, pos, neg = tex_agrupado(limpios, 58)
    l3.move_to([0, -1.3, 0])
    exp = texto(f"positivos: {pos}   ·   negativos: {neg}", 24, GREY_B).next_to(l3, DOWN, buff=0.3)
    scene.play(Write(l3), FadeIn(exp))
    scene.play(Circumscribe(l3[3], color=ACENTO))
    scene.wait(2.5)


# --- 4. Combinadas
def resolver_combinada(scene, nums, letra, ejemplo=False):
    toks = tex_tokens(nums, 62).move_to([0.4, 1.9, 0])
    lab = MathTex(rf"\text{{{letra})}}", font_size=50).next_to(toks, LEFT, buff=0.4)
    scene.play(Write(lab), Write(toks))
    pos = [(t, n) for t, n in zip(toks, nums) if n > 0]
    neg = [(t, n) for t, n in zip(toks, nums) if n < 0]
    if ejemplo:
        y = 0.1
        for sel, x, col, nombre in ((pos, -3.4, POSITIVO, "Positivos"), (neg, 3.4, NEGATIVO, "Negativos")):
            caja = RoundedRectangle(width=5.2, height=1.5, corner_radius=0.25, color=col, fill_opacity=0.1)
            caja.move_to([x, y, 0])
            t = texto(nombre, 24, col).next_to(caja, UP, buff=0.1)
            scene.play(Create(caja), FadeIn(t), run_time=0.5)
            copias = [m.copy() for m, _ in sel]
            dest = VGroup(*[c.copy() for c in copias]).arrange(RIGHT, buff=0.4).move_to(caja)
            scene.play(*[c.animate.move_to(d) for c, d in zip(copias, dest)])
            vals = [abs(n) for _, n in sel]
            s = MathTex(" + ".join(map(str, vals)), "=", str(sum(vals)), font_size=40, color=col)
            scene.play(Write(s.next_to(caja, DOWN, buff=0.25)))
    else:
        for sel, col, nombre, y in ((pos, POSITIVO, "positivos", 0.6), (neg, NEGATIVO, "negativos", -0.3)):
            vals = [abs(n) for _, n in sel]
            if len(vals) > 1:
                s = MathTex(r"\text{" + nombre + ": }", " + ".join(map(str, vals)), "=", str(sum(vals)),
                            font_size=44, color=col)
            else:
                s = MathTex(r"\text{" + nombre + ": }", str(vals[0]), font_size=44, color=col)
            s.move_to([0, y, 0])
            scene.play(*[Indicate(m, color=col) for m, _ in sel], Write(s))
    fin, p, n = tex_agrupado(nums, 60)
    fin.move_to([0, -2.2, 0])
    scene.play(Write(fin))
    r = p - n
    if r == 0:
        txt = "iguales: se anulan → 0"
    else:
        txt = f"distinto signo: {max(p, n)} {MENOS} {min(p, n)} = {abs(r)}, signo del mayor ({'+' if r > 0 else MENOS})"
    scene.play(FadeIn(texto(txt, 24, GREY_B).next_to(fin, DOWN, buff=0.3)), Circumscribe(fin[3], color=ACENTO))
    scene.wait(2.5)


# --- 5. Multiplicaciones y divisiones
def tabla_signos(esq, lado=0.8):
    tabla, celdas = VGroup(), {}
    datos = [[r"\cdot", "+", "-"], ["+", "+", "-"], ["-", "-", "+"]]
    for i, fila in enumerate(datos):
        for j, s in enumerate(fila):
            sq = Square(lado, stroke_color=GREY_B, stroke_width=2).move_to(esq + np.array([j * lado, -i * lado, 0]))
            col = ACENTO
            if i and j:
                col = POSITIVO if s == "+" else NEGATIVO
                sq.set_fill(col, 0.25)
            c = VGroup(sq, MathTex(s, font_size=44, color=col).move_to(sq))
            tabla.add(c)
            celdas[(i, j)] = c
    return tabla, celdas


def resolver_muldiv(scene, items, letras, ejemplo=False):
    if ejemplo:
        a, op, b = items[0]
        tabla, celdas = tabla_signos(np.array([3.2, 1.4, 0]))
        scene.play(FadeIn(tabla))
        m = tex_muldiv(a, op, b)
        m.scale(1.2).move_to([-2.5, 1.0, 0])
        scene.play(Write(m[0]))
        fi = 1 if a > 0 else 2
        co = 1 if b > 0 else 2
        guia = VGroup(SurroundingRectangle(celdas[(fi, 0)], color=WHITE, buff=0.03),
                      SurroundingRectangle(celdas[(0, co)], color=WHITE, buff=0.03))
        scene.play(Create(guia))
        scene.play(Indicate(celdas[(fi, co)], scale_factor=1.3))
        p1 = texto("1.º  El signo: " + pista_muldiv(a, op, b).split(";")[0], 26, ACENTO).move_to([-2.5, -0.4, 0])
        p2 = texto("2.º  Los números:" + pista_muldiv(a, op, b).split(";")[1], 26, ACENTO).next_to(p1, DOWN, buff=0.3)
        p2.align_to(p1, LEFT)
        scene.play(FadeIn(p1))
        scene.play(FadeIn(p2))
        scene.play(Write(m[1]), Circumscribe(m[1], color=ACENTO))
        scene.wait(2.5)
        return
    filas = []
    for (a, op, b), l in zip(items, letras):
        m = VGroup(MathTex(rf"\text{{{l})}}", font_size=42), tex_muldiv(a, op, b)).arrange(RIGHT, buff=0.25)
        filas.append((m, pista_muldiv(a, op, b)))
    filas_resultado(scene, filas, y0=2.2, dy=1.0, x_pista=0.6)


# --- 6. Problemas
def problema_temperatura(scene):
    enun = texto(f"A las 6 h hace {MENOS}4 °C. A mediodía sube 11 grados y por la noche baja 9.", 26)
    enun.move_to([0, 2.6, 0])
    scene.play(Write(enun))
    cx, tmin, tmax, alto, base_y = -4.5, -10, 10, 4.0, -2.4

    def y(t):
        return base_y + (t - tmin) / (tmax - tmin) * alto

    tubo = RoundedRectangle(width=0.45, height=alto + 0.4, corner_radius=0.22).move_to([cx, base_y + alto / 2, 0])
    bulbo = Circle(radius=0.36, color=WHITE, fill_color="#E74C3C", fill_opacity=1).move_to([cx, base_y - 0.45, 0])
    marcas = VGroup()
    for t in range(tmin, tmax + 1, 5):
        m = Line([cx - 0.22, y(t), 0], [cx - 0.4, y(t), 0], stroke_width=2)
        marcas.add(m, Text(fmt_entero(t, False), font_size=18, color=color_entero(t)).next_to(m, LEFT, buff=0.08))
    temp = ValueTracker(-4)
    merc = always_redraw(lambda: Rectangle(width=0.2, height=max(0.01, y(temp.get_value()) - base_y + 0.2),
                                           fill_color="#E74C3C", fill_opacity=1, stroke_width=0)
                         .move_to([cx, (y(temp.get_value()) + base_y - 0.2) / 2, 0]))
    lect = always_redraw(lambda: Text(f"{fmt_entero(round(temp.get_value()))} °C", font_size=30,
                                      color=color_entero(round(temp.get_value())))
                         .move_to([cx + 1.3, y(temp.get_value()), 0]))
    scene.play(Create(tubo), FadeIn(bulbo), FadeIn(marcas))
    scene.add(merc, lect)
    pasos = [("6 h", None, -4), ("mediodía: sube 11", 11, 7), ("noche: baja 9", -9, -2)]
    expr_partes = []
    col_x = 0.2
    for i, (nombre, cambio, valor) in enumerate(pasos):
        if cambio is not None:
            scene.play(temp.animate.set_value(valor), run_time=1.8)
        t = texto(f"{nombre}  →  {fmt_entero(valor)} °C", 26, color_entero(valor)).move_to([col_x, 1.4 - i * 0.7, 0],
                                                                                              aligned_edge=LEFT)
        scene.play(FadeIn(t))
    e = MathTex("-4", "+11", "-9", "=", "-2", font_size=58).move_to([2.6, -1.3, 0])
    for i, n in ((0, -4), (1, 11), (2, -9), (4, -2)):
        e[i].set_color(color_entero(n))
    scene.play(Write(e))
    sol = texto(f"Por la noche hace {MENOS}2 °C", 30, ACENTO).next_to(e, DOWN, buff=0.4)
    scene.play(FadeIn(sol), Circumscribe(e[4], color=ACENTO))
    scene.wait(2.5)
    scene.remove(merc, lect)


def problema_banco(scene):
    enun = texto("Tienes 50 € y pagas 3 cuotas de 20 €. ¿Cuánto dinero te queda?", 28).move_to([0, 2.6, 0])
    scene.play(Write(enun))
    cx, base, k = -4.3, -0.7, 0.04
    eje = Line([cx - 1.3, base, 0], [cx + 1.3, base, 0], stroke_width=3)
    cero = texto("0 €", 20).next_to(eje, RIGHT, buff=0.1)
    saldo = ValueTracker(50)
    barra = always_redraw(lambda: Rectangle(
        width=0.9, height=max(0.01, abs(saldo.get_value()) * k), stroke_width=0,
        fill_color=POSITIVO if saldo.get_value() >= 0 else NEGATIVO, fill_opacity=0.85)
        .move_to([cx, base + saldo.get_value() * k / 2, 0]))
    lab = always_redraw(lambda: Text(f"{fmt_entero(round(saldo.get_value()))} €", font_size=26,
                                     color=color_entero(round(saldo.get_value())))
                        .move_to([cx - 1.35, base + saldo.get_value() * k, 0]))
    scene.play(Create(eje), FadeIn(cero))
    scene.add(barra, lab)
    for v in (30, 10, -10):
        scene.play(saldo.animate.set_value(v), run_time=0.9)
        scene.wait(0.2)
    lineas = VGroup(
        MathTex("50", "+", r"3 \cdot (-20)", font_size=52),
        MathTex("=", "50", "+", "(-60)", font_size=52),
        MathTex("=", "-10", font_size=52),
    )
    lineas[0][0].set_color(POSITIVO)
    lineas[0][2].set_color(NEGATIVO)
    lineas[1][1].set_color(POSITIVO)
    lineas[1][3].set_color(NEGATIVO)
    lineas[2][1].set_color(NEGATIVO)
    lineas.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.2, 0.4, 0])
    nota = texto("pagar = número negativo", 22, GREY_B).next_to(lineas[0], UP, buff=0.25).align_to(lineas[0], LEFT)
    scene.play(FadeIn(nota))
    for l in lineas:
        scene.play(Write(l))
    sol = texto("Te quedan −10 €: ¡debes 10 €!", 30, ACENTO).move_to([2.2, -2.2, 0])
    scene.play(FadeIn(sol))
    scene.wait(2.5)
    scene.remove(barra, lab)


def problema_arquimedes(scene):
    enun = texto("Arquímedes nació en el año 287 a.C. y murió en el 212 a.C.\n¿Cuántos años vivió?", 26)
    enun.move_to([0, 2.5, 0])
    scene.play(Write(enun))
    linea = NumberLine(x_range=[-300, 50, 50], length=12.5, include_tip=False, stroke_width=3).move_to([0, -0.4, 0])
    etiquetas = VGroup()
    for v in range(-300, 51, 50):
        s = "0" if v == 0 else (f"{-v} a.C." if v < 0 else f"{v} d.C.")
        etiquetas.add(Text(s, font_size=18, color=color_entero(v)).next_to(linea.n2p(v), DOWN, buff=0.2))
    nota = texto("Los años antes de Cristo (a.C.) son negativos", 24, GREY_B).move_to([0, 1.4, 0])
    scene.play(Create(linea), FadeIn(etiquetas), FadeIn(nota))
    d1 = Dot(linea.n2p(-287), radius=0.12, color=NEGATIVO)
    d2 = Dot(linea.n2p(-212), radius=0.12, color=NEGATIVO)
    t1 = texto(f"nace: {MENOS}287", 22, NEGATIVO).next_to(d1, UP, buff=0.25)
    t2 = texto(f"muere: {MENOS}212", 22, NEGATIVO).next_to(d2, UP, buff=0.25)
    scene.play(FadeIn(d1, scale=2), FadeIn(t1))
    scene.play(FadeIn(d2, scale=2), FadeIn(t2))
    br = BraceBetweenPoints(linea.n2p(-287), linea.n2p(-212), DOWN).shift(DOWN * 0.55)
    bt = texto("75 años", 26, ACENTO).next_to(br, DOWN, buff=0.1)
    e = MathTex(r"\text{muerte} - \text{nacimiento} =", "-212", "-", "(-287)", "=", "-212", "+287", "=", "75",
                font_size=44).to_edge(DOWN, buff=0.4)
    for i in (1, 3, 5):
        e[i].set_color(NEGATIVO)
    e[6].set_color(POSITIVO)
    e[8].set_color(ACENTO)
    scene.play(Write(e), run_time=2)
    scene.play(GrowFromCenter(br), FadeIn(bt), Circumscribe(e[8], color=ACENTO))
    scene.wait(3)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Operaciones con números enteros")
        pagina_enunciados(self, cab, ENUN_1)
        pagina_enunciados(self, cab, ENUN_2)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        resolver_sumas(self, SUMAS[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        resolver_restas(self, RESTAS[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 3 a)")
        resolver_parentesis(self, PARENTESIS[0], "a")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 4 a)")
        resolver_combinada(self, COMBINADAS[0], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 a)")
        resolver_muldiv(self, MULDIV[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        problema_temperatura(self)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Operaciones con números enteros")

        subtitulo(self, cab, "Ejercicio 1: b) a f)")
        resolver_sumas(self, SUMAS[1:], "bcdef")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2: b) a e)")
        resolver_restas(self, RESTAS[1:], "bcde")
        limpiar(self, cab)
        for letra, item in zip("bc", PARENTESIS[1:]):
            subtitulo(self, cab, f"Ejercicio 3 {letra})")
            resolver_parentesis(self, item, letra)
            limpiar(self, cab)
        for letra, nums in zip("bc", COMBINADAS[1:]):
            subtitulo(self, cab, f"Ejercicio 4 {letra})")
            resolver_combinada(self, nums, letra)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5: b) a f)")
        resolver_muldiv(self, MULDIV[1:], "bcdef")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 b)")
        problema_banco(self)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 c)")
        problema_arquimedes(self)
        limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes operar con números enteros.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
