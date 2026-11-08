"""Tema 8 · Operaciones con decimales (1º ESO)

Escenas:
    SumaRestaDecimales     – coma debajo de coma, completar con ceros; error típico; resta llevando
    PorDiezCienMil         – ×10, ×100, ×1000 y :10, :100: las cifras se mueven, la coma se queda quieta
    MultiplicarDecimales   – el rectángulo 2,3 × 1,4 en décimas; regla: sin comas y contar decimales
    DividirDecimales       – división entre natural (la coma del cociente), añadir ceros, divisor decimal
    FraccionADecimal       – 3/4 = 0,75; 1/3 = 0,333...; redondear
    EjerciciosEjemplo      – enunciados (2 páginas) + primer apartado de cada ejercicio resuelto
    EjerciciosResueltos    – el resto de apartados

Renderizar (desde esta carpeta, con el Python del entorno de Manim):
    ~\\venvs\\manim\\Scripts\\python.exe -m manim -pql t08_operaciones_decimales.py SumaRestaDecimales
    ~\\venvs\\manim\\Scripts\\python.exe publicar.py t08_operaciones_decimales.py
"""
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from estilo import *  # noqa: E402,F403

# Metadatos para la web (los lee publicar.py)
TEMA = "Tema 8 · Operaciones con decimales"
TITULOS = {
    "SumaRestaDecimales": "Sumar y restar decimales",
    "PorDiezCienMil": "Multiplicar y dividir por 10, 100, 1000",
    "MultiplicarDecimales": "Multiplicar decimales",
    "DividirDecimales": "Dividir decimales",
    "FraccionADecimal": "De fracción a decimal y redondeo",
    "EjerciciosEjemplo": "Ejercicios: enunciados y ejemplos resueltos",
    "EjerciciosResueltos": "Ejercicios resueltos",
}

ROSA = "#FF79C6"
ORDEN_POS = ["M", "C", "D", "U", "d", "c", "m", "x"]
SINGULAR = {"M": "millar", "C": "centena", "D": "decena", "U": "unidad",
            "d": "décima", "c": "centésima", "m": "milésima", "x": "diezmilésima"}


# ---------------------------------------------------------------------------
# Utilidades
def limpiar(scene, cab):
    scene.play(*[FadeOut(m) for m in scene.mobjects if m is not cab])


def subtitulo(scene, cab, cadena_txt, color=ACENTO):
    t = texto(cadena_txt, 30, color).next_to(cab, RIGHT, buff=0.6)
    if t.get_right()[0] > config.frame_width / 2 - 0.3:
        t.next_to(cab, DOWN, buff=0.25).align_to(cab, LEFT)
    scene.play(FadeIn(t, shift=DOWN * 0.2))
    return t


def D(s):
    return Decimal(str(s).replace(",", "."))


def ndec(s):
    return len(s.partition(",")[2])


def norm(v):
    """Decimal -> texto con coma y sin ceros sobrantes: 3.90 -> '3,9'; 750.0 -> '750'."""
    return format(v.normalize(), "f").replace(".", ",")


def fmt(v, k):
    """Decimal -> texto con k decimales exactos."""
    return format(v.quantize(Decimal(1).scaleb(-k)), "f").replace(".", ",") if k else str(int(v))


def pad(s, k):
    ent, _, dec = s.partition(",")
    return ent if k == 0 else ent + "," + dec + "0" * (k - len(dec))


def tx(s):
    """Coma decimal para MathTex."""
    return str(s).replace(",", "{,}")


def posiciones(s):
    ent, coma, dec = s.partition(",")
    return ["UDCM"[len(ent) - 1 - i] for i in range(len(ent))] + ([","] if coma else []) + \
        ["dcmx"[i] for i in range(len(dec))]


def colocar(s, fila, centros, size=56):
    """tex_decimal con cada cifra en su casilla de la tabla."""
    t = tex_decimal(s, size)
    for p, c in zip(t, posiciones(s)):
        p.move_to(centros[(fila, c)])
    return t


def filas(scene, rows, y0=1.9, dy=1.0, x0=-6.2, size_nota=22, espera=2.5):
    """rows: lista de (mobject, nota o None). Notas alineadas en columna a la derecha."""
    for i, (m, _) in enumerate(rows):
        m.move_to([x0, y0 - i * dy, 0], aligned_edge=LEFT)
    x = max(m.get_right()[0] for m, _ in rows) + 0.6
    for m, nota in rows:
        scene.play(Write(m), run_time=1.0)
        if nota:
            n = texto(nota, size_nota, GREY_B).move_to([x, m.get_y(), 0], aligned_edge=LEFT)
            if n.get_right()[0] > config.frame_width / 2 - 0.2:
                n.next_to(m, DOWN, buff=0.08).align_to(m, LEFT)
            scene.play(FadeIn(n, shift=LEFT * 0.2), run_time=0.5)
    scene.wait(espera)


class Notas:
    """Una sola nota a la vez en la parte de abajo."""

    def __init__(self, scene, size=26, color=ACENTO, buff=0.4):
        self.scene, self.size, self.color, self.buff, self.actual = scene, size, color, buff, None

    def __call__(self, cadena_txt, color=None):
        nueva = texto(cadena_txt, self.size, color or self.color)
        if nueva.width > config.frame_width - 1.0:
            nueva.scale_to_fit_width(config.frame_width - 1.0)
        nueva.to_edge(DOWN, buff=self.buff)
        if self.actual:
            self.scene.play(FadeOut(self.actual), FadeIn(nueva), run_time=0.6)
        else:
            self.scene.play(FadeIn(nueva), run_time=0.6)
        self.actual = nueva

    def fin(self):
        if self.actual:
            self.scene.play(FadeOut(self.actual), run_time=0.4)
            self.actual = None


