"""Tema 10 · Jerarquía de las operaciones (1º ESO)

Escenas:
    PorQueUnOrden      – 2 + 3 · 4: dos resultados distintos; el ticket (14 €); la escalera de prioridades
    MismoNivel         – 12 : 3 · 2 = 8 y 10 − 4 + 3 = 9: de izquierda a derecha
    Parentesis         – (2 + 3) · 4 frente a 2 + 3 · 4; corchetes: de dentro hacia fuera
    PasoAPaso          – 18 − 2 · 3² + (7 − 3) · 5 y un ejemplo con enteros
    ErroresTipicos     – cuatro errores frecuentes con su versión buena
    EjerciciosEjemplo  – enunciados (2 páginas) + primer apartado de cada ejercicio
    EjerciciosResueltos – el resto

Los pasos NO se escriben a mano: `parse` convierte la expresión en un árbol y `siguientes` elige qué toca
(paréntesis → potencias y raíces → multiplicaciones y divisiones → sumas y restas, de izquierda a derecha).
La operación que toca se marca con una caja amarilla y el resultado baja a la línea siguiente.

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t10_jerarquia.py PasoAPaso
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t10_jerarquia.py
"""
import os
import re
import sys
from math import isqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 10 · Jerarquía de las operaciones"
TITULOS = {
    "PorQueUnOrden": "¿Por qué hace falta un orden?",
    "MismoNivel": "Mismo nivel: de izquierda a derecha",
    "Parentesis": "Paréntesis y corchetes",
    "PasoAPaso": "Resolver paso a paso",
    "ErroresTipicos": "Errores típicos",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

ROSA = "#FF79C6"
NIVELES = [  # (nombre, color)
    ("Paréntesis y corchetes", "#FF79C6"),
    ("Potencias y raíces", "#5DADE2"),
    ("Multiplicaciones y divisiones", "#7BD88F"),
    ("Sumas y restas", "#FF9F43"),
]


# ---------------------------------------------------------------------------
# Utilidades de escena
def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


class Notas:
    """Una sola nota a la vez en la parte de abajo."""

    def __init__(self, scene, size=26, color=ACENTO, buff=0.35):
        self.scene, self.size, self.color, self.buff, self.actual = scene, size, color, buff, None

    def __call__(self, cadena_txt, color=None):
        nueva = texto(cadena_txt, self.size, color or self.color)
        if nueva.width > config.frame_width - 1.0:
            nueva.scale_to_fit_width(config.frame_width - 1.0)
        nueva.to_edge(DOWN, buff=self.buff)
        if self.actual:
            self.scene.play(FadeOut(self.actual), FadeIn(nueva), run_time=0.5)
        else:
            self.scene.play(FadeIn(nueva), run_time=0.5)
        self.actual = nueva

    def fin(self):
        if self.actual:
            self.scene.play(FadeOut(self.actual), run_time=0.4)
            self.actual = None


# ---------------------------------------------------------------------------
# Expresiones: árbol, análisis y pasos
class Nodo:
    def __init__(self, tipo, **kw):
        self.tipo = tipo  # 'num' | 'bin' | 'pow' | 'raiz' | 'par'
        self.__dict__.update(kw)


def Num(v):
    return Nodo("num", v=v)


def parse(s):
    """'18-2*3^2+(7-3)*5', 'sqrt(49)', '[ ]' para corchetes, ':' división, '-3' negativo al empezar."""
    tokens = re.findall(r"sqrt|\d+|[-+*:^()\[\]]", s.replace(" ", ""))
    pos = [0]

    def ver():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def tomar(esperado=None):
        t = tokens[pos[0]]
        assert esperado is None or t == esperado, (t, esperado, s)
        pos[0] += 1
        return t

    def expr(inicio=True):
        nodo = termino(inicio)
        while ver() in ("+", "-"):
            op = tomar()
            nodo = Nodo("bin", op=op, a=nodo, b=termino(False))
        return nodo

    def termino(inicio):
        nodo = factor(inicio)
        while ver() in ("*", ":"):
            op = tomar()
            nodo = Nodo("bin", op=op, a=nodo, b=factor(False))
        return nodo

    def factor(inicio):
        base = primario(inicio)
        if ver() == "^":
            tomar()
            return Nodo("pow", b=base, e=int(tomar()))
        return base

    def primario(inicio):
        t = ver()
        if t == "-" and inicio:          # número negativo al principio de una expresión o paréntesis
            tomar()
            return Num(-int(tomar()))
        if t == "sqrt":
            tomar()
            tomar("(")
            x = expr()
            tomar(")")
            return Nodo("raiz", x=x)
        if t in ("(", "["):
            cierre = ")" if t == "(" else "]"
            tomar()
            x = expr()
            tomar(cierre)
            return simplificar(Nodo("par", x=x, br=t))
        return Num(int(tomar()))

    arbol = expr()
    assert pos[0] == len(tokens), s
    return arbol


def simplificar(n):
    """Un paréntesis con solo un número dentro desaparece (el número ya lleva su signo)."""
    if n.tipo == "par" and n.x.tipo == "num":
        return n.x
    return n


def hijos(n):
    return {"num": [], "bin": [n.a, n.b] if n.tipo == "bin" else [], "pow": [n.b] if n.tipo == "pow" else [],
            "raiz": [n.x] if n.tipo == "raiz" else [], "par": [n.x] if n.tipo == "par" else []}[n.tipo]


def es_num(n):
    return n.tipo == "num"


def valor(n):
    if n.tipo == "num":
        return n.v
    if n.tipo == "par":
        return valor(n.x)
    if n.tipo == "pow":
        return valor(n.b) ** n.e
    if n.tipo == "raiz":
        v = valor(n.x)
        r = isqrt(v)
        assert r * r == v
        return r
    a, b = valor(n.a), valor(n.b)
    if n.op == "+":
        return a + b
    if n.op == "-":
        return a - b
    if n.op == "*":
        return a * b
    assert a % b == 0, "división no exacta"
    return a // b


def nivel_de(n):
    return {"pow": 1, "raiz": 1}.get(n.tipo, 2 if n.tipo == "bin" and n.op in "*:" else 3)


def reducibles(n, fuera_de_par=True):
    """Nodos con todos los hijos numéricos (sin entrar en paréntesis)."""
    res = []
    if n.tipo == "par":
        return res
    if n.tipo in ("bin", "pow", "raiz") and all(es_num(h) for h in hijos(n)):
        res.append(n)
    for h in hijos(n):
        res += reducibles(h)
    return res


def pars_internos(n):
    """Paréntesis que tienen operaciones dentro y ningún paréntesis con operaciones."""
    res = []
    for h in hijos(n):
        res += pars_internos(h)
    if n.tipo == "par" and not res:
        res.append(n)
    return res


def siguientes(arbol):
    """Lista de nodos que se calculan a la vez en el siguiente paso, y el nivel (0..3)."""
    pars = pars_internos(arbol)
    ambitos = [p.x for p in pars] if pars else [arbol]
    objetivo = []
    nivel_min = None
    for amb in ambitos:
        cand = reducibles(amb) if amb.tipo != "num" else []
        if not cand:
            continue
        m = min(nivel_de(c) for c in cand)
        elegidos = [c for c in cand if nivel_de(c) == m]
        if m == 3:  # sumas y restas: solo la de más a la izquierda de cada ámbito
            elegidos = elegidos[:1]
        objetivo += elegidos
        nivel_min = m if nivel_min is None else min(nivel_min, m)
    return objetivo, (0 if pars else nivel_min)


def reducir(n, objetivos, nuevos):
    if any(n is o for o in objetivos):
        r = Num(valor(n))
        nuevos.append(r)
        return r
    if n.tipo == "bin":
        n2 = Nodo("bin", op=n.op, a=reducir(n.a, objetivos, nuevos), b=reducir(n.b, objetivos, nuevos))
    elif n.tipo == "pow":
        n2 = Nodo("pow", b=reducir(n.b, objetivos, nuevos), e=n.e)
    elif n.tipo == "raiz":
        n2 = Nodo("raiz", x=reducir(n.x, objetivos, nuevos))
    elif n.tipo == "par":
        n2 = simplificar(Nodo("par", x=reducir(n.x, objetivos, nuevos), br=n.br))
    else:
        n2 = n
    return n2


OPS = {"+": " + ", "-": " - ", "*": r" \cdot ", ":": " : "}


def trozos(n, marcados, inicio=True):
    """Lista de (tex, marcado) para pintar la expresión con algunos nodos separados."""
    if any(n is m for m in marcados):
        return [(tex(n, inicio), True)]
    if n.tipo == "num":
        return [(tex(n, inicio), False)]
    if n.tipo == "bin":
        return trozos(n.a, marcados, inicio) + [(OPS[n.op], False)] + trozos(n.b, marcados, False)
    if n.tipo == "par":
        a, c = ("(", ")") if n.br == "(" else ("[", "]")
        return [(a, False)] + trozos(n.x, marcados, True) + [(c, False)]
    if n.tipo == "pow" and n.b.tipo == "par":
        return [("(", False)] + trozos(n.b.x, marcados, True) + [(")^{" + str(n.e) + "}", False)]
    return [(tex(n, inicio), False)]


def tex(n, inicio=True):
    if n.tipo == "num":
        return str(n.v) if (n.v >= 0 or inicio) else f"({n.v})"
    if n.tipo == "bin":
        return tex(n.a, inicio) + OPS[n.op] + tex(n.b, False)
    if n.tipo == "par":
        a, c = ("(", ")") if n.br == "(" else ("[", "]")
        return a + tex(n.x, True) + c
    if n.tipo == "pow":
        b = f"({n.b.v})" if n.b.tipo == "num" and n.b.v < 0 else tex(n.b, True)
        return b + "^{" + str(n.e) + "}"
    return r"\sqrt{" + tex(n.x, True) + "}"


def linea(n, marcados, size, color_marca=None):
    """MathTex con '=' delante; devuelve (mobject, lista de submobjects marcados)."""
    partes = [("=", False)] + trozos(n, marcados)
    # juntar trozos seguidos no marcados
    juntos = []
    for t, m in partes:
        if len(juntos) > 1 and not m and not juntos[-1][1]:   # el '=' (índice 0) siempre va aparte
            juntos[-1] = (juntos[-1][0] + t, False)
        else:
            juntos.append((t, m))
    mt = MathTex(*[t for t, _ in juntos], font_size=size)
    marcas = [mt[i] for i, (_, m) in enumerate(juntos) if m]
    if color_marca:
        for m in marcas:
            m.set_color(color_marca)
    return mt, marcas


def resolver(scene, expr_s, x, y0, size=44, dy=0.68, notas=None, ejemplo=False, etiqueta=None, rt=None):
    """Resuelve la expresión línea a línea. Devuelve (VGroup de líneas, valor final)."""
    rt = rt or (1.0 if ejemplo else 0.7)
    arbol = parse(expr_s)
    l0, _ = linea(arbol, [], size)
    l0[0].set_opacity(0)
    l0.move_to([x, y0, 0], aligned_edge=LEFT)
    lineas = VGroup(l0)
    if etiqueta:
        et = texto(etiqueta, 28).next_to(l0, LEFT, buff=0.25)
        et.shift(RIGHT * (l0[0].width + 0.1))
        scene.play(FadeIn(et), run_time=0.3)
        lineas.add(et)
    scene.play(Write(l0), run_time=rt)
    actual, y = l0, y0
    while arbol.tipo != "num":
        objetivos, nivel = siguientes(arbol)
        nombre, col = NIVELES[nivel]
        # misma línea, partida para poder marcar
        partida, marcas = linea(arbol, objetivos, size)
        partida.move_to(actual, aligned_edge=LEFT)
        if actual is l0:
            partida[0].set_opacity(0)
        scene.remove(actual)
        scene.add(partida)
        if actual is l0:
            lineas.submobjects[0] = partida
        else:
            lineas.submobjects[-1] = partida
        actual = partida
        cajas = VGroup(*[SurroundingRectangle(m, color=ACENTO, buff=0.06, stroke_width=3) for m in marcas])
        anims = [Create(cajas)]
        if notas:
            extra = "" if nivel in (0, 1) else ": de izquierda a derecha"
            notas(("Primero, dentro de los paréntesis" if nivel == 0 else nombre) + extra, color=col)
        scene.play(*anims, run_time=0.5)
        if ejemplo:
            scene.wait(0.8)
        nuevos = []
        arbol = reducir(arbol, objetivos, nuevos)
        y -= dy
        nueva, res_marcas = linea(arbol, nuevos, size, color_marca=ACENTO)
        nueva.move_to([x, y, 0], aligned_edge=LEFT)
        nueva.align_to(l0, LEFT)
        resto = VGroup(*[p for p in nueva if not any(p is r for r in res_marcas)])
        anims = [Write(resto)] + [ReplacementTransform(m.copy(), r) for m, r in zip(marcas, res_marcas)]
        scene.play(*anims, run_time=rt)
        scene.add(nueva)
        scene.play(FadeOut(cajas), run_time=0.3)
        lineas.add(nueva)
        actual = nueva
        if ejemplo:
            scene.wait(0.6)
    scene.play(Circumscribe(actual[1:], color=ACENTO), run_time=0.7)
    if notas:
        notas.fin()
    return lineas, arbol.v


def tachar(scene, m):
    """Raya roja encima de una expresión equivocada y una ✗ al lado (se sigue leyendo)."""
    raya = Line(m.get_left() + LEFT * 0.1, m.get_right() + RIGHT * 0.1, color=MAL, stroke_width=4)
    x = MathTex(r"\times", font_size=int(m.height * 110) + 20, color=MAL).next_to(m, RIGHT, buff=0.3)
    scene.play(Create(raya), FadeIn(x, scale=1.5))
    return VGroup(raya, x)


def escalera(size=26, ancho=5.6):
    """Los cuatro niveles de prioridad como escalones."""
    g = VGroup()
    for i, (nombre, col) in enumerate(NIVELES):
        t = texto(f"{i + 1}.º  {nombre}", size, col)
        r = RoundedRectangle(width=max(ancho, t.width + 0.5), height=max(0.62, t.height + 0.3), corner_radius=0.12,
                             stroke_color=col, fill_color=col, fill_opacity=0.18)
        t.move_to(r)
        g.add(VGroup(r, t))
    g.arrange(DOWN, buff=0.15)
    for i, e in enumerate(g):
        e.shift(RIGHT * 0.35 * i)
    return g


# ===========================================================================
class PorQueUnOrden(Scene):
    def construct(self):
        cab = titulo(self, "Jerarquía de las operaciones", "¿Por qué hace falta un orden?")
        e = MathTex(r"2 + 3 \cdot 4", font_size=80).move_to([0, 2.0, 0])
        self.play(Write(e))
        a = VGroup(texto("Ana: de izquierda a derecha", 26, NEGATIVO),
                   MathTex(r"2 + 3 = 5", font_size=48), MathTex(r"5 \cdot 4 = 20", font_size=48),
                   ).arrange(DOWN, buff=0.25).move_to([-3.5, -0.2, 0])
        b = VGroup(texto("Luis: primero la multiplicación", 26, POSITIVO),
                   MathTex(r"3 \cdot 4 = 12", font_size=48), MathTex(r"2 + 12 = 14", font_size=48),
                   ).arrange(DOWN, buff=0.25).move_to([3.5, -0.2, 0])
        for g in (a, b):
            for m in g:
                self.play(FadeIn(m, shift=UP * 0.15), run_time=0.6)
        pregunta = texto("¿20 o 14? ¡Una misma cuenta no puede dar dos resultados!", 28, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(pregunta))
        self.wait(2)
        limpiar(self, cab)

        # El ticket
        subtitulo(self, cab, "Un ejemplo de verdad")
        ticket = VGroup(texto("1 entrada ............ 2 €", 28), texto("3 refrescos ......... 4 € cada uno", 28))
        ticket.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 1.5, 0])
        marco = SurroundingRectangle(ticket, color=GREY_B, buff=0.35, corner_radius=0.1)
        self.play(Create(marco), FadeIn(ticket))
        cuenta = MathTex(r"2", r"+", r"3 \cdot 4", r"= 2 + 12 = 14 \text{ €}", font_size=56).move_to([0, -0.1, 0])
        cuenta[2].set_color(ACENTO)
        self.play(Write(cuenta[:3]))
        nota = texto("3 · 4 son los refrescos: se calcula antes de sumar", 24, ACENTO).next_to(cuenta, DOWN, buff=0.3)
        self.play(FadeIn(nota), Indicate(cuenta[2]))
        self.play(Write(cuenta[3]))
        ok = texto("¡Luis tenía razón! 14 € es lo que pagas", 28, OK).move_to([0, -2.0, 0])
        self.play(FadeIn(ok))
        self.wait(2)
        limpiar(self, cab)

        # La escalera
        subtitulo(self, cab, "El orden que siempre se sigue")
        esc = escalera(28, 7.0).move_to([0, -0.1, 0])
        for e in esc:
            self.play(FadeIn(e, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.4)
        nota = texto("Si hay dos del mismo escalón: de izquierda a derecha", 26, GREY_B).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(nota))
        self.wait(3)


