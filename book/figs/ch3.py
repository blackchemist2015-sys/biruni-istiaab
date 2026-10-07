"""Chapter 3 - rete, fittings, the southern astrolabe and special plates (Figs. 17-24, ff. 22r-27r)."""
from figlib import *
from ch1 import throne

PREC = 13 + 13 / 60       # precession from Ptolemy to al-Biruni's epoch (1310 Alexander)
# (name, ecliptic longitude J2000, latitude): the longitudes are brought back to Biruni's epoch
STARS_J2000 = [
    ("النسر الواقع", 285.3, 61.7), ("النسر الطائر", 301.8, 29.3), ("الفكة", 222.3, 44.3),
    ("رأس الحواء", 262.4, 36.0), ("السماك الرامح", 204.2, 30.7), ("العيوق", 81.9, 22.9),
    ("الدبران", 69.8, -5.5), ("رجل الجبار", 76.8, -31.1), ("الشعرى اليمانية", 104.1, -39.6),
    ("الشعرى الشامية", 115.8, -16.0), ("قلب الأسد", 149.8, 0.5), ("قلب العقرب", 249.8, -4.6),
    ("منكب الجوزاء", 88.8, -16.0), ("الردف", 335.3, 59.9), ("السماك الأعزل", 203.8, -2.1),
    ("فم الحوت", 333.9, -21.0), ("ذنب قيطس", 2.6, -20.8), ("منكب الفرس", 359.4, 31.1),
    ("سهيل", 105.0, -75.8), ("جناح الغراب", 190.7, -14.5), ("فم الفرس", 333.8, 22.1),
]
def stars_epoch():
    return [(n, (l - (50.29 / 3600) * (2000 - 999)) % 360, b) for n, l, b in STARS_J2000]

def pointer(F, tip, toward, size=0.075, kind="fin", fill=True):
    """A flame-shaped star pointer (شظية) whose point is the head of the star."""
    a = ang(toward, tip)
    base = pol(size, a, tip)
    w = size * 0.33
    l = pol(w, a + 90, base); r = pol(w, a - 90, base)
    m1 = pol(size * 0.45, a, tip)
    pts = [tip, pol(w * 0.6, a + 90, m1), l, pol(size * 0.25, a, base), r, pol(w * 0.6, a - 90, m1)]
    if fill:
        F.fill(pts, color=RED if kind == "con" else "#333333", z=4)
    F.poly(pts, kind, lw=0.6, closed=True, z=4)
    return base

def ring(F, c, r1, r2, a1=0, a2=360, kind="con", lw=0.9):
    if a2 - a1 >= 360:
        F.circle(c, r1, kind, lw=lw); F.circle(c, r2, kind, lw=lw)
    else:
        F.arc(c, r1, a1, a2, kind, lw=lw); F.arc(c, r2, a1, a2, kind, lw=lw)

def ecliptic_ring(F, P, rot=lambda p: p, width=0.085, names=True, kind="con", southern=False):
    c, r = P.ecliptic(); c = rot(c)
    F.circle(c, r, kind, lw=1.0); F.circle(c, r - width, kind, lw=0.9)
    for i in range(12):
        lam = i * 30
        p = rot(P.ecl_point(lam))
        a = ang(p, c)
        F.line(pol(r, a, c), pol(r - width, a, c), kind, lw=0.8)
        for d in range(5, 30, 5):
            q = rot(P.ecl_point(lam + d)); b = ang(q, c)
            F.line(pol(r, b, c), pol(r - width * 0.35, b, c), "redthin" if kind == "con" else "thin")
        if names:
            q = rot(P.ecl_point(lam + 15)); b = ang(q, c)
            nm = SIGNS[(i + 6) % 12] if southern else SIGNS[i]
            F.rtext(pol(r - width * 0.62, b, c), nm, b, size=8.5, color=RED if kind == "con" else BLACK)
    return c, r