# ---------------------------------------------------------------------------
# Suma y resta en columnas (coma debajo de coma)
def operar_columnas(scene, a, b, op, centro, tabla=True, w=0.85, h=0.8, size=52, notas=None, nombres=True):
    k = max(ndec(a), ndec(b))
    res = D(a) + D(b) if op == "+" else D(a) - D(b)
    ra, rb, rr = pad(a, k), pad(b, k), fmt(res, k)
    ent = max(len(x.partition(",")[0]) for x in (ra, rb, rr))
    cols = ["UDCM"[i] for i in range(ent - 1, -1, -1)] + ([","] + list("dcmx"[:k]) if k else [])
    grupo, centros = tabla_posiciones(cols, filas=3, centro=np.array([centro[0], centro[1], 0]), w=w, h=h,
                                      nombres=nombres)
    if tabla:
        scene.play(FadeIn(grupo))
    ta, tb = colocar(ra, 0, centros, size), colocar(rb, 1, centros, size)
    extra = []
    for t, s, orig in ((ta, ra, a), (tb, rb, b)):
        n_extra = len(s) - len(orig)
        for p in (t[len(t) - n_extra:] if n_extra else []):
            p.set_color(GREY_B)
            extra.append(p)
    originales = [p for p in list(ta) + list(tb) if p not in extra]
    xs = [centros[(0, c)][0] for c in cols]
    signo = MathTex("+" if op == "+" else "-", font_size=size).move_to(
        [min(xs) - w * 0.9, centros[(1, cols[0])][1], 0])
    y_raya = (centros[(1, cols[0])][1] + centros[(2, cols[0])][1]) / 2
    raya = Line([min(xs) - w * 1.3, y_raya, 0], [max(xs) + w * 0.5, y_raya, 0], stroke_width=3)
    scene.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in originales], lag_ratio=0.08), FadeIn(signo),
               run_time=1.5)
    if notas:
        notas("Coma debajo de coma: cada cifra en su columna")
    if extra:
        scene.play(*[FadeIn(p, scale=1.5) for p in extra])
        if notas:
            notas("Completamos con ceros para tener las mismas cifras decimales")
    scene.play(Create(raya))

    tr = colocar(rr, 2, centros, size).set_color(ACENTO)
    dig_r = {c: p for c, p in zip(posiciones(rr), tr)}
    da = {c: int(p.get_tex_string()) for c, p in zip(posiciones(ra), ta) if c != ","}
    db = {c: int(p.get_tex_string()) for c, p in zip(posiciones(rb), tb) if c != ","}
    columnas = [c for c in cols if c != ","][::-1]
    marco = Rectangle(width=w, height=3 * h, stroke_color=ACENTO, stroke_width=3)
    llevo = 0
    dig_a = {c: p for c, p in zip(posiciones(ra), ta)}
    actual, marcas, cambios = {}, {}, {}
    sitios = [LEFT * w * 0.3 + UP * h * 0.3, RIGHT * w * 0.3 + UP * h * 0.3, UP * h * 0.55]

    def cambiar(col, v):
        """Tacha la cifra de arriba de 'col' y escribe encima su nuevo valor."""
        actual[col] = v
        viejo = marcas.get(col, dig_a[col])
        tacha = Line(viejo.get_corner(DL), viejo.get_corner(UR), color=MAL, stroke_width=3)
        n = cambios.get(col, 0)
        nuevo_m = MathTex(str(v), font_size=int(size * 0.5), color=ACENTO).move_to(centros[(0, col)] + sitios[min(n, 2)])
        scene.play(Create(tacha), FadeIn(nuevo_m, shift=DOWN * 0.15), run_time=0.6)
        marcas[col], cambios[col] = nuevo_m, n + 1
    for j, c in enumerate(columnas):
        x, y = centros[(1, c)][0], centros[(1, c)][1]
        if j == 0:
            marco.move_to([x, y, 0])
            scene.play(Create(marco), run_time=0.4)
        else:
            scene.play(marco.animate.move_to([x, y, 0]), run_time=0.35)
        if c == "U" and "," in rr:
            scene.play(FadeIn(dig_r[","], shift=DOWN * 0.3), run_time=0.4)
            if notas and j == len([q for q in columnas if q in "dcmx"]):
                notas("La coma del resultado baja recta")
        x1, x2 = da.get(c, 0), db.get(c, 0)
        nuevo = 0
        if op == "+":
            s = x1 + x2 + llevo
            dig, nuevo = s % 10, s // 10
            frase = f"{x1} + {x2}" + (f" + {llevo}" if llevo else "") + f" = {s}"
            if nuevo:
                frase += f": escribo {dig} y me llevo 1"
        else:
            # Desagrupar: si arriba no llega, pedimos 1 a la columna de la izquierda (1 décima = 10 centésimas...)
            x1 = actual.setdefault(c, x1)
            if x1 < x2:
                k = j + 1
                while actual.get(columnas[k], da.get(columnas[k], 0)) == 0:
                    k += 1
                izq = columnas[j + 1]
                if k == j + 1:
                    pide = (f"{x1} − {x2} no se puede: deshacemos 1 {SINGULAR[izq]} en 10 {NOMBRE_POS[c]}")
                else:
                    pide = (f"{x1} − {x2} no se puede y al lado hay un 0: pedimos a las {NOMBRE_POS[columnas[k]]}")
                if notas:
                    notas(pide)
                fuente = columnas[k]
                cambiar(fuente, actual.setdefault(fuente, da.get(fuente, 0)) - 1)
                for m in reversed(columnas[j + 1:k]):
                    cambiar(m, 9)
                cambiar(c, x1 + 10)
                x1 = actual[c]
                if notas:
                    scene.wait(0.8)
            dig = x1 - x2
            frase = f"{x1} − {x2} = {dig}"
        anims = []
        if c in dig_r:
            anims.append(Write(dig_r[c]))
        if notas:
            notas(frase)
        if anims:
            scene.play(*anims, run_time=0.6)
        sig = columnas[j + 1] if j + 1 < len(columnas) else None
        if nuevo and sig:
            uno = MathTex("1", font_size=28, color=ACENTO).move_to(centros[(0, sig)] + UP * h * 0.55)
            scene.play(FadeIn(uno, scale=1.5), run_time=0.4)
        llevo = nuevo
        if notas:
            scene.wait(0.8)
    scene.play(FadeOut(marco), Circumscribe(tr, color=ACENTO))
    if notas:
        notas.fin()
    return rr, VGroup(grupo if tabla else VGroup(), ta, tb, tr, signo, raya)


# ---------------------------------------------------------------------------
# División larga (a la española: dividendo | divisor, cociente debajo)
W_DIG, W_COMA, H_FILA = 0.42, 0.13, 0.62


def simular_division(dividendo, divisor, max_dec=3):
    ent, _, dec = dividendo.partition(",")
    digs = [int(c) for c in ent + dec]
    k = len(ent)
    i0 = 0
    while i0 < k - 1 and int(ent[:i0 + 1]) < divisor:
        i0 += 1
    pasos, i, cur, q = [], i0, int(ent[:i0 + 1]), ""
    while True:
        cq, r = divmod(cur, divisor)
        q += str(cq)
        pasos.append((i, cur, cq, r))
        i += 1
        if i >= len(digs):
            if r == 0 or i - k >= max_dec:
                break
            digs.append(0)
        if i == k:
            q += ","
        cur = r * 10 + digs[i]
    return digs, k, i0, pasos, q