# ===========================================================================
class MismoNivel(Scene):
    def construct(self):
        cab = titulo(self, "Mismo nivel", "De izquierda a derecha")
        notas = Notas(self)
        esc = escalera(20, 4.4).scale(0.9).to_corner(UR).shift(DOWN * 0.7)
        self.play(FadeIn(esc))
        self.play(Indicate(esc[2], scale_factor=1.05))
        resolver(self, "12:3*2", -6.0, 1.6, size=60, dy=0.9, notas=notas, ejemplo=True)
        mal = VGroup(MathTex(r"12 : 3 \cdot 2 \neq 12 : 6 = 2", font_size=44, color=MAL))
        mal.move_to([-2.4, -1.4, 0])
        self.play(FadeIn(mal))
        cruz = tachar(self, mal)
        exp = texto("La división va primero porque está a la izquierda", 26, MAL).next_to(mal, DOWN, buff=0.25)
        self.play(FadeIn(exp))
        self.wait(2)
        limpiar(self, cab)

        subtitulo(self, cab, "Sumas y restas: igual")
        esc = escalera(20, 4.4).scale(0.9).to_corner(UR).shift(DOWN * 0.7)
        self.add(esc)
        self.play(Indicate(esc[3], scale_factor=1.05))
        resolver(self, "10-4+3", -6.0, 1.6, size=60, dy=0.9, notas=notas, ejemplo=True)
        mal = MathTex(r"10 - 4 + 3 \neq 10 - 7 = 3", font_size=44, color=MAL).move_to([-2.4, -1.4, 0])
        self.play(FadeIn(mal))
        cruz = tachar(self, mal)
        exp = texto("Primero la resta, que está a la izquierda", 26, MAL).next_to(mal, DOWN, buff=0.25)
        self.play(FadeIn(exp))
        self.wait(3)