def fig17(out):
    F = Fig(6.4, 6.4)
    P = Plate(1.0)
    E = (0, 0)
    Rr = 1.0; w = 0.085
    c, r = ecliptic_ring(F, P)
    F.check("the ecliptic touches the rim at the head of Capricorn", abs(c[1] + r - Rr) < 1e-9)
    # the outer ring (الطوق) on the circle of Capricorn, shown on the northern half where
    # it leaves the ecliptic; it is stepped where it joins the bars
    ring(F, E, Rr, Rr - w, 185, 355)
    for a in (185, 355):
        F.line(pol(Rr, a), pol(Rr - w, a), "con")
    for s in (-1, 1):
        x = s * (Rr - w / 2)
        F.poly([(s * Rr * cosd(5), -Rr * sind(5)), (s * (Rr + 0.07), -0.03), (s * (Rr + 0.07), 0.04), (s * Rr * cosd(8), Rr * sind(8))], "con", lw=0.9)
    # the bars: the meridian and the east-west line, and the central disc (الفلس)
    bw = 0.022
    for s in (-1, 1):
        F.line((-Rr - 0.05, s * bw), (Rr + 0.05, s * bw), "con", lw=0.7)
        F.line((s * bw, -Rr + w), (s * bw, Rr), "con", lw=0.7)
    F.circle(E, 0.085, "con", lw=1.0); F.circle(E, 0.035, "con", lw=0.9)
    # star pointers (stars that fall inside the circle of Capricorn)
    placed = 0
    keep = {"النسر الواقع", "النسر الطائر", "الفكة", "رأس الحواء", "السماك الرامح", "العيوق", "الدبران",
            "رجل الجبار", "الشعرى اليمانية", "الشعرى الشامية", "قلب الأسد", "الردف"}
    for name, lam, beta in stars_epoch():
        if name not in keep: continue
        a_, d_ = eq_from_ecl(lam, beta)
        p = P.star(a_, d_)
        if dist(p, E) > Rr - 0.03 or dist(p, E) < 0.12:
            continue
        toward = c if abs(dist(p, c) - (r - w / 2)) < 0.25 else E
        base = pointer(F, p, toward, kind="con")
        F.text((p[0], p[1] - 0.055), name, size=8.5, color=BLACK)
        placed += 1
    F.check(f"{placed} star heads placed by declination and right ascension for 1310 Alexander", placed > 8)
    F.text((0, 1.06), "الجنوب", size=10, color=GREY); F.text((0, -1.07), "الشمال", size=10, color=GREY)
    return F.save(out)

def horse_head(F, at, s=0.25):
    """The wedge called 'the horse' (الفرس), cut in the shape of a horse's head."""
    x0, y0 = at
    pts = [(0, 0), (0.0, 0.55), (0.12, 0.85), (0.18, 1.05), (0.25, 0.86), (0.42, 0.78), (0.62, 0.6),
           (0.66, 0.48), (0.5, 0.45), (0.38, 0.5), (0.36, 0.3), (0.4, 0.0)]
    F.poly([(x0 + s * x, y0 + s * y) for x, y in pts], "con", lw=0.9, closed=True)
    F.dot((x0 + s * 0.3, y0 + s * 0.68), RED, 3)

