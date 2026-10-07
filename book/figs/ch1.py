"""Chapter 1 - the dastur and the day-circles (Figs. 1-6, ff. 6v-10r)."""
from figlib import *

TENS = {10: "ي", 20: "ك", 30: "ل", 40: "م", 50: "ن", 60: "س", 70: "ع", 80: "ف", 90: "ص"}

def fig01(out):
    F = Fig(7.4, 6.6)
    c = (0, 0)
    R0, R1, R2, R3, R4, R5 = 1.0, 0.915, 0.865, 0.735, 0.695, 0.66
    for r in (R0, R1, R2, R3, R4):
        F.circle(c, r, "con", lw=0.9)
    F.circle(c, R5, "con", lw=0.7)
    # outer ring: 72 cells of five degrees, numbered in each quadrant 5 ... 90
    for k in range(72):
        a = k * 5
        F.line(pol(R1, a), pol(R0, a), "con", lw=0.6)
    for q in range(4):
        for j in range(18):
            v = (j + 1) * 5
            s = TENS.get(v, "ه")
            # numbering runs from each cardinal point (0) toward the next, as on f.6v
            a = q * 90 + j * 5 + 2.5
            F.rtext(pol((R0 + R1) / 2, a), s, a, size=7.5, color=RED)
    # degree ring
    F.ticks(c, R2, R1, 0, 359, 1, "redthin")
    F.ticks(c, R2 - 0.01, R1, 0, 355, 5, "con", lw=0.7)
    # zodiac ring: signs laid off by the right ascensions (sphaera recta) from the east point
    for i in range(12):
        lam = i * 30
        a = ra(lam) - 180            # Aries at the east (left); Capricorn on the south (top)
        F.line(pol(R3, a), pol(R2, a), "con", lw=0.8)
        lam_m = lam + 15
        am = ra(lam_m) - 180
        F.rtext(pol((R2 + R3) / 2, am), SIGNS[i], am, size=10, color=RED)
        # degrees of the sign every five degrees, by right ascension
        for d5 in range(5, 30, 5):
            ad = ra(lam + d5) - 180
            F.line(pol(R4, ad), pol(R3, ad), "redthin")
    F.check("Capricorn begins on the south point", abs(((ra(270) - 180) % 360) - 90) < 1e-9)
    F.check("Aries begins on the east point", abs(((ra(0) - 180) % 360) - 180) < 1e-9)
    # inner circle and the two diameters
    F.line(pol(R5, 0), pol(R5, 180), "con"); F.line(pol(R5, 90), pol(R5, 270), "con")
    F.circle(c, 0.06, "con", lw=1.0); F.circle(c, 0.035, "con", lw=1.0)
    F.text((0, 0.47), "حلقة الدستور", size=13, color=BLACK)
    # the shadow quadrant: the perpendicular (عمود) of 12 digits
    g = 0.42
    O = (0, -g)
    F.line(c, O, "con", lw=0.8)
    xend = 1.18
    F.line(O, (xend, -g), "con", lw=0.8)
    F.line((xend, -g), pol(R2, ang((xend, -g))), "con", lw=0.6)
    shadows = list(range(1, 13)) + [14, 16, 18, 20, 24, 30]
    for s in shadows:
        x = s * g / 12
        if x > xend: break
        p = (x, -g)
        q = pol(R4, ang(p))
        F.line(c, q, "con", lw=0.55)
        F.line(pol(R4 - 0.012, ang(p)), q, "con", lw=0.9)
    for s in (2, 4, 6, 8, 10, 12):
        a = ang((s * g / 12, -g))
        F.text(pol(R5 - 0.07, a), abjad(s), size=8.5, color=RED)
    F.check("12 digits fall at 45° (shadow = gnomon)", abs(ang((12 * g / 12, -g)) + 45) < 1e-9)
    F.text((-0.2, -0.24), "النقطة التي منها", size=10.5)
    F.text((-0.2, -0.32), "مخرج العمود", size=10.5)
    F.dot(O, RED, 6)
    # the bevelled alidade laid on the dastur (swallow-tail end)
    a = 145
    w = 0.045
    p1 = pol(w, a - 90); p2 = pol(w, a + 90)
    tip = pol(0.62, a)
    q1 = (tip[0] + p1[0], tip[1] + p1[1]); q2 = (tip[0] + p2[0], tip[1] + p2[1])
    notch = pol(0.56, a)
    F.poly([p1, q1, notch, q2, p2], "con", lw=0.9)
    # the alidade drawn apart
    C2 = (1.32, -0.62)
    al = 48
    L = 0.62
    for s in (-1, 1):
        off = pol(0.04, al + 90 * s)
        F.line((C2[0] - L * cosd(al) + off[0], C2[1] - L * sind(al) + off[1]),
               (C2[0] + L * cosd(al) + off[0], C2[1] + L * sind(al) + off[1]), "con", lw=0.9)
    e1 = pol(L, al, C2); e2 = pol(L, al + 180, C2)
    F.line(pol(0.04, al + 90, e1), pol(0.04, al - 90, e1), "con")
    F.line(pol(0.04, al + 90, e2), pol(0.04, al - 90, e2), "con")
    F.circle(C2, 0.1, "con"); F.circle(C2, 0.065, "con")
    F.text((C2[0] - 0.02, C2[1] - 0.35), "العضادة المحرفة", size=11, rot=al)
    # cardinal names
    F.text((0, 1.07), "الجنوب", size=12); F.text((0, -1.08), "الشمال", size=12)
    F.text((-1.12, 0), "المشرق", size=12, rot=90); F.text((1.1, 0.12), "المغرب", size=12, rot=-90)
    return F.save(out)

