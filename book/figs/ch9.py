"""Chapter 9 - the moon box, the eclipse plate and the visibility of the crescent (Figs. 79-85)."""
from figlib import *
from ch1 import TENS

def gear(F, c, n, r_pitch, kind="fin", lw=0.8, add=0.8, ded=0.95, rot=0.0, colorf=None):
    """Triangular teeth about the pitch circle (module 1: r_pitch = n/2)."""
    pts = []
    for k in range(n):
        a0 = rot + 360 * k / n
        pts.append(pol(r_pitch - ded, a0, c))
        pts.append(pol(r_pitch + add, a0 + 180 / n, c))
    pts.append(pts[0])
    xs, ys = zip(*pts)
    if colorf is None:
        F.curve(xs, ys, kind, lw=lw)
    else:
        ok = np.array([colorf(x, y) for x, y in pts])
        F.curve_clip(xs, ys, ~ok, "fin", lw=lw); F.curve_clip(xs, ys, ok, "con", lw=lw)
    return pts

def fig79(out):
    F = Fig(5.8, 5.8)
    n = 59; R = 29.5
    E = (0, 0)
    gear(F, E, n, R, "con", lw=0.8, rot=90)
    r_in = 26.0
    F.circle(E, r_in, "con", lw=0.9)
    for k in range(n):
        a = 90 + 360 * k / n + 180 / n
        F.line(pol(r_in, a), pol(R - 0.95, a), "redthin")
    F.line((-r_in, 0), (r_in, 0), "con", lw=0.8); F.line((0, -r_in), (0, r_in), "con", lw=0.8)
    rc = r_in * (math.sqrt(2) - 1); dc = r_in - rc
    for a, nm in ((90, "ع"), (0, "ر"), (270, "م"), (180, "ف")):
        F.circle(pol(dc, a), rc, "con", lw=0.9)
        F.text(pol(dc, a), nm, size=14)
    F.check("the four circles touch each other and the circle ح ط ك ل (r = (√2 − 1) · R)",
            abs(dist(pol(dc, 90), pol(dc, 0)) - 2 * rc) < 1e-9 and abs(dc + rc - r_in) < 1e-9)
    F.check("59 teeth: the wheel turns once in 59 days = two months of 30 and 29 days", 30 + 29 == 59)
    for p, s, d in [((0, R + 1.5), "ج", (0, 1.5)), ((R + 1.5, 0), "ب", (1.5, 0)), ((0, -R - 1.5), "ا", (0, -1.5)),
                    ((-R - 1.5, 0), "د", (-1.5, 0)), ((0, r_in), "ح", (1.2, -1.6)), ((r_in, 0), "ط", (-1.5, 1.4)),
                    ((0, -r_in), "ك", (1.2, 1.6)), ((-r_in, 0), "ل", (1.5, 1.4)), (E, "ه", (1.2, 1.2))]:
        F.lab(p, s, d, size=13)
    return F.save(out)