def fig18(out):
    F = Fig(9.5, 3.4)
    # the axis-pin (القطب) with its cusped head, and the horse through its slot
    px = -2.45
    F.poly([(px - 0.13, 0.05), (px - 0.13, 0.95), (px + 0.13, 0.95), (px + 0.13, 0.05)], "con", lw=0.9)
    t = np.linspace(0, math.pi, 40)
    F.curve(px + 0.13 * np.cos(t), 0.95 + 0.06 + 0.12 * np.sin(t), "con", lw=0.9)
    F.line((px - 0.13, 0.95), (px - 0.13, 1.01), "con"); F.line((px + 0.13, 0.95), (px + 0.13, 1.01), "con")
    F.poly([(px - 0.45, 0.35), (px + 0.25, 0.35), (px + 0.25, 0.48), (px - 0.45, 0.48)], "con", lw=0.9)
    horse_head(F, (px - 0.66, 0.38), 0.4)
    F.poly([(px + 0.13, 0.2), (px + 0.7, 0.2), (px + 0.85, 0.3), (px + 0.13, 0.3)], "con", lw=0.8)
    F.text((px, 1.33), "القطب", size=13, color=BLACK); F.text((px - 0.75, 0.95), "الفرس", size=12, color=BLACK)
    # the alidade (العضادة) in perspective with its two vanes
    ax0, ax1, y0 = -1.6, 2.6, -0.15
    dx, dy = 0.28, 0.16
    F.poly([(ax0, y0), (ax1, y0), (ax1 + dx, y0 + dy), (ax0 + dx, y0 + dy)], "con", closed=True, lw=0.9)
    F.line((ax0, y0 - 0.05), (ax1, y0 - 0.05), "con", lw=0.7)
    F.line((ax0, y0 - 0.05), (ax0, y0), "con", lw=0.7); F.line((ax1, y0 - 0.05), (ax1, y0), "con", lw=0.7)
    F.line((ax0 + 0.15, y0 + dy / 2), (ax1 + 0.1, y0 + dy / 2), "redthin")
    F.circle(((ax0 + ax1) / 2 + dx / 2, y0 + dy / 2), 0.09, "con")
    # اللبنة: a pentagonal vane (house-shaped) with its sighting hole
    lx = ax0 + 0.45
    F.poly([(lx - 0.2, y0 + 0.05), (lx - 0.2, y0 + 0.4), (lx, y0 + 0.62), (lx + 0.2, y0 + 0.4), (lx + 0.2, y0 + 0.05)], "con", lw=0.9)
    F.circle((lx, y0 + 0.34), 0.035, "con")
    F.text((lx + 0.15, y0 + 0.85), "اللبنة", size=12)
    # الهدفة: a diamond-shaped vane
    hx = ax1 - 0.6
    F.poly([(hx, y0 + 0.05), (hx + 0.17, y0 + 0.33), (hx, y0 + 0.62), (hx - 0.17, y0 + 0.33)], "con", closed=True, lw=0.9)
    F.circle((hx, y0 + 0.33), 0.035, "con")
    F.text((hx + 0.05, y0 + 0.85), "الهدفة", size=12)
    F.text(((ax0 + ax1) / 2, y0 + 0.62), "العضادة", size=14)
    # the ring (الحلقة) and the bail (العروة) at the right, as at the page's edge
    C = (3.55, 0.45)
    F.circle(C, 0.55, "con", lw=1.0); F.circle(C, 0.43, "con", lw=0.9)
    F.circle((C[0], C[1] - 0.68), 0.13, "con"); F.circle((C[0], C[1] - 0.68), 0.07, "con")
    F.poly([(C[0] - 0.1, C[1] - 0.8), (C[0] - 0.07, C[1] - 1.05), (C[0] + 0.07, C[1] - 1.05), (C[0] + 0.1, C[1] - 0.8)], "con", lw=0.9)
    F.text(C, "الحلقة", size=12); F.text((C[0] + 0.4, C[1] - 0.8), "العروة", size=11)
    return F.save(out)

def fig19(out, phi=22.0):
    F = Fig(5.6, 5.8)
    P = Plate(1.0, south=True)
    E = (0, 0)
    F.circle(E, 1.0, "con", lw=1.0)
    F.circle(E, P.Re, "con", lw=0.8); F.circle(E, P.r_decl(-EPS), "con", lw=0.8)
    F.line((-1, 0), (1, 0), "con", lw=0.8); F.line((0, -1), (0, 1), "con", lw=0.8)
    F.close_enough("the rim is the circle of Cancer", P.r_decl(EPS), 1.0)
    Z = P.zenith(phi)
    for h in range(0, 90, 6):
        c, r = P.almucantar(phi, h)
        F.arc_clip(c, r, inside=[(E, 1.0)], kind="con", lw=1.25 if h == 0 else 0.7)
    F.circle(Z, 0.035, "con", lw=0.8)
    F.check("the zenith lies between the circles of Cancer and Aries",
            P.Re < dist(Z, E) < 1.0)
    F.text((0, 1.06), "الجنوب", size=10, color=GREY); F.text((0, -1.07), "الشمال", size=10, color=GREY)
    return F.save(out)