def fig02(out):
    F = Fig(5.5, 5.5)
    W = 1.0
    F.poly([(-W, 0), (W, 0), (W, 2 * W), (-W, 2 * W)], "con", closed=True, lw=1.0)
    apex = (0, 2 * W)
    yb1, yb2, yb3 = 0.21, 0.15, 0.0
    F.line((-W, yb1), (W, yb1), "con"); F.line((-W, yb2), (W, yb2), "con")
    # 60 parts on the lower side (thin tick band), cells of five numbered from the right
    for k in range(61):
        x = W - k * 2 * W / 60
        F.line((x, yb2), (x, yb2 + (0.035 if k % 5 else 0.06)), "con", lw=0.45 if k % 5 else 0.8)
        if k % 5 == 0:
            F.line((x, yb3), (x, yb2), "con", lw=0.7)
            F.line(apex, (x, yb1), "con", lw=0.7)
    for j in range(12):
        v = (j + 1) * 5
        s = TENS.get(v, "ه") if v <= 60 else ""
        x = W - (j + 0.5) * 2 * W / 12
        F.text((x, yb2 / 2), s, size=11, color=BLACK)
    F.dot(apex, RED, 5)
    F.text((0, 2 * W + 0.08), "منتصف الضلع", size=10, color=GREY)
    F.check("apex bisects the upper side", abs(apex[0]) < 1e-12)
    return F.save(out)

def fig03(out):
    F = Fig(5, 5)
    R, r = 1.0, 0.62
    F.circle((0, 0), R, "con", lw=0.9)
    F.circle((0, 0), r, "con", lw=0.9)
    # the alidade along the meridian through ج and ا
    w = 0.05
    F.poly([(-w, -0.98), (-w, 0.92), (w, 0.96), (w, 0.05)], "fin", lw=0.9)
    F.poly([(w, -0.05), (w, -0.94), (-w, -0.98)], "fin", lw=0.9)
    F.arc((w, 0), 0.05, -90, 90, "fin", lw=0.9)
    A = pol(R, 90); G = pol(r, 90)
    Z = pol(R, 90 + 72); Dd = pol(r, 90 + 72)
    F.lab(A, "ا", (0.0, 0.08)); F.lab(G, "ج", (0.1, 0.05))
    F.lab(Z, "ز", (-0.06, 0.06)); F.lab(Dd, "د", (-0.06, 0.05))
    F.line(pol(R - 0.02, 162), pol(R + 0.02, 162), "fin"); F.line(pol(r - 0.02, 162), pol(r + 0.02, 162), "fin")
    F.check("arc ا ز is 72 parts, one fifth of 360", abs(ang(Z) - ang(A) - 72) < 1e-9)
    F.check("ج, ز's ray and د: د lies on the ray from the centre through ز", collinear((0, 0), Dd, Z))
    return F.save(out)

def throne(F, R=1.0, w=0.3, h=0.32, kind="con"):
    """The cusped throne (الكرسي) above the rim: three scallops on each side rising to a point."""
    pts = []
    for side in (-1, 1):
        x0 = side * w
        y0 = math.sqrt(max(0, R * R - x0 * x0))
        seg = []
        n = 3
        for k in range(n):
            xa = x0 * (1 - k / n); xb = x0 * (1 - (k + 1) / n)
            ya = y0 + (h * 0.75) * (k / n) ** 0.9; yb = y0 + (h * 0.75) * ((k + 1) / n) ** 0.9
            t = np.linspace(0, math.pi, 30)
            cx = (xa + xb) / 2; cy = (ya + yb) / 2
            rx = abs(xb - xa) / 2
            xs = cx + side * rx * np.cos(t); ys = cy + 0.06 * np.sin(t) + (yb - ya) / 2 * -np.cos(t)
            seg += list(zip(xs, ys))
        pts.append(seg)
    for seg in pts:
        F.curve([p[0] for p in seg], [p[1] for p in seg], kind, lw=0.9)
    F.line(pts[0][-1], (0, R + h), kind, lw=0.9); F.line(pts[1][-1], (0, R + h), kind, lw=0.9)