def fig80(out):
    F = Fig(6.6, 7.4)
    E = (0, 0)
    Rb = 90
    F.circle(E, Rb, "con", lw=1.0); F.circle(E, Rb + 4, "con", lw=1.0)
    c7 = pol(33, 60); c8 = pol(38, 126.2); cs = pol(36, -110, c8); cm = pol(25, -12)
    W = {  # name: (centre, teeth, layer, label)
        "10": (E, 10, 2, "ذات ١٠"), "7": (E, 7, 3, "ذات ٧"), "19": (c7, 19, 2, "ذات ١٩"), "59a": (c7, 59, 3, "ذات ٥٩"),
        "24": (c8, 24, 1, "ذات ٢٤"), "59b": (c8, 59, 2, "ذات ٥٩"), "48": (cs, 48, 1, "ذات ٤٨ للشمس"), "40": (cm, 40, 2, "ذات ٤٠ للقمر")}
    def covered(name):
        c0, n0, l0, _ = W[name]
        others = [(W[k][0], W[k][1] / 2) for k in W if W[k][2] > l0]
        return lambda x, y: any(math.hypot(x - c[0], y - c[1]) < r for c, r in others)
    for name in ("48", "24", "40", "59b", "19", "10", "59a", "7"):
        c, n, l, lab = W[name]
        gear(F, c, n, n / 2, lw=0.8, colorf=covered(name))
    for a, b in (("7", "59a"), ("19", "59b"), ("24", "48"), ("10", "40")):
        d = dist(W[a][0], W[b][0]); s = (W[a][1] + W[b][1]) / 2
        F.check(f"wheels {W[a][1]} and {W[b][1]} mesh: centre distance {d:.2f} = sum of pitch radii {s}", abs(d - s) < 0.05)
    # the new-moon windows of the seventh wheel (blackened)
    rc = 26 * (math.sqrt(2) - 1); dc = 26 - rc
    for a in (90, 270):
        cc = pol(dc, a, c7)
        t = np.linspace(0, 2 * math.pi, 80)
        F.fill(list(zip(cc[0] + rc * np.cos(t), cc[1] + rc * np.sin(t))), color="#111111", z=3)
    for name, off in (("59a", (0, -18)), ("59b", (-8, 18)), ("48", (0, -5)), ("40", (4, -4)), ("19", (0, 0)), ("24", (0, 0)), ("10", (0, -7.5))):
        c, n, l, lab = W[name]
        F.text((c[0] + off[0], c[1] + off[1]), lab, size=9)
    per7 = 59; per_sun = 59 * 59 / 19 * 48 / 24
    F.check(f"periods: 7th wheel {per7} days, moon wheel 28 days, sun wheel {per_sun:.1f} days", abs(per_sun - 366.4) < 0.1)
    F.text((0, -Rb - 13), "ما كان من هذه الدوائر بالسواد فهو ظاهر، وما كان بالحمرة فهو تحت غيره", size=10)
    return F.save(out)

def eclipse_points(R=1.0):
    s3 = math.sqrt(3)
    Z = pol(R, 120); H = pol(R, 30); G = (R, 0)
    T = line_inter(G, Z, (0, 0), H); K = line_inter(G, Z, (0, 0), (0, R))
    r = R / (2 * s3)
    M = (0, -dist((0, 0), K))
    return Z, H, G, T, K, M, r