def fig20(out):
    F = Fig(6.2, 6.2)
    P = Plate(1.0, south=True)
    E = (0, 0)
    Rr, w = 1.0, 0.075
    # the southern rete: the same ecliptic ring, each sign bearing the name of its opposite
    c, r = ecliptic_ring(F, P, southern=True)
    F.check("the ecliptic of the southern rete touches the rim (circle of Cancer)",
            abs(dist(c, E) + r - Rr) < 1e-9 or abs(r - dist(c, E) - Rr) < 1e-9)
    # the first ring (الطوق) left whole and round, bent inward in three places
    bends = [(180, "الصرفة"), (0, "منكب الفرس"), (285, "فم الفرس")]
    for a0, _ in bends:
        pass
    ok = lambda a: all(abs(((a - b + 180) % 360) - 180) > 7.5 for b, _ in bends)
    for rad in (Rr, Rr - w):
        t = np.arange(0, 360.01, 0.5)
        msk = np.array([ok(a) for a in t])
        F.curve_clip(rad * np.cos(t * D), rad * np.sin(t * D), msk, "con", lw=0.9)
    for a0, name in bends:
        cc = pol(Rr - w / 2, a0)
        F.arc(cc, 0.075 + w / 2, a0 + 90, a0 + 270, "con", lw=0.9)
        F.arc(cc, 0.075 - w / 2, a0 + 90, a0 + 270, "con", lw=0.9)
        F.dot(cc, RED, 7)
        F.text(pol(0.2, a0 + 180, cc), name, size=7.5)
    # the east-west bar joining the ring to the ecliptic, and the meridian bar
    for s in (-1, 1):
        F.line((-Rr + w, s * 0.02), (Rr - w, s * 0.02), "con", lw=0.7)
    F.line((0.02, c[1] - r), (0.02, Rr - w), "con", lw=0.7); F.line((-0.02, c[1] - r), (-0.02, Rr - w), "con", lw=0.7)
    F.circle(E, 0.08, "con", lw=1.0); F.circle(E, 0.035, "con", lw=0.9)
    # southern stars and northern ones inside the circle of Cancer
    placed = 0
    for name, lam, beta in stars_epoch():
        a_, d_ = eq_from_ecl(lam, beta)
        if name in [b[1] for b in bends]: continue
        if name not in {"سهيل", "الشعرى اليمانية", "رجل الجبار", "قلب العقرب", "فم الحوت", "ذنب قيطس", "جناح الغراب", "السماك الأعزل"}: continue
        p = P.star(a_, d_)
        if dist(p, E) > Rr - w - 0.02 or dist(p, E) < 0.12: continue
        pointer(F, p, E, kind="con")
        F.text((p[0], p[1] - 0.055), name, size=8.5)
        placed += 1
    F.check(f"{placed} stars placed by the southern projection", placed > 5)
    return F.save(out)

