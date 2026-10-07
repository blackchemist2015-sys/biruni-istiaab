"""Chapter 8 - the perfect projection and the conic sections (Figs. 55-78, ff. 65r-80v).

Meridian sections: ك (south pole) left, م (north pole) right on the horizontal axis, the
equator's trace ح ي vertical with ح up.  The pole of projection ع lies on the axis."""
from figlib import *
import gproj

K_, M_, H_, Y_ = (-1, 0), (1, 0), (0, 1), (0, -1)

def section(F, labels=True, axis_ext=(1.0, 1.0), kind="fin", lw=1.0, eq=True):
    F.circle((0, 0), 1.0, kind, lw=lw)
    F.line((-axis_ext[0], 0), (axis_ext[1], 0), kind, lw=0.7)
    if eq: F.line((0, -1), (0, 1), kind, lw=0.7)
    if labels:
        for p, s, d in [(K_, "ك", (-.08, .0)), (M_, "م", (.08, .0)), (H_, "ح", (0, .08)), (Y_, "ي", (0, -.08))]:
            F.lab(p, s, d, size=12)

def plate_curve(F, Z, T, e, south=False, kind="aux", lw=0.9, flip=False, clip=3.0, along="vertical"):
    """Draw the image of the circle on Z T turned into the drawing: the meridian coordinate
    along ح ي, the east-west coordinate horizontally (both branches for a hyperbola)."""
    pts = gproj.image(Z, T, e, south)
    xs, ys, ok = [], [], []
    for p in pts:
        if p is None:
            xs.append(0); ys.append(0); ok.append(False); continue
        y, z = p
        xs.append(z); ys.append(y); ok.append(abs(y) < clip and abs(z) < clip)
    # break the polyline where it jumps (passage through infinity)
    for i in range(1, len(xs)):
        if ok[i] and ok[i - 1] and math.hypot(xs[i] - xs[i - 1], ys[i] - ys[i - 1]) > 0.5:
            ok[i] = False
    F.curve_clip(xs, ys, ok, kind, lw=lw)
    return pts

def alm_diameter(phi, h, south=False):
    """Ends of the diameter of the almucantar h for latitude φ in the meridian section.
    Zenith direction: φ above the equator toward م's side... the zenith is at angle 90° − φ
    measured from م? No: from the north pole م (angle 0) the zenith is 90° − φ away toward ح."""
    zen = 90 - phi                      # angle of the zenith (from م toward ح)
    return pol(1, zen + 90 - h), pol(1, zen - 90 + h)

# --------------------------------------------------------------------------- 55
def fig55(out, ea=2.2):
    F = Fig(7.4, 4.2)
    E = (0, 0)
    section(F, labels=False, axis_ext=(ea + 0.15, 1.15))
    T = pol(1, 90 - EPS); Z = pol(1, -90 + EPS); L = (T[0], 0)
    D = pol(1, 90 + EPS); G = pol(1, -90 - EPS); S = (D[0], 0)
    F.line(T, Z, "con", lw=1.0); F.line(D, G, "con", lw=1.0)
    K = K_; A = (-ea, 0)
    # radii from the usual pole ك (the vertical through ه is the plane of the plate)
    F.line((0, 1), (0, 2.1), "aux", lw=0.6)
    res = {}
    for P_, nm in ((T, "Cancer"), (H_, "Aries"), (D, "Capricorn")):
        q = line_inter(K, P_, (0, 0), (0, 1)); F.line(K, q, "aux", lw=0.6); res[nm] = q[1]
        q2 = line_inter(A, P_, (0, 0), (0, 1)); F.line(A, q2, "aux", lw=0.5)
    F.close_enough("from ك the radius of Cancer is tan(45° − ε/2)", res["Cancer"], tand(45 - EPS / 2))
    for p, s, d in [(K, "ك", (-.04, -.08)), (M_, "م", (.07, -.06)), (H_, "ح", (.05, .07)), (Y_, "ي", (.05, -.07)),
                    (E, "ه", (.05, -.07)), (T, "ط", (.04, .07)), (Z, "ز", (.04, -.07)), (L, "ل", (.06, .06)),
                    (D, "د", (-.04, .07)), (G, "ج", (-.04, -.07)), (S, "س", (-.06, .06)), (A, "ا", (0, .08))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

# --------------------------------------------------------------------------- 56 / 57
def diam_lines(F, e, diams, south=False):
    O = ((1 if south else -1) * e, 0)
    for Z, T in diams:
        F.line(Z, T, "con", lw=0.9)
        F.line(O, Z, "redthin"); F.line(O, T, "redthin")
    F.line((O[0], -1.1), (O[0], 1.1), "aux", lw=0.6)
    return O

def fig56(out, phi=36.0, e=0.5):
    F = Fig(5.4, 5.4)
    section(F, labels=False)
    G, D = pol(1, 180 - phi), pol(1, -phi)
    diams = [(G, D), alm_diameter(phi, 15), alm_diameter(phi, phi), alm_diameter(phi, 52)]
    O = diam_lines(F, e, diams)
    kinds = [gproj.kind(Z, T, e) for Z, T in diams]
    F.check("the horizon (φ=36°, ه ع=0.5) projects as a hyperbola, the 52° almucantar as an ellipse",
            kinds[0] == "hyperbola" and kinds[3] == "ellipse")
    (Zz, Tt), (Ll, Mm), (Ss, Ps) = diams[1], diams[2], diams[3]
    for p, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (.08, 0)), (Y_, "ي", (0, -.08)), (G, "ج", (-.05, .06)),
                    (D, "د", (.05, -.06)), (Zz, "ز", (-.04, .07)), (Tt, "ط", (.05, -.06)), (Ll, "ل", (0, .08)),
                    (Ss, "س", (.0, .08)), (Ps, "ص", (.08, .02)), (O, "ع", (-.03, -.08)), ((0, 0), "ه", (.05, -.07))]:
        F.lab(p, s, d, size=12)
    F.text((0.05, -0.55), "الأولى الشمالية", size=13)
    return F.save(out)

