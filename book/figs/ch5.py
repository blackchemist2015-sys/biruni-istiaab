"""Chapter 5 - mixed and unusual astrolabes (Figs. 31-43, ff. 36v-43v)."""
from figlib import *
from mixed import *
from ch3 import pointer, stars_epoch

ARI, TAU, GEM, CAN, LEO, VIR, LIB, SCO, SGR, CAP, AQR, PIS = range(12)
NORTH = {ARI, TAU, GEM, CAN, LEO, VIR}
SOUTH = set(range(12)) - NORTH

def check_rete(F, outside, name):
    # pieces are continuous at the equinoxes when both neighbours lie on the same side or both
    # reach the equator; every piece of a northern sign outside comes from the southern ecliptic
    for sg in range(12):
        use, f, P = sign_piece(sg, sg in outside)
        r = [dist(f(l), (0, 0)) for l in (sg * 30 + 1, sg * 30 + 29)]
        inside = all(x < P.Re + 1e-9 for x in r)
        if inside == (sg in outside):
            F.check(f"{name}: sign {sg} on the wrong side", False); return
    F.check(f"{name}: each sign lies outside the equator exactly when it is listed outside", True)

def fig31(out):
    F = Fig(6.2, 6.2)
    outside = SOUTH and (SOUTH | NORTH)          # the drum keeps every sign outside the equator
    outside = set(range(12))
    mixed_rete(F, outside, rot=-90, size=8.5)
    check_rete(F, outside, "المطبل")
    F.line((0, -1), (0, 1), "con", lw=0.8); F.line((-1, 0), (1, 0), "con", lw=0.8)
    F.circle((0, 0), 1.0 - 0.05, "con", lw=0.6)
    # stars of each half by their own projection (northern half: northern arc)
    for name, lam, beta in stars_epoch():
        a_, d_ = eq_from_ecl(lam, beta)
        for south in (False, True):
            P = Plate(1.0, south=south)
            p = rot_pt(P.star(a_, d_), -90)
            if dist(p, (0, 0)) > 0.9 or dist(p, (0, 0)) < 0.15: continue
            # the northern projection serves the half holding the northern arc (right after turning)
            if (p[0] > 0) == (not south) and name in ("النسر الواقع", "العيوق", "الشعرى اليمانية", "قلب العقرب", "رجل الجبار", "الفكة"):
                pointer(F, p, (0, 0), size=0.06, kind="con")
                F.text((p[0], p[1] - 0.05), name, size=7.5)
    return F.save(out)

def fig33(out):
    F = Fig(6.0, 6.0)
    outside = set()
    mixed_rete(F, outside, rot=0, size=8)
    check_rete(F, outside, "الآسي")
    F.circle((0, 0), 0.92, "con", lw=0.8)
    F.line((-0.92, 0), (-0.66, 0), "con"); F.line((0.66, 0), (0.92, 0), "con")
    # the supports of the outer ring as on f.36v: two arched bars above and below
    for sgn in (1, -1):
        F.arc((0, 0), 0.72, 25 if sgn > 0 else 205, 155 if sgn > 0 else 335, "con", lw=0.8)
        F.arc((0, 0), 0.8, 25 if sgn > 0 else 205, 155 if sgn > 0 else 335, "con", lw=0.8)
        for a in ((40, 65, 90, 115, 140) if sgn > 0 else (220, 245, 270, 295, 320)):
            pointer(F, pol(0.72, a), pol(0.6, a), size=0.06, kind="con", fill=False)
    for a in (0, 90, 180, 270):
        F.arc(pol(0.96, a), 0.07, a + 90, a + 270, "con", lw=0.8)
    return F.save(out)

def fig34(out):
    F = Fig(6.0, 6.0)
    outside = {LIB, SCO, SGR, CAN, LEO, VIR}
    mixed_rete(F, outside, rot=90, size=8.5)
    check_rete(F, outside, "المسرطن")
    F.line((-1, 0), (1, 0), "con", lw=0.8); F.line((0, 1), (0, 0.07), "con", lw=0.8)
    return F.save(out)