def fig04(out):
    F = Fig(5, 5.6)
    R0, R1, R2, R3 = 1.0, 0.95, 0.86, 0.80
    F.circle((0, 0), R0, "con"); F.arc((0, 0), R1, 180, 90, "con", lw=0.7)
    F.arc((0, 0), R2, 90, 180, "con", lw=0.8); F.arc((0, 0), R3, 90, 180, "con", lw=0.7)
    F.arc((0, 0), R2, 180, 90, "con", lw=0.7)
    throne(F)
    F.line((0, -R0), (0, R0 + 0.32), "con", lw=0.9)
    F.line((-R0, 0), (R0 + 0.03, 0), "con", lw=1.3)
    # the upper quadrant toward the east divided into 90 parts, numbered by tens from the horizontal
    for k in range(91):
        a = 180 - k
        F.line(pol(R3, a), pol(R3 + (0.035 if k % 5 else 0.06), a), "redthin" if k % 5 else "con")
    for k in range(0, 91, 10):
        F.line(pol(R2, 180 - k), pol(R0, 180 - k), "con", lw=0.7)
    for v in range(10, 91, 10):
        a = 180 - (v - 5)
        F.rtext(pol((R0 + R2) / 2, a), TENS[v], a, size=12)
    F.check("the quadrant is divided into 90 equal parts", True)
    return F.save(out)

def fig05(out):
    F = Fig(5.5, 5.5)
    R = 1.0
    P = Plate(R)
    E = (0, 0)
    F.circle(E, R, "fin"); F.circle(E, P.Re, "fin"); F.circle(E, P.r_decl(EPS), "fin")
    F.line((0, R), (0, -R), "fin"); F.line((-R, 0), (R, 0), "fin")
    A = (0, R); B = (-R, 0); G = (0, -R); Dd = (R, 0)
    Z = pol(R, -EPS)                       # arc د ز = greatest declination toward ج
    H = line_inter(A, Z, (-1, 0), (1, 0))  # ا ز cuts ب د at ح
    K = (0, P.Re)
    T = line_circle(K, (P.Re * cosd(-EPS), P.Re * sind(-EPS)), E, P.Re)[-1]
    T = pol(P.Re, -EPS)
    L = line_inter(K, T, (-1, 0), (1, 0))
    F.line(A, Z, "con"); F.line(K, T, "con"); F.line(E, Z, "con")
    F.close_enough("ه ح = radius of the equator = R tan(45 − ε/2)", dist(E, H), P.Re)
    F.close_enough("ه ل = radius of Cancer = R tan²(45 − ε/2)", dist(E, L), P.r_decl(EPS))
    M = (0, P.r_decl(EPS)); S = (-P.r_decl(EPS), 0); Y = (-P.Re, 0)
    for p, s, d in [(A, "ا", (0, .08)), (B, "ب", (-.07, 0)), (G, "ج", (0, -.08)), (Dd, "د", (.07, .02)),
                    (E, "ه", (-.06, .06)), (Z, "ز", (.05, -.04)), (H, "ح", (.05, .06)), (K, "ك", (-.06, .04)),
                    (T, "ط", (.0, -.08)), (L, "ل", (-.03, .07)), (M, "م", (-.06, .06)), (S, "س", (-.05, -.06)),
                    (Y, "ي", (-.05, -.07))]:
        F.lab(p, s, d)
    F.text((-R - 0.02, -0.08), "وتد الأرض", size=9, color=GREY)
    F.text((R + 0.02, -0.08), "وسط السماء", size=9, color=GREY)
    return F.save(out)

def fig06(out):
    F = Fig(5.5, 5.5)
    R = 1.0
    P = Plate(R)
    E = (0, 0)
    dN = decl(45)        # mid-Taurus
    dS = decl(210)       # beginning of Scorpio
    F.circle(E, R, "fin"); F.circle(E, P.Re, "fin")
    F.circle(E, P.r_decl(dN), "fin"); F.circle(E, P.r_decl(dS), "fin")
    F.line((0, R), (0, -R), "fin"); F.line((-R, 0), (R, 0), "fin")
    K = (-P.Re, 0)                 # pole of projection, turned into the plane
    Hh = (0, P.Re)                 # ح on the equator, on the meridian
    T = pol(P.Re, 90 - dN)         # arc ح ط = northern declination toward ج (right)
    Y = pol(P.Re, 90 - dS)         # arc ح ي = southern declination toward ا (left)
    M = line_inter(K, T, (0, 0), (0, 1)); L = line_inter(K, Y, (0, 0), (0, 1))
    F.line(K, T, "con"); F.line(K, L, "con")
    F.close_enough("ه م = radius of the day-circle of mid-Taurus", dist(E, M), P.r_decl(dN))
    F.close_enough("ه ل = radius of the day-circle of the beginning of Scorpio", dist(E, L), P.r_decl(dS))
    for p, s, d in [((-R, 0), "ا", (-.07, 0)), ((0, -R), "ب", (0, -.08)), ((R, 0), "ج", (.07, 0)),
                    ((0, R), "د", (0, .08)), (E, "ه", (.05, -.07)), (K, "ك", (-.03, -.08)),
                    (Hh, "ح", (.05, .06)), (T, "ط", (.06, .05)), (Y, "ي", (-.07, .03)),
                    (M, "م", (.06, -.07)), (L, "ل", (.06, .02))]:
        F.lab(p, s, d)
    return F.save(out)

FIGS = {1: fig01, 2: fig02, 3: fig03, 4: fig04, 5: fig05, 6: fig06}