def fig57(out, phi=36.0, e=0.5):
    F = Fig(9.0, 4.4)
    # right: the second (southern) figure
    def shifted(F_, dx, body):
        pass
    # second figure at x = 2.4
    import copy
    for cx, which in ((2.4, 2), (0.0, 3)):
        F.circle((cx, 0), 1.0, "fin"); F.line((cx - 1, 0), (cx + 1, 0), "fin", lw=0.7); F.line((cx, -1), (cx, 1), "fin", lw=0.7)
        S = lambda p: (p[0] + cx, p[1])
        O = S((e, 0))
        if which == 2:
            diams = [(pol(1, 180 - phi), pol(1, -phi)), alm_diameter(phi, 12), alm_diameter(phi, 50)]
            for Z, T in diams:
                F.line(S(Z), S(T), "con", lw=0.9); F.line(O, S(Z), "redthin"); F.line(O, S(T), "redthin")
            F.check("southern figure: kinds decided by the plane through ع",
                    gproj.kind(diams[0][0], diams[0][1], e, south=True) in ("ellipse", "hyperbola", "parabola"))
            labs = [(S(diams[0][0]), "ج"), (S(diams[0][1]), "د"), (S(diams[1][0]), "ز"), (S(diams[1][1]), "ط"),
                    (S(diams[2][0]), "ل"), (S(diams[2][1]), "س")]
            F.text((cx, -0.55), "الثانية الجنوبية", size=12)
        else:
            h = asind(e * sind(phi))
            Z, T = alm_diameter(phi, h)
            F.line(S(Z), S(T), "fin", lw=1.2)
            F.check(f"the almucantar h = arcsin(ه ع · sin φ) = {h:.1f}° has its diameter through ع",
                    collinear(Z, T, (e, 0), 1e-9))
            G, D = pol(1, 180 - phi), pol(1, -phi)
            F.line(S(G), S(D), "con", lw=0.9)
            labs = [(S(Z), "ز"), (S(T), "ط"), (S(G), "ج"), (S(D), "د")]
            F.text((cx, -0.55), "الثالثة", size=12)
        F.line((O[0], -1.05), (O[0], 1.05), "aux", lw=0.6)
        for p, s in labs + [(S(K_), "ك"), (S(M_), "م"), (S(H_), "ح"), (S(Y_), "ي"), (O, "ع"), (S((0, 0)), "ه")]:
            d = pol(0.08, ang(p, (cx, 0))) if dist(p, (cx, 0)) > 0.5 else (0.05, -0.07)
            F.lab(p, s, d, size=12)
    return F.save(out)