SIJZI = [
    ("الثوري", {PIS, ARI, VIR, LIB}),
    ("البوري", {TAU, GEM, CAN, SGR, CAP, AQR, VIR, LIB}),
    ("الباطي", {AQR, PIS, ARI, TAU, LEO, VIR, LIB, SCO}),
    ("الصدفي (؟)", {TAU, GEM, CAN, LEO, SCO, SGR, CAP, AQR}),
    ("السلحفي", {TAU, LEO, SCO, AQR}),
    ("الجاموسي", {TAU, GEM, CAN, SGR, CAP, AQR}),
]

def fig35(out):
    F = Fig(11, 7.6)
    pos = [(0, 0), (2.5, 0), (5.0, 0), (7.5, 0), (2.5, -2.55), (5.0, -2.55)]
    pos = [(7.6, 0.0), (0.0, 1.3), (2.5, 1.3), (5.0, 1.3), (1.25, -1.3), (3.75, -1.3)]
    for (name, outside), c in zip(SIJZI, pos):
        mixed_rete(F, outside, rot=-90, c=c, s=1.0, size=6.3, w=0.09)
        check_rete(F, outside, name)
        F.text((c[0], c[1] + 1.12), name, size=13)
    # the fittings legible on the page: ring of البوري, bar and rings of the fourth, horns of الجاموسي
    c = pos[1]; F.circle((c[0], c[1] + 0.82), 0.13, "con"); F.line((c[0] - 0.22, c[1] + 0.97), (c[0], c[1] + 0.55), "con"); F.line((c[0] + 0.22, c[1] + 0.97), (c[0], c[1] + 0.55), "con")
    c = pos[3]; F.line((c[0], c[1] + 0.85), (c[0], c[1] - 0.85), "con"); F.circle((c[0], c[1] + 0.92), 0.08, "con"); F.circle((c[0], c[1] - 0.92), 0.08, "con")
    c = pos[5]
    for sy in (1, -1):
        F.line((c[0] - 0.12, c[1] + sy * 0.99), (c[0], c[1] + sy * 0.62), "con"); F.line((c[0] + 0.12, c[1] + sy * 0.99), (c[0], c[1] + sy * 0.62), "con")
    F.circle((c[0] - 0.42, c[1]), 0.16, "con"); F.circle((c[0] + 0.42, c[1]), 0.16, "con")
    c = pos[4]; F.circle((c[0], c[1] + 0.9), 0.07, "con")
    return F.save(out)

FIGS = {31: fig31, 33: fig33, 34: fig34, 35: fig35}

def fig32(out, phi=22.0):
    F = Fig(5.8, 5.8)
    P = Plate(1.0)
    E = (0, 0)
    F.circle(E, 1.0, "con", lw=1.0); F.circle(E, P.Re, "con", lw=0.8); F.circle(E, P.r_decl(EPS), "con", lw=0.8)
    F.line((-1, 0), (1, 0), "con", lw=0.8); F.line((0, -1), (0, 1), "con", lw=0.8)
    for h in range(-84, 90, 6):
        c, r = P.almucantar(phi, h)
        F.arc_clip(c, r, inside=[(E, 1.0)], kind="con", lw=1.3 if h == 0 else 0.65)
    c0, r0 = P.almucantar(phi, 0)
    cm = (c0[0], -c0[1])
    F.arc_clip(cm, r0, inside=[(E, 1.0)], kind="dot", lw=1.4)
    pts = circle_circle(c0, r0, cm, r0)
    F.check("the two horizons cut each other where the equator meets the east-west line",
            all(abs(abs(p[0]) - P.Re) < 1e-9 and abs(p[1]) < 1e-9 for p in pts))
    cd, rd = P.almucantar(phi, -18); cs, rs = P.almucantar(-phi, 18)
    return F.save(out)