# ===========================================================================
class Parentesis(Scene):
    def construct(self):
        cab = titulo(self, "Paréntesis y corchetes")
        notas = Notas(self)
        intro = texto("Los paréntesis mandan: lo de dentro se hace primero", 28, ROSA)
        intro.next_to(cab, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(intro))
        resolver(self, "(2+3)*4", -6.2, 1.2, size=56, dy=0.85, notas=notas, ejemplo=True)
        resolver(self, "2+3*4", 0.8, 1.2, size=56, dy=0.85, notas=notas, ejemplo=True)
        dif = texto("Los mismos números, distinto resultado: el paréntesis cambia el orden", 26, ACENTO)
        dif.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(dif))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Corchetes: un paréntesis por fuera")
        cajas = texto("Como cajas una dentro de otra: se abren de dentro hacia fuera", 26, GREY_B)
        cajas.next_to(cab, DOWN, buff=0.7).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(cajas))
        resolver(self, "2*[10-(3+1)]", -4.0, 1.0, size=64, dy=1.0, notas=notas, ejemplo=True)
        self.wait(2.5)


# ===========================================================================
class PasoAPaso(Scene):
    def construct(self):
        cab = titulo(self, "Resolver paso a paso")
        notas = Notas(self)
        esc = escalera(20, 4.4).scale(0.9).to_corner(UR).shift(DOWN * 0.6)
        self.play(FadeIn(esc))
        resolver(self, "18-2*3^2+(7-3)*5", -6.2, 2.1, size=54, dy=0.82, notas=notas, ejemplo=True)
        truco = texto("Truco: copia lo que no toca\nsin cambiarlo", 24, GREY_B).next_to(esc, DOWN, buff=0.5)
        self.play(FadeIn(truco))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Con números enteros")
        recuerda = texto("Recuerda los signos: (+)·(−) = −   (−):(+) = −   restar es sumar el opuesto", 24, GREY_B)
        recuerda.next_to(cab, DOWN, buff=0.7).to_edge(LEFT, buff=0.6)
        self.play(FadeIn(recuerda))
        resolver(self, "-3+4*(-2)-(-10):5", -6.2, 1.2, size=54, dy=0.85, notas=notas, ejemplo=True)
        self.wait(3)