def fig81(out):
    F = Fig(10, 5.0)
    R = 1.0; s3 = math.sqrt(3)
    # right: the construction
    cx = 2.4
    S = lambda p: (p[0] + cx, p[1])
    Z, H, G, T, K, M, r = eclipse_points()
    F.circle((cx, 0), R, "fin"); F.line(S((-R, 0)), S((R, 0)), "fin", lw=0.7); F.line(S((0, -R)), S((0, R)), "fin", lw=0.7)
    F.line(S(G), S(Z), "con"); F.line(S((0, 0)), S(Z), "con"); F.line(S((0, 0)), S(H), "con")
    for c in (K, T, M):
        F.circle(S(c), r, "fin", lw=0.9)
    F.check("circle ك (r = R/2√3) touches ه ز", abs(abs(K[0] * sind(120) - K[1] * cosd(120)) - r) < 1e-9)
    F.check("circles ك and ط touch each other", abs(dist(K, T) - 2 * r) < 1e-9)
    F.check("ه ط = ه م", abs(dist((0, 0), T) - dist((0, 0), M)) < 1e-9)
    ri = 1 / s3 - 1 / (2 * s3); ro = s3 / 2
    F.arc(S((0, 0)), ri, -90, 30, "con", lw=0.8); F.arc(S((0, 0)), ro, -90, 30, "con", lw=0.8)
    F.arc(S((0, 0)), 0.5, 120, 240, "con", lw=0.9)
    for k in range(25):
        a = 120 + 5 * k
        F.line(S(pol(0.5, a)), S(pol(0.5 - (0.04 if k % 12 else 0.07), a)), "con", lw=0.6)
    Pc = pol(0.5, 120); Q = pol(0.5, 180); Lc = pol(0.5, 240)
    F.check("ل (at 240°) lies on circle م", abs(dist(Lc, M) - r) < 1e-9)
    for p, s, d in [((-R, 0), "ا", (-.07, 0)), ((0, R), "ب", (0, .08)), (G, "ج", (.07, 0)), ((0, -R), "د", (0, -.08)),
                    ((0, 0), "ه", (.05, -.06)), (Z, "ز", pol(.08, 120)), (H, "ح", pol(.08, 30)), (T, "ط", (.07, .02)),
                    (K, "ك", (-.05, .05)), (M, "م", (.05, -.05)), (Pc, "ص", (-.06, .04)), (Q, "ق", (-.07, 0)), (Lc, "ل", (-.06, -.04)),
                    (pol(ri, 30), "ن", (.0, .07)), (pol(ri, -90), "س", (-.07, 0)), (pol(ro, 30), "ع", (.06, .05)), (pol(ro, -90), "ف", (-.07, 0))]:
        F.lab(S(p), s, d, size=11)
    F.text(S((0, -1.2)), "عمل الوجه الأول من الصفيحة", size=11)
    # left: the finished face
    E = (0, 0)
    F.circle(E, R, "fin"); F.line((-R, 0), (R, 0), "fin", lw=0.7); F.line((0, -R), (0, R), "fin", lw=0.7)
    t = np.linspace(-90, 30, 100)
    band = [pol(ro, a) for a in t] + [pol(ri, a) for a in t[::-1]]
    F.fill(band, color="#e3e6ea", z=0)
    for c in (T, M):
        tt = np.linspace(0, 2 * math.pi, 80)
        F.fill(list(zip(c[0] + r * np.cos(tt), c[1] + r * np.sin(tt))), color="#111111", z=3)
    F.circle(K, r, "fin")
    F.text(K, "فلك الشمس", size=10)
    F.arc(E, 0.5, 120, 240, "fin"); F.arc(E, 0.62, 120, 240, "fin")
    for k in range(25):
        a = 120 + 5 * k
        F.line(pol(0.5, a), pol(0.62, a), "thin")
    for k in range(24):
        a = 122.5 + 5 * k
        F.rtext(pol(0.56, a), abjad(k % 12 + 1), a, size=6)
    F.rtext(pol(0.72, 150), "ساعات طلوع القمر بالنهار", 150, size=8)
    F.rtext(pol(0.72, 210), "ساعات طلوع القمر بالليل", 210, size=8)
    F.text(pol(0.62, -30), "مفضّضة", size=9, color=GREY)
    F.text((0, -1.2), "صورة المفروغ منها", size=11)
    return F.save(out)

def chord(deg): return 2 * sind(deg / 2)

