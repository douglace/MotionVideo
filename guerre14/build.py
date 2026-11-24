#!/usr/bin/env python3
"""Montage « 1914 : comment un assassinat a embrasé le monde » — version illustrée.

23 illustrations peintes (img/iNN.png, 1024x1536) + narration d'origine (narration.m4a)
-> build/guerre14.mp4 en 1080x1920, 30 i/s.

Effets : Ken Burns avec easing, fondus enchaînés, écran partagé Alliance/Entente,
flash + secousse sur les coups de feu, titres de section, compteur de dates,
sous-titres karaoké mot à mot, vignette et grain de film.
"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
DUR = 101.89
XF = 0.40  # durée des fondus enchaînés

GOLD = (232, 184, 74)
RED = (196, 48, 43)
BLUE = (70, 120, 190)
CREAM = (246, 238, 222)

# chiffres alignés (Playfair utilise des chiffres elzéviriens par défaut)
_orig_text = ImageDraw.ImageDraw.text
def _text(self, *a, **k):
    k.setdefault("features", ["lnum"])
    return _orig_text(self, *a, **k)
ImageDraw.ImageDraw.text = _text
_orig_len = ImageFont.FreeTypeFont.getlength
def _len(self, s, *a, **k):
    k.setdefault("features", ["lnum"])
    return _orig_len(self, s, *a, **k)
ImageFont.FreeTypeFont.getlength = _len

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)

F_CAP = font("Playfair-ExtraBold.ttf", 80)
F_HEAD = font("Inter-ExtraBold.ttf", 34)
F_TITLE = font("Playfair-ExtraBold.ttf", 92)
F_BIG = font("Playfair-ExtraBold.ttf", 150)
F_MID = font("Playfair-SemiBold.ttf", 58)
F_DATE = font("Playfair-ExtraBold.ttf", 120)

# ---------------------------------------------------------------- plans
# (image, début, zoom départ, zoom fin, pan x départ, pan x fin, pan y départ, pan y fin)
# pan : -1 = bord gauche/haut, 0 = centre, 1 = bord droit/bas
SHOTS = [
    ("i01", 0.00, 1.00, 1.12, 0.6, 0.1, 0.2, 0.0),
    ("i02", 4.75, 1.18, 1.00, 0.0, 0.0, -0.3, 0.0),
    ("i03", 11.60, 1.00, 1.14, 0.0, 0.0, 0.3, -0.2),
    ("i04", 15.25, 1.10, 1.00, -0.6, 0.5, 0.0, 0.0),
    ("i05", 19.75, 1.00, 1.10, 0.4, -0.3, 0.2, -0.2),
    ("i06", 23.00, 1.12, 1.00, -0.2, 0.3, -0.2, 0.0),
    ("i07", 25.25, 1.00, 1.10, -0.5, 0.4, 0.0, -0.2),
    ("SPLIT", 28.25, 1.00, 1.06, 0, 0, 0, 0),
    ("i08", 32.00, 1.12, 1.00, 0.0, 0.0, -0.2, 0.1),
    ("i09", 35.75, 1.00, 1.12, 0.0, 0.0, 0.1, -0.2),
    ("i10", 39.75, 1.05, 1.15, 0.5, -0.5, -0.2, 0.2),
    ("i11", 44.00, 1.00, 1.16, 0.0, 0.1, 0.0, -0.3),
    ("i12", 49.25, 1.14, 1.02, 0.0, 0.0, -0.2, 0.0),
    ("i13", 53.75, 1.00, 1.12, -0.3, 0.3, 0.0, -0.1),
    ("i14", 60.60, 1.00, 1.16, 0.4, -0.4, 0.3, -0.1),
    ("i15", 66.50, 1.10, 1.00, 0.0, 0.0, -0.2, 0.0),
    ("i16", 68.25, 1.00, 1.12, 0.0, 0.0, 0.2, -0.2),
    ("i17", 74.25, 1.10, 1.00, 0.4, -0.3, 0.0, 0.0),
    ("i18", 77.25, 1.00, 1.10, 0.0, 0.0, 0.2, -0.3),
    ("i19", 79.50, 1.12, 1.00, -0.4, 0.4, 0.0, 0.0),
    ("i20", 84.00, 1.00, 1.14, 0.0, 0.0, 0.0, -0.2),
    ("i21", 86.50, 1.04, 1.16, 0.0, 0.0, -0.5, 0.4),
    ("i22", 90.25, 1.00, 1.10, 0.0, 0.0, 0.3, -0.1),
    ("i23", 93.50, 1.14, 1.00, 0.0, 0.0, 0.0, 0.0),
]

# titres de section (début, fin, texte, couleur du filet)
HEADERS = [
    (0.3, 11.4, "28 JUIN 1914 · SARAJEVO", RED),
    (11.8, 28.0, "1871 — 1914 · LA POUDRIÈRE", RED),
    (28.4, 43.8, "DEUX BLOCS ARMÉS", GOLD),
    (44.2, 60.4, "L'ATTENTAT · L'ULTIMATUM", RED),
    (60.8, 79.3, "5 SEMAINES · EFFET DOMINO", GOLD),
    (79.7, 90.0, "« RENTRÉS AVANT NOËL »", RED),
]

# grandes dates du domino (début, fin, texte)
DATES = [
    (63.5, 68.2, "28 JUILLET"),
    (68.25, 72.7, "1er AOÛT"),
    (72.75, 74.2, "3 AOÛT"),
    (76.0, 79.4, "4 AOÛT"),
]

# flashes de coups de feu (instant, intensité)
FLASHES = [(2.55, 0.85), (3.05, 0.6), (49.25, 1.0)]

# sous-titres : (début, fin, texte) relevés sur la vidéo d'origine
CAPS = [
    (0.25, 1.25, "Le 28 juin"), (1.25, 2.5, "1914,"), (2.5, 3.25, "deux coups de"),
    (3.25, 4.75, "feu à Sarajevo"), (4.75, 5.75, "embrasent la"), (5.75, 6.75, "planète entière."),
    (6.75, 7.75, "Comment un seul"), (7.75, 8.25, "assassinat"), (8.25, 9.5, "a-t-il déclenché"),
    (9.5, 10.25, "la Première"), (10.25, 11.5, "guerre mondiale ?"),
    (11.75, 12.5, "En réalité,"), (12.5, 13.25, "l'Europe est déjà"), (13.25, 14.25, "une poudrière."),
    (14.25, 15.25, "Depuis 40 ans,"), (15.25, 15.75, "les grandes"), (15.75, 16.75, "puissances se"),
    (16.75, 17.5, "disputent"), (17.5, 18.25, "les colonies,"), (18.25, 19.0, "les mers et"),
    (19.0, 19.75, "les frontières."), (19.75, 20.5, "La France veut"), (20.5, 21.0, "reprendre"),
    (21.0, 21.75, "l'Alsace-Lorraine"), (21.75, 23.0, "à l'Allemagne."), (23.0, 23.75, "L'Allemagne"),
    (23.75, 24.75, "réclame un empire"), (24.75, 25.25, "mondial."), (25.25, 25.75, "Et dans les"),
    (25.75, 26.0, "Balkans,"), (26.0, 26.5, "les peuples"), (26.5, 27.25, "exigent leur"),
    (27.25, 28.25, "indépendance."),
    (28.25, 29.0, "Par peur d'être"), (29.0, 29.5, "isolée,"), (29.5, 30.5, "l'Europe se coupe"),
    (30.5, 31.25, "en deux blocs"), (31.25, 32.0, "armés :"), (32.0, 32.25, "la Triple"),
    (32.25, 33.0, "Alliance,"), (33.0, 33.75, "Allemagne,"), (33.75, 35.0, "Autriche-Hongrie"),
    (35.0, 35.75, "et Italie,"), (35.75, 36.5, "face à la"), (36.5, 37.25, "Triple Entente,"),
    (37.25, 38.0, "France,"), (38.0, 38.75, "Russie et"), (38.75, 39.75, "Royaume-Uni."),
    (39.75, 40.25, "Le piège est"), (40.25, 40.75, "simple :"), (40.75, 41.25, "si un pays"),
    (41.25, 41.75, "attaque,"), (41.75, 42.25, "ses alliés"), (42.25, 43.25, "doivent entrer en"),
    (43.25, 44.0, "guerre."),
    (44.0, 45.0, "Le 28 juin"), (45.0, 46.0, "à Sarajevo,"), (46.0, 47.5, "Gavrilo Princip,"),
    (47.5, 48.0, "un jeune"), (48.0, 48.75, "nationaliste"), (48.75, 49.25, "serbe,"),
    (49.25, 50.25, "abat l'archiduc"), (50.25, 50.75, "François-"), (50.75, 51.5, "Ferdinand,"),
    (51.5, 52.5, "héritier de"), (52.5, 54.0, "l'Autriche-Hongrie."), (54.0, 55.75, "Vienne accuse la"),
    (55.75, 57.0, "Serbie et lui"), (57.0, 57.75, "envoie un"), (57.75, 58.5, "ultimatum"),
    (58.5, 59.25, "impossible à"), (59.25, 60.5, "accepter."),
    (60.75, 61.25, "Alors,"), (61.25, 62.0, "les dominos"), (62.0, 62.75, "tombent en 5"),
    (62.75, 63.5, "semaines."), (63.5, 64.5, "Le 28 juillet,"), (64.5, 65.5, "l'Autriche-Hongrie"),
    (65.5, 66.25, "attaque la"), (66.25, 66.5, "Serbie."), (66.5, 67.0, "La Russie"),
    (67.0, 67.75, "mobilise pour la"), (67.75, 68.25, "défendre."), (68.25, 69.5, "Le 1er août,"),
    (69.5, 70.25, "l'Allemagne"), (70.25, 71.25, "déclare la guerre"), (71.25, 72.0, "à la Russie,"),
    (72.0, 72.75, "puis à la"), (72.75, 73.5, "France le 3"), (73.5, 74.25, "août."),
    (74.25, 75.0, "Elle envahit la"), (75.0, 76.0, "Belgique neutre"), (76.0, 77.0, "et le 4"),
    (77.0, 77.25, "août,"), (77.25, 78.0, "le Royaume-Uni"), (78.0, 78.5, "entre dans le"),
    (78.5, 79.5, "conflit."),
    (79.5, 80.75, "Chaque camp jure"), (80.75, 81.5, "qu'il ne fait"), (81.5, 83.0, "que se défendre."),
    (83.0, 83.75, "Tous croient"), (83.75, 84.25, "rentrer avant"), (84.25, 84.75, "Noël."),
    (84.75, 85.25, "Mais la course"), (85.25, 86.25, "aux armements et"), (86.25, 87.25, "les alliances"),
    (87.25, 88.25, "transforment une"), (88.25, 89.0, "crise locale en"), (89.0, 90.25, "guerre totale."),
    (90.25, 91.0, "Quatre ans plus"), (91.0, 91.25, "tard,"), (91.25, 92.25, "18 millions de"),
    (92.25, 93.25, "morts et quatre"), (93.25, 93.75, "empires"), (93.75, 94.75, "effondrés."),
    (94.75, 95.75, "En 1914,"),
]
# mots mis en couleur (rouge) en plus du mot courant (or)
RED_WORDS = {"Sarajevo", "poudrière.", "l'Alsace-Lorraine", "Balkans,", "Princip,", "ultimatum",
             "guerre", "guerre.", "totale.", "Noël.", "neutre", "conflit.", "morts", "effondrés.",
             "assassinat", "Triple", "Alliance,", "Entente,"}

# ---------------------------------------------------------------- utilitaires
def ease(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)

def load_cover(path, scale=1.0):
    im = Image.open(path).convert("RGB")
    s = max(W / im.width, H / im.height) * scale
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

def kenburns(src, p, z0, z1, px0, px1, py0, py1, shake=(0, 0)):
    """Recadre src (déjà >= W x H) avec zoom/pan interpolés, renvoie W x H."""
    e = ease(p)
    z = z0 + (z1 - z0) * e
    base = min(src.width / W, src.height / H)
    cw, ch = W * base / z, H * base / z
    mx, my = (src.width - cw) / 2, (src.height - ch) / 2
    px = px0 + (px1 - px0) * e
    py = py0 + (py1 - py0) * e
    cx = mx + px * mx + shake[0]
    cy = my + py * my + shake[1]
    cx = min(max(cx, 0), src.width - cw)
    cy = min(max(cy, 0), src.height - ch)
    return src.transform((W, H), Image.EXTENT, (cx, cy, cx + cw, cy + ch), Image.BICUBIC)

# ---------------------------------------------------------------- calques fixes
def make_vignette():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((x - W / 2) / (W * 0.62)) ** 2 + ((y - H * 0.45) / (H * 0.62)) ** 2)
    v = np.clip((d - 0.55) / 0.6, 0, 1) ** 1.6 * 0.75
    # dégradé bas pour la lisibilité des sous-titres + haut pour les titres
    g = np.clip((y - H * 0.62) / (H * 0.30), 0, 1) ** 1.3 * 0.78
    t = np.clip((H * 0.16 - y) / (H * 0.16), 0, 1) ** 1.5 * 0.55
    a = 1 - (1 - v) * (1 - g) * (1 - t)
    return (1 - a)[..., None].astype(np.float32)

VIGN = make_vignette()
rng = np.random.default_rng(7)
GRAIN = [rng.normal(0, 7, (H // 2, W // 2)).astype(np.float32) for _ in range(6)]
GRAIN = [np.kron(g, np.ones((2, 2), np.float32))[..., None] for g in GRAIN]

# ---------------------------------------------------------------- textes
def text_w(f, s):
    return f.getlength(s)

def draw_shadowed(img, xy, s, f, fill, stroke=6, shadow=10, spacing=0):
    """Texte avec contour sombre et ombre portée floue, sur un calque RGBA."""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((xy[0] + 4, xy[1] + 8), s, font=f, fill=(0, 0, 0, 200), stroke_width=stroke, stroke_fill=(0, 0, 0, 200))
    lay = lay.filter(ImageFilter.GaussianBlur(shadow))
    d = ImageDraw.Draw(lay)
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(18, 14, 10, 255))
    img.alpha_composite(lay)

_cap_cache = {}
def caption_layer(idx, wi):
    key = (idx, wi)
    if key in _cap_cache:
        return _cap_cache[key]
    _, _, txt = CAPS[idx]
    words = txt.split(" ")
    space = text_w(F_CAP, " ")
    widths = [text_w(F_CAP, w) for w in words]
    total = sum(widths) + space * (len(words) - 1)
    pad = 60
    lay = Image.new("RGBA", (int(total) + 2 * pad, 200), (0, 0, 0, 0))
    # ombre
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    x = pad
    for w, ww in zip(words, widths):
        ds.text((x + 4, 58), w, font=F_CAP, fill=(0, 0, 0, 210), stroke_width=8, stroke_fill=(0, 0, 0, 210))
        x += ww + space
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    lay.alpha_composite(sh)
    d = ImageDraw.Draw(lay)
    x = pad
    for i, (w, ww) in enumerate(zip(words, widths)):
        if i == wi:
            col = GOLD
        elif w in RED_WORDS:
            col = (232, 92, 80)
        else:
            col = CREAM
        if i == wi:
            # soulignement or sous le mot courant
            d.rounded_rectangle((x - 4, 150, x + ww + 4, 158), 4, fill=GOLD + (255,))
        d.text((x, 50), w, font=F_CAP, fill=col + (255,), stroke_width=5, stroke_fill=(20, 15, 10, 255))
        x += ww + space
    _cap_cache[key] = lay
    return lay

_head_cache = {}
def header_layer(i):
    if i in _head_cache:
        return _head_cache[i]
    _, _, txt, col = HEADERS[i]
    tracking = 5
    tw = sum(text_w(F_HEAD, c) + tracking for c in txt) - tracking
    lay = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0 = (W - tw) / 2
    # pastille sombre translucide
    d.rounded_rectangle((x0 - 34, 40, x0 + tw + 34, 112), 36, fill=(14, 11, 9, 170), outline=col + (230,), width=3)
    x = x0
    for c in txt:
        d.text((x, 56), c, font=F_HEAD, fill=CREAM + (255,))
        x += text_w(F_HEAD, c) + tracking
    _head_cache[i] = lay
    return lay

_misc_cache = {}
def cached(key, fn):
    if key not in _misc_cache:
        _misc_cache[key] = fn()
    return _misc_cache[key]

def big_center(lines, top):
    """lines: [(texte, police, couleur)] centrées à partir de y=top."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = top
    for s, f, col in lines:
        if s:
            draw_shadowed(lay, ((W - text_w(f, s)) / 2, y), s, f, col + (255,), stroke=5, shadow=12)
        y += f.size * 1.25
    return lay