def division_larga(scene, dividendo, divisor, x0, y0, size=46, max_dec=3, notas=None, lateral=False, rt=0.5):
    """Dibuja y resuelve dividendo : divisor (divisor natural). Devuelve el cociente (texto)."""
    digs, k, i0, pasos, q = simular_division(dividendo, divisor, max_dec)
    n_orig = len(dividendo.replace(",", ""))
    tiene_coma = "," in dividendo

    def cx(i):
        return x0 + i * W_DIG + (W_COMA if i >= k else 0)

    cifras = [MathTex(str(d), font_size=size, color=WHITE if i < n_orig else GREY_B).move_to([cx(i), y0, 0])
              for i, d in enumerate(digs)]
    coma = MathTex(",", font_size=size, color=WHITE if tiene_coma else GREY_B)
    coma.move_to([x0 + (k - 1) * W_DIG + W_DIG / 2 + W_COMA / 2, y0 - 0.12, 0])
    xd = cx(len(digs) - 1) + W_DIG / 2 + 0.3
    dv = MathTex(str(divisor), font_size=size).move_to([xd + 0.2, y0, 0], aligned_edge=LEFT)
    ancho = max(dv.width, len(q) * W_DIG) + 0.4
    llave = VGroup(Line([xd, y0 + 0.35, 0], [xd, y0 - 0.35, 0]), Line([xd, y0 - 0.35, 0], [xd + ancho, y0 - 0.35, 0]))
    visibles = cifras[:n_orig] + ([coma] if tiene_coma else [])
    scene.play(*[FadeIn(c) for c in visibles], FadeIn(dv), Create(llave), run_time=0.8)

    yq = y0 - H_FILA - 0.05
    xq = [xd + 0.2]

    def escribir_cociente(ch):
        m = MathTex("," if ch == "," else ch, font_size=size, color=ACENTO)
        ancho_c = W_COMA if ch == "," else W_DIG
        m.move_to([xq[0] + ancho_c / 2, yq - (0.12 if ch == "," else 0), 0])
        xq[0] += ancho_c
        return m

    lado = None
    caja = SurroundingRectangle(VGroup(*cifras[:i0 + 1]), color=ACENTO, buff=0.08)
    scene.play(Create(caja), run_time=0.4)
    if notas and i0 > 0:
        notas(f"{int(dividendo.partition(',')[0][:i0])} < {divisor}: cogemos una cifra más")
    resto_prev = None
    for j, (i, cur, cq, r) in enumerate(pasos):
        if j > 0:
            y = y0 - j * H_FILA
            if i >= n_orig:
                aparecer = [FadeIn(cifras[i], scale=1.5)]
                if not tiene_coma and i == k:
                    aparecer.append(FadeIn(coma))
                if notas:
                    notas("No quedan cifras: añadimos un 0" + (" (y la coma)" if not tiene_coma and i == k else ""))
                scene.play(*aparecer, run_time=0.5)
            baja = cifras[i].copy().set_color(WHITE)
            scene.play(baja.animate.move_to([cx(i), y, 0]), run_time=rt)
            if i == k:
                c = escribir_cociente(",")
                if notas:
                    notas("Bajamos la primera cifra decimal: ponemos la coma en el cociente")
                scene.play(FadeIn(c, scale=2), run_time=0.5)
            grupo_cur = VGroup(resto_prev, baja) if resto_prev is not None else baja
            scene.play(caja.animate.become(SurroundingRectangle(grupo_cur, color=ACENTO, buff=0.08)), run_time=0.3)
        if lateral:
            nuevo = MathTex(rf"{cur} : {divisor} = {cq}", r"\quad \text{resto } " + str(r), font_size=30, color=GREY_B)
            nuevo.move_to([xd + 0.2, y0 - 2.4 * H_FILA, 0], aligned_edge=LEFT)
            if lado:
                scene.play(ReplacementTransform(lado, nuevo), run_time=0.4)
            else:
                scene.play(FadeIn(nuevo), run_time=0.4)
            lado = nuevo
        scene.play(Write(escribir_cociente(str(cq))), run_time=rt)
        y_r = y0 - (j + 1) * H_FILA
        rs = str(r)
        resto = VGroup(*[MathTex(ch, font_size=size).move_to([cx(i - len(rs) + 1 + t), y_r, 0])
                         for t, ch in enumerate(rs)])
        scene.play(FadeIn(resto), run_time=rt)
        resto_prev = resto
        if notas:
            scene.wait(0.6)
    fin = [FadeOut(caja)] + ([FadeOut(lado)] if lado else [])
    scene.play(*fin, run_time=0.4)
    return q


def con_divisor_natural(a, b):
    """a : b con b decimal -> (a·10^n, b·10^n, 10^n)."""
    n = ndec(b)
    f = 10 ** n
    return norm(D(a) * f), int(D(b) * f), f


# ---------------------------------------------------------------------------
# Multiplicar en una fila: sin comas -> contar decimales -> poner la coma
def con_n_dec(p, n):
    s = str(p).rjust(n + 1, "0")
    return s if n == 0 else s[:-n] + "," + s[-n:]


def mult_fila(scene, a, b, letra, y, x=-6.4, size=44, notas=None, ancho_max=13.2):
    ia, ib = int(a.replace(",", "")), int(b.replace(",", ""))
    na, nb = ndec(a), ndec(b)
    n, p = na + nb, ia * ib
    exacto, final = con_n_dec(p, n), norm(D(a) * D(b))
    piezas = [
        MathTex(rf"{tx(a)} \cdot {tx(b)}", font_size=size),
        MathTex(rf"\rightarrow\; {ia} \cdot {ib} = {p}", font_size=size, color=GREY_A),
        MathTex(rf"\rightarrow\; {na} + {nb} = {n}" + r"\text{ dec.}", font_size=size, color=COLOR_POS["d"]),
        MathTex(rf"\rightarrow\; {tx(exacto)}" + (rf" = {tx(final)}" if final != exacto else ""), font_size=size,
                color=ACENTO),
    ]
    partes = ([texto(f"{letra})", 30)] if letra else []) + piezas
    g = VGroup(*partes).arrange(RIGHT, buff=0.3)
    ancho_max = min(ancho_max, config.frame_width / 2 - 0.3 - x)
    if g.width > ancho_max:
        g.scale_to_fit_width(ancho_max)
    g.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    frases = [None, "1.º Multiplicamos sin comas",
              f"2.º Contamos los decimales de los dos factores: {na} + {nb} = {n}",
              f"3.º Separamos {n} cifra{'s' if n != 1 else ''} decimal{'es' if n != 1 else ''} desde la derecha"]
    if final != exacto:
        frases[3] += " (y quitamos los ceros del final)"
    if letra:
        scene.play(FadeIn(partes[0]), run_time=0.3)
    for pz, fr in zip(piezas, frases):
        if notas and fr:
            notas(fr)
        scene.play(Write(pz), run_time=0.9)
        if notas:
            scene.wait(1)
    scene.play(Circumscribe(piezas[-1], color=ACENTO), run_time=0.8)
    if notas:
        notas.fin()
    return g