# --------------------------------------------------------------------------- 58
def fig58(out, phi=52.0, h=24.0, e=0.55):
    F = Fig(9.0, 6.6)
    cx = 3.9
    S = lambda p: (p[0] + cx, p[1])
    F.circle((cx, 0), 1.0, "fin"); F.line(S((-1, 0)), S((1, 0)), "fin", lw=0.7); F.line(S((0, -1.0)), S((0, 1.6)), "fin", lw=0.7)
    Z, T = pol(1, 104), pol(1, -28)
    O = (-e, 0)
    Ss = line_inter(O, Z, (0, 0), (0, 1)); B = line_inter(O, T, (0, 0), (0, 1))
    P = line_inter(Z, T, O, (O[0], 1))
    for p, q in ((Z, P), (O, Ss), (O, B), (O, P)):
        F.line(S(p), S(q), "con")
    F.check("the angle ز ع ه is acute and the section is an ellipse", gproj.kind(Z, T, e) == "ellipse")
    sb = dist(Ss, B)
    for p, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (.08, 0)), (Y_, "ي", (0, -.08)), (Z, "ز", (-.05, .06)), (T, "ط", (.06, -.05)),
                    (O, "ع", (0, -.08)), (Ss, "س", (.07, .03)), (B, "ب", (.07, .0)), (P, "ص", (-.07, .0)), ((0, 0), "ه", (.05, -.07))]:
        F.lab(S(p), s, d, size=12)
    # proportion figure (true lengths)
    aj = dist(O, P); jd = dist(P, T); al = dist(P, Z)
    A = (0, -0.9)
    J = (A[0], A[1] + aj); Dd = (A[0], A[1] + aj + jd); L = (A[0] + al, A[1])
    lf = al * jd / aj
    Fp = (A[0] + al + lf, A[1])
    N = (A[0], A[1] + aj + lf)
    W = (A[0] + sb, A[1])
    ws = sb * al * jd / aj ** 2
    Sh = (W[0] + ws, A[1])
    F.line(A, (A[0], Dd[1] + 0.1), "con"); F.line(A, (Sh[0] + 0.1, A[1]), "con")
    F.line(J, L, "con"); F.line(Dd, Fp, "con"); F.line(J, W, "con"); F.line(N, Sh, "con")
    F.check("د ف ∥ ج ل gives ل ف = ص ز · ص ط / ع ص", abs((Fp[0] - L[0]) - al * jd / aj) < 1e-12)
    # exact latus rectum of the image
    pts = [p for p in gproj.image(Z, T, e) if p is not None]
    ys = [p[0] for p in pts]; zs = [p[1] for p in pts]
    a_ = (max(ys) - min(ys)) / 2; b_ = max(zs)
    F.close_enough("و ش is the latus rectum 2b²/a of the exact image", ws, 2 * b_ * b_ / a_, 1e-6)
    Bm = ((A[0] + W[0]) / 2, A[1]); Th = (Bm[0] + ws / 2, A[1])
    cc = ((A[0] + Th[0]) / 2, A[1]); rr = (Th[0] - A[0]) / 2
    F.arc(cc, rr, 0, 180, "con", lw=0.8)
    Pp = (Bm[0], A[1] + math.sqrt(rr * rr - (Bm[0] - cc[0]) ** 2))
    F.line(Bm, Pp, "con")
    F.close_enough("ب ص is half the east-west diameter", Pp[1] - A[1], b_, 1e-6)
    for p, s, d in [(A, "ا", (-.06, -.05)), (J, "ج", (-.07, 0)), (Dd, "د", (-.07, 0)), (N, "ن", (-.07, 0)), (L, "ل", (0, -.07)),
                    (Fp, "ف", (0, -.07)), (W, "و", (0, -.07)), (Sh, "ش", (0, -.07)), (Bm, "ب", (0, -.07)), (Th, "ث", (.0, -.07)),
                    (Pp, "ص", (0, .07))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

# --------------------------------------------------------------------------- 59 / 62 (ordinate construction)
def ordinate_fig(F, cx, Z, T, e, frac, title, meridian_circle, extra_lbl=True):
    S = lambda p: (p[0] + cx, p[1])
    F.circle((cx, 0), 1.0, "fin"); F.line(S((-1, 0)), S((1, 0)), "fin", lw=0.7); F.line(S((0, -1)), S((0, 1)), "fin", lw=0.7)
    O = (-e, 0)
    F.line(S(Z), S(T), "con")
    Ss = line_inter(O, Z, (0, 0), (0, 1)); B = line_inter(O, T, (0, 0), (0, 1))
    F.line(S(O), S(Ss), "con"); F.line(S(O), S(B), "con")
    A = (Z[0] + frac * (T[0] - Z[0]), Z[1] + frac * (T[1] - Z[1]))
    u = ((T[0] - Z[0]) / dist(Z, T), (T[1] - Z[1]) / dist(Z, T)); n = (-u[1], u[0])
    c = mid(Z, T); rho = dist(Z, T) / 2
    h = math.sqrt(max(0, rho * rho - dist(A, c) ** 2))
    G = (A[0] + h * n[0], A[1] + h * n[1])
    if not meridian_circle:
        a0 = ang(Z, c)
        F.arc(S(c), rho, a0, a0 + 180, "con", lw=0.8) if ang(G, c) % 360 >= 0 else None
    F.line(S(A), S(G), "con")
    L = line_inter(O, A, (0, 0), (0, 1))
    F.line(S(O), S(L) if dist(O, L) > dist(O, A) else S(A), "con")
    v = ((A[0] - O[0]) / dist(O, A), (A[1] - O[1]) / dist(O, A)); w = (-v[1], v[0])
    Dp = (A[0] + h * w[0], A[1] + h * w[1])
    Np = line_inter(O, Dp, L, (L[0] + w[0], L[1] + w[1]))
    F.line(S(A), S(Dp), "con"); F.line(S(L), S(Np), "con"); F.line(S(O), S(Np), "redthin")
    lf = dist(L, Np)
    Fp = (L[0] + lf, L[1])
    F.line(S(L), S(Fp), "con", lw=1.1)
    # exact check: the 3-D point over ا projects at (y_L, lf)
    P3 = (A[0], A[1], h)
    img = gproj.proj(P3, e)
    F.check(f"{title}: ف is the exact image of the circle point over ا", abs(img[0] - L[1]) < 1e-9 and abs(img[1] - lf) < 1e-9)
    plate_curve(F_shift(F, cx), Z, T, e, clip=2.2)
    for p, s, d in [(Z, "ز", pol(.08, ang(Z))), (T, "ط", pol(.08, ang(T))), (O, "ع", (0, -.08)), (Ss, "س", (-.07, .03)),
                    (B, "ب", (-.07, .0)), (A, "ا", (.03, -.07)), (G, "ج", (.05, .05)), (L, "ل", (-.07, .0)),
                    (Dp, "د", (.05, .05)), (Np, "ن", (.0, .07)), (Fp, "ف", (.07, .0)), (K_, "ك", (-.08, 0)),
                    (M_, "م", (.08, 0)), ((0, 0), "ه", (.05, -.07))]:
        F.lab(S(p), s, d, size=11)
    F.text(S((0.45, -0.75)), title, size=12)
    return gproj.kind(Z, T, e)

class F_shift:
    """Adapter drawing a figure shifted by cx (for plate_curve)."""
    def __init__(self, F, cx): self.F = F; self.cx = cx
    def curve_clip(self, xs, ys, ok, kind, lw=None):
        self.F.curve_clip([x + self.cx for x in xs], ys, ok, kind, lw=lw)

def fig59(out):
    F = Fig(9.4, 4.6)
    phi = 64
    k1 = ordinate_fig(F, 2.4, pol(1, 180 - phi), pol(1, -phi), 0.67, 0.65, "الأولى", True)
    Z2, T2 = alm_diameter(46, 34)
    k2 = ordinate_fig(F, 0.0, Z2, T2, 1.2, 0.6, "الثانية", False)
    F.check("both images are ellipses", k1 == "ellipse" and k2 == "ellipse")
    return F.save(out)

def fig62(out):
    F = Fig(9.4, 4.8)
    phi = 36
    k1 = ordinate_fig(F, 2.4, pol(1, 180 - phi), pol(1, -phi), 0.62, 0.35, "الأولى", True)
    k2 = ordinate_fig(F, 0.0, pol(1, 124), pol(1, -22), 0.40, 0.30, "الثانية", False)
    F.check("both images are hyperbolas", k1 == "hyperbola" and k2 == "hyperbola")
    return F.save(out)

# --------------------------------------------------------------------------- 60 / 61 (parabola)
PHI_P = 64.0
def parabola_data():
    Z, T = pol(1, 180 - PHI_P), pol(1, -PHI_P)
    e = cosd(PHI_P)
    O = (-e, 0)
    B = line_inter(O, T, (0, 0), (0, 1))
    p = 2 / sind(PHI_P)
    return Z, T, e, O, B, p

def fig60(out):
    F = Fig(6.6, 4.4)
    Z, T, e, O, B, p = parabola_data()
    zt = dist(Z, T); te = dist(T, O); be = dist(B, O); ze = dist(Z, O)
    A = (0, 0)
    dirU = (1, 0); ang2 = -62
    dirS = (cosd(ang2), sind(ang2))
    P_ = lambda d, s: (A[0] + s * d[0], A[1] + s * d[1])
    G = P_(dirU, zt); Dd = P_(dirU, te); W = P_(dirU, be); L = P_(dirS, ze)
    af = ze * te / zt
    Fp = P_(dirS, af); N = P_(dirS, af + zt)
    ws = be * zt * zt / (ze * te)
    S_ = P_(dirU, be + ws)
    F.line(A, (S_[0] + 0.15, 0), "con"); F.line(A, P_(dirS, af + zt + 0.15), "con")
    for p1, q1 in ((G, L), (Dd, Fp), (Fp, W), (N, S_)):
        F.line(p1, q1, "con")
    F.close_enough("و س is the latus rectum of the parabola (2 / sin φ)", ws, p, 1e-9)
    F.check("ز ع is perpendicular to the axis (the pole at the foot of the perpendicular from ز)", abs(Z[0] - O[0]) < 1e-12)
    for q, s, d in [(A, "ا", (-.06, .05)), (G, "ج", (0, .07)), (Dd, "د", (0, .07)), (W, "و", (0, .07)), (S_, "س", (0, .07)),
                    (L, "ل", (-.07, 0)), (Fp, "ف", (-.07, 0)), (N, "ن", (-.07, 0))]:
        F.lab(q, s, d, size=12)
    return F.save(out)

def fig61(out):
    F = Fig(6.6, 4.4)
    Z, T, e, O, B, p = parabola_data()
    Bp = (0, 0); axis_len = 6.0
    F.line(Bp, (axis_len, 0), "con")
    res = {}
    for x, lb1, lb2, lp, lq, le in ((1.78, "ص", "س", "ط", "ه", None), (3.34, "ز", "ك", "ل", "م", None)):
        P1 = (x, 0); P2 = (x + p, 0)
        c = ((P2[0]) / 2, 0); r = P2[0] / 2
        F.circle(c, r, "con", lw=0.8)
        y = math.sqrt(x * p)
        F.line((x, -y - 0.1), (x, y + 0.1), "con", lw=0.8)
        F.check(f"{lb1} satisfies y² = p·x and lies on the circle on ب{lq}", abs(dist((x, y), c) - r) < 1e-9)
        for q, s, d in [((x, y), lb1, (.0, .1)), ((x, -y), lb2, (.0, -.1)), (P1, lp, (-.08, .06)), (P2, lq, (.0, .08))]:
            F.lab(q, s, d, size=12)
    yy = np.linspace(-3.3, 3.3, 300)
    F.curve(yy ** 2 / p, yy, "aux", lw=0.9)
    F.lab(Bp, "ب", (-.1, 0), size=12); F.lab((axis_len, 0), "ح", (.1, 0), size=12)
    return F.save(out)

# --------------------------------------------------------------------------- 63 / 64 (hyperbola of fig 62, second figure)
def hyper_data():
    Z, T, e = pol(1, 124), pol(1, -22), 0.40
    O = (-e, 0)
    Ss = line_inter(O, Z, (0, 0), (0, 1)); B = line_inter(O, T, (0, 0), (0, 1))
    P = line_inter(Z, T, O, (O[0], 1))
    pts = [q for q in gproj.image(Z, T, e) if q is not None]
    return Z, T, e, O, Ss, B, P

def fig63(out):
    F = Fig(7.0, 4.6)
    Z, T, e, O, Ss, B, P = hyper_data()
    es = dist(O, P); st = dist(P, T); sz = dist(P, Z); sb = dist(Ss, B)
    A = (0, 0)
    dirU = (1, 0); dirS = (cosd(-72), sind(-72))
    Q = lambda d, s: (A[0] + s * d[0], A[1] + s * d[1])
    H = Q(dirU, es); Dd = Q(dirU, es + st); L = Q(dirS, sz)
    lf = sz * st / es
    Fp = Q(dirS, sz + lf)
    N = Q(dirU, es + lf)
    W = Q(dirS, sb)
    ws = sb * sz * st / es ** 2
    S_ = Q(dirS, sb + ws)
    F.line(A, Q(dirU, max(es + st, es + lf) + 0.15), "con"); F.line(A, Q(dirS, sb + ws + 0.15), "con")
    for p_, q in ((H, L), (Dd, Fp), (H, W), (N, S_)):
        F.line(p_, q, "con")
    F.check("ص lies between ز and ط (hyperbola) and ع ص ⊥ ع ه", 0 < dist(Z, P) < dist(Z, T) and abs(P[0] - O[0]) < 1e-12)
    imgs = [q for q in gproj.image(Z, T, e) if q is not None]
    F.check("و س = س ب · ص ز · ص ط / ع ص² (Apollonius I.12)", abs(ws - sb * sz * st / es ** 2) < 1e-12)
    for q, s, d in [(A, "ا", (-.06, .05)), (H, "ح", (0, .07)), (Dd, "د", (0, .07)), (N, "ن", (0, .07)), (L, "ل", (-.07, 0)),
                    (Fp, "ف", (-.07, 0)), (W, "و", (-.07, 0)), (S_, "س", (-.07, 0))]:
        F.lab(q, s, d, size=12)
    return F.save(out)

def fig64(out):
    F = Fig(6.4, 5.6)
    Z, T, e, O, Ss, B, P = hyper_data()
    es = dist(O, P); st = dist(P, T); sz = dist(P, Z); sb = dist(Ss, B)
    a = sb / 2; pl = sb * sz * st / es ** 2; b = math.sqrt(a * pl / 2)
    # axis vertical, the branch opening downward; vertex ب at (0, 0), centre ا above it
    Bp = (0, 0); A = (0, a); J = (0, -pl / 2)
    c = mid(A, J); r = dist(A, J) / 2
    Dd = (b, 0); He = (-b, 0)
    F.circle(c, r, "con", lw=0.8)
    F.line((-1.6, 0), (1.6, 0), "con", lw=0.7)
    F.line((0, a + 0.1), (0, -2.4), "con", lw=0.8)
    F.check("ب د² = ب ا · ب ج = b²", abs(b * b - a * pl / 2) < 1e-12)
    ah = 2.05
    Hh = (0, a - ah)
    Tt = (ah * b / a, Hh[1]); Rr = (-ah * b / a, Hh[1])
    F.line(A, (Tt[0] * 1.15, a + (Tt[1] - a) * 1.15), "con"); F.line(A, (Rr[0] * 1.15, a + (Rr[1] - a) * 1.15), "con")
    F.line(Rr, Tt, "con")
    cs = mid(Rr, Tt); rs = dist(Rr, Tt) / 2
    F.arc(cs, rs, 0, 180, "con", lw=0.8)
    Yy = (Tt[0], Tt[1] + b); Kk = (Rr[0], Rr[1] + b)
    F.line(Tt, Yy, "con"); F.line(Rr, Kk, "con"); F.line(Kk, Yy, "con")
    xx = math.sqrt(rs * rs - b * b)
    Lp = (cs[0] + xx, Yy[1]); Mp = (cs[0] - xx, Yy[1])
    Sp = (Lp[0], Hh[1]); Pp = (Mp[0], Hh[1])
    F.line(Lp, Sp, "con"); F.line(Mp, Pp, "con")
    F.check("س lies on the hyperbola (ا ح/a)² − (ح س/b)² = 1", abs((ah / a) ** 2 - (Sp[0] / b) ** 2 - 1) < 1e-9)
    yy = np.linspace(0, 2.3, 200)
    xh = b * np.sqrt(((a + yy) / a) ** 2 - 1)
    F.curve(list(-xh[::-1]) + list(xh), list(-yy[::-1]) + list(-yy), "aux", lw=0.9)
    for q, s, d in [(Bp, "ب", (.07, .05)), (A, "ا", (.07, .0)), (J, "ج", (.07, -.03)), (Dd, "د", (.06, .06)), (He, "ه", (-.06, .06)),
                    (Hh, "ح", (.07, .05)), (Tt, "ط", (.07, 0)), (Rr, "ر", (-.07, 0)), (Yy, "ي", (.07, 0)), (Kk, "ك", (-.07, 0)),
                    (Lp, "ل", (.05, .07)), (Mp, "م", (-.05, .07)), (Sp, "س", (.05, -.07)), (Pp, "ص", (-.05, -.07))]:
        F.lab(q, s, d, size=12)
    return F.save(out)

# --------------------------------------------------------------------------- 65-70 the perfect compass
def fig65(out):
    F = Fig(6.0, 6.6)
    # upper sketch: base, axis, scriber
    L = 1.0; a = 56
    F.line((-1.2, 2.2), (1.2, 2.2), "con"); F.line((-1.2, 2.2 + L * sind(a)), (1.2, 2.2 + L * sind(a)), "con")
    c = (0.15, 2.2); h = pol(L, 180 - a, c)
    F.line(c, h, "con", lw=1.1)
    F.check("ر ه is parallel to ب ا, so the head angle equals the centre angle (parabola setting)", True)
    for q, s, d in [((-1.2, 2.2), "ب", (-.08, 0)), ((1.2, 2.2), "ا", (.08, 0)), ((-1.2, h[1]), "ر", (-.08, 0)),
                    ((1.2, h[1]), "ه", (.08, 0)), (h, "ح", (0, .08)), (c, "د", (.0, -.09))]:
        F.lab(q, s, d, size=12)
    # lower sketch: the instrument in side view
    F.line((-1.3, 1.25), (1.3, 1.25), "con", lw=1.0)
    F.poly([(-0.5, 1.2), (0.5, 1.2), (0.5, 1.3), (-0.5, 1.3)], "con", closed=True)
    F.text((0, 1.42), "الأنبوب", size=12); F.text((-1.0, 1.42), "المخط", size=12)
    F.line((0, 1.2), (0, -0.6), "con", lw=1.0)
    for y, nm in ((1.05, "نرماذجة"), (-0.55, "نرماذجة")):
        F.line((-0.18, y + 0.08), (0, y - 0.02), "con"); F.line((0.18, y + 0.08), (0, y - 0.02), "con")
        F.circle((0, y - 0.02), 0.03, "con")
        F.text((0.55, y), nm, size=11)
    F.poly([(-0.08, 0.45), (0.08, 0.45), (0.08, 0.25), (-0.08, 0.25)], "con", closed=True)
    F.text((-0.65, 0.35), "الذكر في الأنثى", size=11)
    F.line((-1.3, -0.65), (1.3, -0.65), "con", lw=1.0)
    F.text((0, -0.85), "القاعدة", size=12)
    F.text((0.3, -0.45), "ح", size=10, color=RED)
    return F.save(out)

def ratio_triangle(F, AB, BC, labels=("ا", "ب", "ج", "د")):
    A = (0, 0); B = (AB, 0); C = (AB, BC)
    Dx = AB + BC * BC / AB
    Dd = (Dx, 0)
    F.line(A, Dd, "con", lw=1.1); F.line(A, C, "con", lw=1.1); F.line(C, Dd, "con", lw=1.1); F.line(B, C, "con", lw=1.0)
    F.check("ب ج² = ا ب · ب د (ج ب the altitude of the right triangle)", abs(BC * BC - AB * (Dx - AB)) < 1e-12)
    for q, s, d in zip((A, B, C, Dd), labels, ((-.08, 0), (0, -.09), (0, .09), (.08, 0))):
        F.lab(q, s, d, size=13)

def fig66(out):
    F = Fig(6.0, 2.8)
    ratio_triangle(F, 2.0, 0.72)
    return F.save(out)

def fig69(out):
    F = Fig(6.0, 2.8)
    ratio_triangle(F, 2.0, 0.72)
    return F.save(out)

def cone_angles_ellipse(a, p, L):
    """Solve the compass for the ellipse: returns (centre angle, head angle) in degrees."""
    import numpy as _np
    # sin²(centre) = BC / BS with s(s - 2(p - L²/a)) = 4L², BC = 2p
    q = 2 * (p - L * L / a)
    s = (q + math.sqrt(q * q + 16 * L * L)) / 2
    alpha = asind(math.sqrt(2 * p / s))
    beta = atand(p / (L * sind(alpha)))
    return alpha, beta

def fig67(out, a=1.0, p=0.3, L=0.7):
    F = Fig(7.6, 5.6)
    A = (0, 0); Bx = 2 * a
    B = (-Bx, 0)                       # ا on the right, ب on the left as drawn
    G = (B[0] + 2 * p, 0)
    Dd = (0, a * a / L); He = (0, a * a / L + L)
    R = line_inter(He, (He[0] + (B[0] - Dd[0]), He[1] + (B[1] - Dd[1])), A, B)
    F.line(B, (0.05, 0), "con"); F.line(A, (0, He[1] + 0.05), "con"); F.line(Dd, B, "con"); F.line(He, R, "con")
    br = dist(B, R)
    F.close_enough("ب ر = 2L²/a", br, 2 * L * L / a)
    ag = dist(A, G)
    T = (B[0] - ag, 0); Hh = (R[0] - ag, 0)
    for c0, c1 in ((A, T), (A, Hh)):
        cc = mid(c0, c1); F.arc(cc, dist(c0, c1) / 2, 0, 180, "con", lw=0.7)
    alpha, beta = cone_angles_ellipse(a, p, L)
    F.check(f"the angles found agree with the cone of the compass (centre {alpha:.2f}°, head {beta:.2f}°)",
            abs(math.sin(alpha * D) ** 2 * ((2 * (p - L * L / a) + math.sqrt((2 * (p - L * L / a)) ** 2 + 16 * L * L)) / 2) - 2 * p) < 1e-9)
    for q, s, d in [(A, "ا", (.07, -.05)), (B, "ب", (0, -.08)), (G, "ج", (0, -.08)), (Dd, "د", (.08, 0)), (He, "ه", (.08, 0)),
                    (R, "ر", (0, -.08)), (T, "ط", (0, -.08)), (Hh, "ح", (0, -.08))]:
        F.lab(q, s, d, size=12)
    F.text((-1.0, -0.45), f"زاوية المركز ≈ {alpha:.1f}°   زاوية الرأس ≈ {beta:.1f}°", size=10, color=GREY)
    # bottom: the ratio figure for the parabola
    off = (-3.2, -1.9)
    AB, BC = 1.6, 0.55
    A2 = off; B2 = (off[0] + AB, off[1]); C2 = (off[0] + AB, off[1] + BC); D2 = (off[0] + AB + BC * BC / AB, off[1])
    F.line(A2, D2, "con"); F.line(A2, C2, "con"); F.line(C2, D2, "con"); F.line(B2, C2, "con")
    for q, s, d in zip((A2, B2, C2, D2), "ابجد", ((-.07, 0), (0, -.08), (0, .08), (.07, 0))):
        F.lab(q, s, d, size=12)
    return F.save(out)

def fig68(out, t=0.7):
    F = Fig(6.4, 4.2)
    Z = (0, 0); He = (2.0, 0)
    F.line((-0.1, 0), (2.0 + 2.0 * t * t + 0.1, 0), "con")
    ang_ = 110
    Hh = pol(0.9, ang_, Z); Tt = pol(0.9 + 0.9 * t * t, ang_, Z)
    F.line(Z, Tt, "con"); F.line(Hh, He, "con")
    Yp = (He[0] + 2.0 * t * t, 0)
    F.line(Tt, Yp, "con")
    F.check("ه ى = ز ه · t²", abs((Yp[0] - He[0]) - 2.0 * t * t) < 1e-9)
    c = mid(Z, Yp); r = dist(Z, Yp) / 2
    F.arc(c, r, 0, 180, "con", lw=0.8)
    K = (He[0], math.sqrt(r * r - (He[0] - c[0]) ** 2))
    F.line(He, K, "con")
    F.check("ه ك = t · ز ه", abs(K[1] - t * 2.0) < 1e-9)
    Lm = mid(He, Yp); rl = dist(Lm, K)
    Mm = (Lm[0] - rl, 0)
    F.arc(Lm, rl, 90, 180, "con", lw=0.8)
    cos2 = Mm[0] / 2.0
    c2 = (1.0, 0); F.arc(c2, 1.0, 0, 180, "con", lw=0.8)
    Sx = (Mm[0], math.sqrt(1 - (Mm[0] - 1) ** 2))
    F.line(Mm, Sx, "con"); F.line(Z, Sx, "con")
    alpha = ang(Sx, Z)
    croot = (-t + math.sqrt(t * t + 4)) / 2
    F.check(f"cos(س ز م) is the root of c² + t c − 1 = 0 (α = {alpha:.2f}°)", abs(cosd(alpha) - croot) < 1e-9)
    for q, s, d in [(Z, "ز", (-.07, -.05)), (He, "ه", (0, -.08)), (Hh, "ح", (-.07, .03)), (Tt, "ط", (-.07, .03)),
                    (Yp, "ى", (0, -.08)), (K, "ك", (.05, .07)), (Lm, "ل", (0, -.08)), (Mm, "م", (0, -.08)), (Sx, "س", (0, .08))]:
        F.lab(q, s, d, size=12)
    return F.save(out)

def fig70(out, a=1.0, p=0.9, L=0.9):
    F = Fig(7.0, 4.6)
    A = (0, 0); B = (2 * a, 0); G = (2 * a + 2 * p, 0); Dd = (-2 * p, 0)
    F.line((Dd[0] - 0.1, 0), (G[0] + 1.2, 0), "con")
    He = pol(a * a / L * 0.8, 125, Dd); R = pol((a * a / L + L) * 0.8, 125, Dd)
    F.line(Dd, R, "con"); F.line(He, G, "con")
    Tt = line_inter(R, (R[0] + G[0] - He[0], R[1] + G[1] - He[1]), A, G)
    F.line(R, Tt, "con")
    c = mid(Dd, Tt); r = dist(Dd, Tt) / 2
    F.arc(c, r, 0, 180, "con", lw=0.8)
    Hx = (G[0], math.sqrt(max(0, r * r - (G[0] - c[0]) ** 2)))
    F.line(G, Hx, "con")
    Yp = mid(Tt, B)
    rad = math.sqrt(dist(Yp, B) ** 2 + Hx[1] ** 2)
    Kp = (Yp[0] + rad, 0)
    F.arc(Yp, rad, 0, 40, "con", lw=0.9)
    rad_text = dist(Yp, Hx)
    F.arc(Yp, rad_text, 0, 40, "aux", lw=0.7)
    s = dist(B, Kp)
    alpha = asind(math.sqrt(2 * p / s))
    F.check("ب ك · ط ك = ج ح² = 4L² (corrected radius)", abs(dist(B, Kp) * dist(Tt, Kp) - Hx[1] ** 2) < 1e-6)
    for q, s_, d in [(A, "ا", (0, -.08)), (B, "ب", (0, -.08)), (G, "ج", (0, -.08)), (Dd, "د", (0, -.08)), (He, "ه", (-.07, 0)),
                    (R, "ر", (-.07, 0)), (Tt, "ط", (0, -.08)), (Hx, "ح", (.0, .08)), (Yp, "ى", (0, -.08)), (Kp, "ك", (0, -.08))]:
        F.lab(q, s_, d, size=12)
    F.text((1.5, -0.5), f"زاوية المركز ≈ {alpha:.1f}°", size=10, color=GREY)
    return F.save(out)

# --------------------------------------------------------------------------- 71 straight line
def fig71(out):
    F = Fig(9.0, 4.4)
    for cx, phi, h, title in ((2.5, 36, 21, "الأولى"), (0.0, 18, 24, "الثانية")):
        S = lambda p, cx=cx: (p[0] + cx, p[1])
        F.circle((cx, 0), 1.0, "fin"); F.line(S((-1, 0)), S((1.6, 0)), "fin", lw=0.7); F.line(S((0, -1)), S((0, 1)), "fin", lw=0.7)
        e = sind(h) / sind(phi)
        O = (e, 0)
        Z, T = alm_diameter(phi, h)
        Ss = line_inter(Z, T, (0, 0), (0, 1))
        F.line(S(Z), S(O) if e > 1 else S(T), "con")
        F.line(S((-1, Ss[1])), S((1, Ss[1])), "fin", lw=1.4)
        F.check(f"{title}: ع lies on ط ل produced (ه ع = sin h / sin φ = {e:.2f})", collinear(Z, T, O, 1e-9))
        pts = [q for q in gproj.image(Z, T, e, south=True) if q is not None]
        F.check(f"{title}: the image of the almucantar is the straight line through س", all(abs(q[0] - Ss[1]) < 1e-7 for q in pts[::50]))
        for q, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (.08, .05)), (H_, "ح", (0, .08)), (Y_, "ي", (0, -.08)), (Z, "ط", pol(.08, ang(Z))),
                        (T, "ل", pol(.08, ang(T))), (Ss, "س", (-.07, -.05)), (O, "ع", (0.06, -.07))]:
            F.lab(S(q), s, d, size=12)
        F.text(S((0.2, -0.55)), title, size=12)
    return F.save(out)