def fig21(out, phi=30.0):
    F = Fig(5.6, 5.8)
    P = Plate(1.0)
    E = (0, 0)
    F.circle(E, 1.0, "con", lw=1.0); F.circle(E, P.Re, "con", lw=0.8)
    rc = P.r_decl(EPS); F.circle(E, rc, "con", lw=0.8)
    F.line((-1, 0), (1, 0), "con", lw=0.8); F.line((0, 0), (0, 1), "con", lw=0.8)
    c0, r0 = P.almucantar(phi, 0)
    F.arc_clip(c0, r0, inside=[(E, 1.0)], kind="con", lw=1.2)
    # the equal hours: the horizon turned about the pole by 15° each hour (below the horizon)
    for k in range(1, 13):
        cc = pol(dist(c0, E), 90 - 15 * k)    # horizon centre rotated westward→downward
        ok_in = [(E, 1.0)]
        t = np.linspace(0, 2 * math.pi, 1441)
        x = cc[0] + r0 * np.cos(t); y = cc[1] + r0 * np.sin(t)
        rr = np.hypot(x, y)
        below = (x - c0[0]) ** 2 + (y - c0[1]) ** 2 > r0 * r0
        msk = (rr <= 1.0) & (rr >= rc) & below
        F.curve_clip(x, y, msk, "con", lw=0.7)
    # check: the point of the hour line on a day-circle is 15k° of hour angle from sunset
    d = 10.0
    H0 = acosd(-tand(phi) * tand(d))
    p = P.eq(H0 + 15 * 3, d)
    cc = pol(dist(c0, E), 90 - 15 * 3)
    F.check("the 3rd equal-hour line passes 45° of hour angle after sunset on every day-circle",
            abs(dist(p, cc) - r0) < 1e-9)
    for k in range(12):
        d = -EPS * 0.6
        H0 = acosd(-tand(phi) * tand(d))
        p = P.eq(H0 + 15 * (k + 0.5), d)
        if dist(p, E) < 0.97:
            F.text(p, abjad(k + 1), size=11)
    F.text((0, -0.33 * 1), "لعرض ل", size=13)
    return F.save(out)

def fig22(out, phi=36.0):
    F = Fig(4.8, 7.0)
    P = Plate(1.0)
    E = (0, 0)
    Re = P.Re
    F.circle(E, 1.0, "fin"); F.circle(E, Re, "fin")
    A = (-1.0, 0); B = (0, -1.0); G = (1.0, 0); Dd = (0, 1.0)
    K = (-Re, 0); M = (Re, 0); T = (0, Re); L = (0, -Re)
    F.line(A, G, "fin", lw=0.8)
    Hh = pol(Re, 180 - phi)                 # arc ك ه = latitude
    Y = line_inter(K, Hh, (0, 0), (0, 1))   # south point of the horizon, beyond the plate
    c0, r0 = P.almucantar(phi, 0)
    S_ = (0, c0[1] - r0)                    # north point of the horizon
    S = mid(S_, Y)
    F.close_enough("ي is the south point of the horizon", Y[1], c0[1] + r0)
    F.close_enough("س, the midpoint of ص ي, is the centre of the horizon", S[1], c0[1])
    F.line((0, -1.0), (0, Y[1] + 0.05), "fin", lw=0.7)
    F.line(K, Y, "con")
    F.arc_clip(c0, r0, inside=[(E, 1.0)], kind="fin", lw=1.2)
    F.line((-1.15, S[1]), (1.15, S[1]), "con")
    F.check("the centre س falls between ط and د (latitude 36°)", Re < S[1] < 1.0)
    for p, s, d in [(A, "ا", (-.07, 0)), (B, "ب", (0, -.07)), (G, "ج", (.07, 0)), (Dd, "د", (.06, .06)),
                    (K, "ك", (-.06, -.05)), (M, "م", (.06, -.05)), (T, "ط", (.05, -.06)), (L, "ل", (.05, -.05)),
                    (Hh, "ه", (-.06, .03)), (Y, "ي", (.06, 0)), (S_, "ص", (.06, -.05)), (S, "س", (-.06, -.05))]:
        F.lab(p, s, d)
    Hc = max(line_circle(K, Y, E, 1.0), key=lambda p: p[1])
    F.lab(Hc, "ح", (-.06, .04))
    return F.save(out)