# ---------------------------------------------------------------------------
# Redondear
def redondear(scene, s, pos, letra, y, x=-6.2, size=60, notas=None):
    k = "dcm".index(pos) + 1
    t = tex_decimal(s, size)
    ps = posiciones(s)
    idx = ps.index(pos)
    res = fmt(D(s).quantize(Decimal(1).scaleb(-k), rounding=ROUND_HALF_UP), k)
    lab = texto(f"{letra}) a las {NOMBRE_POS[pos]}:" if letra else f"A las {NOMBRE_POS[pos]}:", 26, COLOR_POS[pos])
    g = VGroup(lab, t).arrange(RIGHT, buff=0.4).move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    scene.play(FadeIn(lab), Write(t), run_time=0.9)
    caja = SurroundingRectangle(t[idx], color=COLOR_POS[pos], buff=0.08)
    scene.play(Create(caja), run_time=0.5)
    sig = int(t[idx + 1].get_tex_string())
    flecha = Arrow(t[idx + 1].get_top() + UP * 0.55, t[idx + 1].get_top() + UP * 0.05, buff=0, color=ACENTO,
                   stroke_width=4, max_tip_length_to_length_ratio=0.35)
    if notas:
        notas(f"Miramos la cifra siguiente: {sig}" + (" ≥ 5 → la cifra de la caja sube 1" if sig >= 5
                                                         else " < 5 → la cifra de la caja se queda igual"))
    scene.play(GrowArrow(flecha), Indicate(t[idx + 1], color=ACENTO, scale_factor=1.4))
    r = VGroup(MathTex(r"\approx", font_size=size), tex_decimal(res, size)).arrange(RIGHT, buff=0.25)
    r.next_to(t, RIGHT, buff=0.4)
    nota = texto("sube 1" if sig >= 5 else "igual", 22, OK if sig >= 5 else GREY_B).next_to(flecha, UP, buff=0.05)
    scene.play(Write(r), FadeIn(nota))
    scene.play(Circumscribe(r[1], color=ACENTO), run_time=0.8)
    if notas:
        scene.wait(1)
        notas.fin()
    return res


# ---------------------------------------------------------------------------
# ×10, ×100... en la tabla
def mover_en_tabla(scene, s, op, n, centros, fila=0, size=60, notas=None, linea_y=2.2):
    k = len(str(n)) - 1
    res = D(s) * n if op == "x" else D(s) / n
    rs = norm(res)
    simb = r"\cdot" if op == "x" else ":"
    enun = MathTex(rf"{tx(s)} {simb} {n} =", font_size=58).move_to([-1.0, linea_y, 0])
    scene.play(Write(enun))
    t = colocar(s, fila, centros, size)
    scene.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in t], lag_ratio=0.1))
    if notas:
        lugares = f"{k} lugar{'es' if k > 1 else ''}"
        notas(f"Cada cifra se mueve {lugares} a la " + ("IZQUIERDA: vale " if op == "x" else "DERECHA: vale ")
              + f"{n} veces " + ("más" if op == "x" else "menos") + ". La coma no se mueve.")
    movs = []
    ocupadas = set()
    cero_inicial = s.partition(",")[0].strip("0") == ""  # 0,5 -> el 0 de las unidades no cuenta
    for p, c in zip(t, posiciones(s)):
        if c == ",":
            continue
        if cero_inicial and c in "UDCM":
            movs.append(FadeOut(p))
            continue
        nuevo = ORDEN_POS[ORDEN_POS.index(c) + (-k if op == "x" else k)]
        ocupadas.add(nuevo)
        movs.append(p.animate.move_to(centros[(fila, nuevo)]).set_color(COLOR_POS[nuevo]))
    scene.play(*movs, run_time=1.6)
    ceros = VGroup()
    for c in posiciones(rs):
        if c != "," and c not in ocupadas:
            ceros.add(MathTex("0", font_size=size, color=GREY_B).move_to(centros[(fila, c)]))
    if len(ceros):
        scene.play(FadeIn(ceros, scale=1.5))
        if notas:
            notas("Rellenamos los huecos con ceros", GREY_B)
    if "," not in rs:
        scene.play(t[posiciones(s).index(",")].animate.set_opacity(0.25))
    r = tex_decimal(rs, 58).next_to(enun, RIGHT, buff=0.3)
    scene.play(Write(r), Circumscribe(r, color=ACENTO))
    scene.wait(1.5)
    if notas:
        notas.fin()
    return VGroup(enun, t, ceros, r)


# ===========================================================================
class SumaRestaDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Sumar y restar decimales", "Coma debajo de coma")
        notas = Notas(self)
        ctx = texto("Un cuaderno cuesta 3,45 € y un libro 12,8 €. ¿Cuánto pagamos?", 28).move_to([0, 2.5, 0])
        self.play(FadeIn(ctx))
        operar_columnas(self, "3,45", "12,8", "+", (0, -0.2), w=1.0, h=0.85, notas=notas)
        sol = texto("Pagamos 16,25 €", 32, OK).move_to([4.6, -0.2, 0])
        self.play(FadeIn(sol))
        self.wait(2.5)
        limpiar(self, cab)

        # Error típico: alinear por la derecha
        subtitulo(self, cab, "¡Cuidado con este error!")
        mal = VGroup(MathTex(r"3{,}45", font_size=64), MathTex(r"+\;12{,}8", font_size=64)).arrange(DOWN, buff=0.25,
                                                                                                    aligned_edge=RIGHT)
        raya = Line(mal.get_corner(DL) + DOWN * 0.15, mal.get_corner(DR) + DOWN * 0.15)
        malg = VGroup(mal, raya).move_to([-3.2, 0.4, 0])
        self.play(Write(mal), Create(raya))
        cruz = Cross(malg, stroke_color=MAL, stroke_width=6)
        self.play(Create(cruz))
        exp = texto("Alineando por la derecha sumaríamos\ncentésimas con décimas: ¡NO!", 28, MAL).move_to([3.0, 1.0, 0])
        self.play(FadeIn(exp))
        bien = VGroup(tex_decimal("3,45", 64), tex_decimal("12,80", 64)).arrange(DOWN, buff=0.25)
        bien[0].shift(RIGHT * (bien[1][2].get_x() - bien[0][1].get_x()))
        bien[1][-1].set_color(GREY_B)
        okm = texto("Coma debajo de coma ✓", 28, OK).next_to(bien, UP, buff=0.3)
        VGroup(bien, okm).move_to([3.0, -1.4, 0])
        self.play(FadeIn(okm), Write(bien))
        self.wait(3)
        limpiar(self, cab)

        # Resta llevando
        subtitulo(self, cab, "Restar: igual, coma debajo de coma")
        operar_columnas(self, "7,2", "3,85", "-", (0, 0.0), w=1.0, h=0.85, notas=notas)
        regla = texto("Si faltan cifras decimales, completamos con ceros", 26, ACENTO).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(regla))
        self.wait(3)