def ruler_point(lam, north_proj, Re):
    d = decl(lam); a = ra(lam) - 180
    r = Re * cosd(d) / (1 + sind(d)) if north_proj else Re * cosd(d) / (1 - sind(d))
    return pol(r, a)

def fig36(out):
    F = Fig(5.6, 5.0)
    E = (0, 0)
    t = tand(45 - EPS / 2)
    A = (-1, 0); Dd = (0, 1); G = (0, -1); B = pol(1, 180 + EPS)
    F.circle(E, 1.0, "fin")
    H = line_inter(G, B, (0, 0), (1, 0)); T = line_inter(Dd, B, (0, 0), (1, 0))
    F.close_enough("ه ح = Capricorn of the first ruler = tan(45° + ε/2)", -H[0], tand(45 + EPS / 2))
    F.close_enough("ه ط = Cancer of the first ruler = tan(45° − ε/2)", -T[0], t)
    rt = -T[0]
    F.circle(E, rt, "con")
    K = (0, rt); L = pol(rt, 180 + EPS)
    M = line_inter(K, L, (0, 0), (1, 0)); rm = -M[0]
    F.close_enough("ه م = equator of the second ruler = tan²(45° − ε/2)", rm, t * t)
    F.circle(E, rm, "con")
    Fq = (0, rm); S = pol(rm, 180 + EPS)
    Ain = line_inter(Fq, S, (0, 0), (1, 0))
    F.line(H, (1.05, 0), "fin", lw=0.7); F.line((0, -1.03), (0, 1.03), "fin", lw=0.7)
    F.line(G, H, "con"); F.line(Dd, B, "con"); F.line(K, M, "con"); F.line(Fq, Ain, "con")
    F.line(E, B, "con", lw=0.6)
    for p, s, d in [(A, "ا", (-.03, .07)), (B, "ب", (-.05, -.06)), (G, "ج", (0, -.08)), (Dd, "د", (0, .08)),
                    (E, "ه", (.05, -.06)), (H, "ح", (-.07, 0)), (T, "ط", (.0, .07)), (K, "ك", (.06, .03)),
                    (L, "ل", (-.03, -.07)), (M, "م", (.0, .07)), (Fq, "ف", (.06, .03)), (S, "س", (-.04, -.06)),
                    (Ain, "ع", (.03, .07))]:
        F.lab(p, s, d)
    return F.save(out)

def sijzi_curve(rot=90):
    """The anemone rete as one closed curve (scaled so that the rim, Capricorn of the first ruler, is 1)."""
    t = tand(45 - EPS / 2)
    k = 1 / tand(45 + EPS / 2)          # scale: equator of the first ruler -> k
    Re1 = 1.0 * k; Re2 = t * t * k
    segs = [((0, 90), True, Re1), ((90, 180), False, Re2), ((180, 270), True, Re2), ((270, 360), False, Re1)]
    out = []
    for (l0, l1), nproj, Re in segs:
        lams = np.linspace(l0, l1, 181)
        out.append([rot_pt(ruler_point(l, nproj, Re), rot) for l in lams])
    return out, Re1, Re2, t * k