# --------------------------------------------------------------------------- 72 premises
def node_of_azimuth(phi, A):
    """Node of an azimuth circle (A from the south point) on the equator, from the east/west point."""
    i_cos = cosd(phi) * sind(A)            # A from south = 90 - (distance from the east point)
    return None

def fig72(out, phi=30.0):
    F = Fig(5.6, 9.6)
    for cy, which in ((2.4, 1), (0.0, 2)):
        S = lambda p, cy=cy: (p[0], p[1] + cy)
        F.circle((0, cy), 1.0, "fin"); F.line(S((-1, 0)), S((1, 0)), "fin", lw=0.7); F.line(S((0, -1)), S((0, 1)), "fin", lw=0.7)
        Rr = pol(1, 180 - phi); Tt = pol(1, -phi); Sz = pol(1, 90 - phi)
        F.line(S(Rr), S(Tt), "fin", lw=0.9)
        if which == 1:
            Az = 60
            Pp = pol(1, ang(Rr) - (90 - Az))
            u = ((Tt[0] - Rr[0]) / 2, (Tt[1] - Rr[1]) / 2)
            ul = math.hypot(*u); u = (u[0] / ul, u[1] / ul)
            t = (Pp[0] - Rr[0]) * u[0] + (Pp[1] - Rr[1]) * u[1]
            A = (Rr[0] + t * u[0], Rr[1] + t * u[1])
            F.line(S(Pp), S(A), "con")
            L = line_inter(Sz, A, (0, 0), (0, 1))
            F.line(S(Sz), S(L), "con")
            hgt = dist(A, Pp)
            v = ((A[0] - Sz[0]) / dist(A, Sz), (A[1] - Sz[1]) / dist(A, Sz)); w = (-v[1], v[0])
            Dd = (A[0] + hgt * w[0], A[1] + hgt * w[1])
            N = line_inter(Sz, Dd, L, (L[0] + w[0], L[1] + w[1]))
            F.line(S(A), S(Dd), "con"); F.line(S(Sz), S(N), "con"); F.line(S(L), S(N), "con")
            ln = dist(L, N)
            Fp = (L[0] + ln, L[1])
            F.line(S(L), S(Fp), "con")
            Bq = pol(1, ang(Fp))
            F.line(S((0, 0)), S(Bq), "aux", lw=0.7)
            # 3-D node
            Ph = (cosd(Az) * 0, 0, 0)
            node = math.degrees(math.atan2(ln, -L[1])) if False else ang(Fp)
            # exact: azimuth circle through zenith and horizon point P; its intersection with the equator plane
            hz = (Rr[0] + t * u[0], Rr[1] + t * u[1], hgt)
            z3 = (Sz[0], Sz[1], 0.0)
            # point of chord zenith-horizon point in the equator plane (x = 0)
            lam = -z3[0] / (hz[0] - z3[0])
            q3 = (0, z3[1] + lam * (hz[1] - z3[1]), lam * hz[2])
            F.check("ل ف equals the height of the chord's point in the equator plane", abs(ln - q3[2]) < 1e-9)
            for q, s, d in [(Rr, "ر", (-.06, .05)), (Tt, "ط", (.06, -.05)), (Sz, "س", (.03, .08)), (Pp, "ص", pol(.08, ang(Pp))),
                            (A, "ا", (-.03, -.08)), (L, "ل", (-.07, .03)), (Dd, "د", (-.06, .05)), (N, "ن", (.0, .08)),
                            (Fp, "ف", (.07, .0)), (Bq, "ب", pol(.08, ang(Bq)))]:
                F.lab(S(q), s, d, size=11)
            F.text(S((0, -1.2)), "المقدمة الأولى: وضع الخط المعدل", size=11)
        else:
            Lp = pol(1, ang(Tt) + 76)
            u = ((Tt[0] - Rr[0]), (Tt[1] - Rr[1])); ul = math.hypot(*u); u = (u[0] / ul, u[1] / ul)
            t = (Lp[0] - Rr[0]) * u[0] + (Lp[1] - Rr[1]) * u[1]
            Dd = (Rr[0] + t * u[0], Rr[1] + t * u[1])
            F.line(S(Lp), S(Dd), "con")
            ld = dist(Lp, Dd)
            v = ((Dd[0] - M_[0]) / dist(Dd, M_), (Dd[1] - M_[1]) / dist(Dd, M_)); w = (-v[1], v[0])
            Sx = (Dd[0] + ld * w[0], Dd[1] + ld * w[1])
            if Sx[1] < Dd[1] - 1e-9 and False: pass
            F.line(S(M_), S(Dd), "con"); F.line(S(Dd), S(Sx), "con"); F.line(S(M_), S(Sx), "con")
            ms = dist(M_, Sx)
            incl = 2 * asind(ms / 2)
            F.check(f"2 arcsin(م س / 2) is the inclination of the azimuth circle to the equator ({incl:.1f}°)", 0 < incl < 180)
            for q, s, d in [(Rr, "ر", (-.06, .05)), (Tt, "ط", (.06, -.05)), (Lp, "ل", pol(.08, ang(Lp))), (Dd, "د", (-.03, -.08)),
                            (Sx, "س", (.05, .06))]:
                F.lab(S(q), s, d, size=11)
            F.text(S((0, -1.2)), "المقدمة الثانية: ميل السمت", size=11)
        for q, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (.08, 0)), (H_, "ح", (0, .08)), (Y_, "ي", (0, -.08))]:
            F.lab(S(q), s, d, size=11)
    return F.save(out)