# ===========================================================================
class PorDiezCienMil(Scene):
    def construct(self):
        cab = titulo(self, "Por 10, 100, 1000", "Las cifras se mueven, la coma se queda quieta")
        notas = Notas(self, size=24)
        cols = ["C", "D", "U", ",", "d", "c", "m"]
        tabla, centros = tabla_posiciones(cols, filas=1, centro=np.array([0, 0.1, 0]), w=1.05, h=1.0)
        self.play(FadeIn(tabla))
        for s, op, n in (("3,47", "x", 10), ("3,47", "x", 100), ("0,5", "x", 1000)):
            g = mover_en_tabla(self, s, op, n, centros, notas=notas)
            self.play(FadeOut(g))
        for s, op, n in (("45,2", ":", 10), ("3,1", ":", 100)):
            g = mover_en_tabla(self, s, op, n, centros, notas=notas)
            self.play(FadeOut(g))
        limpiar(self, cab)

        subtitulo(self, cab, "Resumen")
        r1 = VGroup(MathTex(r"\cdot 10,\ \cdot 100,\ \cdot 1000", font_size=48, color=OK),
                    texto("las cifras pasan 1, 2 o 3 lugares a la IZQUIERDA\n(es como mover la coma a la derecha)", 26))
        r2 = VGroup(MathTex(r": 10,\ : 100,\ : 1000", font_size=48, color=COLOR_POS["d"]),
                    texto("las cifras pasan 1, 2 o 3 lugares a la DERECHA\n(es como mover la coma a la izquierda)", 26))
        for r in (r1, r2):
            r.arrange(RIGHT, buff=0.5)
        VGroup(r1, r2).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to([0, 0.4, 0])
        self.play(FadeIn(r1, shift=RIGHT * 0.2))
        self.play(FadeIn(r2, shift=RIGHT * 0.2))
        truco = texto("Tantos lugares como ceros tiene el 10, 100, 1000", 28, ACENTO).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(truco))
        self.wait(3)


# ===========================================================================
class MultiplicarDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Multiplicar decimales", "El rectángulo de 2,3 × 1,4")
        s = 1.75
        a, b = 2.3, 1.4
        c0 = np.array([-3.1, -0.4, 0])
        rect = Rectangle(width=a * s, height=b * s, stroke_color=WHITE, stroke_width=3, fill_color=ACENTO,
                         fill_opacity=0.25).move_to(c0)
        izq, abajo = rect.get_left()[0], rect.get_bottom()[1]
        finas = VGroup(*[Line([izq + s * i / 10, abajo, 0], [izq + s * i / 10, abajo + b * s, 0], stroke_width=0.8,
                              color=GREY_B) for i in range(1, 23)],
                       *[Line([izq, abajo + s * j / 10, 0], [izq + a * s, abajo + s * j / 10, 0], stroke_width=0.8,
                              color=GREY_B) for j in range(1, 14)])
        gruesas = VGroup(*[Line([izq + s * i, abajo, 0], [izq + s * i, abajo + b * s, 0], stroke_width=3) for i in (1, 2)],
                         Line([izq, abajo + s, 0], [izq + a * s, abajo + s, 0], stroke_width=3))
        la = MathTex(r"2{,}3", font_size=40).next_to(Brace(rect, DOWN), DOWN, buff=0.1)
        lb = MathTex(r"1{,}4", font_size=40).next_to(Brace(rect, LEFT), LEFT, buff=0.1)
        self.play(FadeIn(rect), GrowFromCenter(Brace(rect, DOWN)), GrowFromCenter(Brace(rect, LEFT)), FadeIn(la), FadeIn(lb))
        p1 = texto("Lados: 2,3 y 1,4.\nEl área es 2,3 × 1,4", 26).move_to([3.4, 2.0, 0])
        self.play(FadeIn(p1))
        self.play(Create(gruesas))
        uni = texto("Los cuadrados grandes son de 1 × 1", 24, GREY_B).move_to([3.4, 0.9, 0])
        self.play(FadeIn(uni))
        self.play(Create(finas), run_time=2)
        cuad = Square(s / 10, stroke_color=ACENTO, fill_color=ACENTO, fill_opacity=1).move_to(
            [izq + s / 20, abajo + s / 20, 0])
        c1 = VGroup(texto("Cada cuadradito:", 24), MathTex(r"0{,}1 \cdot 0{,}1 = 0{,}01", font_size=40, color=ACENTO))
        c1.arrange(DOWN, buff=0.12).move_to([3.4, -0.2, 0])
        self.play(FadeIn(cuad, scale=3), FadeIn(c1))
        c2 = VGroup(texto("Cuadraditos:", 24), MathTex(r"23 \cdot 14 = 322", font_size=40))
        c2.arrange(DOWN, buff=0.12).move_to([3.4, -1.5, 0])
        self.play(FadeIn(c2))
        res = MathTex(r"2{,}3 \cdot 1{,}4 = 322 \text{ centésimas} = 3{,}22", font_size=44, color=ACENTO)
        res.to_edge(DOWN, buff=0.35)
        self.play(Write(res))
        self.wait(3)
        limpiar(self, cab)

        subtitulo(self, cab, "La regla")
        notas = Notas(self)
        mult_fila(self, "2,3", "1,4", "", 1.4, x=-5.5, size=52, notas=notas)
        mult_fila(self, "0,25", "0,4", "", -0.3, x=-5.5, size=52, notas=notas)
        regla = texto("El resultado lleva tantos decimales\ncomo los dos factores juntos", 30, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(regla))
        self.wait(3)