def fig37(out):
    F = Fig(6.0, 6.0)
    E = (0, 0)
    segs, Re1, Re2, C1 = sijzi_curve(90)
    F.circle(E, 1.0, "con", lw=1.0); F.circle(E, 0.94, "con", lw=0.8)
    names = [(0, "الربيع"), (1, "الصيف"), (2, "الخريف"), (3, "الشتاء")]
    w = 0.06
    for i, seg in enumerate(segs):
        xs, ys = zip(*seg); F.curve(xs, ys, "con", lw=1.0)
        cc, rr = circle3(seg[0], seg[90], seg[-1])
        inner = [pol(rr - w, ang(p, cc), cc) for p in seg]
        xs, ys = zip(*inner); F.curve(xs, ys, "con", lw=0.9)
        for j in range(0, 181, 60):
            F.line(seg[j], inner[j], "con", lw=0.8)
        for j in range(30, 181, 60):
            m = pol(rr - w * 0.55, ang(seg[j], cc), cc)
            F.rtext(m, SIGN_ABBR[(i * 3 + j // 60) % 12], ang(m, cc), size=7.5)
    F.check("the quarters join: Aries on the first equator", abs(dist(segs[0][0], E) - Re1) < 1e-9 and abs(dist(segs[3][-1], E) - Re1) < 1e-9)
    F.check("at the solstices the first ruler's Cancer meets the second ruler's Capricorn",
            abs(dist(segs[0][-1], E) - dist(segs[1][0], E)) < 1e-9 and abs(dist(segs[2][-1], E) - dist(segs[3][0], E)) < 1e-9)
    F.check("at Libra both second-ruler arcs meet on the second equator", abs(dist(segs[1][-1], E) - Re2) < 1e-9)
    F.circle(E, 0.06, "con"); F.line((-0.94, 0), (0.94, 0), "con", lw=0.7); F.line((0, -0.94), (0, 0.94), "con", lw=0.7)
    # the circle above the rete and the rim cusps, as on f.39v
    F.circle((0, 0.72), 0.2, "con", lw=0.8)
    for a in (90, 270):
        F.arc(pol(0.97, a), 0.08, a + 90, a + 270, "con", lw=0.8)
    for a in range(0, 360, 30):
        if a % 90: pointer(F, pol(0.94, a), pol(0.8, a), size=0.05, kind="con", fill=False)
    return F.save(out)

def fig38(out, phi=36.0):
    F = Fig(10, 5.0)
    t = tand(45 - EPS / 2)
    Re1, C1, Re2 = 1.0, t, t * t
    for cx, matched, title in [(2.3, True, "المقنطرات المتكافئة"), (0, False, "المقنطرات غير المتكافئة")]:
        c = (cx, 0)
        for r in (Re1, C1, Re2):
            F.circle(c, r, "con", lw=1.0 if r == Re1 else 0.8)
        F.circle(c, 1.05, "con", lw=0.8)
        F.line((cx - 1.05, 0), (cx + 1.05, 0), "con", lw=0.8); F.line((cx, -1.05), (cx, 1.05), "con", lw=0.8)
        for Re, r_in, r_out, ruler in [(Re1, C1, Re1, 1), (Re2, 0, C1, 2)]:
            yc = Re / tand(phi); rr = Re / sind(phi)
            for s in (1, -1):
                hc = (cx, s * yc)
                t_ = np.linspace(0, 2 * math.pi, 2000)
                x = hc[0] + rr * np.cos(t_); y = hc[1] + rr * np.sin(t_)
                rho = np.hypot(x - cx, y)
                ok = (rho >= r_in) & (rho <= r_out)
                if matched:
                    # one kind on each side, exchanged between the two rulers
                    side = (x < cx) if (s == 1) == (ruler == 1) else (x > cx)
                    ok &= side
                F.curve_clip(x, y, ok, "dot", lw=1.6)
            F.check(f"ruler {ruler}: northern and southern horizons cut each other on its equator",
                    abs(math.hypot(Re, 0) - Re) < 1e-12)
        F.text((cx, 1.15), title, size=12)
    return F.save(out)

def fig39(out, phi=33.0, phi2=45.0):
    F = Fig(9.0, 5.0)
    P = Plate(1.0)
    E = (0, 0)
    F.circle(E, 1.0, "con", lw=1.0); F.circle(E, P.Re, "con", lw=0.8); F.circle(E, P.r_decl(EPS), "con", lw=0.8)
    F.line((-1, 0), (1, 0), "con", lw=0.8); F.line((0, -1), (0, 1), "con", lw=0.8)
    from ch3 import ecliptic_ring
    ecliptic_ring(F, P, kind="fin", width=0.09)
    # the solid horizon drawn apart: the lune between the horizons of 33° and 45°
    ox = 2.45
    c1, r1 = P.almucantar(phi, 0); c2, r2 = P.almucantar(phi2, 0)
    T = lambda p: (p[0] + ox, p[1])
    pts = []
    for (c, r) in ((c1, r1), (c2, r2)):
        a0 = ang((-P.Re, 0), c); a1 = ang((P.Re, 0), c)
        ts = np.linspace(a0, a1 + (360 if a1 < a0 else 0), 200) if False else np.linspace(a0 % 360, a1 % 360 if a1 % 360 > a0 % 360 else a1 % 360 + 360, 200)
        arc_pts = [T(pol(r, a, c)) for a in ts]
        # keep the lower arc (through the north point)
        if min(p[1] for p in arc_pts) > -0.01:
            ts = np.linspace(a1 % 360, a0 % 360 + 360 if a0 % 360 < a1 % 360 else a0 % 360, 200)
            arc_pts = [T(pol(r, a, c)) for a in ts]
        xs, ys = zip(*arc_pts); F.curve(xs, ys, "con", lw=1.1)
    F.check("both horizons pass through the east and west points", abs(dist(c1, (P.Re, 0)) - r1) < 1e-9 and abs(dist(c2, (P.Re, 0)) - r2) < 1e-9)
    hub = T(E)
    F.circle(hub, 0.07, "con"); F.circle(hub, 0.035, "con")
    n1 = T((0, c1[1] - r1))
    F.line((hub[0] - 0.02, hub[1] - 0.07), (hub[0] - 0.02, n1[1]), "con"); F.line((hub[0] + 0.02, hub[1] - 0.07), (hub[0] + 0.02, n1[1]), "con")
    F.line((hub[0] - 0.025, hub[1] + 0.07), (hub[0] - 0.025, 0.95), "con"); F.line((hub[0] + 0.025, hub[1] + 0.07), (hub[0] + 0.025, 0.95), "con")
    F.text((hub[0] + 0.15, 0.6), "العمود", size=11, rot=-90)
    # the two vanes on one day-circle (that of Cancer)
    rc = P.r_decl(EPS)
    for s, nm in ((-1, "لبنة"), (1, "هدفة")):
        q = [p for p in circle_circle(c1, r1, E, rc) if p[1] < 0.2]
        p = T(min(q, key=lambda z: s * -z[0]))
        F.poly([(p[0], p[1] - 0.06), (p[0] + 0.05, p[1]), (p[0], p[1] + 0.06), (p[0] - 0.05, p[1])], "con", closed=True)
        F.text((p[0] + s * 0.05, p[1] + 0.15), nm, size=11)
    F.text((hub[0] + 0.12, hub[1] - 0.12), "فلس", size=11)
    F.text((ox, -0.75), "الأفق المجسم", size=12)
    return F.save(out)

def fig40(out):
    F = Fig(5.6, 5.6)
    P = Plate(1.0)
    E = (0, 0)
    F.circle(E, 0.12, "con", lw=1.0); F.circle(E, 0.07, "con", lw=0.9)
    pairs = [(21, 33), (24, 36), (27, 39), (30, 42)]
    for q, (a, b) in enumerate(pairs):
        rot = 90 * q
        R = lambda p: rot_pt(p, rot)
        arcs = []
        for phi in (a, b):
            c, r = P.almucantar(phi, 0)
            nth = (0, c[1] - r); W = (P.Re, 0)
            a0 = ang(nth, c); a1 = ang(W, c)
            ts = np.linspace(a0, a1 if a1 > a0 else a1 + 360, 120)
            arcs.append([R(pol(r, t, c)) for t in ts])
            F.check(f"horizon {phi}° runs from the north point to the west point", abs(dist(c, W) - r) < 1e-9) if q == 0 else None
        for ar_ in arcs:
            xs, ys = zip(*ar_); F.curve(xs, ys, "con", lw=1.0)
        F.line(arcs[0][0], arcs[1][0], "con")
        # bar from the hub to the piece, along the meridian
        F.line(R((-0.02, -0.12)), R((-0.02, arcs and -P.almucantar(a, 0)[1] * 0 + (P.almucantar(a, 0)[0][1] - P.almucantar(a, 0)[1]))), "con", lw=0.8)
        F.line(R((0.02, -0.12)), R((0.02, P.almucantar(b, 0)[0][1] - P.almucantar(b, 0)[1])), "con", lw=0.8)
        m1 = arcs[0][70]; m2 = arcs[1][70]
        F.rtext(pol(dist(m1, E) - 0.08, ang(m1)), f"لعرض {abjad(a)}", ang(m1), size=10)
        F.rtext(pol(dist(m2, E) + 0.08, ang(m2)), f"لعرض {abjad(b)}", ang(m2), size=10)
    return F.save(out)

def fig41(out):
    F = Fig(10, 3.0)
    P = Plate(1.0)
    E = (0, 0)
    w = 0.13
    for r in sorted(set(round(P.r_decl(decl(l)), 9) for l in range(0, 360, 30))):
        for side in (1, -1):
            a0 = 90 - math.degrees(math.asin(min(1, 0.3 / r))) if side > 0 else 270 - math.degrees(math.asin(min(1, 0.3 / r)))
            F.arc(E, r, -math.degrees(math.asin(min(1, 0.3 / r))) + (0 if side > 0 else 180),
                  math.degrees(math.asin(min(1, 0.3 / r))) + (0 if side > 0 else 180), "aux", lw=0.5)
    F.circle(E, 0.07, "con", lw=1.0); F.circle(E, 0.035, "con", lw=0.9)
    # right half above the fiducial edge: Capricorn ... Gemini; left half below it: Cancer ... Sagittarius
    for side, l0 in ((1, 270), (-1, 90)):
        y0, y1 = (0, w) if side == 1 else (0, -w)
        F.poly([(side * 0.07, y0), (side * 1.0, y0), (side * 1.1, y1), (side * 0.07, y1)], "con", lw=0.9, closed=True)
        for k in range(6):
            la, lb = l0 + 30 * k, l0 + 30 * (k + 1)
            ra_, rb = P.r_decl(decl(la % 360)), P.r_decl(decl(lb % 360))
            F.line((side * ra_, y0), (side * ra_, y1), "con", lw=0.9)
            if k == 5: F.line((side * rb, y0), (side * rb, y1), "con", lw=0.9)
            for d in range(2, 30, 2):
                r = P.r_decl(decl((la + d) % 360))
                F.line((side * r, y0), (side * r, y0 + (y1 - y0) * (0.35 if d % 10 else 0.5)), "redthin")
            rm = P.r_decl(decl((la + 15) % 360))
            F.text((side * rm, y0 + (y1 - y0) * 0.72), SIGN_ABBR[(la % 360) // 30], size=8.5, rot=90)
    F.check("Capricorn and Sagittarius (equal declination) fall at the same distance on the two halves",
            abs(P.r_decl(decl(300)) - P.r_decl(decl(240))) < 1e-12)
    return F.save(out)

def fig42(out):
    F = Fig(7.2, 5.0)
    PN = Plate(1.0); PS = Plate(1.0, south=True)
    Re = PN.Re
    E = (0, 0)
    xmax = math.sqrt(1 - Re * Re)
    y = Re
    F.arc(E, Re, 60, 120, "aux", lw=0.5)
    # the strip under the tangent line: degrees, and two rows of sign names
    h1, h2, h3 = 0.05, 0.13, 0.21
    for yy in (y, y - h1, y - h2, y - h3):
        F.line((-xmax, yy), (xmax, yy), "con", lw=0.8)
    F.line((-xmax, y), (-xmax, y - h3), "con"); F.line((xmax, y), (xmax, y - h3), "con")
    xs_check = []
    for lam in range(0, 91):
        for side, P_, l_top, l_bot in ((-1, PS, lam, 180 - lam), (1, PN, 360 - lam, 180 + lam)):
            d = decl(l_top)
            r = P_.r_decl(d)
            x = side * math.sqrt(max(0, r * r - Re * Re))
            if lam % 30 == 0:
                F.line((x, y), (x, y - h3), "con", lw=0.8)
            elif lam % 2 == 0:
                F.line((x, y), (x, y - (0.03 if lam % 10 else h1)), "redthin")
            if lam == 30: xs_check.append(abs(x))
    for i in range(3):
        for side in (-1, 1):
            lam_mid = 15 + 30 * i
            P_ = PS if side < 0 else PN
            r = P_.r_decl(decl(lam_mid) * (1 if side < 0 else -1) * (1 if side < 0 else 1) if side < 0 else -decl(lam_mid))
            r = P_.r_decl(decl(lam_mid)) if side < 0 else PN.r_decl(-decl(lam_mid))
            x = side * math.sqrt(r * r - Re * Re)
            top = [["الحمل", "الثور", "الجوزاء"], ["الحوت", "الدلو", "الجدي"]][side > 0][i]
            bot = [["السنبلة", "الأسد", "السرطان"], ["الميزان", "العقرب", "القوس"]][side > 0][i]
            F.text((x, y - (h1 + h2) / 2), top, size=9); F.text((x, y - (h2 + h3) / 2), bot, size=9)
    F.check("the two halves are symmetric: equal declinations at equal distances", abs(xs_check[0] - xs_check[1]) < 1e-9)
    # the bar along the meridian divided into the parts of the greatest declination
    bw = 0.05
    F.poly([(-bw, y), (-bw, 1.0), (bw, 1.0), (bw, y)], "con", lw=0.9)
    for d in range(0, 24, 1):
        r = PN.r_decl(-d)
        F.line((-bw if d % 5 else -bw, r), (bw if d % 5 == 0 else 0, r), "redthin" if d % 5 else "con")
        if d % 5 == 0 and d:
            F.text((bw + 0.05, r), abjad(d), size=8)
    F.line((-0.015, y - h3), (-0.015, 0.06), "con"); F.line((0.015, y - h3), (0.015, 0.06), "con")
    F.circle(E, 0.06, "con"); F.circle(E, 0.025, "con")
    return F.save(out)

def fig43(out):
    F = Fig(5.6, 5.6)
    P = Plate(1.0)
    E = (0, 0)
    seq = [(270, 90), (300, 180), (330, 270), (0, 360), (30, 450), (60, 540), (90, 630)]   # (λ, angle)
    pts = []
    for lam, a in seq:
        r = P.r_decl(decl(lam))
        F.circle(E, r, "con", lw=0.7)
        pts.append(pol(r, a))
    F.line((-1.05, 0), (1.05, 0), "con", lw=0.7); F.line((0, -1.05), (0, 1.05), "con", lw=0.7)
    names = ["ط", "ي", "ز", "د", "ا", "ب", "ج"]
    for i in range(6):
        P1, P2 = pts[i], pts[i + 1]
        n1 = dist(P1, E); n2 = dist(P2, E)
        u = (n1 * n1 - n2 * n2) / (2 * n1)
        C = pol(u, ang(P1))
        r = n1 - u
        F.check(f"quarter {i+1} passes through both ends", abs(dist(C, P2) - r) < 1e-9) if i < 2 else None
        a0 = ang(P1, C); a1 = ang(P2, C)
        F.arc(C, r, a0, a1 if a1 > a0 else a1 + 360, "fin", lw=1.4)
    for p, s in zip(pts, names):
        F.lab(p, s, pol(0.07, ang(p) + 25), size=12, dotit=True)
    return F.save(out)

FIGS.update({32: fig32, 36: fig36, 37: fig37, 38: fig38, 39: fig39, 40: fig40, 41: fig41, 42: fig42, 43: fig43})
