"""Tema 2 · Fracciones y números decimales (2º ESO)

Sigue el índice del libro: fracciones · suma y resta · multiplicación, división y potencias ·
operaciones combinadas con fracciones · fracciones y decimales · operaciones combinadas con decimales ·
raíces cuadradas con decimales · notación científica (números grandes).

Escenas:
    Fracciones             – repaso: qué es, de una cantidad, equivalentes, simplificar, negativas, comparar
    SumaResta              – mismo denominador, distinto (con barras), regla, ejemplos con enteros y negativos
    MultiplicarDividir     – modelo de área, simplificar antes de multiplicar, cuántas veces cabe, la inversa
    PotenciasFracciones    – (a/b)ⁿ, signos, el paréntesis importa, propiedades
    CombinadasFracciones   – jerarquía con fracciones (motor nuevo, con común denominador)
    FraccionesDecimales    – fracción → decimal, tipos, el truco del denominador, decimal exacto → fracción
    PorQuePeriodico (E1)   – extra: por qué el denominador decide (piezas de primos, restos de 1 : 7, otras escalas)
    FraccionGeneratriz     – decimal periódico → fracción: la regla, 3 + 3 ejemplos y por qué funciona (método de la x)
    CombinadasDecimales    – jerarquía con decimales; periódicos: mejor en fracción
    RaicesDecimales        – raíces exactas con decimales y aproximar √20 a las décimas y centésimas
    NotacionCientifica     – números grandes: a · 10ⁿ con 1 ≤ a < 10
    OperacionesNotacion    – producto, cociente, ajustar el resultado, sumas
    EjerciciosEjemplo      – enunciados (3 páginas) + primer apartado de cada ejercicio
    EjerciciosResueltos1   – ejercicios 1 a 7
    EjerciciosResueltos2   – ejercicios 9 a 13

Usa el estilo y algunas utilidades de 1ESO/Matematicas/codigo (temas 5, 8, 9 y 10).

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t02_fracciones_decimales.py SumaResta
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t02_fracciones_decimales.py
"""
import os
import re
import sys
from fractions import Fraction
from math import gcd, isqrt, lcm

COMUN = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "..", "..", "1ESO", "Matematicas", "codigo"))
sys.path.insert(0, COMUN)
from estilo import *  # noqa: E402,F403
from t05_fracciones import flecha_op, resolver_simplifica  # noqa: E402
from t08_operaciones_decimales import division_larga, periodico, COLOR_PERIODO, COLOR_ANTE  # noqa: E402
from t09_potencias_raices import Notas, limpiar, subtitulo  # noqa: E402
from t10_jerarquia import NIVELES, tachar, escalera, Nodo as Nd  # noqa: E402

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 2 · Fracciones y números decimales"
TITULOS = {
    "Fracciones": "Fracciones (repaso)",
    "SumaResta": "Suma y resta de fracciones",
    "MultiplicarDividir": "Multiplicación y división de fracciones",
    "PotenciasFracciones": "Potencias de fracciones",
    "CombinadasFracciones": "Operaciones combinadas con fracciones",
    "FraccionesDecimales": "Fracciones y números decimales",
    "PorQuePeriodico": "¿Por qué sale exacto o periódico?",
    "FraccionGeneratriz": "De decimal periódico a fracción",
    "CombinadasDecimales": "Operaciones combinadas con decimales",
    "RaicesDecimales": "Raíces cuadradas con decimales",
    "NotacionCientifica": "Notación científica: números grandes",
    "OperacionesNotacion": "Operaciones en notación científica",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos1": "Ejercicios resueltos (1 – 7)",
    "EjerciciosResueltos2": "Ejercicios resueltos (9 – 13)",
}
EXTRAS = {"PorQuePeriodico": "E2"}  # vídeos extra: etiqueta propia, no cuentan en la numeración
# páginas interactivas: (etiqueta, título, ruta desde 2ESO/Matematicas, escena tras la que va)
INTERACTIVOS = [("E1", "Pruébalo tú: M.C.D. y m.c.m.", "../../1ESO/Matematicas/interactivos/factores_mcd_mcm.html?m=mcm&a=4&b=6", "SumaResta")]

ROSA = "#FF79C6"
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


# ---------------------------------------------------------------------------
# Utilidades generales
def L(*partes, size=46):
    """Línea de cálculo: '=' en [0] y luego los trozos."""
    return M("=", *partes, size=size)


def pasos(scene, lineas, x, y0, dy=0.78, notas=None, ejemplo=False, etiqueta=None, final=True):
    """Escribe líneas una debajo de otra (alineadas a la izquierda). lineas: [(mobject con '=' en [0], nota)].
    La primera línea no enseña su '='. Devuelve el VGroup."""
    g = VGroup()
    rt = 0.9 if ejemplo else 0.7
    for i, (m, nota) in enumerate(lineas):
        m.move_to([x, y0 - i * dy, 0], aligned_edge=LEFT)
        if i == 0:
            m[0].set_opacity(0)
            if etiqueta:
                et = texto(etiqueta, 28).next_to(m[1], LEFT, buff=0.25)
                scene.play(FadeIn(et), run_time=0.3)
                g.add(et)
        scene.play(Write(m), run_time=rt)
        g.add(m)
        if nota and notas:
            notas(nota)
            scene.wait(1.5 if ejemplo else 0.6)
    if final:
        scene.play(Circumscribe(lineas[-1][0][1:], color=ACENTO), run_time=0.7)
    return g


def tarjeta(contenido, color=ACENTO, buff=0.3):
    r = SurroundingRectangle(contenido, color=color, buff=buff, corner_radius=0.15,
                             fill_color=color, fill_opacity=0.08)
    return VGroup(r, contenido)


def regla(*partes, frase, size=46, color=ACENTO):
    f = M(*partes, size=size)
    t = texto(frase, 24, GREY_B)
    return tarjeta(VGroup(f, t).arrange(DOWN, buff=0.25), color)


def fr(n, d):
    """\\dfrac con signo delante."""
    return ("-" if n < 0 else "") + rf"\dfrac{{{abs(n)}}}{{{d}}}"


def PF(n, d, e):
    """Potencia de fracción para M(): base (con paréntesis) azul y exponente rosa."""
    return [(r"\left(" + fr(n, d) + r"\right)", BASE), ("^{" + str(e) + "}", EXPONENTE)]


def ft(v, par=False):
    """Fracción en texto: 3/4, −3/4, 2."""
    v = Fraction(v)
    s = str(abs(v.numerator)) if v.denominator == 1 else f"{abs(v.numerator)}/{v.denominator}"
    if v < 0:
        s = MENOS + s
        if par:
            s = f"({s})"
    return s