# ===========================================================================
class DividirDecimales(Scene):
    def construct(self):
        cab = titulo(self, "Dividir decimales", "La coma del cociente")
        notas = Notas(self)
        ctx = texto("Tres amigos se reparten 7,5 €. ¿Cuánto le toca a cada uno?", 28).move_to([0, 2.5, 0])
        self.play(FadeIn(ctx))
        q = division_larga(self, "7,5", 3, -2.2, 1.2, size=60, notas=notas, lateral=True, rt=0.7)
        sol = texto(f"A cada uno le tocan {q} €", 32, OK).to_edge(DOWN, buff=1.2)
        notas.fin()
        self.play(FadeIn(sol))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Si no es exacta, añadimos ceros")
        q = division_larga(self, "7", 4, -2.2, 1.6, size=60, notas=notas, lateral=True, rt=0.6)
        notas.fin()
        r = MathTex(rf"7 : 4 = {tx(q)}", font_size=56, color=ACENTO).to_edge(DOWN, buff=1.0)
        self.play(Write(r))
        self.wait(2.5)
        limpiar(self, cab)

        # Divisor decimal
        subtitulo(self, cab, "Si el divisor tiene coma")
        e = MathTex(r"4{,}8 : 0{,}6 = \ ?", font_size=60).move_to([0, 2.3, 0])
        q1 = texto("¿Cuántas veces cabe 0,6 en 4,8?", 28, ACENTO).next_to(e, DOWN, buff=0.25)
        self.play(Write(e), FadeIn(q1))
        k = 2.0
        recta = NumberLine(x_range=[0, 5, 1], length=5 * k, include_numbers=False, include_tip=False).move_to([0, 0.0, 0])
        nums = VGroup(*[MathTex(str(i), font_size=30).next_to(recta.n2p(i), DOWN, buff=0.15) for i in range(6)])
        total = Line(recta.n2p(0), recta.n2p(4.8), stroke_width=10, color=COLOR_POS["U"]).shift(UP * 0.35)
        self.play(Create(recta), FadeIn(nums), Create(total))
        trozos = VGroup()
        for i in range(8):
            t = Line(recta.n2p(0.6 * i), recta.n2p(0.6 * (i + 1)), stroke_width=12,
                     color=ACENTO if i % 2 == 0 else ROSA).shift(UP * 0.75)
            n = MathTex(str(i + 1), font_size=28, color=t.get_color()).next_to(t, UP, buff=0.08)
            self.play(Create(t), FadeIn(n), run_time=0.3)
            trozos.add(t, n)
        cabe = texto("¡Cabe 8 veces!", 30, OK).move_to([0, -1.3, 0])
        self.play(FadeIn(cabe))
        self.wait(1)
        truco = MathTex(r"4{,}8 : 0{,}6", r"=", r"48 : 6", "=", "8", font_size=56).move_to([0, -2.3, 0])
        truco[2].set_color(ACENTO)
        truco[4].set_color(OK)
        self.play(Write(truco))
        notas("Multiplicamos los dos por 10: el divisor queda sin coma y el resultado no cambia")
        self.wait(3)
        notas.fin()