def fig82(out):
    F = Fig(10, 5.0)
    R = 1.0; s3 = math.sqrt(3)
    Z_, H_, G_, T_, K, M, r = eclipse_points()
    cx = 2.4
    S = lambda p: (p[0] + cx, p[1])
    F.circle((cx, 0), R, "fin"); F.line(S((-R, 0)), S((R, 0)), "fin", lw=0.7); F.line(S((0, -R)), S((0, R)), "fin", lw=0.7)
    F.circle(S(K), r, "fin"); F.circle(S(M), r, "fin", lw=0.7)
    Z = pol(R, 120); T = pol(R, 60); Hh = pol(R, 130); Y = pol(R, 50)
    for q in (Z, T, Hh, Y):
        F.line(S((0, 0)), S(q), "con", lw=0.8)
    P = pol(dist((0, 0), K) * cosd(30), 120)
    F.check("ه ز touches circle ك (tangent from ه)", abs(dist(P, K) - r) < 1e-9)
    F.circle(S((0, 0)), chord(5), "con")
    c10 = chord(10)
    Fp = (chord(15), 0); Lp = (-R + chord(5), 0)
    F.arc(S((Lp[0] / 2 - R / 2 + 0.0, 0)), 0, 0, 1, "con")
    F.arc(S(((Lp[0] - 0) / 2, 0)), abs(Lp[0]) / 2, 0, 180, "con", lw=0.8)
    Ain = pol(R - chord(7), 130); Nn = pol(R - chord(7), 60); Sp = pol(R - chord(11), 120)
    F.arc(S((0, 0)), R - chord(7), 60, 130, "con", lw=0.7)
    for q in (pol(c10, 120), pol(c10, 60), Fp, Ain, Nn, Sp):
        F.dot(S(q), RED, 5)
    for p, s, d in [((-R, 0), "ا", (-.07, 0)), ((0, R), "ب", (0, .08)), ((R, 0), "ج", (.07, 0)), ((0, -R), "د", (0, -.08)),
                    (Z, "ز", pol(.08, 120)), (T, "ط", pol(.08, 60)), (Hh, "ح", pol(.08, 130)), (Y, "ي", pol(.08, 50)),
                    (K, "ك", (.06, .03)), (P, "ص", (-.06, .03)), (Fp, "ف", (0, -.07)), (Lp, "ل", (0, -.07)),
                    (Ain, "ع", (-.05, -.05)), (Nn, "ن", (.05, -.05)), (Sp, "س", (.05, -.05)), ((0, 0), "ه", (.05, -.07))]:
        F.lab(S(p), s, d, size=11)
    F.text(S((0, -1.2)), "عمل الشبكة", size=11)
    # left: the rete cut out
    E = (0, 0)
    F.arc(E, R, 0, 180, "fin", lw=1.1); F.arc(((Lp[0]) / 2 * 0 + 0, 0), R - chord(5), 0, 180, "fin", lw=0.9)
    F.line((-R, 0), (R, 0), "fin", lw=0.9)
    lower = [pol(R, a) for a in np.linspace(180, 360, 90)]
    F.fill(lower, color="#efe7d6", z=0); F.arc(E, R, 180, 360, "fin", lw=1.1)
    tt = np.linspace(0, 2 * math.pi, 80)
    F.fill(list(zip(M[0] + r * np.cos(tt), M[1] + r * np.sin(tt))), color="white", z=1); F.circle(M, r, "fin")
    F.text(M, "الفلك المظهر", size=8); F.text((M[0], M[1] - 0.09), "لزيادة نور القمر ونقصانه", size=7)
    F.circle(K, r, "fin"); F.text(K, "فلك الجوزهر", size=8)
    F.arc(E, 0.5, 120, 180, "fin"); F.arc(E, 0.5 - chord(3), 125, 180, "fin")
    F.circle(E, chord(5), "fin")
    for a, nm in ((120, "مري البعد الأول"), (60, "مري البعد الثاني")):
        F.line(pol(chord(5), a), pol(c10, a), "fin", lw=1.2)
        F.rtext(pol(0.33, a + 15), nm, a + 15, size=7)
    F.line((chord(5), 0), Fp, "fin", lw=1.2); F.text((0.2, -0.06), "مري عرض القمر", size=7)
    for q, nm in ((Sp, "مري ساعات ابتداء الكسوف"), (Ain, "مري ساعات نصف الكسوف والمكث"), (Nn, "مري الأصابع المعدلة")):
        F.line(pol(R - chord(5), ang(q)), q, "fin", lw=1.0)
        F.rtext(pol(dist(q, E) - 0.1, ang(q)), nm, ang(q), size=6.5)
    F.text((0, -1.2), "صورة الشبكة المخرّقة المفروغ منها", size=11)
    return F.save(out)