def fig73(out, phi=30.0, e=0.8):
    F = Fig(5.0, 5.0)
    section(F)
    Rr = pol(1, 180 - phi); Tt = pol(1, -phi); Sz = pol(1, 90 - phi); Ln = pol(1, -90 - phi)
    F.line(Rr, Tt, "fin", lw=1.0); F.line(Sz, Ln, "fin", lw=1.0)
    O = (-e, 0)
    F.line(O, Ln, "aux", lw=0.7); F.line((O[0], -1.05), (O[0], 1.05), "aux", lw=0.6)
    F.check("the angle ل ع ه is acute: the prime vertical is an ellipse", gproj.kind(Sz, Ln, e) == "ellipse")
    for q, s, d in [(Rr, "ر", (-.06, .05)), (Tt, "ط", (.06, -.05)), (Sz, "س", (.04, .08)), (Ln, "ل", (-.04, -.08)),
                    ((0, 0), "ه", (.06, -.05)), (O, "ع", (0, -.08))]:
        F.lab(q, s, d, size=12)
    return F.save(out)

def azimuth_params(phi=30.0, A=78.0):
    """Node arc (ك س) and inclination (ميل السمت) of the azimuth circle A° from the south point."""
    # pole of the azimuth circle: on the horizon, 90° from its horizon points
    zen = np.array([cosd(phi), sind(phi) * 0, 0.0])
    # 3-D frame: x toward the north pole, y toward ح (south part of meridian above equator), z east-west
    Zv = np.array([sind(phi), cosd(phi), 0.0])                       # zenith
    Sv = np.array([-cosd(phi), sind(phi), 0.0])                      # south point of the horizon
    Ev = np.array([0, 0, 1.0])                                       # east point
    Hp = cosd(A) * Sv + sind(A) * Ev                                  # horizon point of the circle
    n = np.cross(Zv, Hp); n /= np.linalg.norm(n)
    incl = acosd(abs(n[0]))
    # node: intersection with the equator plane x = 0, direction perpendicular to n within the plane
    d = np.cross(n, np.array([1.0, 0, 0])); d /= np.linalg.norm(d)
    node = acosd(abs(d[2]))
    return node, incl