# ===========================================================================
class FraccionADecimal(Scene):
    def construct(self):
        cab = titulo(self, "De fracción a decimal", "Dividimos el numerador entre el denominador")
        notas = Notas(self)
        f = VGroup(fraccion(3, 4, 72), MathTex("= 3 : 4", font_size=60)).arrange(RIGHT, buff=0.3).move_to([-4.0, 1.5, 0])
        self.play(Write(f))
        q = division_larga(self, "3", 4, 0.0, 1.6, size=56, notas=notas, rt=0.5)
        notas.fin()
        r = VGroup(fraccion(3, 4, 60), MathTex("=", font_size=56), tex_decimal(q, 60)).arrange(RIGHT, buff=0.25)
        r.move_to([-4.0, -1.0, 0])
        self.play(Write(r))
        ex = texto("Decimal exacto: la división termina (resto 0)", 26, OK).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ex))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "A veces no termina nunca")
        f = VGroup(fraccion(1, 3, 72), MathTex("= 1 : 3", font_size=60)).arrange(RIGHT, buff=0.3).move_to([-4.0, 1.5, 0])
        self.play(Write(f))
        q = division_larga(self, "1", 3, 0.0, 1.6, size=56, max_dec=4, rt=0.4)
        r = VGroup(fraccion(1, 3, 60), MathTex(r"= 0{,}3333\ldots", font_size=56)).arrange(RIGHT, buff=0.25)
        r.move_to([-4.0, -1.0, 0])
        self.play(Write(r))
        ex = texto("El resto siempre es 1: el 3 se repite para siempre", 26, ACENTO).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ex))
        self.wait(2.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Redondear: quedarnos con menos cifras")
        n = tex_decimal("2,368", 72).move_to([0, 2.0, 0])
        self.play(Write(n))
        redondear(self, "2,368", "c", "", 0.5, x=-4.5, notas=notas)
        redondear(self, "2,368", "d", "", -1.0, x=-4.5, notas=notas)
        self.wait(1)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejemplo: 10 € entre 3 personas")
        e = MathTex(r"10 : 3 = 3{,}333\ldots", r"\approx 3{,}33 \text{ €}", font_size=60).move_to([0, 1.4, 0])
        e[1].set_color(ACENTO)
        self.play(Write(e[0]))
        self.play(Write(e[1]))
        c = texto("Redondeamos a los céntimos (centésimas)", 26, GREY_B).next_to(e, DOWN, buff=0.3)
        self.play(FadeIn(c))
        comp = MathTex(r"3 \cdot 3{,}33 = 9{,}99 \text{ €}", font_size=52).move_to([0, -0.7, 0])
        self.play(Write(comp))
        sobra = texto("Sobra 1 céntimo", 30, ROSA).next_to(comp, DOWN, buff=0.3)
        self.play(FadeIn(sobra))
        self.wait(3)


# ===========================================================================
# EJERCICIOS
# ===========================================================================
SUMA_RESTA = [("4,25", "+", "3,6"), ("12,07", "+", "0,95"), ("9,4", "-", "2,75"), ("15", "-", "3,08")]
SUMA_RESTA_E = ("0,6", "0,45", "0,3")  # e) 0,6 + 0,45 − 0,3
POR_UNIDAD = [("2,58", "x", 10), ("0,037", "x", 100), ("4,1", "x", 1000), ("63,5", ":", 10), ("2,4", ":", 100),
              ("7", ":", 1000)]
MULTIPLICA = [("3,2", "4"), ("1,5", "2,6"), ("0,35", "1,2"), ("0,05", "0,3")]
DIVIDE = [("9,6", "4"), ("13,5", "5"), ("6", "8"), ("2,4", "0,3"), ("7,5", "0,25"), ("1,44", "1,2")]
FRAC_DEC = [(3, 5), (7, 8), (2, 3)]
REDONDEA = [("3,1416", "c"), ("12,857", "d"), ("0,995", "c")]
PROBLEMAS = [
    "a) Compras 3 cuadernos de 1,25 € y un bolígrafo de 2,40 €. Pagas con 10 €.\n"
    "     ¿Cuánto te devuelven?",
    "b) Echamos 35 litros de gasolina a 1,62 € el litro. ¿Cuánto pagamos?",
    "c) ¿Cuántos trozos de 0,75 m salen de una cuerda de 7,5 m?",
    "d) Una cena cuesta 47,40 € y pagan 4 amigos a partes iguales.\n"
    "     ¿Cuánto paga cada uno?",
]
SIMB = {"+": "+", "-": MENOS, "x": "·", ":": ":"}


def op_txt(a, op, b):
    return f"{a} {SIMB[op]} {b}"


def pagina_enunciados(scene, cab, bloques, size=23):
    grupo = VGroup()
    for cabecera, cuerpo in bloques:
        b = VGroup(texto(cabecera, 27, ACENTO), texto(cuerpo, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        grupo.add(b)
    grupo.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(cab, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
    scene.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in grupo], lag_ratio=0.3))
    pausa = texto("¡Pausa el vídeo e inténtalo!", 26, ACENTO).to_edge(DOWN, buff=0.25)
    scene.play(FadeIn(pausa))
    scene.wait(3)
    limpiar(scene, cab)


def enunciados_1():
    sr = [f"{l}) {op_txt(*o)}" for l, o in zip("abcd", SUMA_RESTA)]
    sr.append(f"e) {SUMA_RESTA_E[0]} + {SUMA_RESTA_E[1]} {MENOS} {SUMA_RESTA_E[2]}")
    pu = [f"{l}) {op_txt(*o)}" for l, o in zip("abcdef", POR_UNIDAD)]
    return [
        ("1. Suma o resta:", "     ".join(sr[:3]) + "\n" + "     ".join(sr[3:])),
        ("2. Calcula:", "     ".join(pu[:3]) + "\n" + "     ".join(pu[3:])),
        ("3. Multiplica:", "     ".join(f"{l}) {a} · {b}" for l, (a, b) in zip("abcd", MULTIPLICA))),
        ("4. Divide:", "     ".join(f"{l}) {a} : {b}" for l, (a, b) in zip("abcdef", DIVIDE))),
    ]


def enunciados_2():
    return [
        ("5. Fracciones y redondeo:",
         "a) Escribe como decimal:   " + "     ".join(f"{n}/{d}" for n, d in FRAC_DEC) +
         "\n     (si no termina, redondea a las centésimas)\n"
         "b) Redondea:   " + "     ".join(f"{s} a las {NOMBRE_POS[p]}" for s, p in REDONDEA[:2]) +
         "\n     " + "     ".join(f"{s} a las {NOMBRE_POS[p]}" for s, p in REDONDEA[2:])),
        ("6. Problemas:", "\n".join(PROBLEMAS)),
    ]


def resolver_division(scene, a, b, letra, x0, y, notas=None, lateral=False, cabecera=None, max_dec=3, size=46,
                      resultado_fmt=None):
    """letra) a : b [= a' : b'] = cociente, con la división larga debajo."""
    if "," in b:
        a2, b2, f = con_divisor_natural(a, b)
        partes = [rf"{tx(a)} : {tx(b)}", rf"= {tx(a2)} : {b2}"]
    else:
        a2, b2, f = a, int(b), 1
        partes = [cabecera or rf"{tx(a)} : {tx(b)}"]
    head = MathTex(*partes, font_size=44)
    lab = texto(f"{letra})", 28) if letra else VGroup()
    hg = VGroup(lab, head).arrange(RIGHT, buff=0.3).move_to([0, y, 0]).align_to([x0 - 0.5, 0, 0], LEFT)
    scene.play(FadeIn(lab), Write(head[0]), run_time=0.8)
    if len(partes) > 1:
        if notas:
            notas(f"El divisor tiene coma: multiplicamos los dos por {f}")
        scene.play(Write(head[1]), run_time=0.8)
        if notas:
            scene.wait(1)
    q = division_larga(scene, a2, b2, x0, y - 1.05, size=size, max_dec=max_dec, notas=notas, lateral=lateral)
    qs = resultado_fmt(q) if resultado_fmt else rf"= {tx(q)}"
    r = MathTex(qs, font_size=44, color=ACENTO).next_to(head, RIGHT, buff=0.25)
    scene.play(Write(r))
    scene.play(Circumscribe(r, color=ACENTO), run_time=0.7)
    if notas:
        notas.fin()
    return q


def resolver_por_unidad(scene, items, letras):
    rows = []
    for (s, op, n), l in zip(items, letras):
        res = D(s) * n if op == "x" else D(s) / n
        k = len(str(n)) - 1
        simb = r"\cdot" if op == "x" else ":"
        m = MathTex(rf"\text{{{l})}}\;\; {tx(s)} {simb} {n} = ", tx(norm(res)), font_size=48)
        m[1].set_color(ACENTO)
        nota = f"{k} lugar{'es' if k > 1 else ''} a la " + ("izquierda" if op == "x" else "derecha")
        rows.append((m, nota))
    filas(scene, rows, y0=2.0, dy=0.95, x0=-5.8, size_nota=24)


def problema_compra(scene, notas=None):
    e = texto(PROBLEMAS[0][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    c = D("1.25") * 3
    s = c + D("2.40")
    d = D(10) - s
    rows = [
        (MathTex(rf"3 \cdot 1{{,}}25 = {tx(fmt(c, 2))}", font_size=50), "los 3 cuadernos"),
        (MathTex(rf"{tx(fmt(c, 2))} + 2{{,}}40 = {tx(fmt(s, 2))}", font_size=50), "más el bolígrafo: lo que gastamos"),
        (MathTex(rf"10 - {tx(fmt(s, 2))} = {tx(fmt(d, 2))}", font_size=50, color=ACENTO), "lo que nos devuelven"),
    ]
    filas(scene, rows, y0=1.0, dy=1.05, x0=-5.0, size_nota=26, espera=1)
    sol = texto(f"Nos devuelven {fmt(d, 2)} €", 32, OK).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_gasolina(scene):
    e = texto(PROBLEMAS[1][3:], 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    mult_fila(scene, "35", "1,62", "", 0.6, x=-5.0, size=52)
    sol = texto(f"Pagamos {fmt(D(35) * D('1.62'), 2)} €", 32, OK).to_edge(DOWN, buff=0.8)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_cuerda(scene):
    e = texto(PROBLEMAS[2][3:], 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    q = resolver_division(scene, "7,5", "0,75", "", -1.5, 1.3, lateral=True)
    sol = texto(f"Salen {q} trozos", 32, OK).to_edge(DOWN, buff=0.5)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def problema_cena(scene):
    e = texto(PROBLEMAS[3][3:].replace("\n     ", "\n"), 26).move_to([0, 2.4, 0])
    scene.play(Write(e), run_time=1.5)
    q = resolver_division(scene, "47,40", "4", "", -2.0, 1.3, lateral=True)
    sol = texto(f"Cada uno paga {q} €", 32, OK).to_edge(DOWN, buff=0.4)
    scene.play(FadeIn(sol))
    scene.wait(2.5)


def frac_cabecera(n, d):
    return rf"\frac{{{n}}}{{{d}}} = {n} : {d}"


def frac_resultado(q):
    dec = q.partition(",")[2]
    if len(dec) >= 3 and len(set(dec)) == 1:
        red = fmt(D(q.replace(",", ".")), 2)
        return rf"= {tx(q)}\ldots \approx {tx(red)}"
    return rf"= {tx(q)}"


class EjerciciosEjemplo(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios", "Operaciones con decimales")
        pagina_enunciados(self, cab, enunciados_1())
        pagina_enunciados(self, cab, enunciados_2(), size=22)
        intro = texto("Resolvemos el primer apartado de cada ejercicio", 34, ACENTO)
        self.play(Write(intro))
        self.wait(1)
        self.play(FadeOut(intro))
        notas = Notas(self)

        subtitulo(self, cab, "Ejercicio 1 a)")
        operar_columnas(self, "4,25", "3,6", "+", (0, 0.3), w=1.0, h=0.85, notas=notas)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2 a)")
        cols = ["C", "D", "U", ",", "d", "c", "m"]
        tabla, centros = tabla_posiciones(cols, filas=1, centro=np.array([0, 0.1, 0]), w=1.05, h=1.0)
        self.play(FadeIn(tabla))
        mover_en_tabla(self, "2,58", "x", 10, centros, notas=notas)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3 a)")
        mult_fila(self, *MULTIPLICA[0], "a", 0.6, x=-5.6, size=56, notas=notas)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 4 a)")
        resolver_division(self, *DIVIDE[0], "a", -2.0, 1.9, notas=notas, lateral=True, size=56)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 a)")
        n, d = FRAC_DEC[0]
        resolver_division(self, str(n), str(d), "a", -2.0, 1.9, notas=notas, lateral=True, size=56,
                          cabecera=frac_cabecera(n, d), resultado_fmt=frac_resultado)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 b)")
        redondear(self, *REDONDEA[0], "a", 0.6, x=-5.6, size=72, notas=notas)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 6 a)")
        problema_compra(self)
        limpiar(self, cab)

        fin = texto("En el siguiente vídeo resolvemos el resto.", 32, GREY_B)
        self.play(FadeIn(fin))
        self.wait(2)


