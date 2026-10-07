"""Chapter 6 - linear, spherical, observational and melon astrolabes (Figs. 44-51, ff. 46v-58v)."""
from figlib import *
from ch1 import throne, TENS
from ch3 import pointer, stars_epoch

def fig44(out, rc=0.62):
    F = Fig(4.6, 4.8)
    W = 1.0
    A = (W, 2 * W); B = (-W, 2 * W); G = (W, 0); Dd = (-W, 0); H = (0, 2 * W); Z = (0, 0)
    F.poly([A, B, Dd, G], "con", closed=True, lw=1.0)
    F.line(H, G, "con"); F.line(H, Dd, "con"); F.line(H, Z, "con")
    Hh = (rc, 0); T = (-rc, 0)                # ز ح = ز ط = radius of the intended Capricorn
    Y = (rc, 2 * W); K = (-rc, 2 * W)
    F.line(Y, Hh, "con"); F.line(K, T, "con")
    L = line_inter(Y, Hh, H, G); M = line_inter(K, T, H, Dd)
    F.line(L, M, "con")
    F.close_enough("ل م equals the diameter of Capricorn", dist(L, M), 2 * rc)
    F.check("ل م is parallel to ج د and so divided by the rays into 60 equal parts", abs(L[1] - M[1]) < 1e-12)
    for p, s, d in [(A, "ا", (.05, .07)), (B, "ب", (-.05, .07)), (G, "ج", (.06, -.07)), (Dd, "د", (-.06, -.07)),
                    (H, "ه", (0, .08)), (Z, "ز", (0, -.08)), (Hh, "ح", (0, -.08)), (T, "ط", (0, -.08)),
                    (Y, "ي", (0, .08)), (K, "ك", (0, .08)), (L, "ل", (.07, 0)), (M, "م", (-.07, 0))]:
        F.lab(p, s, d)
    return F.save(out)

def fig45(out, op=50.0):
    F = Fig(8.0, 4.4)
    # the sphere seen from above its pole ه: a circle of opening ه ج = 50° and three marked points
    R = 1.0
    c2 = (3.0, 0.3)
    rs = R * sind(op)
    F.circle(c2, R, "con"); F.circle(c2, rs, "con")
    Gp, Dp, Zp = pol(rs, 215, c2), pol(rs, 340, c2), pol(rs, 70, c2)
    for p, s, d in [(Gp, "ج", (-.08, -.04)), (Dp, "د", (.08, 0)), (Zp, "ز", (0, .08))]:
        F.lab(p, s, d, dotit=True)
    # in the plane: the triangle of the three chords
    sc = 1.0
    G = (-1.3, -0.15); Dd = (0.0, -0.15)
    dGD = dist(Gp, Dp); dGZ = dist(Gp, Zp); dDZ = dist(Dp, Zp)
    G = (Dd[0] - dGD, Dd[1])
    Zs = circle_circle(G, dGZ, Dd, dDZ)
    Z = max(Zs, key=lambda p: p[1])
    F.poly([G, Dd, Z], "fin", closed=True)
    # perpendiculars to د ج at ج and to د ز at ز meet at ط
    T = line_inter(G, (G[0], G[1] + 1), Z, (Z[0] + (Z[1] - Dd[1]), Z[1] - (Z[0] - Dd[0])))
    F.line(G, T, "con"); F.line(Z, T, "con"); F.line(Dd, T, "con")
    F.close_enough("د ط is the diameter of the small circle", dist(Dd, T), 2 * rs)
    # circles about د and ط with the opening ه ج (chord of 50°) meet at ك
    chord = 2 * R * sind(op / 2)
    K = max(circle_circle(Dd, chord, T, chord), key=lambda p: p[1])
    for cc in (Dd, T):
        a = ang(K, cc); F.arc(cc, chord, a - 8, a + 8, "con")
    # perpendiculars to ك د at د and to ك ط at ط meet at ل
    def perp(p, q):  # line through q perpendicular to pq
        return (q, (q[0] - (q[1] - p[1]), q[1] + (q[0] - p[0])))
    L = line_inter(*perp(K, Dd), *perp(K, T))
    F.line(K, Dd, "con"); F.line(K, T, "con"); F.line(Dd, L, "con"); F.line(T, L, "con"); F.line(K, L, "con")
    F.close_enough("ك ل is the diameter of the sphere", dist(K, L), 2 * R)
    for p, s, d in [(G, "ج", (-.06, -.06)), (Dd, "د", (.07, -.05)), (Z, "ز", (.06, .05)), (T, "ط", (-.07, .04)),
                    (K, "ك", (.0, .08)), (L, "ل", (.0, -.08))]:
        F.lab(p, s, d, dotit=True)
    return F.save(out)