# ===========================================================================
class ErroresTipicos(Scene):
    def construct(self):
        cab = titulo(self, "Errores típicos")
        errores = [
            (r"5 + 4 \cdot 3 = 9 \cdot 3 = 27", r"5 + 4 \cdot 3 = 5 + 12 = 17", "Sumar antes de multiplicar"),
            (r"12 : 2 \cdot 3 = 12 : 6 = 2", r"12 : 2 \cdot 3 = 6 \cdot 3 = 18", "Multiplicar antes de dividir"),
            (r"20 - 5 + 3 = 20 - 8 = 12", r"20 - 5 + 3 = 15 + 3 = 18", "Sumar antes de restar"),
            (r"-2^2 = 4", r"-2^2 = -4 \quad (-2)^2 = 4", "Olvidar que el − no es de la base"),
        ]
        for mal_s, bien_s, nombre in errores:
            # comprobación de los resultados buenos con el motor
            n = texto(nombre, 30, ACENTO).next_to(cab, DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
            mal = MathTex(mal_s, font_size=56, color=MAL).move_to([0, 0.7, 0])
            bien = MathTex(bien_s, font_size=56, color=OK).move_to([0, -1.0, 0])
            ok = MathTex(r"\checkmark", font_size=56, color=OK).next_to(bien, RIGHT, buff=0.3)
            self.play(FadeIn(n))
            self.play(Write(mal))
            cruz = tachar(self, mal)
            self.play(Write(bien), FadeIn(ok))
            self.wait(2)
            self.play(FadeOut(VGroup(n, mal, cruz, bien, ok)))
        resumen = escalera(28, 7.0).move_to([0, -0.2, 0])
        self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.3) for e in resumen], lag_ratio=0.25))
        self.wait(3)