class EjerciciosResueltos(Scene):
    def construct(self):
        cab = titulo(self, "Ejercicios resueltos", "Operaciones con decimales")

        subtitulo(self, cab, "Ejercicio 1 b) y c)")
        for (a, op, b), l, x in zip(SUMA_RESTA[1:3], "bc", (-3.6, 3.4)):
            lab = texto(f"{l})", 30).move_to([x - 2.6, 1.6, 0])
            self.play(FadeIn(lab))
            operar_columnas(self, a, b, op, (x, -0.2), w=0.8, h=0.8, size=48, nombres=False)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 1 d) y e)")
        a, op, b = SUMA_RESTA[3]
        self.play(FadeIn(texto("d)", 30).move_to([-6.2, 1.6, 0])))
        operar_columnas(self, a, b, op, (-4.0, -0.2), w=0.75, h=0.8, size=46, nombres=False)
        x, y, z = SUMA_RESTA_E
        self.play(FadeIn(texto(f"e)  {x} + {y} {MENOS} {z}", 26).move_to([2.8, 2.3, 0])))
        r1, _ = operar_columnas(self, x, y, "+", (0.9, -0.2), w=0.7, h=0.8, size=44, nombres=False)
        operar_columnas(self, r1, z, "-", (4.9, -0.2), w=0.7, h=0.8, size=44, nombres=False)
        self.wait(1.5)
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 2: b) a f)")
        resolver_por_unidad(self, POR_UNIDAD[1:], "bcdef")
        limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 3: b), c) y d)")
        for (a, b), l, y in zip(MULTIPLICA[1:], "bcd", (1.6, 0.0, -1.6)):
            mult_fila(self, a, b, l, y, size=44)
        self.wait(2)
        limpiar(self, cab)

        for sub, items, letras in (("Ejercicio 4 b) y c)", DIVIDE[1:3], "bc"), ("Ejercicio 4 d) y e)", DIVIDE[3:5], "de"),
                                   ("Ejercicio 4 f)", DIVIDE[5:], "f")):
            subtitulo(self, cab, sub)
            for (a, b), l, x in zip(items, letras, (-4.6, 2.0)):
                resolver_division(self, a, b, l, x, 2.0)
            self.wait(1.5)
            limpiar(self, cab)

        subtitulo(self, cab, "Ejercicio 5 a): b) y c)")
        for (n, d), l, x in zip(FRAC_DEC[1:], "bc", (-4.6, 2.2)):
            resolver_division(self, str(n), str(d), l, x, 2.0, cabecera=frac_cabecera(n, d),
                              resultado_fmt=frac_resultado)
        self.wait(1.5)
        limpiar(self, cab)
        subtitulo(self, cab, "Ejercicio 5 b): b) y c)")
        for (s, p), l, y in zip(REDONDEA[1:], "bc", (1.0, -1.0)):
            redondear(self, s, p, l, y, x=-5.6, size=64)
        nota = texto("0,995 → 0,99 + 0,01 = 1,00 (las centésimas se quedan: 1,00)", 24, GREY_B).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(nota))
        self.wait(2)
        limpiar(self, cab)

        for sub, f in (("Ejercicio 6 b)", problema_gasolina), ("Ejercicio 6 c)", problema_cuerda),
                       ("Ejercicio 6 d)", problema_cena)):
            subtitulo(self, cab, sub)
            f(self)
            limpiar(self, cab)

        fin = texto("¡Muy bien! Ya sabes operar con decimales.", 34, ACENTO)
        self.play(Write(fin))
        self.wait(2)