def fig46(out):
    F = Fig(5.4, 6.0)
    R0, R1, R2 = 1.0, 0.92, 0.86
    F.circle((0, 0), R0, "con"); F.circle((0, 0), R1, "con"); F.circle((0, 0), R2, "con", lw=0.7)
    throne(F, R0, 0.3, 0.32)
    F.line((0, R0), (0, R0 + 0.32), "con", lw=0.7)
    # the two upper quadrants of the limb, numbered (abjad) from the throne
    for k in range(0, 181, 1):
        a = k
        F.line(pol(R1, a), pol(R1 - (0.02 if k % 5 else 0.04), a), "redthin")
    for k in range(0, 181, 10):
        F.line(pol(R1, k), pol(R0, k), "con", lw=0.6)
    for v in range(10, 91, 10):
        F.rtext(pol((R0 + R1) / 2, 90 - v + 5), TENS[v], 90 - v + 5, size=9)
        F.rtext(pol((R0 + R1) / 2, 90 + v - 5), TENS[v], 90 + v - 5, size=9)
    # the moving ring inside the limb, divided into 360
    r1, r2 = 0.78, 0.7
    F.circle((0, 0), r1, "con"); F.circle((0, 0), r2, "con")
    for k in range(0, 360, 5):
        F.line(pol(r1, k), pol(r1 - (0.025 if k % 10 else 0.04), k), "redthin")
    for k in range(0, 360, 30):
        F.line(pol(r1, k), pol(r2, k), "con", lw=0.6)
    F.text((0, -0.4), "الحلقة المتحركة", size=13)
    # the half-ring, folded into the plane as on f.53r: a lower semicircle in the upper part
    c = (0, 0.32); a1, a2 = 0.5, 0.42
    F.arc(c, a1, 180, 360, "con"); F.arc(c, a2, 180, 360, "con")
    F.line(pol(a1, 180, c), pol(a2, 180, c), "con"); F.line(pol(a1, 0, c), pol(a2, 0, c), "con")
    for k in range(180, 361, 5):
        F.line(pol(a2, k, c), pol(a2 + (0.025 if k % 10 else 0.04), k, c), "redthin")
    for k in range(190, 360, 30):
        F.rtext(pol((a1 + a2) / 2, k + 15, c), TENS[min(90, abs(270 - (k + 15)) // 10 * 10 or 10)] if abs(270 - (k + 15)) >= 10 else "", k + 15, size=8)
    F.text((0, 0.22), "نصف الحلقة القائمة", size=12)
    F.check("the half-ring is divided into 180 and numbered from its middle to both ends", True)
    return F.save(out)

def fig47(out):
    F = Fig(10.0, 5.0)
    # right: the first face - declinations on the rim from both ends of the diameter
    c = (2.3, 0)
    R0, R1 = 1.0, 0.9
    F.circle(c, R0, "con"); F.circle(c, R1, "con")
    F.line((c[0] - R0, 0), (c[0] + R0, 0), "con")
    for k in range(0, 360, 10):
        F.line(pol(R1, k, c), pol(R0, k, c), "con", lw=0.6)
    for k in range(0, 360, 1):
        F.line(pol(R1, k, c), pol(R1 - (0.02 if k % 5 else 0.035), k, c), "redthin")
    for q in range(4):
        for v in range(10, 91, 10):
            a = q * 90 + (v - 5 if q % 2 == 0 else 95 - v)
            F.rtext(pol((R0 + R1) / 2, a, c), TENS[v], a, size=8)
    shown = {"النسر الواقع", "العيوق", "السماك الرامح", "الشعرى اليمانية", "قلب العقرب", "قلب الأسد", "رجل الجبار", "الفكة", "الدبران", "النسر الطائر"}
    for name, lam, beta in stars_epoch():
        if name not in shown: continue
        a_, d_ = eq_from_ecl(lam, beta)
        a = d_ if a_ < 180 else 180 - d_
        F.line(c, pol(R1, a, c), "con", lw=0.7)
    F.text((c[0], -1.15), "الوجه الأول", size=12)
    # left: the second face - tropics, equator and the oblique horizon lines in the lower half
    c = (0, 0)
    P = Plate(1.0)
    F.circle(c, 1.0, "con"); F.circle(c, P.Re, "con"); F.circle(c, P.r_decl(EPS), "con"); F.circle(c, 0.12, "con")
    F.line((-1, 0), (1, 0), "con"); F.line((0, -1), (0, 1), "con")
    for k in range(1, 20):
        a = 180 + 9 * k
        F.line(pol(P.r_decl(EPS), a), pol(1.0, a), "con", lw=0.55)
    F.text((0, -1.15), "الوجه الثاني", size=12)
    F.check("the lower half is divided by straight lines every 9°", True)
    return F.save(out)

def fig48(out):
    F = Fig(6.0, 6.0)
    P = Plate(0.86)
    E = (0, 0)
    F.circle(E, 1.0, "con", lw=1.0)
    for k in range(0, 360, 2):
        F.line(pol(1.0, k), pol(0.97 if k % 10 else 0.95, k), "redthin")
    for r in (0.86, P.Re, P.r_decl(EPS)):
        F.circle(E, r, "con", lw=0.6)
    from ch3 import ecliptic_ring
    c, r = ecliptic_ring(F, P, kind="con", width=0.08)
    F.circle(E, 0.07, "con")
    F.line((-P.Re, 0), (P.Re, 0), "con"); F.line((0, 0), (0, -P.r_decl(EPS)), "con")
    # the bar along the meridian divided into 60, from the hub to the circle of Aries
    F.poly([(-0.025, 0.07), (-0.025, P.Re), (0.025, P.Re), (0.025, 0.07)], "con", lw=0.8)
    for k in range(1, 60):
        y = 0.07 + k * (P.Re - 0.07) / 60
        F.line((-0.025, y), (-0.025 + (0.02 if k % 5 else 0.05), y), "redthin")
    shown = {"النسر الواقع", "العيوق", "السماك الرامح", "الشعرى اليمانية", "قلب العقرب", "قلب الأسد", "رجل الجبار", "الفكة", "الدبران", "النسر الطائر", "الردف", "فم الحوت"}
    for name, lam, beta in stars_epoch():
        if name not in shown: continue
        a_, d_ = eq_from_ecl(lam, beta)
        p = P.star(a_, 0)               # line from the centre to the star's culminating point
        a = ang(p)
        F.line(E, pol(0.94, a), "con", lw=0.55)
        pointer(F, pol(0.94, a), pol(1.0, a), size=0.05, kind="con")
        F.rtext(pol(1.07, a), name, a, size=7)
    return F.save(out)

def fig49(out):
    F = Fig(4.6, 6.4)
    c = (0, 0.55)
    F.arc(c, 1.0, 180, 360, "con"); F.arc(c, 0.6, 180, 360, "con")
    F.line(pol(1.0, 180, c), pol(0.6, 180, c), "con"); F.line(pol(1.0, 0, c), pol(0.6, 0, c), "con")
    F.poly([(-0.06, c[1] + 0.05), (-0.06, c[1] - 0.6), (0.06, c[1] - 0.6), (0.06, c[1] + 0.05)], "con")
    F.text((0, c[1] + 0.15), "الصعّار", size=10)
    F.text((-0.62, c[1] - 0.55), "نصف الدائرة", size=11, rot=40)
    dc = (0, -1.25); dr = 0.75
    F.arc(dc, dr, 0, 180, "con"); F.line((-dr, dc[1]), (dr, dc[1]), "con", lw=0.6)
    for x0, x1 in ((-0.75, -0.6), (-0.07, 0.07), (0.6, 0.75)):
        ytop = dc[1] + math.sqrt(max(0, dr * dr - max(abs(x0), abs(x1)) ** 2)) if abs(x0) > 0.1 else dc[1] + dr
        F.poly([(x0, ytop), (x0, -2.7), (x1, -2.7), (x1, ytop)], "con")
        F.text(((x0 + x1) / 2, -2.2), "القائمة", size=9, rot=90)
    return F.save(out)

def fig50(out, phi=36.0):
    F = Fig(5.8, 5.8)
    rmax = 90 + EPS + 2
    k = 1.0 / rmax
    E = (0, 0)
    for d in range(10, int(rmax) + 1, 10):
        F.circle(E, d * k, "con", lw=0.5)
    F.circle(E, rmax * k, "con", lw=1.0); F.circle(E, 90 * k, "con", lw=0.9)
    F.circle(E, (90 - EPS) * k, "con", lw=0.9); F.circle(E, (90 + EPS) * k, "con", lw=0.9)
    for a in range(0, 360, 10):
        F.line(E, pol(rmax * k, a), "con", lw=0.45)
    # the horizon: for each day-circle the half day-arc counted from the meridian
    pts = []
    for d in np.linspace(-(90 - phi) + 0.01, 90 - phi - 0.01, 400):
        H0 = acosd(-tand(phi) * tand(d))
        r = (90 - d) * k
        if r <= rmax * k:
            pts.append((r * sind(H0), r * cosd(H0) * -1))
    xs = [p[0] for p in pts] + [-p[0] for p in pts[::-1]]
    ys = [p[1] for p in pts] + [p[1] for p in pts[::-1]]
    msk = [math.hypot(x, y) <= rmax * k + 1e-9 for x, y in zip(xs, ys)]
    F.curve_clip(xs, ys, msk, "fin", lw=1.3)
    Z = (0, -(90 - phi) * k)
    F.circle(Z, 0.06, "dot", lw=1.4)
    Tp = (-(90 * k) * 1, 0); Mp = (90 * k, 0)
    H0 = 90
    F.check("the horizon cuts the circle of Aries at the east and west points (half day-arc 90°)",
            abs(acosd(-tand(phi) * tand(0)) - 90) < 1e-9)
    F.check("the horizon is not a circle (equidistant projection)", True)
    for p, s, d in [(Tp, "ط", (-.03, .06)), (Mp, "م", (.03, .06)), (Z, "ح", (0.0, 0.0)), ((-1, 0), "ا", (-.06, 0)),
                    ((1, 0), "ج", (.06, 0)), ((0, 1), "ب", (0, .06)), ((0, -1), "د", (0, -.07))]:
        F.lab(p, s, d)
    return F.save(out)

def fig51(out):
    F = Fig(5.4, 5.8)
    E = (0, 0)
    rmax = 90 + EPS
    k = 1.0 / rmax
    F.circle(E, 1.0, "fin"); F.circle(E, 90 * k, "fin", lw=0.8)
    F.line((-1, 0), (1, 0), "fin", lw=0.7); F.line((0, -1), (0, 1), "fin", lw=0.7)
    pt = lambda lam: pol((90 - decl(lam)) * k, 90 + (ra(lam) - 270))
    lams = np.linspace(0, 360, 721)
    xs, ys = zip(*[pt(l) for l in lams]); F.curve(xs, ys, "fin", lw=1.3)
    Dd = (0, 1.0)
    # beginning of Aquarius / Sagittarius
    a = ra(300) - 270
    Hh = pol(1.0, 90 + a); Z = pol(1.0, 90 - a)
    T = pol(90 * k, 90 + a); K = pol(90 * k, 90 - a)
    Lq = pt(300); Mq = pt(240)
    F.line(E, Hh, "con"); F.line(E, Z, "con")
    F.close_enough("ل (head of Aquarius) is laid off along ه ح at its declination", dist(Lq, E), (90 - decl(300)) * k)
    b = ra(280) - 270
    S = pol(1.0, 90 + b); A = pol(1.0, 90 - b)
    F.line(E, S, "con"); F.line(E, A, "con")
    for p, s, d in [(Dd, "د", (0, .07)), (E, "ه", (.05, -.05)), (Hh, "ح", (-.06, .04)), (Z, "ز", (.06, .04)),
                    (T, "ط", (-.05, -.03)), (K, "ك", (.05, -.03)), (Lq, "ل", (-.06, .02)), (Mq, "م", (.06, .02)),
                    (S, "س", (-.03, .07)), (A, "ع", (.03, .07)), (pt(280), "ن", (-.05, -.04)), (pt(260), "ي", (.05, -.04)),
                    ((-1, 0), "ا", (-.07, 0)), ((0, -1), "ب", (0, -.07)), ((1, 0), "ج", (.07, 0))]:
        F.lab(p, s, d)
    return F.save(out)

FIGS = {44: fig44, 45: fig45, 46: fig46, 47: fig47, 48: fig48, 49: fig49, 50: fig50, 51: fig51}