# Comprobación de los ejemplos fijos de ErroresTipicos (si el motor no da lo mismo, falla al importar)
assert valor(parse("5+4*3")) == 17 and valor(parse("12:2*3")) == 18 and valor(parse("20-5+3")) == 18
assert valor(parse("(-2)^2")) == 4


# ===========================================================================
# EJERCICIOS
# ===========================================================================
SIN_PARENTESIS = ["5+4*3", "20-12:4", "6*2-3*3", "18:3*2", "15-6+2"]
CON_PARENTESIS = ["(5+4)*3", "20-(12-4)", "(18:3)*(7-5)", "2*[15-(4+6)]"]
CON_POTENCIAS = ["3+2^3", "4*5^2", "50-6^2:4", "sqrt(49)+3*2^2", "(2+3)^2-2^2-3^2"]
CON_ENTEROS = ["-6+3*(-4)", "10-(-8):2", "(-2)^3+5*2", "-3*(5-9)+(-1)^4"]
PON_PARENTESIS = [("2+3*5", 25, "(2+3)*5"), ("12-4-2", 10, "12-(4-2)"), ("24:4+2", 4, "24:(4+2)")]
PROBLEMAS = [
    ("a) Compras 3 libretas de 2 € y 2 bolis de 1 €. ¿Cuánto pagas?", "3*2+2*1", "€"),
    ("b) 4 amigos pagan a partes iguales una pizza de 30 € y 6 € de bebidas.\n"
     "     ¿Cuánto paga cada uno?", "(30+6):4", "€"),
    ("c) A las 8 h hay −3 °C y la temperatura sube 2 °C cada hora durante 5 horas.\n"
     "     ¿Qué temperatura hay a las 13 h?", "-3+2*5", "°C"),
]
for _lista in (SIN_PARENTESIS, CON_PARENTESIS, CON_POTENCIAS, CON_ENTEROS):
    for _e in _lista:
        valor(parse(_e))  # que todas se puedan calcular (divisiones exactas, raíces exactas)