def dec_str(v, tex=False):
    """Fraction con desarrollo decimal finito → '0,75' (o '0{,}75' para LaTeX)."""
    v = Fraction(v)
    k = 0
    while (v * 10 ** k).denominator != 1:
        k += 1
        assert k <= 8, f"{v} no es decimal exacto"
    n = abs(v.numerator * 10 ** k // v.denominator)
    s = str(n).rjust(k + 1, "0")
    if k:
        s = s[:-k] + "," + s[-k:]
    if v < 0:
        s = ("-" if tex else MENOS) + s
    return s.replace(",", "{,}") if tex else s


def raw_txt(n, d):
    if d == 1:
        return ft(n)
    return (MENOS if n * d < 0 else "") + f"{abs(n)}/{abs(d)}"


# ---------------------------------------------------------------------------
# Motor de operaciones combinadas con fracciones o decimales
# (el mismo orden que el tema 10 de 1º, pero los números son Fraction)
MODO = ["frac"]


def Num(v, disp=None, dec=False):
    return Nd("num", v=Fraction(v), disp=disp, dec=dec)


def parse_f(s):
    """'(1/2+1/3)*3/5-1/4', '2,5-1,2*0,5', 'sqrt(0,49)'. ':' es dividir; '/' solo escribe fracciones."""
    tokens = re.findall(r"sqrt|\d+,\d+|\d+/\d+|\d+|[-+*:^()\[\]]", s.replace(" ", ""))
    pos = [0]

    def ver():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def tomar(esperado=None):
        t = tokens[pos[0]]
        assert esperado is None or t == esperado, (t, esperado, s)
        pos[0] += 1
        return t

    def numero(t, signo=1):
        if "," in t:
            return Num(signo * Fraction(t.replace(",", ".")), dec=True)
        if "/" in t:
            n, d = map(int, t.split("/"))
            return Num(Fraction(signo * n, d), disp=(signo * n, d))
        return Num(signo * int(t))

    def expr(inicio=True):
        nodo = termino(inicio)
        while ver() in ("+", "-"):
            op = tomar()
            nodo = Nd("bin", op=op, a=nodo, b=termino(False))
        return nodo

    def termino(inicio):
        nodo = factor(inicio)
        while ver() in ("*", ":"):
            op = tomar()
            nodo = Nd("bin", op=op, a=nodo, b=factor(False))
        return nodo

    def factor(inicio):
        base = primario(inicio)
        if ver() == "^":
            tomar()
            return Nd("pow", b=base, e=int(tomar()))
        return base

    def primario(inicio):
        t = ver()
        if t == "-" and inicio:
            tomar()
            return numero(tomar(), -1)
        if t == "sqrt":
            tomar()
            tomar("(")
            x = expr()
            tomar(")")
            return Nd("raiz", x=x)
        if t in ("(", "["):
            cierre = ")" if t == "(" else "]"
            tomar()
            x = expr()
            tomar(cierre)
            return simplificar(Nd("par", x=x, br=t))
        return numero(tomar())

    arbol = expr()
    assert pos[0] == len(tokens), s
    return arbol


def simplificar(n):
    if n.tipo == "par" and n.x.tipo == "num":
        return n.x
    return n


def hijos(n):
    return {"num": lambda: [], "bin": lambda: [n.a, n.b], "pow": lambda: [n.b],
            "raiz": lambda: [n.x], "par": lambda: [n.x]}[n.tipo]()


def es_num(n):
    return n.tipo == "num"


def raiz_exacta(v):
    r = Fraction(isqrt(v.numerator), isqrt(v.denominator))
    assert r * r == v, f"raíz no exacta de {v}"
    return r


def valor(n):
    if n.tipo == "num":
        return n.v
    if n.tipo == "par":
        return valor(n.x)
    if n.tipo == "pow":
        return valor(n.b) ** n.e
    if n.tipo == "raiz":
        return raiz_exacta(valor(n.x))
    a, b = valor(n.a), valor(n.b)
    return {"+": a + b, "-": a - b, "*": a * b, ":": a / b if b else None}[n.op]


def nivel_de(n):
    return {"pow": 1, "raiz": 1}.get(n.tipo, 2 if n.tipo == "bin" and n.op in "*:" else 3)


def reducibles(n):
    res = []
    if n.tipo == "par":
        return res
    if n.tipo in ("bin", "pow", "raiz") and all(es_num(h) for h in hijos(n)):
        res.append(n)
    for h in hijos(n):
        res += reducibles(h)
    return res


def pars_internos(n):
    res = []
    for h in hijos(n):
        res += pars_internos(h)
    if n.tipo == "par" and not res:
        res.append(n)
    return res


def es_frac_disp(n):
    return n.tipo == "num" and not n.dec and (n.disp is not None or n.v.denominator != 1)


def tiene_frac(n):
    return es_frac_disp(n) or any(tiene_frac(h) for h in hijos(n))


def tex_num(n, inicio=True):
    if n.dec or (MODO[0] == "dec" and n.v.denominator != 1):
        s = dec_str(n.v, tex=True)
    elif es_frac_disp(n):
        a, b = n.disp or (n.v.numerator, n.v.denominator)
        s = fr(a, b)
    else:
        s = str(n.v.numerator)
    if n.v < 0 and not inicio:
        s = r"\left(" + s + r"\right)"
    return s


OPS = {"+": " + ", "-": " - ", "*": r" \cdot ", ":": " : "}


def corchetes(n):
    grande = tiene_frac(n.x)
    if n.br == "(":
        return (r"\Big(", r"\Big)") if grande else ("(", ")")
    return (r"\Big[", r"\Big]") if grande else ("[", "]")


def tex_f(n, inicio=True):
    if n.tipo == "num":
        return tex_num(n, inicio)
    if n.tipo == "bin":
        return tex_f(n.a, inicio) + OPS[n.op] + tex_f(n.b, False)
    if n.tipo == "par":
        a, c = corchetes(n)
        return a + tex_f(n.x, True) + c
    if n.tipo == "pow":
        if n.b.tipo == "num" and (n.b.v < 0 or es_frac_disp(n.b)):
            b = r"\left(" + tex_num(n.b, True) + r"\right)"
        else:
            b = tex_f(n.b, True)
        return b + "^{" + str(n.e) + "}"
    return r"\sqrt{" + tex_f(n.x, True) + "}"


def trozos_f(n, marcados, inicio=True):
    if any(n is m for m in marcados):
        return [(tex_f(n, inicio), True)]
    if n.tipo == "num":
        return [(tex_f(n, inicio), False)]
    if n.tipo == "bin":
        return trozos_f(n.a, marcados, inicio) + [(OPS[n.op], False)] + trozos_f(n.b, marcados, False)
    if n.tipo == "par":
        a, c = corchetes(n)
        return [(a, False)] + trozos_f(n.x, marcados, True) + [(c, False)]
    if n.tipo == "pow" and n.b.tipo == "par":
        a, c = corchetes(n.b)
        return [(a, False)] + trozos_f(n.b.x, marcados, True) + [(c + "^{" + str(n.e) + "}", False)]
    return [(tex_f(n, inicio), False)]


def linea_f(n, marcados, size, color_marca=None):
    partes = [("=", False)] + trozos_f(n, marcados)
    juntos = []
    for t, m in partes:
        if len(juntos) > 1 and not m and not juntos[-1][1]:
            juntos[-1] = (juntos[-1][0] + t, False)
        else:
            juntos.append((t, m))
    mt = MathTex(*[t for t, _ in juntos], font_size=size)
    marcas = [mt[i] for i, (_, m) in enumerate(juntos) if m]
    if color_marca:
        for m in marcas:
            m.set_color(color_marca)
    return mt, marcas


def reemplazar(n, cambios, nuevos):
    for viejo, nuevo in cambios:
        if n is viejo:
            nuevos.append(nuevo)
            return nuevo
    if n.tipo == "bin":
        return Nd("bin", op=n.op, a=reemplazar(n.a, cambios, nuevos), b=reemplazar(n.b, cambios, nuevos))
    if n.tipo == "pow":
        return Nd("pow", b=reemplazar(n.b, cambios, nuevos), e=n.e)
    if n.tipo == "raiz":
        return Nd("raiz", x=reemplazar(n.x, cambios, nuevos))
    if n.tipo == "par":
        return simplificar(Nd("par", x=reemplazar(n.x, cambios, nuevos), br=n.br))
    return n


def tt(v, par=False):
    """Número en texto según el modo (fracción o decimal)."""
    v = Fraction(v)
    if MODO[0] == "dec":
        s = dec_str(abs(v))
        return (f"({MENOS}{s})" if par else MENOS + s) if v < 0 else s
    return ft(v, par)


def resultado(num, den):
    """'a/b' y, si se puede simplificar, ' = c/d (simplificamos)'."""
    s = raw_txt(num, den)
    r = Fraction(num, den)
    if (abs(r.numerator), r.denominator) != (abs(num), abs(den)):
        s += f" = {ft(r)}  (simplificamos)"
    return s


def detalle(n):
    """Explicación de un único cálculo (para la nota de abajo)."""
    modo = MODO[0]
    if n.tipo == "pow":
        b, e = valor(n.b), n.e
        r = b ** e
        if e == 0:
            return f"Exponente 0: ({tt(b)})⁰ = 1"
        if modo == "dec":
            return f"{tt(b)}{str(e).translate(SUP)} = " + " · ".join([tt(b, True)] * e) + f" = {tt(r)}"
        s = f"({tt(b)}){str(e).translate(SUP)} = "
        if b.denominator != 1:
            s += (MENOS if r < 0 else "") +                 f"{abs(b.numerator)}{str(e).translate(SUP)}/{b.denominator}{str(e).translate(SUP)} = "
        s += tt(r)
        if b < 0:
            s += "  (base negativa, exponente " + ("par → +)" if e % 2 == 0 else "impar → −)")
        return s
    if n.tipo == "raiz":
        x = valor(n.x)
        r = raiz_exacta(x)
        return f"√{tt(x)} = {tt(r)}, porque {tt(r, True)}² = {tt(x)}"
    a, b = valor(n.a), valor(n.b)
    r = valor(n)
    if n.op in "+-":
        return f"{tt(a)} {'+' if n.op == '+' else MENOS} {tt(b, True)} = {tt(r)}"
    if modo == "dec":
        if n.op == "*":
            return f"Multiplicamos: {tt(a)} · {tt(b, True)} = {tt(r)}"
        k = 0
        while (b * 10 ** k).denominator != 1:
            k += 1
        if k:
            return (f"Quitamos la coma del divisor: {tt(a)} : {tt(b)} = {tt(a * 10 ** k)} : {tt(b * 10 ** k)} "
                    f"= {tt(r)}")
        return f"Dividimos: {tt(a)} : {tt(b, True)} = {tt(r)}"
    if a.denominator == 1 and b.denominator == 1 and (n.op == "*" or r.denominator == 1):
        return f"{tt(a)} {'·' if n.op == '*' else ':'} {tt(b, True)} = {tt(r)}"
    if n.op == "*":
        return (f"Multiplicamos: {tt(a)} · {tt(b, True)} = "
                + resultado(a.numerator * b.numerator, a.denominator * b.denominator))
    inv = 1 / b
    return (f"Por la inversa: {tt(a)} : {tt(b, True)} = {tt(a)} · {tt(inv, True)} = "
            + resultado(a.numerator * inv.numerator, a.denominator * inv.denominator))


def hojas(c):
    """Términos de una cadena de sumas y restas: [(signo, num)]."""
    if c.tipo == "num":
        return [(1, c)]
    return hojas(c.a) + [(1 if c.op == "+" else -1, c.b)]


def mapear(c, f):
    if c.tipo == "num":
        return f(c)
    return Nd("bin", op=c.op, a=mapear(c.a, f), b=mapear(c.b, f))


def den_visible(h):
    return h.disp[1] if h.disp else h.v.denominator


def num_visible(h):
    return h.disp[0] if h.disp else h.v.numerator


def paso_cadenas(cadenas):
    """Sumas y restas de fracciones: primero común denominador, luego numeradores."""
    pares = []
    if any(len({den_visible(h) for _, h in hojas(c)}) > 1 for c in cadenas):
        dens = set()
        for c in cadenas:
            ds = [h.v.denominator for _, h in hojas(c)]
            m = lcm(*ds)
            dens |= set(ds)
            pares.append((c, mapear(c, lambda h, m=m: Num(h.v, disp=(h.v.numerator * (m // h.v.denominator), m)))))
        if len(cadenas) > 1:
            return pares, "Reducimos cada paréntesis a común denominador"
        dist = sorted(d for d in dens if d != 1)
        if len(dist) == 1:
            return pares, f"Pasamos los enteros a denominador {m}"
        return pares, f"Común denominador: m.c.m.({', '.join(map(str, dist))}) = {m}"
    for c in cadenas:
        pares.append((c, Num(valor(c))))
    if len(cadenas) > 1:
        return pares, "Sumamos y restamos los numeradores"
    hs = hojas(cadenas[0])
    contrib = [s * num_visible(h) for s, h in hs]
    den = den_visible(hs[0][1])
    cuenta = str(contrib[0]).replace("-", MENOS) + "".join(
        f" + {c}" if c >= 0 else f" {MENOS} {-c}" for c in contrib[1:])
    total = sum(contrib)
    if den == 1:
        return pares, f"Sumamos y restamos: {cuenta} = {ft(total)}"
    return pares, (f"Sumamos y restamos los numeradores: {cuenta} = {str(total).replace('-', MENOS)}  →  "
                   + resultado(total, den))


def paso_f(arbol):
    """Siguiente paso: (lista de (nodo viejo, nodo nuevo), nivel, nota)."""
    pars = pars_internos(arbol)
    ambitos = [p.x for p in pars] if pars else [arbol]
    info = []
    for amb in ambitos:
        cand = reducibles(amb) if amb.tipo != "num" else []
        if cand:
            m = min(nivel_de(c) for c in cand)
            info.append((amb, m, [c for c in cand if nivel_de(c) == m]))
    nivel = 0 if pars else min(m for _, m, _ in info)
    pref = "Dentro del paréntesis: " if pars else ""
    if MODO[0] == "frac":
        bajos = [t for t in info if t[1] < 3]
        if not bajos:
            pares, nota = paso_cadenas([amb for amb, _, _ in info])
            return pares, nivel, pref + (nota[0].lower() + nota[1:] if pref else nota)
        info = bajos
    pares = []
    for amb, m, eleg in info:
        if m == 3:
            eleg = eleg[:1]
        pares += [(c, Num(valor(c), dec=MODO[0] == "dec")) for c in eleg]
    if len(pares) == 1:
        d = detalle(pares[0][0])
        nota = pref + (d[0].lower() + d[1:] if pref else d)
    elif pars:
        nota = "Primero, dentro de los paréntesis"
    else:
        nota = NIVELES[nivel][0] + ("" if nivel == 1 else ": de izquierda a derecha")
    return pares, nivel, nota


def resolver_f(scene, expr_s, x, y0, size=44, dy=1.0, notas=None, ejemplo=False, etiqueta=None, modo="frac",
               rt=None, espera=None, al_lado=False):
    """Resuelve la expresión línea a línea (fracciones o decimales). Devuelve (VGroup, valor).
    al_lado=True: el resultado final se escribe a la derecha de la última línea (ahorra una línea)."""
    MODO[0] = modo
    rt = rt or (1.0 if ejemplo else 0.7)
    espera = espera if espera is not None else (1.4 if ejemplo else 0.6)
    arbol = parse_f(expr_s)
    l0, _ = linea_f(arbol, [], size)
    l0[0].set_opacity(0)
    l0.move_to([x, y0, 0], aligned_edge=LEFT)
    lineas = VGroup(l0)
    if etiqueta:
        et = texto(etiqueta, 28).next_to(l0[1], LEFT, buff=0.25)
        scene.play(FadeIn(et), run_time=0.3)
        lineas.add(et)
    scene.play(Write(l0), run_time=rt)
    actual, y = l0, y0
    while arbol.tipo != "num":
        pares, nivel, nota = paso_f(arbol)
        _, col = NIVELES[nivel]
        partida, marcas = linea_f(arbol, [p[0] for p in pares], size)
        partida.move_to(actual, aligned_edge=LEFT)
        if actual is l0:
            partida[0].set_opacity(0)
        scene.remove(actual)
        scene.add(partida)
        idx = [i for i, m in enumerate(lineas) if m is actual][0]
        lineas.submobjects[idx] = partida
        actual = partida
        cajas = VGroup(*[SurroundingRectangle(m, color=ACENTO, buff=0.06, stroke_width=3) for m in marcas])
        if notas:
            notas(nota, color=col)
        scene.play(Create(cajas), run_time=0.5)
        scene.wait(espera)
        nuevos = []
        arbol = reemplazar(arbol, pares, nuevos)
        nueva, res_marcas = linea_f(arbol, nuevos, size, color_marca=ACENTO)
        if al_lado and arbol.tipo == "num":
            nueva.next_to(actual, RIGHT, buff=0.25)
            nueva.shift(UP * (actual[0].get_center()[1] - nueva[0].get_center()[1]))
        else:
            y -= dy
            nueva.move_to([x, y, 0], aligned_edge=LEFT)
            nueva.align_to(l0, LEFT)
        resto = VGroup(*[p for p in nueva if not any(p is r for r in res_marcas)])
        scene.play(Write(resto), *[ReplacementTransform(m.copy(), r) for m, r in zip(marcas, res_marcas)],
                   run_time=rt)
        scene.add(nueva)
        scene.play(FadeOut(cajas), run_time=0.3)
        lineas.add(nueva)
        actual = nueva
    scene.play(Circumscribe(actual[1:], color=ACENTO), run_time=0.7)
    if notas:
        notas.fin()
    MODO[0] = "frac"
    return lineas, arbol.v


def valor_expr(s, modo="frac"):
    MODO[0] = modo
    v = valor(parse_f(s))
    MODO[0] = "frac"
    return v


def num_lineas(s, modo="frac", al_lado=False):
    """Cuántas líneas ocupa la solución (para colocar)."""
    MODO[0] = modo
    a, k = parse_f(s), 1
    while a.tipo != "num":
        pares, _, _ = paso_f(a)
        a = reemplazar(a, pares, [])
        k += 1
    MODO[0] = "frac"
    return k - 1 if al_lado and k > 1 else k


# ===========================================================================
class Fracciones(Scene):
    def construct(self):
        cab = titulo(self, "Fracciones", "Repaso de 1.º ESO")
        notas = Notas(self)

        # --- Qué es
        b = barra(5, 3, ancho=7).move_to([-1.6, 1.2, 0])
        f = fraccion(3, 5, 80).next_to(b, RIGHT, buff=1.0)
        self.play(Create(b), run_time=1)
        self.play(Write(f))
        tn = texto("partes que tomamos", 24, NUMERADOR).next_to(f[0], RIGHT, buff=0.3)
        td = texto("partes iguales", 24, DENOMINADOR).next_to(f[2], RIGHT, buff=0.3)
        self.play(FadeIn(tn), FadeIn(td))
        self.wait(1)
        # De una cantidad: 3/5 de 40
        llave = Brace(b, DOWN, buff=0.1)
        t40 = MathTex("40", font_size=44).next_to(llave, DOWN, buff=0.1)
        self.play(GrowFromCenter(llave), FadeIn(t40))
        notas("¿Cuánto es 3/5 de 40? Cada parte vale 40 : 5 = 8")
        ochos = VGroup(*[MathTex("8", font_size=40, color=BLACK if i < 3 else WHITE).move_to(p) for i, p in enumerate(b)])
        self.play(LaggedStart(*[FadeIn(o) for o in ochos], lag_ratio=0.15))
        c = M(r"\dfrac{3}{5}", r"\text{ de } 40 = 40 : 5 \cdot 3 =", ("24", ACENTO), size=52).move_to([0, -1.8, 0])
        self.play(Write(c))
        self.play(Circumscribe(c[2], color=ACENTO))
        self.wait(1.5)
        notas.fin()
        limpiar(self, cab)

        # --- Equivalentes
        subtitulo(self, cab, "Fracciones equivalentes")
        datos = [(2, 3), (4, 6), (8, 12)]
        filas = VGroup()
        for i, (n, d) in enumerate(datos):
            bb = barra(d, n, ancho=6.5, alto=0.6).move_to([0.6, 1.6 - i * 1.2, 0])
            ff = fraccion(n, d, 50).next_to(bb, LEFT, buff=0.6)
            filas.add(VGroup(ff, bb))
        for fl in filas:
            self.play(Write(fl[0]), Create(fl[1]), run_time=0.8)
        notas("Las tres pintan la misma cantidad: son equivalentes")
        self.wait(1.5)
        cruz = M(r"\dfrac{2}{3} = \dfrac{8}{12}", r"\quad\Leftrightarrow\quad", r"2 \cdot 12 = 3 \cdot 8 = 24",
                 size=46).move_to([0, -2.0, 0])
        cruz[2].set_color(ACENTO)
        self.play(Write(cruz))
        notas("Productos cruzados iguales")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Simplificar
        subtitulo(self, cab, "Simplificar: la fracción irreducible")
        f1 = fraccion(18, 24, 80).move_to([-3.0, 0.8, 0])
        f2 = fraccion(3, 4, 80).move_to([3.0, 0.8, 0])
        self.play(Write(f1))
        m = MathTex(r"\text{M.C.D.}(18, 24) = 6", font_size=44, color=ACENTO).move_to([0, 2.4, 0])
        self.play(Write(m))
        fl = flecha_op(f1, f2, ":", 6)
        self.play(Create(fl))
        self.play(Write(f2))
        irr = texto("3/4 ya no se puede simplificar: es irreducible", 28, OK).move_to([0, -1.4, 0])
        self.play(FadeIn(irr), Circumscribe(f2, color=ACENTO))
        self.wait(2)
        limpiar(self, cab)

        # --- Negativas
        subtitulo(self, cab, "Fracciones negativas")
        e = M(r"-\dfrac{3}{4}", "=", r"\dfrac{-3}{4}", "=", r"\dfrac{3}{-4}", size=64).move_to([0, 1.6, 0])
        e[0].set_color(NEGATIVO)
        self.play(Write(e))
        notas("El signo puede ir delante, arriba o abajo: casi siempre lo ponemos delante")
        recta = NumberLine(x_range=[-1, 1, 0.25], length=11, include_tip=False, stroke_width=3,
                           tick_size=0.1).move_to([0, -0.9, 0])
        etq = VGroup(*[MathTex(s, font_size=34).next_to(recta.n2p(v), DOWN, buff=0.25)
                       for s, v in (("-1", -1), ("0", 0), ("1", 1))])
        self.play(Create(recta), FadeIn(etq))
        p = Dot(recta.n2p(-0.75), radius=0.12, color=NEGATIVO)
        pt = MathTex(r"-\dfrac{3}{4}", font_size=40, color=NEGATIVO).next_to(p, UP, buff=0.25)
        p2 = Dot(recta.n2p(0.75), radius=0.12, color=POSITIVO)
        pt2 = MathTex(r"\dfrac{3}{4}", font_size=40, color=POSITIVO).next_to(p2, UP, buff=0.25)
        self.play(FadeIn(p, scale=2), Write(pt))
        self.play(FadeIn(p2, scale=2), Write(pt2))
        notas("Son opuestas: a la misma distancia del 0")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Comparar
        subtitulo(self, cab, "Comparar: con el mismo denominador")
        a = fraccion(5, 6, 72).move_to([-4.2, 1.2, 0])
        bq = fraccion(7, 9, 72).move_to([-4.2, -1.3, 0])
        self.play(Write(a), Write(bq))
        m = MathTex(r"\text{m.c.m.}(6, 9) = 18", font_size=44, color=ACENTO).move_to([0, 2.7, 0])
        self.play(Write(m))
        a2 = fraccion(15, 18, 72).move_to([0.4, 1.2, 0])
        b2 = fraccion(14, 18, 72).move_to([0.4, -1.3, 0])
        self.play(Create(flecha_op(a, a2, "x", 3)), Write(a2))
        self.play(Create(flecha_op(bq, b2, "x", 2)), Write(b2))
        notas("Mismo denominador: es mayor la que tiene mayor numerador (15 > 14)")
        r = M(r"\dfrac{5}{6}", ">", r"\dfrac{7}{9}", size=72).move_to([4.6, 0, 0])
        r[1].set_color(ACENTO)
        self.play(Write(r))
        self.play(Circumscribe(r, color=ACENTO))
        self.wait(2.5)


# ===========================================================================
def juntar(scene, b1, k1, b2, k2, n, ancho, alto, pos):
    """Barra vacía de n partes; los k1 trozos coloreados de b1 y los k2 de b2 viajan a ella."""
    suma = barra(n, 0, ancho=ancho, alto=alto).move_to(pos)
    scene.play(Create(suma), run_time=0.8)
    trozos = [b1[i].copy() for i in range(k1)] + [b2[i].copy() for i in range(k2)]
    scene.play(LaggedStart(*[t.animate.move_to(suma[j]) for j, t in enumerate(trozos)],
                           lag_ratio=0.3), run_time=2)
    return suma, trozos


class SumaResta(Scene):
    def construct(self):
        cab = titulo(self, "Suma y resta de fracciones")
        notas = Notas(self)

        # --- Mismo denominador
        subtitulo(self, cab, "Mismo denominador")
        b1 = barra(7, 2, ancho=5.6, alto=0.7, color=NUMERADOR).move_to([-3.4, 1.6, 0])
        b2 = barra(7, 3, ancho=5.6, alto=0.7, color=BASE).move_to([3.4, 1.6, 0])
        for i in range(3):
            b2[i].set_fill(BASE)
        f = cadena((2, 7), "+", (3, 7), "=", (5, 7), size=60).move_to([0, -1.1, 0])
        self.play(Create(b1), Create(b2))
        self.play(Write(f[:3]))
        juntar(self, b1, 2, b2, 3, 7, 5.6, 0.7, [0, 0.4, 0])
        self.play(Write(f[3:]))
        notas("Mismo denominador: sumamos los numeradores y dejamos el denominador")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Distinto denominador
        subtitulo(self, cab, "Distinto denominador")
        b1 = barra(2, 1, ancho=5.2, alto=0.7, color=NUMERADOR).move_to([-3.3, 0.9, 0])
        b2 = barra(3, 1, ancho=5.2, alto=0.7, color=BASE).move_to([3.3, 0.9, 0])
        f1 = fraccion(1, 2, 50).next_to(b1, UP, buff=0.2)
        f2 = fraccion(1, 3, 50).next_to(b2, UP, buff=0.2)
        self.play(Create(b1), Create(b2), Write(f1), Write(f2))
        notas("Mitades y tercios no se pueden juntar: son trozos de distinto tamaño")
        self.wait(1.5)
        notas("Partimos las dos en sextos (m.c.m.(2, 3) = 6)")
        n1 = barra(6, 3, ancho=5.2, alto=0.7, color=NUMERADOR).move_to(b1)
        n2 = barra(6, 2, ancho=5.2, alto=0.7, color=BASE).move_to(b2)
        g1 = fraccion(3, 6, 50).move_to(f1)
        g2 = fraccion(2, 6, 50).move_to(f2)
        self.play(ReplacementTransform(b1, n1), ReplacementTransform(b2, n2),
                  ReplacementTransform(f1, g1), ReplacementTransform(f2, g2), run_time=1.5)
        self.wait(1)
        juntar(self, n1, 3, n2, 2, 6, 5.2, 0.7, [0, -0.5, 0])
        c = cadena((1, 2), "+", (1, 3), "=", (3, 6), "+", (2, 6), "=", (5, 6), size=54).move_to([0, -2.0, 0])
        self.play(Write(c), run_time=2)
        self.play(Circumscribe(c[-1], color=ACENTO))
        notas.fin()
        self.wait(1)
        limpiar(self, cab)

        # --- Regla
        subtitulo(self, cab, "Paso a paso")
        pasos_t = VGroup(*[texto(s, 30) for s in (
            "1.º  Buscamos el m.c.m. de los denominadores",
            "2.º  Pasamos cada fracción a ese denominador",
            "3.º  Sumamos o restamos los numeradores",
            "4.º  Simplificamos si se puede")]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        caja = tarjeta(pasos_t, buff=0.4).move_to([0, 0, 0])
        self.play(Create(caja[0]))
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.2) for p in pasos_t], lag_ratio=0.4), run_time=2.5)
        self.wait(3)
        limpiar(self, cab)

        # --- Con enteros y negativos
        subtitulo(self, cab, "Con enteros y varios términos")
        resolver_f(self, "2-3/4+5/6", -4.0, 1.8, size=56, dy=1.45, notas=notas, ejemplo=True)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Con negativos")
        resolver_f(self, "-1/6+3/4-5/12", -4.0, 1.8, size=56, dy=1.45, notas=notas, ejemplo=True)
        self.wait(2)


# ===========================================================================
class MultiplicarDividir(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicación y división", "de fracciones")
        notas = Notas(self)

        # --- Modelo de área: 2/3 de 3/4
        subtitulo(self, cab, "Multiplicar: la fracción de una fracción")
        w, h = 4.8, 3.6
        orig = np.array([-6.4, -1.6, 0])
        celdas = VGroup()
        for i in range(4):
            for j in range(3):
                celdas.add(Rectangle(width=w / 4, height=h / 3, stroke_color=WHITE, stroke_width=2,
                                     fill_color=VACIO, fill_opacity=1)
                           .move_to(orig + [w / 8 + i * w / 4, h / 6 + j * h / 3, 0]))
        self.play(Create(celdas))
        cols = VGroup(*[c for k, c in enumerate(celdas) if k // 3 < 3])
        notas("Pintamos 3/4 del cuadrado (3 columnas de 4)")
        self.play(cols.animate.set_fill(BASE, 0.75))
        t1 = MathTex(r"\dfrac{3}{4}", font_size=50, color=BASE).move_to([0.6, 1.6, 0])
        self.play(Write(t1))
        notas("Y ahora 2/3 de esa parte (2 filas de 3)")
        dob = VGroup(*[c for k, c in enumerate(celdas) if k // 3 < 3 and k % 3 < 2])
        self.play(dob.animate.set_fill(ACENTO, 1))
        t2 = MathTex(r"\dfrac{2}{3} \text{ de } \dfrac{3}{4}", "=", r"\dfrac{2}{3} \cdot \dfrac{3}{4}", font_size=50)
        t2.move_to([2.4, 1.6, 0])
        self.play(ReplacementTransform(t1, t2))
        notas("Quedan 6 casillas de 12")
        r = M("=", r"\dfrac{2 \cdot 3}{3 \cdot 4}", "=", (r"\dfrac{6}{12}", ACENTO), "=", (r"\dfrac{1}{2}", ACENTO),
              size=50).next_to(t2, DOWN, buff=0.5).align_to(t2, LEFT)
        self.play(Write(r), run_time=1.5)
        self.wait(1)
        notas.fin()
        rg = regla(r"\dfrac{a}{b} \cdot \dfrac{c}{d} = \dfrac{a \cdot c}{b \cdot d}",
                   frase="numerador por numerador, denominador por denominador", size=46).scale(0.8)
        rg.move_to([3.0, -2.3, 0])
        self.play(FadeIn(rg))
        self.wait(2.5)
        limpiar(self, cab)

        # --- Simplificar antes de multiplicar
        subtitulo(self, cab, "Truco: simplificar antes de multiplicar")
        e = M(r"\dfrac{4}{9} \cdot \dfrac{15}{8}", "=", r"\dfrac{4 \cdot 15}{9 \cdot 8}", "=", size=56)
        e.move_to([-2.8, 1.4, 0])
        self.play(Write(e))
        notas("Descomponemos en factores primos y no multiplicamos todavía")
        nn = MathTex("2", r"\cdot", "2", r"\cdot", "3", r"\cdot", "5", font_size=56)
        dd = MathTex("3", r"\cdot", "3", r"\cdot", "2", r"\cdot", "2", r"\cdot", "2", font_size=56)
        raya = Line(LEFT, RIGHT, stroke_width=3).set_width(max(nn.width, dd.width) + 0.2)
        nn.next_to(raya, UP, buff=0.12)
        dd.next_to(raya, DOWN, buff=0.12)
        frac = VGroup(nn, raya, dd).next_to(e, RIGHT, buff=0.3)
        self.play(Write(frac))
        notas("Un factor igual arriba y abajo se va (dividimos los dos entre él)")
        rayas = VGroup()
        for i, j in ((0, 4), (2, 6), (4, 0)):
            for m_ in (nn[i], dd[j]):
                rayas.add(Line(m_.get_corner(DL), m_.get_corner(UR), color=MAL, stroke_width=5))
            self.play(Create(rayas[-2]), Create(rayas[-1]), run_time=0.6)
        fin = M("=", (r"\dfrac{5}{3 \cdot 2}", None), "=", (r"\dfrac{5}{6}", ACENTO), size=56)
        fin.next_to(e, DOWN, buff=1.4).align_to(e[1], LEFT)
        self.play(Write(fin))
        self.play(Circumscribe(fin[-1], color=ACENTO))
        notas("Sin números grandes: 4 · 15 = 60 y 9 · 8 = 72 nos habría dado 60/72 = 5/6")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Dividir: ¿cuántas veces cabe?
        subtitulo(self, cab, "Dividir: ¿cuántas veces cabe?")
        q = M("3", ":", r"\dfrac{1}{4}", "=", r"\ ?", size=60).move_to([0, 2.0, 0])
        self.play(Write(q))
        notas("¿Cuántos cuartos caben en 3 unidades?")
        bars = VGroup(*[barra(4, 4, ancho=3.6, alto=0.8, color=BASE) for _ in range(3)]).arrange(RIGHT, buff=0.25)
        bars.move_to([0, 0.3, 0])
        self.play(Create(bars))
        nums = VGroup()
        for k, cel in enumerate([c for b_ in bars for c in b_]):
            nums.add(MathTex(str(k + 1), font_size=30, color=BLACK).move_to(cel))
        self.play(LaggedStart(*[FadeIn(n_) for n_ in nums], lag_ratio=0.12), run_time=2)
        r12 = MathTex("12", font_size=60, color=ACENTO).move_to(q[4])
        self.play(ReplacementTransform(q[4], r12))
        igual = M("3", ":", r"\dfrac{1}{4}", "=", "3", r"\cdot", r"\dfrac{4}{1}", "=", ("12", ACENTO),
                  size=56).move_to([0, -1.6, 0])
        self.play(Write(igual))
        notas("Dividir entre 1/4 es lo mismo que multiplicar por 4/1: la fracción inversa")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Regla de la división
        subtitulo(self, cab, "Dividir es multiplicar por la inversa")
        rg = regla(r"\dfrac{a}{b} : \dfrac{c}{d} = \dfrac{a}{b} \cdot \dfrac{d}{c}",
                   frase="damos la vuelta a la segunda fracción y multiplicamos", size=52).move_to([0, 1.7, 0])
        self.play(FadeIn(rg))
        c = cadena((3, 5), ":", (9, 10), "=", (3, 5), r"\cdot", (10, 9), "=", (30, 45), "=", (2, 3), size=56)
        c.move_to([0, -0.9, 0])
        trozos = [(c[:3], None), (c[3:6], "La inversa de 9/10 es 10/9"),
                  (c[6:8], "Multiplicamos: 3 · 10 = 30 y 5 · 9 = 45"),
                  (c[8:], "Simplificamos: M.C.D.(30, 45) = 15")]
        for m_, nota in trozos:
            self.play(Write(m_))
            if nota:
                notas(nota)
                self.wait(1.3)
        self.play(Circumscribe(c[-1], color=ACENTO))
        notas("Y los signos, igual que con los enteros: (−)·(+) = −,  (−):(−) = +")
        self.wait(3)
        notas.fin()


# ===========================================================================
class PotenciasFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Potencias de fracciones")
        notas = Notas(self)

        lineas = [(L(*PF(2, 3, 3), size=56), None),
                  (L(r"\dfrac{2}{3} \cdot \dfrac{2}{3} \cdot \dfrac{2}{3}", size=56), "Multiplicamos la fracción 3 veces"),
                  (L(r"\dfrac{2 \cdot 2 \cdot 2}{3 \cdot 3 \cdot 3}", size=56), None),
                  (L(r"\dfrac{2^3}{3^3}", "=", (r"\dfrac{8}{27}", ACENTO), size=56),
                   "Se eleva el numerador y el denominador")]
        pasos(self, lineas, -6.0, 2.3, dy=1.45, notas=notas, ejemplo=True)
        rg = regla(r"\left(\dfrac{a}{b}\right)^{n} = \dfrac{a^{n}}{b^{n}}", frase="numerador y denominador", size=54)
        rg.move_to([3.6, 0.2, 0])
        self.play(FadeIn(rg))
        notas.fin()
        self.wait(2.5)
        limpiar(self, cab)

        # --- Signos
        subtitulo(self, cab, "Base negativa: mira el exponente")
        izq = pasos(self, [(L(*PF(-1, 2, 2), size=56), None),
                           (L(r"\dfrac{(-1)^2}{2^2}", "=", (r"+\dfrac{1}{4}", POSITIVO), size=56), None)],
                    -6.2, 1.4, dy=1.8, final=False)
        par = texto("exponente par → positivo", 26, POSITIVO).next_to(izq, DOWN, buff=0.5).align_to(izq, LEFT)
        self.play(FadeIn(par))
        der = pasos(self, [(L(*PF(-2, 3, 3), size=56), None),
                           (L(r"\dfrac{(-2)^3}{3^3}", "=", (r"-\dfrac{8}{27}", NEGATIVO), size=56), None)],
                    0.8, 1.4, dy=1.8, final=False)
        imp = texto("exponente impar → negativo", 26, NEGATIVO).next_to(der, DOWN, buff=0.5).align_to(der, LEFT)
        self.play(FadeIn(imp))
        self.wait(2.5)
        limpiar(self, cab)

        # --- El paréntesis importa
        subtitulo(self, cab, "¡El paréntesis importa!")
        a = M(*PF(2, 3, 2), "=", r"\dfrac{4}{9}", size=60).move_to([-3.4, 1.0, 0])
        b = M(r"\dfrac{2^2}{3}", "=", r"\dfrac{4}{3}", size=60).move_to([3.4, 1.0, 0])
        self.play(Write(a))
        self.play(Write(b))
        ta = texto("se eleva toda la fracción", 24, GREY_B).next_to(a, DOWN, buff=0.4)
        tb = texto("solo se eleva el 2", 24, GREY_B).next_to(b, DOWN, buff=0.4)
        self.play(FadeIn(ta), FadeIn(tb))
        dist = MathTex(r"\dfrac{4}{9} \neq \dfrac{4}{3}", font_size=60, color=MAL).move_to([0, -1.6, 0])
        self.play(Write(dist))
        self.wait(2.5)
        limpiar(self, cab)

        # --- Propiedades
        subtitulo(self, cab, "Las mismas propiedades que con enteros")
        filas = [
            (M(*PF(2, 3, 4), r"\cdot", *PF(2, 3, 3), "=", *PF(2, 3, 7), size=46), "misma base: sumamos exponentes"),
            (M(*PF(3, 5, 6), ":", *PF(3, 5, 4), "=", *PF(3, 5, 2), "=", r"\dfrac{9}{25}", size=46),
             "misma base: restamos exponentes"),
            (M(r"\Big[", *PF(1, 2, 2), r"\Big]", ("^{3}", EXPONENTE), "=", *PF(1, 2, 6), "=", r"\dfrac{1}{64}", size=46),
             "potencia de potencia: multiplicamos"),
            (M(*PF(5, 7, 0), "=", ("1", ACENTO), size=46), "exponente 0: siempre 1"),
        ]
        g = VGroup()
        for i, (m_, t) in enumerate(filas):
            m_.move_to([-6.3, 1.5 - i * 1.3, 0], aligned_edge=LEFT)
            tt_ = texto(t, 26, GREY_B).move_to([0.8, m_.get_y(), 0], aligned_edge=LEFT)
            self.play(Write(m_), run_time=0.9)
            self.play(FadeIn(tt_), run_time=0.4)
            g.add(m_, tt_)
            self.wait(0.8)
        self.wait(3)


# ===========================================================================
class CombinadasFracciones(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones combinadas", "con fracciones")
        notas = Notas(self)
        esc = escalera(20, 4.4).scale(0.9).to_corner(UR).shift(DOWN * 0.6)
        self.play(FadeIn(esc))
        notas("El mismo orden de siempre: paréntesis, potencias, · y :, + y −")
        self.wait(2)
        resolver_f(self, "(1/2+1/3)*3/5-1/4", -6.3, 2.0, size=48, dy=1.12, notas=notas, ejemplo=True, al_lado=True)
        self.wait(2)
        limpiar(self, cab)

        subtitulo(self, cab, "Otro ejemplo")
        resolver_f(self, "3-2/5*(1/2+3/4)", -5.5, 2.3, size=46, dy=1.1, notas=notas, ejemplo=True, al_lado=True)
        consejo = texto("Consejo: simplifica en cada paso\ny los números no crecen", 26, GREY_B).move_to([3.8, 0.5, 0])
        self.play(FadeIn(consejo))
        self.wait(2.5)


# ===========================================================================
class FraccionesDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Fracciones y decimales")
        notas = Notas(self)

        subtitulo(self, cab, "De fracción a decimal: dividimos")
        f = VGroup(fraccion(5, 12, 72), MathTex("= 5 : 12", font_size=56)).arrange(RIGHT, buff=0.3).move_to([-4.2, 1.6, 0])
        self.play(Write(f))
        division_larga(self, "5", 12, -0.4, 1.7, size=52, max_dec=4, lateral=True, rt=0.4)
        res = VGroup(fraccion(5, 12, 56), MathTex(r"= 0{,}41666\ldots =", font_size=52),
                     periodico("0", "41", "6", 60)).arrange(RIGHT, buff=0.25).move_to([0, -2.2, 0])
        self.play(Write(res))
        notas("El resto 8 se repite: el 6 sale para siempre")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Los tres tipos
        subtitulo(self, cab, "Tres tipos de decimales")
        tipos = [
            ("Exacto", fraccion(3, 4, 44), VGroup(MathTex(r"0{,}75", font_size=56)), "la división termina", OK),
            ("Periódico puro", fraccion(2, 3, 44), periodico("0", "", "6", 56), "se repite desde la coma",
             COLOR_PERIODO),
            ("Periódico mixto", fraccion(5, 12, 44), periodico("0", "41", "6", 56), "hay cifras antes del periodo",
             COLOR_ANTE),
        ]
        cajas = VGroup()
        for nombre, frac, num, desc, col in tipos:
            fila = VGroup(frac, MathTex("=", font_size=50), num).arrange(RIGHT, buff=0.2)
            c = VGroup(texto(nombre, 30, col), fila, texto(desc, 22, GREY_B)).arrange(DOWN, buff=0.35)
            cajas.add(tarjeta(c, col))
        cajas.arrange(RIGHT, buff=0.35).move_to([0, 0, 0])
        if cajas.width > 13.4:
            cajas.scale_to_fit_width(13.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.3) for c in cajas], lag_ratio=0.4), run_time=2.5)
        self.wait(3)
        limpiar(self, cab)

        # --- Truco del denominador
        subtitulo(self, cab, "¿Exacto o periódico? Mira el denominador")
        notas("Con la fracción irreducible, descomponemos el denominador")
        a = M(r"\dfrac{3}{40}", r"\quad 40 = 2^3 \cdot 5", size=52).move_to([-3.2, 1.3, 0])
        ar = texto("solo 2 y 5 → exacto: 0,075", 28, OK).next_to(a, DOWN, buff=0.35)
        b = M(r"\dfrac{5}{12}", r"\quad 12 = 2^2 \cdot", ("3", MAL), size=52).move_to([3.4, 1.3, 0])
        br_ = texto("hay un 3 → periódico", 28, COLOR_PERIODO).next_to(b, DOWN, buff=0.35)
        self.play(Write(a))
        self.play(FadeIn(ar))
        self.play(Write(b))
        self.play(FadeIn(br_))
        porq = texto("¿Por qué? 10, 100, 1000... solo tienen factores 2 y 5", 26, GREY_B).move_to([0, -1.3, 0])
        self.play(FadeIn(porq))
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Decimal exacto → fracción
        subtitulo(self, cab, "De decimal exacto a fracción")
        l1 = pasos(self, [(L(r"0{,}35", size=58), None),
                          (L(r"\dfrac{35}{100}", size=58), "Dos decimales: denominador 100"),
                          (L((r"\dfrac{7}{20}", ACENTO), size=58), "Simplificamos entre 5")],
                   -5.6, 1.9, dy=1.6, notas=notas, ejemplo=True)
        l2 = pasos(self, [(L(r"2{,}4", size=58), None),
                          (L(r"\dfrac{24}{10}", size=58), "Un decimal: denominador 10"),
                          (L((r"\dfrac{12}{5}", ACENTO), size=58), "Simplificamos entre 2")],
                   1.4, 1.9, dy=1.6, notas=notas, ejemplo=True)
        notas("Pero ¿y los periódicos? Lo vemos en el siguiente vídeo")
        self.wait(2.5)
        notas.fin()


# ===========================================================================
# Vídeo extra E1: ¿por qué unas fracciones dan decimal exacto y otras periódico?
def ladrillos(ps, r=0.28):
    """Fila de piezas de primos (las de divisibilidad de 1.º: 2 azul, 3 verde, 5 naranja, 7 lila)."""
    return VGroup(*[pieza(p, r) for p in ps]).arrange(RIGHT, buff=0.1)


def fila_factores(n, ps, x, y, size=46):
    """'n =' + piezas, con las piezas empezando en x."""
    b = ladrillos(ps).move_to([x, y, 0], aligned_edge=LEFT)
    et = MathTex(f"{n} =", font_size=size).next_to(b, LEFT, buff=0.25)
    return VGroup(et, b)


def ciclo_restos(n, d):
    """Pasos de n : d como [(dividendo, cifra, resto)] hasta que un resto se repite."""
    pasos, r = [(n, n // d, n % d)], n % d
    vistos = {r}
    while True:
        dd = r * 10
        c, r = dd // d, dd % d
        pasos.append((dd, c, r))
        if r in vistos or r == 0:
            return pasos
        vistos.add(r)


def restos_division(scene, notas, n, d, nota_final):
    """Divide n : d anotando cada resto en su casilla (1 ... d−1) hasta que uno se repite."""
    pasos = ciclo_restos(n, d)
    per = "".join(str(c) for _, c, _ in pasos[1:])
    grande = d <= 7
    tit_r = texto(f"Restos posibles (menores que {d})", 24, GREY_B).move_to([3.4, 2.1, 0])
    cajas = VGroup(*[VGroup(Square(0.65 if grande else 0.5, stroke_color=WHITE, stroke_width=2,
                                   fill_color=BASE, fill_opacity=0),
                            MathTex(str(i), font_size=38 if grande else 30)) for i in range(1, d)])
    cajas.arrange(RIGHT, buff=0.15 if grande else 0.1).next_to(tit_r, DOWN, buff=0.3)
    q = MathTex(rf"\dfrac{{{n}}}{{{d}}} =", r"0{,}", *per, font_size=56).move_to([3.4, -0.4, 0])
    scene.play(FadeIn(tit_r), FadeIn(cajas))
    notas(f"Dividimos {n} : {d}. El resto siempre es menor que {d}")
    for i, (dd, c, r) in enumerate(pasos):
        fl = M(rf"{dd} : {d}", r"\to", (str(c), ACENTO), r"\quad\text{resto }", (str(r), BASE), size=42)
        fl.move_to([-6.3, 1.9 - i * 0.62, 0], aligned_edge=LEFT)
        caja = cajas[r - 1]
        scene.play(Write(fl), Write(q[:2]) if i == 0 else Write(q[1 + i]), run_time=0.7 if i else 1.0)
        if i == len(pasos) - 1:
            scene.play(Indicate(caja, color=ACENTO, scale_factor=1.4), Circumscribe(fl[4], color=ACENTO))
        else:
            scene.play(caja[0].animate.set_fill(BASE, 0.55), run_time=0.35)
    notas(f"¡Resto {pasos[-1][2]} otra vez! Desde aquí todo se repite: {', '.join(per)}...")
    scene.wait(1.5)
    fin = VGroup(MathTex(rf"\dfrac{{{n}}}{{{d}}} =", font_size=56), periodico("0", "", per, 58))
    fin.arrange(RIGHT, buff=0.25).move_to(q, aligned_edge=LEFT)
    scene.play(ReplacementTransform(q, fin))
    notas(nota_final, color=COLOR_PERIODO)
    scene.wait(2.5)
    notas.fin()


class PorQuePeriodico(Scene):
    def construct(self):
        cab = titulo(self, "¿Exacto o periódico?", "¿Por qué depende del denominador?")
        notas = Notas(self)

        # --- 1. Un decimal exacto es una fracción decimal
        subtitulo(self, cab, "Un decimal exacto...")
        ej = VGroup(*[VGroup(MathTex(d + " =", font_size=54), fraccion(n, den, 54)).arrange(RIGHT, buff=0.2)
                      for d, n, den in ((r"0{,}5", 5, 10), (r"0{,}25", 25, 100), (r"0{,}075", 75, 1000))])
        ej.arrange(RIGHT, buff=1.3).move_to([0, 1.6, 0])
        for e in ej:
            self.play(Write(e), run_time=0.8)
        notas("...siempre se puede escribir con denominador 10, 100, 1000...")
        self.wait(1)
        filas = [fila_factores(n, ps, -0.6, y) for n, ps, y in
                 ((10, [2, 5], -0.1), (100, [2, 2, 5, 5], -0.9), (1000, [2, 2, 2, 5, 5, 5], -1.7))]
        for e, f in zip(ej, filas):
            self.play(TransformFromCopy(e[1][2], f[0]), run_time=0.7)
            self.play(LaggedStart(*[GrowFromCenter(p) for p in f[1]], lag_ratio=0.15), run_time=0.7)
        notas("Y 10, 100, 1000... solo están hechos de doses y cincos")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- 2. Solo 2 y 5: se completa
        subtitulo(self, cab, "Si solo hay 2 y 5, lo completamos")
        f = fraccion(3, 40, 64).move_to([-5.3, 1.4, 0])
        self.play(Write(f))
        b40 = ladrillos([2, 2, 2, 5]).move_to([-2.0, 1.4, 0], aligned_edge=LEFT)
        et40 = MathTex("40 =", font_size=46).next_to(b40, LEFT, buff=0.25)
        self.play(TransformFromCopy(f[2], et40), LaggedStart(*[GrowFromCenter(p) for p in b40], lag_ratio=0.15))
        notas("Para llegar a 1000 = 2 · 2 · 2 · 5 · 5 · 5 faltan dos cincos")
        self.wait(1)
        extra = ladrillos([5, 5]).next_to(b40, RIGHT, buff=0.1)
        marco = DashedVMobject(SurroundingRectangle(extra, color=ACENTO, buff=0.1, corner_radius=0.1))
        lab = MathTex(r"5 \cdot 5 = 25", font_size=36, color=ACENTO).next_to(marco, DOWN, buff=0.15)
        self.play(LaggedStart(*[FadeIn(p, scale=1.8) for p in extra], lag_ratio=0.3), Create(marco))
        et_n = MathTex(r"40 \cdot 25 =", font_size=46).next_to(b40, LEFT, buff=0.25)
        mil = MathTex("= 1000", font_size=46, color=OK).next_to(marco, RIGHT, buff=0.25)
        self.play(FadeIn(lab), ReplacementTransform(et40, et_n), Write(mil))
        self.wait(1)
        linea = cadena(fraccion(3, 40, 54), "=", fraccion(r"3 \cdot 25", r"40 \cdot 25", 54), "=",
                       fraccion(75, 1000, 54), "=", MathTex(r"0{,}075", font_size=58, color=OK),
                       size=54).move_to([0, -1.1, 0])
        for m in (linea[2][0], linea[2][2]):
            m[0][-2:].set_color(ACENTO)
        notas("Multiplicamos arriba y abajo por 25: sale una fracción decimal")
        self.play(Write(linea), run_time=2)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- 3. Con un 3 no se puede
        subtitulo(self, cab, "Si hay un 3, imposible")
        f = fraccion(1, 3, 64).move_to([-5.4, 1.4, 0])
        tres = pieza(3, 0.28).next_to(f, DOWN, buff=0.6)
        et3 = MathTex("3 =", font_size=46).next_to(tres, LEFT, buff=0.2)
        self.play(Write(f))
        self.play(TransformFromCopy(f[2], et3), GrowFromCenter(tres))
        filas = [fila_factores(n, ps, -1.2, y) for n, ps, y in
                 ((10, [2, 5], 1.6), (100, [2, 2, 5, 5], 0.6), (1000, [2, 2, 2, 5, 5, 5], -0.4))]
        self.play(*[FadeIn(fl) for fl in filas])
        notas("¿Podemos convertir el 3 en 10, 100, 1000...?")
        for fl in filas:
            c = tres.copy()
            self.play(c.animate.next_to(fl, RIGHT, buff=0.35), run_time=0.6)
            self.play(Create(Cross(c, stroke_color=MAL, stroke_width=6)), run_time=0.35)
        notas("No: ninguno tiene un 3, multipliquemos lo que multipliquemos")
        self.wait(1.5)
        res = VGroup(fraccion(1, 3, 54), MathTex(r"= 0{,}3333\ldots =", font_size=54),
                     periodico("0", "", "3", 58)).arrange(RIGHT, buff=0.25).move_to([0, -1.9, 0])
        self.play(Write(res))
        notas("Así que la división no termina nunca: periódico", color=COLOR_PERIODO)
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- 3b. Lo mismo con 7, 11...
        subtitulo(self, cab, "Lo mismo con 7, 11, 13...")
        datos = [([7], (1, 7), ("0", "", "142857")),
                 ([11], (1, 11), ("0", "", "09")),
                 ([2, 3], (1, 6), ("0", "1", "6"))]
        filas = VGroup()
        for i, (ps, (n, d), per) in enumerate(datos):
            y = 1.5 - i * 1.45
            b = ladrillos(ps).move_to([-3.2, y, 0], aligned_edge=RIGHT)
            et = MathTex(f"{d} =", font_size=46).next_to(b, LEFT, buff=0.25)
            fila = VGroup(fraccion(n, d, 54), MathTex("=", font_size=54), periodico(*per, size=56))
            fila.arrange(RIGHT, buff=0.25).move_to([-1.8, y, 0], aligned_edge=LEFT)
            filas.add(VGroup(et, b, fila))
            self.play(FadeIn(et), LaggedStart(*[GrowFromCenter(p) for p in b], lag_ratio=0.2), run_time=0.7)
            self.play(Write(fila), run_time=1.0)
        self.play(Circumscribe(filas[2][1][1], color=MAL, shape=Circle))
        notas("Basta un primo que no sea 2 ni 5 (aunque también haya un 2)")
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- 4. ¿Por qué se repite? Primero uno corto (4 : 11) y luego uno largo (1 : 7)
        subtitulo(self, cab, "¿Y por qué se repite? Uno fácil")
        restos_division(self, notas, 4, 11, "El 4 vuelve enseguida: se repiten 2 cifras, 0,363636...")
        limpiar(self, cab)
        subtitulo(self, cab, "Uno más largo: 1 : 7")
        restos_division(self, notas, 1, 7, "Solo hay 6 restos posibles: como mucho en 6 pasos alguno se repite")
        limpiar(self, cab)

        # --- 5. Es por contar de 10 en 10
        subtitulo(self, cab, "Todo es por contar de 10 en 10")
        diez = fila_factores(10, [2, 5], 1.0, 1.7)
        intro = texto("Nuestros números van de 10 en 10, y", 28).next_to(diez, LEFT, buff=0.35)
        VGroup(intro, diez).move_to([0, 1.7, 0])
        self.play(FadeIn(intro), FadeIn(diez))
        h1 = M(r"\dfrac{1}{3}\ \text{de hora}", "=", r"0{,}333\ldots\ \text{h}", size=50).move_to([-3.0, 0.2, 0])
        h2 = M(r"\dfrac{1}{3}\ \text{de hora}", "=", (r"20\ \text{min}", OK), size=50)
        h2.move_to(h1, aligned_edge=LEFT).shift(DOWN * 1.5)
        self.play(Write(h1))
        notas("En horas, un tercio da periódico...")
        self.wait(1)
        self.play(Write(h2))
        sesenta = fila_factores(60, [2, 2, 3, 5], 3.6, -1.3)
        min_t = texto("1 h = 60 min", 28, GREY_B).next_to(sesenta, UP, buff=0.35)
        self.play(FadeIn(min_t), FadeIn(sesenta))
        self.play(Circumscribe(sesenta[1][2], color=ACENTO, shape=Circle))
        notas("...pero en minutos es exacto: los minutos van de 60 en 60, y el 60 sí tiene un 3")
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- 6. Otras escalas, otros primos
        subtitulo(self, cab, "Otras escalas, otros primos")
        xs = [0.8, 3.1, 5.4]
        cabecera = VGroup(texto("Partes iguales:", 24, GREY_B).move_to([-6.8, 1.9, 0], aligned_edge=LEFT),
                          *[fraccion(1, d, 46).move_to([x, 1.9, 0]) for d, x in zip((3, 5, 7), xs)])
        self.play(FadeIn(cabecera))
        escalas = [
            ("1 = 10 décimas", [2, 5], [(r"3{,}33\ldots", False), ("2", True), (r"1{,}42\ldots", False)],
             "En decimal, 1 = 10 décimas: solo se reparte bien entre 2 y 5"),
            ("1 docena = 12", [2, 2, 3], [("4", True), (r"2{,}4", False), (r"1{,}71\ldots", False)],
             "La docena: 12 = 2 · 2 · 3 tiene un 3, pero no un 5 (¡2,4 huevos!)"),
            ("1 h = 60 min", [2, 2, 3, 5], [(r"20\ \text{min}", True), (r"12\ \text{min}", True),
                                            (r"8{,}57\ldots", False)],
             "Los minutos: 60 tiene 2, 3 y 5"),
            ("1 vuelta = 360°", [2, 2, 2, 3, 3, 5], [(r"120^\circ", True), (r"72^\circ", True),
                                                     (r"51{,}4\ldots^\circ", False)],
             "Los grados: 360 tiene 2, 3 y 5 (¡y dos treses!)"),
        ]
        celdas = []
        for i, (et, ps, vals, nota) in enumerate(escalas):
            y = 0.95 - i * 0.9
            lab = texto(et, 26).move_to([-6.8, y, 0], aligned_edge=LEFT)
            b = VGroup(*[pieza(p, 0.22) for p in ps]).arrange(RIGHT, buff=0.06)
            b.move_to([-3.9, y, 0], aligned_edge=LEFT)
            notas(nota)
            self.play(FadeIn(lab), LaggedStart(*[GrowFromCenter(p) for p in b], lag_ratio=0.1), run_time=0.8)
            fila_c = VGroup(*[MathTex(v, font_size=40, color=OK if ok else MAL).move_to([x, y, 0])
                              for (v, ok), x in zip(vals, xs)])
            self.play(LaggedStart(*[Write(c) for c in fila_c], lag_ratio=0.4), run_time=1.2)
            celdas.append(fila_c)
            self.wait(1.2)
        col7 = VGroup(cabecera[3], *[f[2] for f in celdas])
        self.play(Create(SurroundingRectangle(col7, color=MAL, buff=0.15, corner_radius=0.1)))
        notas("Ninguna escala tiene un 7: un séptimo nunca sale exacto", color=MAL)
        self.wait(2)
        notas("Cada escala reparte exacto solo entre sus primos. La nuestra es el 10: solo 2 y 5")
        self.wait(3)
        notas.fin()
        limpiar(self, cab)

        # --- Resumen
        lineas = VGroup(
            texto("Fracción irreducible: mira los primos del denominador", 30),
            texto("solo 2 y 5  →  decimal exacto", 30, OK),
            texto("algún otro (3, 7, 11...)  →  periódico", 30, COLOR_PERIODO),
            texto("¡Ojo! Simplifica antes:  6/15 = 2/5 = 0,4", 24, GREY_B),
        ).arrange(DOWN, buff=0.35)
        card = tarjeta(lineas).move_to([0, -0.2, 0])
        self.play(FadeIn(card[0]), LaggedStart(*[FadeIn(l, shift=UP * 0.2) for l in lineas], lag_ratio=0.4))
        self.wait(4)


# ===========================================================================
def fila_x(coef, ent, ante, per, reps, size=56):
    """'100x = 36,3636...' con el periodo en rosa. Devuelve MathTex con [0]=coef x, [1]='=', resto."""
    partes = [coef + "x", "=", ent + "{,}" + ante if ante else ent + "{,}"]
    partes += [per] * reps + [r"\ldots"]
    t = MathTex(*partes, font_size=size)
    for i in range(3, 3 + reps):
        t[i].set_color(COLOR_PERIODO)
    if ante:
        t[2][len(ent) + 1:].set_color(COLOR_ANTE)
    t.coma = t[2][len(ent)]
    return t


def alinear_coma(filas, x):
    for f_ in filas:
        f_.shift(RIGHT * (x - f_.coma.get_x()))


def restar_filas(scene, arriba, abajo, coef, valor, notas):
    """Raya de la resta, colas tachadas y el resultado 'coef x = valor' (con las comas alineadas)."""
    menos = MathTex("-", font_size=56).next_to(abajo, LEFT, buff=0.35)
    menos.set_x(min(arriba.get_left()[0], abajo.get_left()[0]) - 0.4)
    y = abajo.get_bottom()[1] - 0.2
    raya = Line([menos.get_left()[0], y, 0], [max(arriba.get_right()[0], abajo.get_right()[0]), y, 0], stroke_width=3)
    scene.play(FadeIn(menos), Create(raya))
    notas("Restamos: las colas infinitas son iguales y se van")
    colas = VGroup(*[Line(m_.get_corner(DL), m_.get_corner(UR), color=MAL, stroke_width=4)
                     for f_ in (arriba, abajo) for m_ in f_[3:]])
    scene.play(Create(colas))
    res = MathTex(coef + "x", "=", valor, font_size=60)
    res.shift(RIGHT * (abajo.coma.get_x() - res[2].get_right()[0] - 0.1))
    res.set_y(y - 0.6)
    scene.play(Write(res))
    return res


def fila_regla(ent, ante, per, size=50):
    """0,4(36) = (436 − 4)/990 = 432/990 = 24/55 con las cifras del periodo en rosa y las del anteperiodo en azul.
    Devuelve VGroup(número, resto de trozos...) para escribirlos por partes."""
    todo, resta = int(ent + ante + per), int(ent + ante)
    a, b = str(todo), str(resta)
    num = f"{a} - {b}"
    den = "9" * len(per) + "0" * len(ante)
    f1 = fraccion(num, den, size, colores=False)
    # colores: en «a» las últimas cifras son periodo y antes anteperiodo; en «b» las últimas son anteperiodo
    for k, ch in enumerate(a):
        desde_fin = len(a) - k
        if desde_fin <= len(per):
            f1[0][0][k].set_color(COLOR_PERIODO)
        elif desde_fin <= len(per) + len(ante):
            f1[0][0][k].set_color(COLOR_ANTE)
    for k, ch in enumerate(b):
        if len(b) - k <= len(ante):
            f1[0][0][len(a) + 1 + k].set_color(COLOR_ANTE)
    for k, ch in enumerate(den):
        f1[2][0][k].set_color(COLOR_PERIODO if ch == "9" else COLOR_ANTE)
    v = todo - resta
    q = Fraction(v, int(den))
    trozos = [periodico(ent, ante, per, size + 6), MathTex("=", font_size=size), f1, MathTex("=", font_size=size)]
    if q.denominator == int(den):
        trozos.append(fraccion(v, int(den), size, color=ACENTO))
    else:
        trozos += [fraccion(v, int(den), size, colores=False), MathTex("=", font_size=size),
                   fraccion(q.numerator, q.denominator, size, color=ACENTO)]
    return VGroup(*trozos).arrange(RIGHT, buff=0.25)


def ejemplos_regla(scene, notas, datos, x=-5.6, y0=1.75, dy=1.55):
    filas = []
    for i, (ent, ante, per, nota) in enumerate(datos):
        f_ = fila_regla(ent, ante, per).move_to([x, y0 - i * dy, 0], aligned_edge=LEFT)
        scene.play(Write(f_[0]), run_time=0.7)
        notas(nota)
        scene.play(Write(VGroup(*f_[1:3])), run_time=1.0)
        scene.wait(0.8)
        scene.play(Write(VGroup(*f_[3:])), run_time=0.9)
        scene.wait(1.2)
        filas.append(f_)
    return filas


class FraccionGeneratriz(Scene):
    def construct(self):
        cab = titulo(self, "De decimal periódico a fracción", "La fracción generatriz")
        notas = Notas(self)

        # --- 1. La regla
        subtitulo(self, cab, "La regla")
        t1 = VGroup(texto("Periódico puro", 30, COLOR_PERIODO),
                    MathTex(r"\dfrac{\text{número sin coma} \;-\; \text{parte entera}}"
                            r"{\text{un 9 por cada cifra del periodo}}", font_size=40))
        t2 = VGroup(texto("Periódico mixto", 30, COLOR_ANTE),
                    MathTex(r"\dfrac{\text{número sin coma} \;-\; \text{lo que va antes del periodo}}"
                            r"{\text{un 9 por cifra del periodo y un 0 por cifra del anteperiodo}}", font_size=40))
        cards = []
        for t_, col in ((t1, COLOR_PERIODO), (t2, COLOR_ANTE)):
            t_.arrange(DOWN, buff=0.3)
            if t_.width > 12.4:
                t_.scale_to_fit_width(12.4)
            cards.append(tarjeta(t_, col))
        VGroup(*cards).arrange(DOWN, buff=0.45).move_to([0, -0.15, 0])
        self.play(FadeIn(cards[0], shift=UP * 0.2))
        notas("Puro: el periodo empieza justo después de la coma")
        self.wait(3)
        self.play(FadeIn(cards[1], shift=UP * 0.2))
        notas("Mixto: antes del periodo hay otras cifras (el anteperiodo)")
        self.wait(4)
        notas.fin()
        limpiar(self, cab)

        # --- 2. Tres ejemplos de periódico puro
        subtitulo(self, cab, "Periódico puro: ejemplos")
        ejemplos_regla(self, notas, [
            ("0", "", "7", "Periodo de 1 cifra: abajo un 9"),
            ("0", "", "36", "Periodo de 2 cifras: abajo 99. Luego simplificamos (entre 9)"),
            ("2", "", "5", "Con parte entera: 25 − 2 = 23 arriba"),
        ])
        self.wait(1)
        notas.fin()
        limpiar(self, cab)

        # --- 3. Tres ejemplos de periódico mixto
        subtitulo(self, cab, "Periódico mixto: ejemplos")
        ejemplos_regla(self, notas, [
            ("1", "2", "3", "Antes del periodo va 12: arriba 123 − 12. Abajo un 9 y un 0"),
            ("0", "4", "36", "Periodo de 2 cifras y anteperiodo de 1: abajo 990"),
            ("0", "58", "3", "Anteperiodo de 2 cifras: abajo 900"),
        ])
        self.wait(1)
        notas.fin()
        limpiar(self, cab)

        # --- 4. ¿Por qué funciona? Puro
        subtitulo(self, cab, "¿Por qué funciona? (puro)")
        n = periodico("0", "", "36", 64).move_to([4.2, 2.0, 0])
        self.play(Write(n))
        f1 = fila_x("", "0", "", "36", 3)
        f2 = fila_x("100", "36", "", "36", 3)
        alinear_coma([f1, f2], -1.6)
        f1.set_y(1.4)
        f2.set_y(0.3)
        self.play(Write(f1))
        notas("Llamamos x al número")
        self.wait(1)
        notas("El periodo tiene 2 cifras: multiplicamos por 100 (la coma salta 2 lugares)")
        self.play(Write(f2))
        self.wait(1.5)
        self.play(f1.animate.set_y(0.3), f2.animate.set_y(1.4))
        restar_filas(self, f2, f1, "99", "36", notas)
        self.wait(1)
        fin = M("x", "=", r"\dfrac{36}{99}", "=", (r"\dfrac{4}{11}", ACENTO), size=60).move_to([4.2, -1.0, 0])
        self.play(Write(fin))
        notas("Despejamos x: 36 entre 99, ¡justo lo que dice la regla!")
        self.play(Circumscribe(fin[2], color=ACENTO))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- 5. ¿Por qué funciona? Mixto
        subtitulo(self, cab, "¿Por qué funciona? (mixto)")
        n = periodico("1", "2", "3", 64).move_to([4.6, 2.0, 0])
        self.play(Write(n))
        f0 = fila_x("", "1", "2", "3", 4)
        f2 = fila_x("100", "123", "", "3", 4)
        f1 = fila_x("10", "12", "", "3", 4)
        alinear_coma([f0, f1, f2], -1.6)
        for f_, y in ((f0, 2.0), (f2, 0.9), (f1, -0.1)):
            f_.set_y(y)
        self.play(Write(f0))
        notas("Queremos dos números con la misma cola: el periodo justo detrás de la coma")
        self.wait(1.5)
        self.play(Write(f2))
        notas("×100: la coma salta el anteperiodo y el periodo (2 lugares)")
        self.wait(1.5)
        self.play(Write(f1))
        notas("×10: la coma salta solo el anteperiodo (1 lugar)")
        self.wait(1.5)
        self.play(f0.animate.set_opacity(0.4))
        restar_filas(self, f2, f1, "90", "111", notas)
        notas("100x − 10x = 90x   y   123 − 12 = 111")
        fin = M("x", "=", r"\dfrac{111}{90}", "=", (r"\dfrac{37}{30}", ACENTO), size=60).move_to([4.2, -1.3, 0])
        self.play(Write(fin))
        notas("123 − 12 arriba y 90 abajo: ¡otra vez la regla!")
        self.play(Circumscribe(fin[2], color=ACENTO))
        self.wait(2.5)
        notas.fin()


# ===========================================================================
class CombinadasDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones combinadas", "con decimales")
        notas = Notas(self)
        esc = escalera(20, 4.4).scale(0.9).to_corner(UR).shift(DOWN * 0.6)
        self.play(FadeIn(esc))
        resolver_f(self, "4,2-(1,5+0,3)*2", -6.2, 2.0, size=54, dy=0.9, notas=notas, ejemplo=True, modo="dec")
        self.wait(2)
        limpiar(self, cab)

        subtitulo(self, cab, "Con potencias y raíces")
        resolver_f(self, "1,2^2:0,4-sqrt(0,49)", -5.0, 1.8, size=56, dy=0.95, notas=notas, ejemplo=True, modo="dec")
        self.wait(2)
        limpiar(self, cab)

        subtitulo(self, cab, "Si hay periódicos: mejor en fracción")
        e = M(r"0{,}\overset{\frown}{3} + \dfrac{1}{6}", size=60).move_to([-3.2, 1.8, 0])
        self.play(Write(e))
        notas("0,333... no se puede escribir entero: lo pasamos a fracción, 0,(3) = 3/9 = 1/3")
        self.wait(2)
        resolver_f(self, "1/3+1/6", -4.6, 0.3, size=56, dy=1.45, notas=notas, ejemplo=True, al_lado=True)
        self.wait(2.5)


# ===========================================================================
class RaicesDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Raíces cuadradas", "con decimales")
        notas = Notas(self)

        subtitulo(self, cab, "Raíces exactas")
        a = M(r"\sqrt{0{,}49} =", ("0{,}7", ACENTO), size=60).move_to([-3.6, 1.6, 0])
        ac = M(r"\text{porque } 0{,}7^2 = 0{,}7 \cdot 0{,}7 = 0{,}49", size=40).next_to(a, DOWN, buff=0.35)
        b = M(r"\sqrt{1{,}44} =", ("1{,}2", ACENTO), size=60).move_to([3.4, 1.6, 0])
        bc = M(r"\text{porque } 1{,}2^2 = 1{,}44", size=40).next_to(b, DOWN, buff=0.35)
        self.play(Write(a))
        self.play(FadeIn(ac))
        self.play(Write(b))
        self.play(FadeIn(bc))
        notas("Al elevar al cuadrado, se duplican los decimales: la raíz tiene la mitad")
        self.wait(2)
        error = M(r"\sqrt{0{,}9}", r"= 0{,}3", size=60).move_to([-2.0, -1.2, 0])
        self.play(Write(error))
        tachar(self, error[1])
        expl = M((r"0{,}3^2 = 0{,}09 \neq 0{,}9", MAL), size=44).next_to(error, RIGHT, buff=1.4)
        self.play(Write(expl))
        notas("¡Cuidado! 0,9 tiene 1 decimal (impar): su raíz no es exacta")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Aproximar √20
        subtitulo(self, cab, "Aproximar √20")
        t = M(r"4^2 = 16 \ <\ 20\ <\ 25 = 5^2", size=48).move_to([0, 2.3, 0])
        self.play(Write(t))
        notas("√20 está entre 4 y 5. Probamos con las décimas")
        r1 = NumberLine(x_range=[4, 5, 0.1], length=12, include_tip=False, stroke_width=3, tick_size=0.1)
        r1.move_to([0, 0.9, 0])
        e1 = VGroup(*[MathTex(dec_str(Fraction(40 + k, 10)).replace(",", "{,}"), font_size=26)
                      .next_to(r1.n2p(4 + k / 10), DOWN, buff=0.2) for k in range(11)])
        self.play(Create(r1), FadeIn(e1))
        pr = VGroup(M(r"4{,}4^2 = 19{,}36", r"\ <\ 20", size=40), M(r"4{,}5^2 = 20{,}25", r"\ >\ 20", size=40))
        pr.arrange(RIGHT, buff=1.2).move_to([0, -0.5, 0])
        pr[0][1].set_color(OK)
        pr[1][1].set_color(MAL)
        self.play(Write(pr[0]))
        self.play(Write(pr[1]))
        tramo = Line(r1.n2p(4.4), r1.n2p(4.5), color=ACENTO, stroke_width=10)
        self.play(Create(tramo))
        a1 = M(r"\sqrt{20} \approx", ("4{,}4", ACENTO), size=48).move_to([0, -1.5, 0])
        self.play(Write(a1))
        notas("Aproximación a las décimas (por defecto)")
        self.wait(1.5)
        # centésimas
        self.play(FadeOut(pr), FadeOut(a1), FadeOut(t))
        r2 = NumberLine(x_range=[4.4, 4.5, 0.01], length=12, include_tip=False, stroke_width=3, tick_size=0.1)
        r2.move_to([0, -1.0, 0])
        e2 = VGroup(*[MathTex(dec_str(Fraction(440 + k, 100), True), font_size=22)
                      .next_to(r2.n2p(4.4 + k / 100), DOWN, buff=0.2) for k in range(0, 11, 2)])
        zoom = VGroup(DashedLine(r1.n2p(4.4), r2.n2p(4.4), color=GREY_B), DashedLine(r1.n2p(4.5), r2.n2p(4.5), color=GREY_B))
        notas("Repetimos con las centésimas, entre 4,4 y 4,5")
        self.play(Create(zoom), Create(r2), FadeIn(e2))
        pr2 = VGroup(M(r"4{,}47^2 = 19{,}9809", r"\ <\ 20", size=38), M(r"4{,}48^2 = 20{,}0704", r"\ >\ 20", size=38))
        pr2.arrange(RIGHT, buff=0.8).move_to([0, 2.1, 0])
        pr2[0][1].set_color(OK)
        pr2[1][1].set_color(MAL)
        self.play(Write(pr2[0]))
        self.play(Write(pr2[1]))
        tramo2 = Line(r2.n2p(4.47), r2.n2p(4.48), color=ACENTO, stroke_width=10)
        self.play(Create(tramo2))
        a2 = M(r"\sqrt{20} \approx", ("4{,}47", ACENTO), size=50).move_to([0, -2.5, 0])
        self.play(Write(a2))
        notas("La calculadora dice 4,4721...: ¡bien aproximado!")
        self.wait(3)
        notas.fin()


# ===========================================================================
def cient(a, n, size=56, color=ACENTO):
    """a · 10ⁿ para M(): a (str con {,}) y la potencia de 10."""
    return [(a, color), r"\cdot", ("10", BASE), ("^{" + str(n) + "}", EXPONENTE)]


def saltar_coma(scene, cifras, saltos, y, size=72, notas=None):
    """Escribe un número entero (cifras) y mueve la coma 'saltos' lugares hacia la izquierda contando."""
    ds = VGroup(*[MathTex(c, font_size=size) for c in cifras]).arrange(RIGHT, buff=0.12).move_to([0, y, 0])
    scene.play(Write(ds))
    coma = MathTex(",", font_size=size, color=ACENTO)
    base_y = ds.get_bottom()[1] + 0.02

    def pos(j):  # hueco detrás de la cifra j
        x = (ds[j].get_right()[0] + ds[j + 1].get_left()[0]) / 2 if j + 1 < len(ds) else ds[j].get_right()[0] + 0.08
        return np.array([x, base_y, 0])

    coma.move_to(pos(len(ds) - 1), aligned_edge=DOWN)
    scene.play(FadeIn(coma, scale=2))
    cuenta = VGroup()
    for k in range(saltos):
        j = len(ds) - 2 - k
        a = pos(j + 1)
        b = pos(j)
        arco = ArcBetweenPoints(a + UP * (ds.height + 0.15), b + UP * (ds.height + 0.15), angle=-PI / 1.5,
                                color=ACENTO, stroke_width=3)
        num = MathTex(str(k + 1), font_size=26, color=ACENTO).next_to(arco, UP, buff=0.05)
        scene.play(Create(arco), FadeIn(num), coma.animate.move_to(b, aligned_edge=DOWN), run_time=0.35)
        cuenta.add(arco, num)
    return ds, coma, cuenta


class NotacionCientifica(Scene):
    def construct(self):
        cab = titulo(self, "Notación científica", "Números muy grandes")
        notas = Notas(self)

        d = M(r"\text{Distancia Tierra--Sol: }", r"150\,000\,000", r"\text{ km}", size=48).move_to([0, 2.0, 0])
        self.play(Write(d))
        notas("Tantos ceros cansan... y es fácil equivocarse al contarlos")
        self.wait(1.5)
        pot = VGroup(*[M(("10", BASE), ("^{" + str(k) + "}", EXPONENTE), "=", "1" + "0" * k, size=40)
                       for k in (1, 2, 3, 6)]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -0.4, 0])
        self.play(LaggedStart(*[FadeIn(p) for p in pot], lag_ratio=0.3))
        notas("Las potencias de 10: el exponente dice cuántos ceros hay")
        self.wait(2)
        notas.fin()
        self.play(FadeOut(pot))

        # --- La coma salta
        ds, coma, cuenta = saltar_coma(self, "150000000", 8, 0.0, notas=notas)
        notas("Movemos la coma hasta dejar una sola cifra (no nula) delante: 8 saltos")
        self.wait(1.5)
        res = M(r"150\,000\,000 =", *cient(r"1{,}5", 8, 60), size=60).move_to([0, -1.8, 0])
        self.play(Write(res))
        self.play(Circumscribe(res[1:], color=ACENTO))
        self.wait(2)
        notas.fin()
        limpiar(self, cab)

        # --- Forma general
        subtitulo(self, cab, "La forma")
        rg = regla(("a", ACENTO), r"\cdot", ("10", BASE), ("^{n}", EXPONENTE),
                   frase="1 ≤ a < 10  (una sola cifra antes de la coma, que no sea 0)", size=72).move_to([0, 1.6, 0])
        self.play(FadeIn(rg))
        ej = [M(r"45\,000\,000 =", *cient(r"4{,}5", 7, 52), size=52),
              M(r"302\,000\,000\,000 =", *cient(r"3{,}02", 11, 52), size=52)]
        VGroup(*ej).arrange(DOWN, buff=0.45).move_to([0, -1.0, 0])
        for e in ej:
            self.play(Write(e))
            self.wait(0.8)
        notas("Contamos las cifras que hay detrás de la primera: 7 y 11")
        self.wait(2.5)
        notas.fin()
        limpiar(self, cab)

        # --- Al revés y no científica
        subtitulo(self, cab, "Al revés, y una trampa")
        r = M(*cient(r"6{,}2", 5, 56), "=", r"620\,000", size=56).move_to([0, 2.0, 0])
        self.play(Write(r))
        notas("La coma salta 5 lugares a la derecha: rellenamos con ceros")
        self.wait(2)
        t = M(r"25 \cdot 10^{6}", size=56).move_to([-3.8, 0.0, 0])
        self.play(Write(t))
        no = texto("25 tiene dos cifras:\nno es notación científica", 26, MAL).next_to(t, DOWN, buff=0.4)
        self.play(FadeIn(no))
        bien = M("=", *cient(r"2{,}5", 7, 56), size=56).next_to(t, RIGHT, buff=0.4)
        self.play(Write(bien))
        notas("25 = 2,5 · 10: el exponente sube 1")
        self.wait(3)
        notas.fin()


class OperacionesNotacion(Scene):
    def construct(self):
        cab = titulo(self, "Operaciones", "en notación científica")
        notas = Notas(self)

        subtitulo(self, cab, "Multiplicar")
        lineas = [(L(r"(3 \cdot 10^{5}) \cdot (2 \cdot 10^{4})", size=44), None),
                  (L(r"(3 \cdot 2) \cdot (10^{5} \cdot 10^{4})", size=44), "Juntamos los números y las potencias de 10"),
                  (L(*cient("6", 9, 52), size=44), "Misma base: sumamos los exponentes, 5 + 4 = 9")]
        pasos(self, lineas, -6.4, 1.8, dy=1.0, notas=notas, ejemplo=True)
        self.wait(1)
        lineas = [(L(r"(6 \cdot 10^{5}) \cdot (5 \cdot 10^{7})", size=44), None),
                  (L(r"30 \cdot 10^{12}", size=44), "6 · 5 = 30 y 5 + 7 = 12"),
                  (L(*cient("3", 13, 52), size=44), "30 = 3 · 10: ajustamos, el exponente sube 1")]
        pasos(self, lineas, 0.6, 1.8, dy=1.0, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Dividir")
        lineas = [(L(r"(8 \cdot 10^{9}) : (2 \cdot 10^{3})", size=44), None),
                  (L(r"(8 : 2) \cdot (10^{9} : 10^{3})", size=44), None),
                  (L(*cient("4", 6, 52), size=44), "Misma base: restamos los exponentes, 9 − 3 = 6")]
        pasos(self, lineas, -6.4, 1.8, dy=1.0, notas=notas, ejemplo=True)
        lineas = [(L(r"(1{,}2 \cdot 10^{8}) : (4 \cdot 10^{3})", size=44), None),
                  (L(r"0{,}3 \cdot 10^{5}", size=44), "1,2 : 4 = 0,3 y 8 − 3 = 5"),
                  (L(*cient("3", 4, 52), size=44), "0,3 empieza por 0: 0,3 = 3 : 10, así que el exponente baja 1")]
        pasos(self, lineas, 0.6, 1.8, dy=1.0, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Sumar y restar")
        lineas = [(L(r"2{,}5 \cdot 10^{6} + 4 \cdot 10^{6}", size=44), None),
                  (L(r"(2{,}5 + 4) \cdot 10^{6}", size=44), "Mismo exponente: sumamos los números"),
                  (L(*cient(r"6{,}5", 6, 52), size=44), None)]
        pasos(self, lineas, -6.4, 1.8, dy=1.0, notas=notas, ejemplo=True)
        lineas = [(L(r"3 \cdot 10^{7} + 5 \cdot 10^{6}", size=44), None),
                  (L(r"30 \cdot 10^{6} + 5 \cdot 10^{6}", size=44), "Distinto exponente: primero los igualamos"),
                  (L(r"35 \cdot 10^{6}", "=", *cient(r"3{,}5", 7, 52), size=44), "Y ajustamos: 35 = 3,5 · 10")]
        pasos(self, lineas, 0.6, 1.8, dy=1.0, notas=notas, ejemplo=True)
        notas.fin()
        self.wait(2.5)


assert valor_expr("2-3/4+5/6") == Fraction(25, 12)
assert valor_expr("-1/6+3/4-5/12") == Fraction(1, 6)
assert valor_expr("(1/2+1/3)*3/5-1/4") == Fraction(1, 4)
assert valor_expr("3-2/5*(1/2+3/4)") == Fraction(5, 2)
assert valor_expr("4,2-(1,5+0,3)*2", "dec") == Fraction(6, 10)
assert valor_expr("1,2^2:0,4-sqrt(0,49)", "dec") == Fraction(29, 10)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
SIMPLIFICA = [(18, 24), (45, 75), (84, 126)]
ORDENA = [[(3, 4), (5, 6), (2, 3), (7, 12)], [(-1, 2), (3, 5), (-3, 4), (1, 10)]]
SUMAS = ["2/3+5/6", "3/4-5/6", "2-3/5+1/10", "-1/4+5/6-1/3"]
MULDIV = ["4/9*3/8", "-5/6:10/3", "6*(-2/9)", "3/4:9/2*6"]
POTENCIAS = ["(2/3)^3", "(-1/2)^4", "(-3/5)^3", "(5/7)^0"]
UNA_POTENCIA = [
    ("(2/3)⁴ · (2/3)³", [[*PF(2, 3, 4), r"\cdot", *PF(2, 3, 3)], [*PF(2, 3, "4+3")], [*PF(2, 3, 7)]],
     "Misma base: sumamos exponentes"),
    ("(3/5)⁷ : (3/5)⁵", [[*PF(3, 5, 7), ":", *PF(3, 5, 5)], [*PF(3, 5, "7-5")], [*PF(3, 5, 2), "=", (r"\dfrac{9}{25}", ACENTO)]],
     "Misma base: restamos exponentes"),
    ("[(1/2)³]²", [[r"\Big[", *PF(1, 2, 3), r"\Big]", ("^{2}", EXPONENTE)], [*PF(1, 2, r"3 \cdot 2")],
                   [*PF(1, 2, 6), "=", (r"\dfrac{1}{64}", ACENTO)]], "Potencia de potencia: multiplicamos exponentes"),
]
COMBINADAS = ["1/2+3/4*2/3", "(2/3-1/4):5/6", "(1/2)^2+3/4:(-3/2)", "2-(1/3+1/2)*6/5"]
FRAC_DEC = [(7, 8), (5, 11), (7, 12)]
GENERATRIZ = [("0", "45", "", None), ("0", "", "7", None), ("2", "1", "6", None)]
DECIMALES = ["2,5-1,2*0,5", "(3,6-1,8):0,6+0,25", "0,3^2+1,5:0,25"]
RAICES = ["0,64", "1,21", "30"]

for _s in SUMAS + MULDIV + POTENCIAS + COMBINADAS:
    valor_expr(_s)
for _s in DECIMALES:
    valor_expr(_s, "dec")
assert valor_expr(COMBINADAS[0]) == 1 and valor_expr(COMBINADAS[3]) == 1
assert valor_expr(SUMAS[3]) == Fraction(1, 4)


def txt_f(s):
    """Expresión del motor en texto para los enunciados."""
    t = s.replace("sqrt", "√").replace("*", " · ").replace(":", " : ")
    t = re.sub(r"(?<=[\d)\]])([+-])", r" \1 ", t)
    t = re.sub(r"\^(\d+)", lambda m: m.group(1).translate(SUP), t)
    return t.replace("-", MENOS)


def lista(items, por_linea=4, sep="      "):
    trozos = [f"{l}) {t}" for l, t in zip("abcdefgh", items)]
    return "\n".join(sep.join(trozos[i:i + por_linea]) for i in range(0, len(trozos), por_linea))


def pagina_enunciados(scene, cab, bloques, size=25):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 27, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
    if grupo.width > config.frame_width - 1.0:
        grupo.scale_to_fit_width(config.frame_width - 1.0).to_edge(LEFT, buff=0.5)
    if grupo.get_bottom()[1] < -3.0:
        grupo.scale(((cab.get_bottom()[1] - 0.4) + 3.0) / grupo.height).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.3)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


PROBLEMA = ("Un depósito de 600 litros está lleno. El lunes se gastan 2/5 del agua\n"
            "y el martes, 1/4 de lo que quedaba. ¿Cuántos litros quedan?")
LUZ = "La luz recorre 3 · 10⁵ km por segundo. ¿Cuántos km recorre en un día (8,64 · 10⁴ s)?"


def txt_gen(it):
    ent, ante, per, _ = it
    return f"{ent},{ante}" + (f"({per})" if per else "")


def enunciados_1():
    return [
        ("1. Simplifica hasta la fracción irreducible:", lista([f"{n}/{d}" for n, d in SIMPLIFICA], 3)),
        ("2. Ordena de menor a mayor:", "\n".join(
            f"{l}) " + ",   ".join(ft(Fraction(n, d)) for n, d in o) for l, o in zip("ab", ORDENA))),
        ("3. Calcula y simplifica:", lista([txt_f(s) for s in SUMAS], 4)),
        ("4. Multiplica y divide:", lista([txt_f(s) for s in MULDIV], 4)),
        ("5. Calcula:", lista([txt_f(s) for s in POTENCIAS], 4)),
    ]


def enunciados_2():
    return [
        ("6. Escribe como una sola potencia:", lista([u[0] for u in UNA_POTENCIA], 3)),
        ("7. Calcula paso a paso:", lista([txt_f(s) for s in COMBINADAS], 2)),
        ("8. Problema:", PROBLEMA),
        ("9. Pasa a decimal y di de qué tipo es:", lista([f"{n}/{d}" for n, d in FRAC_DEC], 3)),
    ]


def enunciados_3():
    return [
        ("10. Escribe la fracción generatriz (el periodo entre paréntesis):", lista([txt_gen(g) for g in GENERATRIZ], 3)),
        ("11. Calcula:", lista([txt_f(s) for s in DECIMALES], 3)),
        ("12. Raíces:", "a) √0,64      b) √1,21      c) √30 aproximada a las centésimas"),
        ("13. Notación científica:", "a) Escribe en notación científica: 45 000 000  y  302 000 000 000\n"
                                     f"b) (2,5 · 10⁶) · (4 · 10³)      c) (9 · 10¹²) : (3 · 10⁴)\n"
                                     f"d) {LUZ}"),
    ]


# --- 2. Ordenar
def ej_ordena(scene, fracs, letra, notas, ejemplo=False):
    vals = [Fraction(n, d) for n, d in fracs]
    m = lcm(*[d for _, d in fracs])
    lab = texto(f"{letra}) De menor a mayor", 28, ACENTO).move_to([-4.6, 2.6, 0])
    xs = [-4.6, -1.6, 1.4, 4.4]
    orig = [MathTex(fr(n, d), font_size=54).move_to([x - 0.5, 1.5, 0]) for (n, d), x in zip(fracs, xs)]
    scene.play(FadeIn(lab), LaggedStart(*[Write(f) for f in orig], lag_ratio=0.15))
    t = MathTex(rf"\text{{m.c.m.}}({', '.join(str(d) for _, d in fracs)}) = {m}", font_size=38, color=ACENTO)
    t.move_to([2.6, 2.6, 0])
    scene.play(Write(t))
    notas("Pasamos todas a denominador " + str(m) + " y comparamos los numeradores")
    nuevas = []
    for (n, d), f in zip(fracs, orig):
        g = MathTex("=", fr(n * m // d, m), font_size=46).next_to(f, RIGHT, buff=0.12)
        scene.play(FadeIn(g), run_time=0.5)
        nuevas.append(g)
    lo = -1 if min(vals) < 0 else 0
    recta = NumberLine(x_range=[lo, 1, 1 / m], length=12, include_tip=False, stroke_width=3, tick_size=0.07)
    recta.move_to([0, -1.0, 0])
    marcas = VGroup(*[MathTex(str(v), font_size=30).next_to(recta.n2p(v), DOWN, buff=0.2)
                      for v in range(lo, 2)])
    scene.play(Create(recta), FadeIn(marcas))
    for v, f in zip(vals, orig):
        dot = Dot(recta.n2p(float(v)), radius=0.09, color=NEGATIVO if v < 0 else ACENTO)
        scene.play(f.copy().animate.scale(0.6).next_to(recta.n2p(float(v)), UP, buff=0.2), FadeIn(dot), run_time=0.5)
    if lo < 0:
        notas("Los negativos van antes que los positivos")
    orden = sorted(range(len(fracs)), key=lambda i: vals[i])
    partes = []
    for j, i in enumerate(orden):
        if j:
            partes.append("<")
        partes.append(fr(*fracs[i]))
    c = MathTex(*partes, font_size=50).move_to([0, -2.4, 0])
    scene.play(Write(c), run_time=1.3)
    scene.play(Circumscribe(c, color=ACENTO))
    notas.fin()
    scene.wait(1.5 if ejemplo else 1)


# --- 6. Una sola potencia
def ej_una_potencia(scene, i, x, y0, notas, ejemplo=False, size=48):
    _, ls, nota = UNA_POTENCIA[i]
    lineas = [(L(*partes, size=size), nota if k == 1 else None) for k, partes in enumerate(ls)]
    pasos(scene, lineas, x, y0, dy=size / 40, notas=notas, ejemplo=ejemplo, etiqueta=f"{'abc'[i]})")


# --- 8. Problema del depósito
def problema_deposito(scene, notas, ejemplo=False):
    e = texto(PROBLEMA, 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    lineas = [
        (M(r"\text{Lunes: }", r"\dfrac{2}{5} \text{ de } 600 = 600 : 5 \cdot 2 =", ("240", ACENTO), r"\text{ L}", size=40),
         "Fracción de una cantidad: dividimos entre el denominador y multiplicamos por el numerador"),
        (M(r"\text{Quedan: }", r"600 - 240 =", ("360", ACENTO), r"\text{ L}", size=40), None),
        (M(r"\text{Martes: }", r"\dfrac{1}{4} \text{ de } 360 = 360 : 4 =", ("90", ACENTO), r"\text{ L}", size=40),
         "¡Ojo! El 1/4 es de lo que quedaba (360), no de 600"),
        (M(r"\text{Quedan: }", r"360 - 90 =", ("270", ACENTO), r"\text{ L}", size=40), None),
    ]
    for i, (m_, nota) in enumerate(lineas):
        m_.move_to([-5.8, 1.1 - i * 1.0, 0], aligned_edge=LEFT)
        scene.play(Write(m_), run_time=0.9)
        if nota:
            notas(nota)
            scene.wait(1.5 if ejemplo else 0.8)
    notas.fin()
    sol = texto("Quedan 270 litros", 32, OK).to_edge(DOWN, buff=0.45)
    scene.play(FadeIn(sol))
    scene.wait(2)


# --- 9. Fracción → decimal
def ej_frac_dec(scene, n, d, letra, notas, ejemplo=False):
    lab = texto(f"{letra})", 30).move_to([-6.3, 1.6, 0])
    f = VGroup(fraccion(n, d, 64), MathTex(f"= {n} : {d}", font_size=52)).arrange(RIGHT, buff=0.3)
    f.next_to(lab, RIGHT, buff=0.3)
    scene.play(FadeIn(lab), Write(f))
    q = division_larga(scene, str(n), d, -0.4, 1.7, size=50, max_dec=4, lateral=True, rt=0.4 if ejemplo else 0.3)
    v = Fraction(n, d)
    # tipo
    ds = d
    for p in (2, 5):
        while ds % p == 0:
            ds //= p
    if ds == 1:
        num = MathTex(dec_str(v, True), font_size=56)
        tipo, col = "Decimal exacto", OK
    else:
        dec = q.split(",")[1]
        # buscar periodo con la división real
        r, digs, vistos = n % d, "", {}
        while r not in vistos:
            vistos[r] = len(digs)
            r *= 10
            digs += str(r // d)
            r %= d
        ini = vistos[r]
        ante, per = digs[:ini], digs[ini:]
        num = periodico(str(n // d), ante, per, 60)
        tipo, col = ("Periódico mixto", COLOR_ANTE) if ante else ("Periódico puro", COLOR_PERIODO)
    res = VGroup(fraccion(n, d, 56), MathTex("=", font_size=52), num).arrange(RIGHT, buff=0.25).move_to([-3.8, -0.9, 0])
    scene.play(Write(res))
    t = texto(tipo, 32, col).next_to(res, DOWN, buff=0.4)
    scene.play(FadeIn(t))
    if ejemplo:
        notas("Resto 0: la división termina" if ds == 1 else "Un resto se repite: las cifras se repiten")
        scene.wait(1.5)
    notas.fin()
    scene.wait(1.5)


# --- 10. Fracción generatriz
def ej_generatriz(scene, it, x, y0, notas, letra, ejemplo=False, size=48):
    ent, ante, per, _ = it
    if not per:
        k = len(ante)
        n = int(ent + ante)
        v = Fraction(n, 10 ** k)
        lineas = [(L(f"{ent}{{,}}{ante}", size=size), None),
                  (L(fr(n, 10 ** k), size=size), f"Decimal exacto: {k} decimales → denominador 1" + "0" * k)]
        if v.denominator != 10 ** k:
            lineas.append((L((fr(v.numerator, v.denominator), ACENTO), size=size),
                           f"Simplificamos entre {10 ** k // v.denominator}"))
        pasos(scene, lineas, x, y0, dy=1.2, notas=notas, ejemplo=ejemplo, etiqueta=f"{letra})")
        return
    todo = int(ent + ante + per)
    sin = int(ent + ante)
    den = int("9" * len(per) + "0" * len(ante))
    v = Fraction(todo - sin, den)
    over = rf"{ent}{{,}}{ante}\overset{{\frown}}{{{per}}}"
    if sin == 0:
        lineas = [(L(over, size=size), None),
                  (L((fr(todo, den), ACENTO), size=size),
                   f"Periódico puro: el periodo arriba y un 9 por cada cifra del periodo abajo")]
        pasos(scene, lineas, x, y0, dy=1.15, notas=notas, ejemplo=ejemplo, etiqueta=f"{letra})")
        return
    lineas = [(L(over, size=size), None),
              (L(rf"\dfrac{{{todo} - {sin}}}{{{den}}}", size=size),
               f"Número sin coma ({todo}) − lo que no se repite ({sin}); " +
               f"{len(per)} nueve" + ("s" if len(per) > 1 else "") +
               (f" y {len(ante)} cero" + ("s" if len(ante) > 1 else "") if ante else "") + " abajo"),
              (L(fr(todo - sin, den), size=size), None)]
    if (v.numerator, v.denominator) != (todo - sin, den):
        lineas.append((L((fr(v.numerator, v.denominator), ACENTO), size=size),
                       f"Simplificamos entre {(todo - sin) // v.numerator}"))
    pasos(scene, lineas, x, y0, dy=1.15, notas=notas, ejemplo=ejemplo, etiqueta=f"{letra})")


# --- 12. Raíces
def ej_raiz(scene, s, letra, x, y0, notas, ejemplo=False, size=52):
    v = Fraction(s.replace(",", "."))
    if "," in s:
        r = raiz_exacta(v)
        lineas = [(L(rf"\sqrt{{{s.replace(',', '{,}')}}}", size=size), None),
                  (L((dec_str(r, True), ACENTO), size=size),
                   f"Porque {dec_str(r)}² = {s}: dos decimales → la raíz tiene uno")]
        pasos(scene, lineas, x, y0, dy=1.0, notas=notas, ejemplo=ejemplo, etiqueta=f"{letra})")
        return
    n = int(s)
    a = isqrt(n)
    b = next(k for k in range(10 * a, 10 * a + 11) if k * k > 100 * n) - 1
    c = next(k for k in range(10 * b, 10 * b + 11) if k * k > 100 * 100 * n) - 1

    def sq(k, dec):
        return dec_str(Fraction(k * k, 10 ** (2 * dec)), True)

    filas = [
        (M(rf"{a}^2 = {a * a} < {n} < {(a + 1) ** 2} = {a + 1}^2", size=size - 6), f"√{n} está entre {a} y {a + 1}"),
        (M(rf"{dec_str(Fraction(b, 10), True)}^2 = {sq(b, 1)} < {n} < {sq(b + 1, 1)} = {dec_str(Fraction(b + 1, 10), True)}^2",
           size=size - 6), "Décimas: probamos hasta pasarnos"),
        (M(rf"{dec_str(Fraction(c, 100), True)}^2 = {sq(c, 2)} < {n} < {sq(c + 1, 2)} = {dec_str(Fraction(c + 1, 100), True)}^2",
           size=size - 6), "Centésimas: lo mismo, un paso más fino"),
        (M(rf"\sqrt{{{n}}} \approx", (dec_str(Fraction(c, 100), True), ACENTO), size=size), None),
    ]
    lab = texto(f"{letra})", 28).move_to([x - 0.5, y0, 0])
    scene.play(FadeIn(lab))
    for i, (m_, nota) in enumerate(filas):
        m_.move_to([x, y0 - i * 1.0, 0], aligned_edge=LEFT)
        scene.play(Write(m_), run_time=0.9)
        if nota:
            notas(nota)
            scene.wait(1.3 if ejemplo else 0.7)
    scene.play(Circumscribe(filas[-1][0], color=ACENTO))
    notas.fin()


# --- 13. Notación científica
def ej_cient(scene, k, notas, ejemplo=False):
    if k == 0:
        ds, coma, cuenta = saltar_coma(scene, "45000000", 7, 1.2)
        r1 = M(r"45\,000\,000 =", *cient(r"4{,}5", 7, 52), size=52).move_to([0, -0.6, 0])
        scene.play(Write(r1))
        r2 = M(r"302\,000\,000\,000 =", *cient(r"3{,}02", 11, 52), size=52).next_to(r1, DOWN, buff=0.5)
        notas("Contamos las cifras detrás de la primera")
        scene.play(Write(r2))
        notas.fin()
        scene.wait(1.5)
        return
    if k == 1:
        lineas = [(L(r"(2{,}5 \cdot 10^{6}) \cdot (4 \cdot 10^{3})", size=52), None),
                  (L(r"10 \cdot 10^{9}", size=52), "2,5 · 4 = 10 y 6 + 3 = 9"),
                  (L(*cient("1", 10, 52), size=52), "10 = 1 · 10: el exponente sube 1")]
    elif k == 2:
        lineas = [(L(r"(9 \cdot 10^{12}) : (3 \cdot 10^{4})", size=52), None),
                  (L(*cient("3", 8, 52), size=52), "9 : 3 = 3 y 12 − 4 = 8")]
    else:
        e = texto(LUZ.replace(". ", ".\n"), 26).move_to([0, 2.4, 0])
        scene.play(Write(e))
        lineas = [(L(r"(3 \cdot 10^{5}) \cdot (8{,}64 \cdot 10^{4})", size=50), "Distancia = velocidad · tiempo"),
                  (L(r"25{,}92 \cdot 10^{9}", size=50), "3 · 8,64 = 25,92 y 5 + 4 = 9"),
                  (L(*cient(r"2{,}592", 10, 50), r"\text{ km}", size=50), "Ajustamos: la coma salta 1 a la izquierda")]
        pasos(scene, lineas, -5.0, 1.0, dy=1.0, notas=notas, ejemplo=ejemplo)
        notas.fin()
        scene.wait(1.5)
        return
    pasos(scene, lineas, -4.8, 1.2, dy=1.0, notas=notas, ejemplo=ejemplo)
    notas.fin()
    scene.wait(1.2)


def ej_expr(scene, s, letra, notas, ejemplo=False, modo="frac", x=-4.0, y0=None, size=None, dy=None):
    n = num_lineas(s, modo)
    size = size or (54 if ejemplo else 48)
    dy = dy or (1.15 if modo == "frac" else 0.85) * size / 48
    if y0 is None:
        y0 = min(2.0, (n - 1) * dy / 2 - 0.2)
    resolver_f(scene, s, x, y0, size=size, dy=dy, notas=notas, ejemplo=ejemplo, etiqueta=f"{letra})", modo=modo)


def dos_expr(scene, items, letras, notas, modo="frac", size=44):
    """Dos expresiones lado a lado."""
    dy = (1.1 if modo == "frac" else 0.8) * size / 48
    for s, l, x in zip(items, letras, (-6.0, 0.9)):
        resolver_f(scene, s, x, 1.8, size=size, dy=dy, notas=notas, etiqueta=f"{l})", modo=modo)
    scene.wait(1.2)


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Fracciones y decimales")
        notas = Notas(self)
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2())
        pagina_enunciados(self, cab, enunciados_3())
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))

        subtitulo(self, cab, "Ejercicio 1 a)")
        resolver_simplifica(self, SIMPLIFICA[:1], "a", ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 a)")
        ej_ordena(self, ORDENA[0], "a", notas, ejemplo=True)
        limpiar(self, cab)
        for k, (lista_, nombre) in enumerate(((SUMAS, 3), (MULDIV, 4), (POTENCIAS, 5))):
            subtitulo(self, cab, f"Ejercicio {nombre} a)")
            ej_expr(self, lista_[0], "a", notas, ejemplo=True)
            self.wait(1)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6 a)")
        ej_una_potencia(self, 0, -3.5, 1.6, notas, ejemplo=True, size=56)
        notas.fin()
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 7 a)")
        ej_expr(self, COMBINADAS[0], "a", notas, ejemplo=True)
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 8")
        problema_deposito(self, notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 9 a)")
        ej_frac_dec(self, *FRAC_DEC[0], "a", notas, ejemplo=True)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 10 a)")
        ej_generatriz(self, GENERATRIZ[0], -3.0, 1.6, notas, "a", ejemplo=True, size=58)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 11 a)")
        ej_expr(self, DECIMALES[0], "a", notas, ejemplo=True, modo="dec")
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 12 a)")
        ej_raiz(self, RAICES[0], "a", -3.0, 1.0, notas, ejemplo=True, size=60)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 13 a)")
        ej_cient(self, 0, notas, ejemplo=True)
        limpiar(self, cab)

        fin = texto("En los siguientes vídeos resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos1(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 1 a 7")
        notas = Notas(self, size=24)
        subtitulo(self, cab, "Ejercicio 1: b) y c)")
        resolver_simplifica(self, SIMPLIFICA[1:], "bc")
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 2 b)")
        ej_ordena(self, ORDENA[1], "b", notas)
        limpiar(self, cab)
        for lista_, nombre in ((SUMAS, 3), (MULDIV, 4), (POTENCIAS, 5)):
            subtitulo(self, cab, f"Ejercicio {nombre}: b) y c)")
            dos_expr(self, lista_[1:3], "bc", notas)
            limpiar(self, cab)
            subtitulo(self, cab, f"Ejercicio {nombre} d)")
            ej_expr(self, lista_[3], "d", notas, size=50)
            self.wait(1)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 6: b) y c)")
        for i, x in zip((1, 2), (-6.2, 0.7)):
            ej_una_potencia(self, i, x, 1.8, notas, size=42)
        notas.fin()
        self.wait(1)
        limpiar(self, cab)
        for s, l in zip(COMBINADAS[1:], "bcd"):
            subtitulo(self, cab, f"Ejercicio 7 {l})")
            ej_expr(self, s, l, notas, x=-5.0, size=44)
            self.wait(1.2)
            limpiar(self, cab)
        fin = texto("En el siguiente vídeo: ejercicios 9 a 13.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos2(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Ejercicios 9 a 13")
        notas = Notas(self, size=24)
        for (n, d), l in zip(FRAC_DEC[1:], "bc"):
            subtitulo(self, cab, f"Ejercicio 9 {l})")
            ej_frac_dec(self, n, d, l, notas)
            limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 10: b) y c)")
        ej_generatriz(self, GENERATRIZ[1], -6.0, 1.6, notas, "b", size=44)
        ej_generatriz(self, GENERATRIZ[2], 0.8, 1.6, notas, "c", size=44)
        notas.fin()
        self.wait(1.2)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 11: b) y c)")
        dos_expr(self, DECIMALES[1:], "bc", notas, modo="dec", size=42)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 12 b)")
        ej_raiz(self, RAICES[1], "b", -3.0, 1.0, notas, size=56)
        self.wait(1.2)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 12 c)")
        ej_raiz(self, RAICES[2], "c", -5.0, 1.6, notas, size=50)
        self.wait(1.2)
        limpiar(self, cab)
        for k, l in ((1, "b"), (2, "c"), (3, "d")):
            subtitulo(self, cab, f"Ejercicio 13 {l})")
            ej_cient(self, k, notas)
            limpiar(self, cab)
        fin = texto("¡Muy bien! Ya dominas fracciones y decimales.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