def fig83(out):
    F = Fig(10, 5.0)
    R = 1.0; s3 = math.sqrt(3)
    E = (0, 0)
    K = (0, R / s3); r = R / (2 * s3)
    # left: the construction
    F.circle(E, R, "fin"); F.line((-R, 0), (R, 0), "fin", lw=0.8); F.line((0, -R), (0, R), "fin", lw=0.8)
    F.circle(K, r, "fin")
    F.text(K, "فلك القمر", size=8, color=GREY)
    for p, s, d in [((-R, 0), "ا", (-.07, 0)), ((0, R), "ب", (0, .08)), ((R, 0), "ج", (.07, 0)), ((0, -R), "د", (0, -.08))]:
        F.lab(p, s, d, size=11)
    F.text((0, -1.2), "عمل الوجه الآخر من الصفيحة", size=11)
    # right: the finished face
    cx = 2.4
    S = lambda p: (p[0] + cx, p[1])
    F.circle((cx, 0), R, "fin"); F.line(S((-R, 0)), S((R, 0)), "fin", lw=0.6); F.line(S((0, -R)), S((0, R)), "fin", lw=0.6)
    radii = [chord(10), chord(15), 0.5, R / s3, R - chord(11), R - chord(7)]
    names = ["مدار مري البعد الأول", "مدار عرض القمر", "مدار ساعات طلوع القمر", "", "مدار ساعات بدو الكسوف", "مدار الأصابع المعدلة"]
    for rr, nm, a in zip(radii, names, (207, 300, 150, 0, 250, 20)):
        F.circle((cx, 0), rr, "con", lw=0.9)
        if nm:
            F.rtext(S(pol(rr + 0.035, a)), nm, a, size=7)
    F.circle(S(K), r, "fin")
    pts = circle_circle(K, r, E, R / s3)
    F.check("arc ر ك ح: cos of its half-angle seen from ه is 7/8", all(abs(abs(cosd(ang(p) - 90)) - 7 / 8) < 1e-9 for p in pts))
    for p in pts:
        F.dot(S(p), BLACK, 4)
    pr = max(pts, key=lambda p: p[0]); pl = min(pts, key=lambda p: p[0])
    for p, s, d in [((R, 0), "ج", (.07, 0)), ((0, R), "ب", (0, .08)), ((0, -R), "د", (0, -.08)), ((-R, 0), "ا", (-.07, 0)),
                    (K, "ك", (0, .05)), (pr, "ر", (.05, .03)), (pl, "ح", (-.05, .03)), (E, "ه", (.04, -.06))]:
        F.lab(S(p), s, d, size=11)
    F.text(S((0, -1.2)), "صورة المفروغ منها", size=11)
    return F.save(out)

def crescent_plate(R=1.0):
    Pz = Plate(R, eps=EPS + 5)          # the outer circle is the day-circle of declination −(ε + 5)
    return Pz