for _e, _v, _sol in PON_PARENTESIS:
    assert valor(parse(_sol)) == _v and valor(parse(_e)) != _v


def txt_expr(s):
    """Expresión del enunciado en texto plano (Text)."""
    t = s.replace("*", " · ").replace(":", " : ").replace("+", " + ").replace("-", " − ")
    t = re.sub(r"sqrt\((\d+)\)", r"√\1", t)
    t = re.sub(r"\^(\d)", lambda m: m.group(1).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")), t)
    t = re.sub(r"\( − ", "(−", t)
    t = re.sub(r"^ − ", "−", t)
    return re.sub(r"\s+", " ", t).strip()


def lista(items, por_linea=3):
    trozos_ = [f"{l}) {txt_expr(t)}" for l, t in zip("abcdef", items)]
    return "\n".join("      ".join(trozos_[i:i + por_linea]) for i in range(0, len(trozos_), por_linea))


def pagina_enunciados(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 28, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(cab, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
    if grupo.width > config.frame_width - 1.0:
        grupo.scale_to_fit_width(config.frame_width - 1.0).to_edge(LEFT, buff=0.5)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def enunciados_1():
    return [
        ("1. Calcula (sin paréntesis):", lista(SIN_PARENTESIS, 5)),
        ("2. Calcula (con paréntesis y corchetes):", lista(CON_PARENTESIS, 4)),
        ("3. Calcula (con potencias y raíces):", lista(CON_POTENCIAS, 3)),
        ("4. Calcula (con números enteros):", lista(CON_ENTEROS, 4)),
    ]


def enunciados_2():
    pon = "      ".join(f"{l}) {txt_expr(e)} = {v}" for l, (e, v, _) in zip("abc", PON_PARENTESIS))
    return [
        ("5. Pon paréntesis para que la igualdad sea cierta:", pon),
        ("6. Escribe UNA sola expresión y resuélvela:", "\n".join(p for p, _, _ in PROBLEMAS)),
    ]


def resolver_dos(scene, items, letras, notas, size=44, ys=(1.7, 1.7), xs=(-6.4, 0.4), dy=0.66):
    """Uno o dos apartados en columnas."""
    for e, l, x, y in zip(items, letras, xs, ys):
        resolver(scene, e, x + 0.55, y, size=size, dy=dy, notas=notas, etiqueta=f"{l})")
    scene.wait(1.2)


def pon_parentesis(scene, e, v, sol, letra, y, notas, ejemplo=False):
    lab = texto(f"{letra})", 30).move_to([-6.2, y, 0])
    sin = MathTex(tex(parse(e)), f"= {valor(parse(e))}", font_size=48).next_to(lab, RIGHT, buff=0.3)
    sin[1].set_color(MAL)
    scene.play(FadeIn(lab), Write(sin))
    if notas:
        notas(f"Sin paréntesis da {valor(parse(e))}, no {v}: hay que cambiar el orden")
    tachar(scene, sin[1])
    con = MathTex(tex(parse(sol)), f"= {v}", font_size=48).move_to([2.6, y, 0])
    con[1].set_color(OK)
    scene.play(Write(con))
    ok = MathTex(r"\checkmark", font_size=48, color=OK).next_to(con, RIGHT, buff=0.25)
    scene.play(FadeIn(ok), Circumscribe(con, color=ACENTO))
    if ejemplo:
        scene.wait(1.5)


def problema(scene, i, notas, ejemplo=False):
    enun, e, u = PROBLEMAS[i]
    t = texto(enun[3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    if t.width > config.frame_width - 1.0:
        t.scale_to_fit_width(config.frame_width - 1.0)
    scene.play(Write(t), run_time=1.5)
    _, v = resolver(scene, e, -2.5, 1.0, size=56, dy=0.85, notas=notas, ejemplo=ejemplo)
    v_txt = f"{MENOS}{abs(v)}" if v < 0 else str(v)
    sol = texto(f"Solución: {v_txt} {u}", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Jerarquía de las operaciones")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        for sub, lista_, y in (("Ejercicio 1 a)", SIN_PARENTESIS, 1.4), ("Ejercicio 2 a)", CON_PARENTESIS, 1.4),
                               ("Ejercicio 3 a)", CON_POTENCIAS, 1.4), ("Ejercicio 4 a)", CON_ENTEROS, 1.4)):
            subtitulo(self, cab, sub)
            resolver(self, lista_[0], -3.0, y, size=60, dy=0.95, notas=notas, ejemplo=True, etiqueta="a)")
            self.wait(1)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 a)")
        pon_parentesis(self, *PON_PARENTESIS[0], "a", 0.6, notas, ejemplo=True)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        problema(self, 0, notas, ejemplo=True)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Jerarquía de las operaciones")
        notas = Notas(self, size=24)
        pantallas = [
            ("Ejercicio 1: b) y c)", SIN_PARENTESIS[1:3], "bc"),
            ("Ejercicio 1: d) y e)", SIN_PARENTESIS[3:5], "de"),
            ("Ejercicio 2: b) y c)", CON_PARENTESIS[1:3], "bc"),
            ("Ejercicio 2 d)", CON_PARENTESIS[3:4], "d"),
            ("Ejercicio 3: b) y c)", CON_POTENCIAS[1:3], "bc"),
            ("Ejercicio 3: d) y e)", CON_POTENCIAS[3:5], "de"),
            ("Ejercicio 4: b) y c)", CON_ENTEROS[1:3], "bc"),
            ("Ejercicio 4 d)", CON_ENTEROS[3:4], "d"),
        ]
        for sub, items, letras in pantallas:
            subtitulo(self, cab, sub)
            resolver_dos(self, items, letras, notas)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5: b) y c)")
        pon_parentesis(self, *PON_PARENTESIS[1], "b", 1.0, notas)
        pon_parentesis(self, *PON_PARENTESIS[2], "c", -1.0, notas)
        notas.fin()
        self.wait(1.5)
        limpiar(self, cab)
        for i, sub in ((1, "Ejercicio 6 b)"), (2, "Ejercicio 6 c)")):
            subtitulo(self, cab, sub)
            problema(self, i, notas)
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes en qué orden se opera.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