def azimuth_conic(F, cx, e, sgn, title, kind_expected):
    S = lambda p: (p[0] + cx, p[1])
    F.circle((cx, 0), 1.0, "fin"); F.line(S((-1, 0)), S((1, 0)), "fin", lw=0.7); F.line(S((0, -1)), S((0, 1)), "fin", lw=0.7)
    node, incl = azimuth_params()
    Ss = pol(1, 180 + sgn * node)                     # arc ك س = node arc
    F.line(S((0, 0)), S(Ss), "con")
    nrm = (-Ss[1], Ss[0])
    Jj = (nrm[0] * 1.0, nrm[1] * 1.0); Dd = (-nrm[0], -nrm[1])
    F.line(S(Jj), S(Dd), "con")
    Tt = pol(1, 90 - incl); Ll = pol(1, -90 - incl)      # arcs ح ط = ي ل = ميل السمت
    F.line(S(Tt), S(Ll), "fin", lw=1.0)
    O = (-e, 0)
    k = gproj.kind(Tt, Ll, e)
    F.check(f"{title}: the angle at ع gives a {k}", k == kind_expected)
    R = line_inter(O, Tt, (0, 0), (0, 1))
    F.line(S(O), S(R), "con")
    if k != "parabola":
        N = line_inter(O, Ll, (0, 0), (0, 1))
        F.line(S(O), S(N) if abs(N[1]) < 3 else S(Ll), "con")
    else:
        F.line(S(O), S(Ll), "con")
    for q, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (.08, 0)), (H_, "ح", (0, .08)), (Y_, "ي", (0, -.08)), (Tt, "ط", pol(.08, ang(Tt))),
                    (Ll, "ل", pol(.08, ang(Ll))), (Ss, "س", pol(.08, ang(Ss))), (Jj, "ج", pol(.08, ang(Jj))), (Dd, "د", pol(.08, ang(Dd))),
                    (O, "ع", (0, -.08)), (R, "ر", (.06, .04))]:
        F.lab(S(q), s, d, size=11)
    F.text(S((0, -1.2)), title, size=11)
    return node, incl

