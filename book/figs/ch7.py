"""Chapter 7 - the complete astrolabe by cylindrical projection (Figs. 52-54, ff. 62r-63r)."""
from figlib import *

def deviation(phi, A):
    """Inclination i of an azimuth circle (A from the east point) to the equator, and the
    deviation of its line of nodes from the meridian, in the orthographic projection."""
    ci = cosd(phi) * cosd(A)
    i = acosd(ci)
    dev = acosd(sind(A) / sind(i))
    return i, dev

def fig52(out, phi=36.0, A=20.0):
    F = Fig(5.6, 5.6)
    E = (0, 0)
    F.circle(E, 1.0, "fin")
    F.line((-1, 0), (1, 0), "fin", lw=0.7); F.line((0, -1), (0, 1), "fin", lw=0.7)
    i, dv = deviation(phi, A)
    ci = cosd(i)
    Z = pol(1, 90 + dv); T = pol(1, -90 + dv); H = pol(1, 90 - dv); K = pol(1, -90 - dv)
    Y = pol(1, dv); N = pol(1, 180 + dv); M = pol(1, 180 - dv); L = pol(1, -dv)
    for p, q in ((Z, T), (H, K), (Y, N), (M, L)):
        F.line(p, q, "con", lw=0.9)
    Fp = pol(ci, dv); Sp = pol(ci, 180 + dv); Ap = pol(ci, 180 - dv); Sq = pol(ci, -dv)
    # the two ellipses (not drawn in the manuscript) - grey
    for ax in (90 + dv, 90 - dv):
        t = np.linspace(0, 2 * math.pi, 400)
        x = np.cos(t); y = ci * np.sin(t)
        X = x * cosd(ax) - y * sind(ax); Y_ = x * sind(ax) + y * cosd(ax)
        F.curve(X, Y_, "aux", lw=0.8)
    # check against the 3-D azimuth circle: the zenith projects at cos φ on ه د
    zen = (0, cosd(phi))
    ax = 90 + dv
    u = zen[0] * cosd(ax) + zen[1] * sind(ax); v = -zen[0] * sind(ax) + zen[1] * cosd(ax)
    F.check("the ellipse passes through the image of the zenith (cos φ on ه د)", abs(u * u + (v / ci) ** 2 - 1) < 1e-9)
    F.check("minor semi-axis = cos i = cos φ · cos A", abs(ci - cosd(phi) * cosd(A)) < 1e-12)
    F.check("the major axis lies along the line of nodes, deviation from the meridian = arccos(sin A / sin i)",
            abs(cosd(dv) - sind(A) / sind(i)) < 1e-12)
    for p, s, d in [((-1, 0), "ا", (-.07, 0)), ((0, -1), "ب", (0, -.08)), ((1, 0), "ج", (.07, 0)), ((0, 1), "د", (0, .08)),
                    (E, "ه", (.06, .05)), (Z, "ز", pol(.08, 90 + dv)), (T, "ط", pol(.08, -90 + dv)), (H, "ح", pol(.08, 90 - dv)),
                    (K, "ك", pol(.08, -90 - dv)), (Y, "ي", pol(.08, dv)), (N, "ن", pol(.08, 180 + dv)), (M, "م", pol(.08, 180 - dv)),
                    (L, "ل", pol(.08, -dv)), (Fp, "ف", (.0, .07)), (Sp, "ص", (0, -.07)), (Ap, "ع", (0, .07)), (Sq, "س", (0, -.07))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

def fig53(out, phi=36.0, A=20.0):
    F = Fig(6.0, 3.6)
    E = (0, 0)
    F.arc(E, 1.0, 0, 180, "con"); F.line((-1, 0), (1, 0), "con")
    A_ = (1, 0); S_ = (-1, 0)
    B = pol(1, 90 - phi)
    G = pol(1, 90 - phi + A)
    Dd = (B[0] * (G[0] * B[0] + G[1] * B[1]), B[1] * (G[0] * B[0] + G[1] * B[1]))   # foot of ج on ه ب
    Zx = math.sqrt(1 - Dd[1] ** 2)
    Z = (Zx, Dd[1])
    H = (Z[0], 0)
    cd = dist(G, Dd)
    T = (cd, 0)
    K = line_inter(T, (T[0], 1), E, Z)
    u = (Z[0], Z[1]); n = (-u[1], u[0])
    L = None
    for p in line_circle(K, (K[0] + n[0], K[1] + n[1]), E, 1.0):
        if p[1] > 0: L = p
    for p, q in ((E, B), (G, Dd), (Dd, Z), (Z, H), (E, Z), (T, K), (K, L)):
        F.line(p, q, "con")
    i, dv = deviation(phi, A)
    F.close_enough("ز ح = cos i (minor semi-axis)", Z[1], cosd(i))
    F.close_enough("arc ز ل = the deviation", abs(ang(L) - ang(Z)), dv)
    for p, s, d in [(A_, "ا", (.06, -.03)), (S_, "س", (-.06, -.03)), (E, "ه", (0, -.08)), (B, "ب", (.05, .06)),
                    (G, "ج", (.03, .07)), (Dd, "د", (-.06, .02)), (Z, "ز", (.06, .05)), (H, "ح", (0, -.08)),
                    (T, "ط", (0, -.08)), (K, "ك", (.06, .02)), (L, "ل", (0, .07))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

def fig54(out):
    F = Fig(5.0, 4.2)
    a, b = 1.0, 0.6
    E = (0, 0)
    A = (a, 0); B = (-a, 0); G = (0, -b); Dd = (0, b)
    F.line((-1.2, 0), (1.2, 0), "con", lw=0.9); F.line((0, -b - 0.05), (0, 0.95), "con", lw=0.9)
    c = math.sqrt(a * a - b * b)
    H = (c, 0); Z = (-c, 0)
    F.arc(G, a, ang(H, G), ang(Z, G), "con")
    F.line(G, H, "con"); F.line(G, Z, "con")
    F.close_enough("ه ح = √(ه ا² − ه ج²)", dist(E, H), c)
    t = np.linspace(0, 2 * math.pi, 300)
    F.curve(a * np.cos(t), b * np.sin(t), "aux", lw=0.8)
    p = (a * cosd(115), b * sind(115))
    F.check("for every point ن of the curve ح ن + ن ز = ا ب", abs(dist(H, p) + dist(Z, p) - 2 * a) < 1e-12)
    for q, s, d in [(A, "ا", (.07, .05)), (B, "ب", (-.07, .05)), (G, "ج", (0, -.08)), (Dd, "د", (.05, .3)),
                    (E, "ه", (.05, .06)), (H, "ح", (.04, .07)), (Z, "ز", (-.04, .07))]:
        F.lab(q, s, d, size=13)
    return F.save(out)

FIGS = {52: fig52, 53: fig53, 54: fig54}