def fig23(out, phi=36.0):
    F = Fig(5.6, 5.6)
    P = Plate(1.0)
    E = (0, 0)
    F.circle(E, 1.0, "con", lw=0.9); F.circle(E, 1.12, "con", lw=0.9)
    F.circle(E, P.Re, "con", lw=0.8)
    c0, r0 = P.almucantar(phi, 0)
    Sn = (0, c0[1] - r0); Ys = (0, c0[1] + r0)
    F.line((-1, 0), (1, 0), "con", lw=0.8)
    # great circles through the north and south points of the horizon: 'horizons' turned
    # about the north-south line; each cuts the equator 15° (one equal hour) from the next
    for k in range(12):
        # the circle through ص, ي and the equator point at 15k° from the east point
        q = pol(P.Re, 180 - 15 * k)
        if abs(q[0]) < 1e-9:
            F.line((0, -1.0), (0, 1.0), "con", lw=0.8); continue
        cc, rr = circle3(Sn, Ys, q)
        F.arc_clip(cc, rr, inside=[(E, 1.0)], kind="con", lw=1.1 if k == 0 else 0.75)
        q2 = pol(P.Re, -15 * k)
        F.check(f"circle {k} cuts the equator at two opposite points ({15*k}°)", abs(dist(cc, q2) - rr) < 1e-9) if k in (1, 4) else None
    F.circle(Sn, 0.05, "con", lw=0.9)
    for a in (55, 125, 235, 305):
        for dd in (-2, 2):
            F.line(pol(1.0, a + dd), pol(1.12, a + dd), "con", lw=0.9)
    return F.save(out)

def fig24(out):
    F = Fig(6.2, 6.2)
    P = Plate(1.0)
    E = (0, 0)
    Re = P.Re; rc = P.r_decl(EPS)
    F.circle(E, 1.0, "con", lw=1.0); F.circle(E, Re, "con", lw=0.9); F.circle(E, rc, "con", lw=0.9)
    F.line((-1, 0), (1, 0), "con", lw=0.6); F.line((0, -1), (0, 1), "con", lw=0.6)
    origins = {180: list(range(0, 33, 4)), 90: list(range(1, 34, 4)), 0: list(range(2, 31, 4)), 270: list(range(3, 32, 4))}
    msk_ok = 0
    for a0, lats in origins.items():
        O = pol(Re, a0)
        for L in lats:
            if L == 0:
                F.line(pol(rc, a0), pol(1.0, a0), "con", lw=0.8)
                continue
            # a horizon of latitude L through the two origins on the diameter at a0, turned so
            # that its outer part runs clockwise (as on f.27r) from each origin
            r_std = Re / sind(L)
            rotc = pol(Re / tand(L), a0 - 90)
            okf = lambda x, y: rc - 1e-9 <= math.hypot(x, y) <= 1.0 + 1e-9
            e1, e2 = F.arc_component(rotc, r_std, O, okf, "con", lw=0.6)
            if abs(dist(rotc, O) - r_std) < 1e-9: msk_ok += 1
            # latitude number at the outer end
            h = e1 if math.hypot(*e1) > math.hypot(*e2) else e2
            if lats.index(L) % 2 == 0:
                F.text(pol(1.05, ang(h)), abjad(L), size=8)
    F.check("every horizon passes through its origin on the equator", msk_ok == sum(len(v) for v in origins.values()) - 1)
    # the declination ladders on each half-diameter between the tropics (every 2°, numbered by tens)
    for a0 in (0, 90, 180, 270):
        n = pol(0.035, a0 + 90); m = pol(-0.035, a0 + 90)
        F.line((n[0] + rc * cosd(a0), n[1] + rc * sind(a0)), (n[0] + cosd(a0), n[1] + sind(a0)), "con", lw=0.7)
        F.line((m[0] + rc * cosd(a0), m[1] + rc * sind(a0)), (m[0] + cosd(a0), m[1] + sind(a0)), "con", lw=0.7)
        for d in range(-22, 23, 2):
            rd = P.r_decl(d)
            p = pol(rd, a0)
            F.line((p[0] + n[0], p[1] + n[1]), (p[0] + m[0], p[1] + m[1]), "con", lw=0.45 if d % 10 else 0.8)
    F.text((0.1, 0.0), "", size=8)
    return F.save(out)

FIGS = {17: fig17, 18: fig18, 19: fig19, 20: fig20, 21: fig21, 22: fig22, 23: fig23, 24: fig24}