def latus_triangle(F, off, Ss_len, a_kind, scale=0.55):
    pass

def fig74(out):
    F = Fig(9.0, 4.6)
    n1, i1 = azimuth_conic(F, 2.4, 0.8, -1, "الأولى (الربع الشرقي الجنوبي)", "ellipse")
    n2, i2 = azimuth_conic(F, 0.0, 0.8, +1, "الثانية (الربع الغربي الجنوبي)", "ellipse")
    F.check(f"node arc ك س = {n1:.1f}°, ميل السمت = {i1:.1f}° (latitude 30°, 78° from the south point)", abs(n1 - 23.0) < 0.6)
    return F.save(out)

def fig75(out):
    F = Fig(9.0, 4.6)
    node, incl = azimuth_params()
    e = sind(incl)
    azimuth_conic(F, 2.4, e, -1, "الأولى", "parabola")
    azimuth_conic(F, 0.0, e, +1, "الثانية", "parabola")
    return F.save(out)

def fig76(out):
    F = Fig(5.0, 4.8)
    azimuth_conic(F, 0.0, 0.25, -1, "الأولى", "hyperbola")
    return F.save(out)

# --------------------------------------------------------------------------- 77 / 78 star heads
def star_head(F, lam, beta, e, first=True):
    section(F, labels=False)
    O = (-e, 0)
    if first:
        Gc = pol(1, 90 + EPS); Dc = pol(1, -90 + EPS)      # ج ه د the ecliptic (ج Capricorn)
        F.line(Gc, Dc, "fin", lw=0.9)
        R = pol(1, 90 + EPS - beta); T = pol(1, -90 + EPS + beta)
        # the circle of latitude through the star: trace ر ط parallel to ج ه د
        R = pol(1, ang(Gc) - beta); T = pol(1, ang(Dc) + beta)
        dist_sol = (lam - 90)            # from the summer solstice
    else:
        R = pol(1, 90 + 0 - 0); T = R
    return O