def paste_alpha(base, lay, xy, alpha):
    if alpha <= 0:
        return
    if alpha < 1:
        lay = lay.copy()
        a = lay.getchannel("A").point(lambda v: int(v * alpha))
        lay.putalpha(a)
    base.alpha_composite(lay, (int(xy[0]), int(xy[1])))

# ---------------------------------------------------------------- rendu d'un plan
IMGS = {}
def src(name):
    if name not in IMGS:
        path = os.path.join(HERE, "img", name + ".png")
        if not os.path.exists(path):  # aperçu avant que toutes les images existent
            path = os.path.join(HERE, "img", "i01.png")
        IMGS[name] = load_cover(path, 1.0)
    return IMGS[name]

def shake_at(t):
    sx = sy = 0.0
    for ft, k in FLASHES:
        dt = t - ft
        if 0 <= dt < 0.45:
            amp = 22 * k * (1 - dt / 0.45)
            sx += amp * math.sin(dt * 90)
            sy += amp * math.cos(dt * 70)
    return sx, sy

def render_shot(k, t):
    name, t0, z0, z1, px0, px1, py0, py1 = SHOTS[k]
    t1 = SHOTS[k + 1][1] if k + 1 < len(SHOTS) else DUR
    p = (t - t0) / (t1 - t0 + XF)
    sh = shake_at(t)
    if name == "SPLIT":
        # écran partagé : Triple-Alliance (rouge) à gauche, Triple-Entente (bleu) à droite
        out = Image.new("RGB", (W, H))
        e = ease(p)
        for side, nm in ((0, "i08"), (1, "i09")):
            s = src(nm)
            z = z0 + (z1 - z0) * e
            base = min(s.width / W, s.height / H)
            cw, ch = (W / 2) * base / z, H * base / z
            cx = (s.width - cw) / 2 + (-1 if side == 0 else 1) * 40 * e
            cy = (s.height - ch) / 2
            half = s.transform((W // 2, H), Image.EXTENT, (cx, cy, cx + cw, cy + ch), Image.BICUBIC)
            # glissement d'entrée
            slide = int((1 - ease((t - t0) / 0.6)) * (W // 2))
            out.paste(half, (0 - slide if side == 0 else W // 2 + slide, 0))
        tint = Image.new("RGB", (W, H))
        dt = ImageDraw.Draw(tint)
        dt.rectangle((0, 0, W // 2, H), fill=(120, 20, 20))
        dt.rectangle((W // 2, 0, W, H), fill=(20, 40, 110))
        out = Image.blend(out, tint, 0.16)
        d = ImageDraw.Draw(out)
        d.rectangle((W // 2 - 4, 0, W // 2 + 4, H), fill=GOLD)
        return out
    return kenburns(src(name), p, z0, z1, px0, px1, py0, py1, sh)

def shot_index(t):
    k = 0
    for i, s in enumerate(SHOTS):
        if t >= s[1]:
            k = i
    return k

# ---------------------------------------------------------------- image complète
def frame(t):
    k = shot_index(t)
    img = render_shot(k, t)
    # fondu enchaîné vers le plan suivant
    if k + 1 < len(SHOTS):
        tn = SHOTS[k + 1][1]
        if t > tn - XF:
            a = ease((t - (tn - XF)) / XF)
            img = Image.blend(img, render_shot(k + 1, t), a)

    arr = np.asarray(img, dtype=np.float32)
    # étalonnage léger : contraste + chaleur
    arr = (arr - 128) * 1.06 + 128
    arr[..., 0] *= 1.03
    arr[..., 2] *= 0.96
    arr = arr * VIGN + GRAIN[int(t * FPS) % len(GRAIN)]
    # flash blanc des coups de feu
    for ft, kk in FLASHES:
        dt = t - ft
        if 0 <= dt < 0.35:
            f = kk * (1 - dt / 0.35) ** 2
            arr = arr * (1 - f) + 255 * f
    # fondu au noir final
    if t > DUR - 1.2:
        arr *= max(0.0, (DUR - t) / 1.2)
    if t < 0.4:
        arr *= t / 0.4
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")

    # titres de section
    for i, (a0, a1, _, _) in enumerate(HEADERS):
        if a0 <= t <= a1:
            al = min(1, (t - a0) / 0.4, (a1 - t) / 0.3)
            dy = (1 - ease(min(1, (t - a0) / 0.4))) * -30
            paste_alpha(img, header_layer(i), (0, 80 + dy), al)

    # gros titres contextuels
    def card(key, a0, a1, lines, top):
        if a0 <= t <= a1:
            al = min(1, (t - a0) / 0.35, (a1 - t) / 0.3)
            lay = cached(key, lambda: big_center(lines, top))
            sc = 0.92 + 0.08 * ease(min(1, (t - a0) / 0.35))
            if sc < 0.999:
                lay2 = lay.resize((int(W * sc), int(H * sc)), Image.BILINEAR)
                paste_alpha(img, lay2, ((W - lay2.width) / 2, (H - lay2.height) / 2), al)
            else:
                paste_alpha(img, lay, (0, 0), al)

    card("alliance", 32.0, 35.6, [("TRIPLE-", F_TITLE, (235, 90, 80)), ("ALLIANCE", F_TITLE, (235, 90, 80))], 250)
    card("entente", 36.5, 39.6, [("TRIPLE-", F_TITLE, (120, 165, 235)), ("ENTENTE", F_TITLE, (120, 165, 235))], 250)
    card("piege", 40.75, 43.9, [("1 PAYS ATTAQUÉ", F_MID, CREAM), ("=", F_MID, GOLD), ("TOUS EN GUERRE", F_TITLE, (235, 90, 80))], 230)
    card("ultim", 57.75, 60.4, [("ULTIMATUM", F_TITLE, (235, 90, 80)), ("48 HEURES", F_MID, CREAM)], 250)
    card("total", 89.0, 90.2, [("GUERRE", F_TITLE, (235, 90, 80)), ("TOTALE", F_TITLE, (235, 90, 80))], 280)
    # compteur des morts
    if 91.25 <= t <= 93.45:
        n = int(18_000_000 * ease(min(1, (t - 91.25) / 1.1)))
        s = f"{n:,}".replace(",", " ")
        al = min(1, (t - 91.25) / 0.3, (93.45 - t) / 0.25)
        lay = big_center([("1914 — 1918", F_MID, CREAM), (s, F_TITLE, GOLD), ("MORTS", F_MID, CREAM)], 240)
        paste_alpha(img, lay, (0, 0), al)
    if 93.4 <= t <= DUR:
        al = min(1, (t - 93.4) / 0.4)
        lay = cached("emp", lambda: big_center([("QUATRE EMPIRES", F_MID, (235, 90, 80)), ("EFFONDRÉS", F_TITLE, CREAM)], 230))
        paste_alpha(img, lay, (0, 0), al * (1 if t < DUR - 1.2 else max(0, (DUR - t) / 1.2)))
    # phrases de conclusion (affichées comme dans la version d'origine)
    for key, a0, s, col, y in (("fin1", 96.0, "Personne n'a voulu tout détruire.", CREAM, 1430),
                               ("fin2", 98.4, "Personne n'a su arrêter la machine.", GOLD, 1530)):
        if t >= a0:
            al = min(1, (t - a0) / 0.6) * (1 if t < DUR - 1.2 else max(0, (DUR - t) / 1.2))
            lay = cached(key, lambda s=s, col=col, y=y: big_center([(s, F_MID, col)], y))
            paste_alpha(img, lay, (0, 0), al)

    # dates du domino
    for i, (a0, a1, s) in enumerate(DATES):
        if a0 <= t <= a1:
            al = min(1, (t - a0) / 0.25, (a1 - t) / 0.25)
            lay = cached(("date", i), lambda s=s: big_center([(s, F_DATE, GOLD)], 230))
            dx = (1 - ease(min(1, (t - a0) / 0.3))) * 80
            paste_alpha(img, lay, (dx, 0), al)

    # sous-titres karaoké
    for i, (c0, c1, txt) in enumerate(CAPS):
        if c0 <= t < c1 + 0.05:
            words = txt.split(" ")
            lens = np.cumsum([len(w) + 1 for w in words])
            frac = (t - c0) / max(c1 - c0, 0.01)
            wi = int(np.searchsorted(lens / lens[-1], min(frac, 0.999), side="right"))
            lay = caption_layer(i, min(wi, len(words) - 1))
            pop = ease(min(1, (t - c0) / 0.12))
            if lay.width > W:
                s = W / lay.width
                lay = lay.resize((W, int(lay.height * s)), Image.BILINEAR)
            y = 1500 + (1 - pop) * 18
            paste_alpha(img, lay, ((W - lay.width) / 2, y), 0.35 + 0.65 * pop)
            break
    return img.convert("RGB")

# ---------------------------------------------------------------- main
def main():
    out = os.path.join(HERE, "build", "guerre14.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        for t in map(float, sys.argv[2:]):
            frame(t).save(os.path.join(HERE, "build", f"preview_{t:06.2f}.png"))
        return
    n = int(round(DUR * FPS))
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", os.path.join(HERE, "narration.m4a"), "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "copy", "-shortest", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame(i / FPS).tobytes())
        if i % 300 == 0:
            print(f"{i}/{n}", flush=True)
    p.stdin.close()
    p.wait()
    print(out)

if __name__ == "__main__":
    main()