def fig84(out):
    F = Fig(5.6, 7.2)
    P = crescent_plate()
    Re = P.Re
    E = (0, 0)
    F.circle(E, 1.0, "fin"); F.line((-1, 0), (1, 0), "fin", lw=0.7); F.line((0, -1.6), (0, 1), "fin", lw=0.7)
    F.circle(E, Re, "fin")
    F.close_enough("the equator ح ط ك م has radius tan((85° − ε)/2)", Re, tand((85 - EPS) / 2))
    K = (-Re, 0); Mm = (Re, 0)
    B = (0, 1.0)
    # ز on the circle such that ب ز passes through ك
    Zs = [q for q in line_circle(B, K, E, 1.0) if q[1] < 0.99]
    Z = Zs[0]
    F.line(B, Z, "con")
    phi_ = 90 - EPS
    c, r = P.almucantar(phi_, 0)
    F.arc_clip(c, r, inside=[(E, 1.0)], kind="fin", lw=1.2)
    Lp = (0, c[1] + r) if c[1] + r < 1 else (0, c[1] - r)
    Lp = (0, c[1] + r)
    Sp = P.zenith(phi_)
    F.check("ص (pole of the ecliptic) is the zenith of the horizon ك ل م", abs(Sp[1] - Re * tand(EPS / 2)) < 1e-9)
    cA, rA = circle3(Mm, Sp, K)
    Ain = cA
    F.close_enough("ع lies on ه د produced at ه ع = ه ك · cot ε", -Ain[1], Re / tand(EPS))
    F.arc_clip(cA, rA, inside=[(E, 1.0)], kind="con", lw=0.9)
    F.line((-1.2, Ain[1]), (1.2, Ain[1]), "con")
    for h in (5, -5):
        cc, rr = P.almucantar(phi_, h)
        F.arc_clip(cc, rr, inside=[(E, 1.0)], kind="redthin")
    c5, r5 = P.almucantar(phi_, 5)
    for k in range(1, 6):
        ca, ra_ = P.azimuth(phi_, 30 * k)
        F.arc_clip(ca, ra_, inside=[(E, 1.0)], outside=[(c5, r5)], kind="redthin")
        ca, ra_ = P.azimuth(phi_, -30 * k)
        F.arc_clip(ca, ra_, inside=[(E, 1.0)], outside=[(c5, r5)], kind="redthin")
    cd, rd = P.almucantar(phi_, -5)
    F.check("the fifth almucantar of depression touches ا ب ج د at ب", abs(cd[1] + rd - 1.0) < 1e-6 or abs(cd[1] - rd + 1.0) < 1e-6 or abs(dist(cd, E) + rd - 1.0) < 1e-6)
    S_ = pol(Re, -EPS)
    F.line(K, Sp, "con")
    for p, s, d in [((-1, 0), "ا", (-.07, 0)), (B, "ب", (0, .08)), ((1, 0), "ج", (.07, 0)), ((0, -1), "د", (.06, -.06)),
                    (E, "ه", (.05, -.06)), (K, "ك", (-.06, .05)), (Mm, "م", (.06, -.05)), ((0, Re), "ح", (.06, .05)),
                    (Z, "ز", (-.05, -.06)), (Lp, "ل", (.05, .06)), (Sp, "ص", (.06, .04)), (Ain, "ع", (.06, .06))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

def fig85(out, phi=41.0):
    F = Fig(5.6, 5.6)
    P = crescent_plate()
    Re = P.Re
    E = (0, 0)
    F.circle(E, 1.0, "con"); F.line((-1, 0), (1, 0), "con", lw=0.7); F.line((0, -1), (0, 1), "con", lw=0.7)
    F.circle(E, Re, "con")
    rt = Re * Re
    F.circle(E, rt, "con"); F.circle(E, 0.15, "fin")
    F.close_enough("ر ط has the radius r²/R of the day-circle of declination ε + 5", rt, P.r_decl(EPS + 5))
    c0, r0 = P.almucantar(phi, 0); c10, r10 = P.almucantar(phi, -10)
    okf = lambda: None
    t = np.linspace(-math.pi, math.pi, 4001)
    def piece(c, r):
        x = c[0] + r * np.cos(t); y = c[1] + r * np.sin(t)
        rr = np.hypot(x, y)
        m = (rr <= 1.0) & (rr >= rt) & (x > 0)
        return x[m], y[m]
    xh, yh = piece(c0, r0); xd, yd = piece(c10, r10)
    oh = np.argsort(yh); od = np.argsort(yd)
    poly = list(zip(xh[oh], yh[oh])) + list(zip(xd[od][::-1], yd[od][::-1]))
    F.fill(poly, color="#efe7d6", z=0)
    F.curve(xh[oh], yh[oh], "fin", lw=1.3); F.curve(xd[od], yd[od], "fin", lw=1.3)
    Ain = (xh[oh][-1], yh[oh][-1]); Sp = (xh[oh][0], yh[oh][0]); Pp = (xd[od][-1], yd[od][-1]); Fp = (xd[od][0], yd[od][0])
    F.line(Ain, Pp, "fin"); F.line(Sp, Fp, "fin")
    for q in (Sp, Fp):
        F.line(pol(0.15, ang(q)), q, "fin", lw=1.0)
    F.check("the horizon passes through the west point م of the equator", abs(dist(c0, (Re, 0)) - r0) < 1e-9)
    Lq = pol(Re, 90 + phi)
    F.line(E, Lq, "con", lw=0.6)
    for p, s, d in [((-1, 0), "ا", (-.07, 0)), ((0, 1), "ب", (0, .08)), ((1, 0), "ج", (.07, 0)), ((0, -1), "د", (0, -.08)),
                    (E, "ه", (-.05, -.06)), ((-Re, 0), "ك", (-.05, .05)), ((Re, 0), "م", (-.06, -.05)), ((0, Re), "ح", (.05, .05)),
                    (Lq, "ل", (-.05, .05)), ((0, rt), "ر", (.05, .05)), ((0, -rt), "ط", (.05, -.05)),
                    (Ain, "ع", (.06, .03)), (Sp, "س", (.05, -.05)), (Pp, "ص", (.06, .03)), (Fp, "ف", (.0, -.07))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

FIGS = {79: fig79, 80: fig80, 81: fig81, 82: fig82, 83: fig83, 84: fig84, 85: fig85}