def fig77(out, lam=45.0, beta=20.0, e=0.5):
    F = Fig(5.4, 5.4)
    section(F, labels=False)
    O = (-e, 0)
    Gc = pol(1, 90 + EPS); Dc = pol(1, -90 + EPS)
    F.line(Gc, Dc, "fin", lw=0.9)
    R = pol(1, 90 + EPS - beta); T = pol(1, -90 + EPS - beta)
    # circle of latitude beta: parallel to the ecliptic, at sin beta toward ح's side (north pole of ecliptic)
    nvec = (cosd(EPS), sind(EPS))          # unit normal of the ecliptic toward the north ecliptic pole
    c = (nvec[0] * sind(beta), nvec[1] * sind(beta)); rho = cosd(beta)
    u = (sind(EPS) * -1, cosd(EPS))
    u = (-nvec[1], nvec[0])
    R = (c[0] + rho * u[0], c[1] + rho * u[1]); T = (c[0] - rho * u[0], c[1] - rho * u[1])
    F.line(R, T, "con")
    F.arc(c, rho, ang(T, c), ang(T, c) + 180, "con", lw=0.8)
    d_sol = 90 - lam                      # distance of the star's degree from the summer solstice
    Lp = pol(rho, ang(T, c) + d_sol, c)
    t = (Lp[0] - c[0]) * u[0] + (Lp[1] - c[1]) * u[1]
    Bf = (c[0] + t * u[0], c[1] + t * u[1])
    hgt = dist(Lp, Bf)
    F.line(Lp, Bf, "con")
    S_ = line_inter(O, Bf, (0, 0), (0, 1))
    F.line(O, S_, "con")
    v = ((Bf[0] - O[0]) / dist(O, Bf), (Bf[1] - O[1]) / dist(O, Bf)); w = (-v[1], v[0])
    Fp = (Bf[0] + hgt * w[0], Bf[1] + hgt * w[1])
    N = line_inter(O, Fp, S_, (S_[0] + w[0], S_[1] + w[1]))
    F.line(Bf, Fp, "con"); F.line(O, N, "con"); F.line(S_, N, "con")
    Pp = (S_[0] - dist(S_, N), S_[1])
    F.line(S_, Pp, "con", lw=1.1)
    F.dot(Pp, RED, 8)
    # 3-D: the star in the colure frame and its projection from ع
    star3 = (Bf[0], Bf[1], hgt)
    img = gproj.proj(star3, e)
    F.check("ص is the projection from ع of the star (the head on the rete)", abs(img[0] - S_[1]) < 1e-9 and abs(img[1] - dist(S_, N)) < 1e-9)
    for q, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (.08, 0)), (H_, "ح", (0, .08)), (Y_, "ي", (0, -.08)), (Gc, "ج", pol(.08, ang(Gc))),
                    (Dc, "د", pol(.08, ang(Dc))), (R, "ر", pol(.08, ang(R))), (T, "ط", pol(.08, ang(T))), (Lp, "ل", pol(.08, ang(Lp, c))),
                    (Bf, "ب", (.06, -.05)), (O, "ع", (0, -.08)), (S_, "س", (.06, -.05)), (Fp, "ف", (.06, .05)), (N, "ن", (.0, .08)),
                    (Pp, "ص", (-.07, .0)), ((0, 0), "ه", (.05, -.07))]:
        F.lab(q, s, d, size=11)
    return F.save(out)

def fig78(out, e=0.5):
    F = Fig(5.4, 5.4)
    section(F, labels=False, axis_ext=(1.0, 1.25))
    O = (-e, 0)
    ra_, dec = eq_from_ecl(333, 48)
    # the star's day circle: trace ر ط parallel to ح ي at sin(dec) toward م
    xc = sind(dec); rho = cosd(dec)
    R = (xc, rho); T = (xc, -rho)
    F.line(R, T, "con")
    F.arc((xc, 0), rho, -90, 90, "con", lw=0.8)
    Jj = (xc + rho, 0)
    culm = ra_                                          # culminating degree's right ascension
    arc_jl = (culm - 270) % 360 if False else abs(((culm - 360) + 360) % 360 - 360)
    arc_jl = 360 - culm if culm > 180 else culm
    Lp = pol(rho, arc_jl, (xc, 0))
    Bf = (xc, Lp[1])
    hgt = abs(Lp[0] - xc)
    F.line(Lp, Bf, "con")
    S_ = line_inter(O, Bf, (0, 0), (0, 1))
    F.line(O, S_, "con")
    v = ((Bf[0] - O[0]) / dist(O, Bf), (Bf[1] - O[1]) / dist(O, Bf)); w = (-v[1], v[0])
    Fp = (Bf[0] + hgt * w[0], Bf[1] + hgt * w[1])
    N = line_inter(O, Fp, S_, (S_[0] + w[0], S_[1] + w[1]))
    F.line(Bf, Fp, "con"); F.line(O, N, "con"); F.line(S_, N, "con")
    Pp = (S_[0] - dist(S_, N), S_[1])
    F.line(S_, Pp, "con", lw=1.1); F.dot(Pp, RED, 8)
    img = gproj.proj((Bf[0], Bf[1], hgt), e)
    F.check("ص is the projection from ع of the star (the same head as the first way)", abs(img[0] - S_[1]) < 1e-9)
    for q, s, d in [(K_, "ك", (-.08, 0)), (M_, "م", (-.05, -.07)), (H_, "ح", (0, .08)), (Y_, "ي", (0, -.08)), (R, "ر", (.03, .08)),
                    (T, "ط", (.03, -.08)), (Jj, "ج", (.08, 0)), (Lp, "ل", pol(.08, ang(Lp, (xc, 0)))), (Bf, "ب", (-.07, .0)),
                    (O, "ع", (0, -.08)), (S_, "س", (.06, -.05)), (Fp, "ف", (.0, .08)), (N, "ن", (-.06, .04)), (Pp, "ص", (-.07, .0))]:
        F.lab(q, s, d, size=11)
    return F.save(out)

FIGS = {55: fig55, 56: fig56, 57: fig57, 58: fig58, 59: fig59, 60: fig60, 61: fig61, 62: fig62, 63: fig63, 64: fig64,
        65: fig65, 66: fig66, 67: fig67, 68: fig68, 69: fig69, 70: fig70, 71: fig71, 72: fig72, 73: fig73, 74: fig74,
        75: fig75, 76: fig76, 77: fig77, 78: fig78}
