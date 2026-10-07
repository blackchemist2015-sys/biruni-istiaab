"""Chapter 4 - the back of the astrolabe (Figs. 25-30, ff. 28r-33v)."""
from figlib import *
from ch1 import TENS

def back(F, R0=1.0, R1=0.965, R2=0.93):
    F.circle((0, 0), R0, "con", lw=1.0); F.circle((0, 0), R1, "con", lw=0.8); F.circle((0, 0), R2, "con", lw=0.6)

def fig25(out):
    F = Fig(5.6, 5.6)
    R0, R1, R2, R3 = 1.0, 0.86, 0.84, 0.82
    F.circle((0, 0), R0, "con"); F.circle((0, 0), R1, "con", lw=0.8); F.circle((0, 0), R3, "con", lw=0.7)
    F.line((-R0, 0), (R0, 0), "con"); F.line((0, -R0), (0, R0), "con")
    # the altitude quadrant ا د graduated from د (0) to ا (90)
    for k in range(91):
        F.line(pol(R3, k), pol(R2 if k % 5 else R1, k), "redthin")
    for k in range(0, 360, 10):
        F.line(pol(R1, k), pol(R0, k), "con", lw=0.6)
    for v in range(10, 91, 10):
        F.rtext(pol((R0 + R1) / 2, v - 5), TENS[v], v - 5, size=12)
    # from every tenth degree a line parallel to ب ه د as far as the radius ه ا: the sines
    for k in range(10, 90, 10):
        p = pol(R3, k)
        F.line(p, (0, p[1]), "con", lw=0.7)
        F.check(f"the line from {k}° cuts ه ا at the sine of {k}°", abs(p[1] / R3 - sind(k)) < 1e-12) if k == 30 else None
    # the radius ه د divided into 60 equal parts, numbered by tens
    yb = -0.075
    F.line((0, yb), (R3, yb), "con", lw=0.8)
    F.line((0, yb - 0.075), (R3, yb - 0.075), "con", lw=0.8)
    for k in range(61):
        x = k * R3 / 60
        F.line((x, 0), (x, -0.025 if k % 5 else -0.045), "redthin")
        if k % 10 == 0:
            F.line((x, yb), (x, yb - 0.075), "con", lw=0.7)
    for j, v in enumerate(range(10, 61, 10)):
        F.text(((j + 0.5) * R3 / 6, yb - 0.04), TENS[v], size=11)
    for p, s, d in [((0, R0), "ا", (0, .07)), ((-R0, 0), "ب", (-.07, 0)), ((0, -R0), "ج", (0, -.08)),
                    ((R0, 0), "د", (.07, 0)), ((0, 0), "ه", (-.05, .05))]:
        F.lab(p, s, d)
    return F.save(out)

SIGN_DECL = [-EPS, decl(300), decl(330), 0.0, decl(30), decl(60), EPS]   # Capricorn ... Cancer

def day_radii(r_in=0.28, r_out=0.86):
    return [r_in + i * (r_out - r_in) / 6 for i in range(7)]

def seasonal_hours(F, phi, radii, label=True):
    """Seasonal-hour lines in the altitude quadrant (upper left, 0° on the left, 90° at the top)."""
    for r in radii:
        F.arc((0, 0), r, 90, 180, "con", lw=0.7)
    lines = []
    for k in range(1, 7):
        pts = []
        for r, d in zip(radii, SIGN_DECL):
            H0 = acosd(-tand(phi) * tand(d))
            t = H0 * (1 - k / 6)
            a = asind(sind(phi) * sind(d) + cosd(phi) * cosd(d) * cosd(t))
            pts.append(pol(r, 180 - a))
        lines.append(pts)
        xs, ys = zip(*pts)
        F.curve(xs, ys, "con", lw=0.9)
    return lines

def fig26(out, phi=36.0):
    F = Fig(5.6, 5.6)
    back(F)
    F.line((-1, 0), (1, 0), "con", lw=0.8); F.line((0, -1), (0, 1), "con", lw=0.8)
    F.circle((0, 0), 0.16, "con"); F.circle((0, 0), 0.07, "con")
    radii = day_radii(0.2, 0.86)
    # altitude scale on the upper-left limb
    for k in range(91):
        F.line(pol(0.93, 180 - k), pol(0.9 if k % 5 else 0.88, 180 - k), "redthin")
    for k in range(0, 91, 10):
        F.line(pol(0.965, 180 - k), pol(1.0, 180 - k), "con", lw=0.5)
    for v in range(10, 91, 10):
        F.rtext(pol(0.982, 180 - v + 5), TENS[v], 180 - v + 5, size=8)
    hl = seasonal_hours(F, phi, radii)
    # the opposite quadrant: noon and the two afternoon-prayer lines
    for r in radii:
        F.arc((0, 0), r, 270, 360, "con", lw=0.7)
    names = ["الزوال", "أول العصر", "آخر العصر"]
    for n in range(3):
        pts = []
        for r, d in zip(radii, SIGN_DECL):
            hn = 90 - phi + d
            h = hn if n == 0 else atand(1 / (1 / tand(hn) + n))
            pts.append(pol(r, -h))
        xs, ys = zip(*pts)
        F.curve(xs, ys, "con", lw=1.0)
        F.rtext(pol(0.9, ang(pts[-1]) + 1), names[n], ang(pts[-1]), size=9)
    F.check("the sixth seasonal hour coincides with the noon line (opposite quadrant)",
            all(abs(ang(p) - 180 + (90 - phi + d)) < 1e-9 for p, d in zip(hl[5], SIGN_DECL)))
    return F.save(out)

def fig27(out, phi=36.0):
    F = Fig(5.6, 5.6)
    back(F)
    F.line((-1.02, 0), (1.02, 0), "con", lw=0.8); F.line((0, -1), (0, 1), "con", lw=0.8)
    F.circle((0, 0), 0.2, "con", lw=1.2); F.circle((0, 0), 0.08, "con")
    radii = day_radii(0.2, 0.86)
    for r in radii:
        F.line((-r, 0), (-r, 0), "con")
    hl = seasonal_hours(F, phi, radii)
    F.line((-0.86, -0.06), (-0.2, -0.06), "con", lw=0.6)
    for r in radii:
        F.line((-r, 0), (-r, -0.06), "con", lw=0.6)
    F.check("the sixth hour line is the noon line: altitude 90 − φ + δ on every day-circle",
            all(abs((180 - ang(p)) - (90 - phi + d)) < 1e-9 for p, d in zip(hl[5], SIGN_DECL)))
    return F.save(out)

def analemma(F, ox, phi, d, a, title):
    o = (ox, 0)
    F.circle(o, 1.0, "con", lw=0.9)
    P = lambda q: (q[0] + ox, q[1])
    A = P((0, 1)); B = P((-1, 0)); G = P((0, -1)); Dd = P((1, 0)); E = o
    F.line(B, Dd, "fin", lw=0.7); F.line(A, G, "fin", lw=0.7)
    Z = P(pol(1, 180 - phi)); H = P(pol(1, -phi))
    F.line(Z, H, "con", lw=0.8)
    L = P(pol(1, 180 - phi - a))
    labs = [(A, "ا", (0, .09)), (B, "ب", (-.08, 0)), (G, "ج", (0, -.09)), (Dd, "د", (.08, 0)),
            (E, "ه", (.06, -.06)), (Z, "ز", (-.07, .03)), (H, "ح", (.07, -.03)), (L, "ل", (-.03, .08))]
    if d == 0:
        M = (ox, sind(a) / cosd(phi))
        F.line(L, M, "con");
        S = (ox - math.sqrt(1 - M[1] ** 2), M[1])
        F.line(M, S, "con")
        F.arc(o, 1.0, ang(S, o), 180, "con", lw=2.0)
        t = 90 - acosd(M[1])
        labs += [(M, "م", (.06, 0)), (S, "س", (-.07, .03))]
        T_ = 90 - (180 - ang(S, o)) + 90
        F.check("arc س ب equals the hour angle from sunrise (equinox)",
                abs((180 - ang(S, o)) - (90 - acosd(sind(a) / cosd(phi)))) < 1e-9)
    else:
        T = P(pol(1, 90 - d))
        xt = sind(d)
        Ff = (ox + xt, 0)
        Y = (ox + xt, -xt * tand(phi))
        F.line(T, Y if Y[1] < 0 else Ff, "con")
        F.line(T, Ff, "con")
        my = (sind(a) - sind(phi) * sind(d)) / cosd(phi)
        M = (ox + xt, my)
        F.line(L, M, "con")
        rd = cosd(d)
        ky = Y[1]
        K = (Ff[0] - math.sqrt(rd * rd - ky * ky), ky)
        S = (Ff[0] - math.sqrt(rd * rd - my * my), my)
        F.arc(Ff, rd, 90, ang(K, Ff), "con", lw=0.8)
        F.line(Y, K, "con"); F.line(M, S, "con")
        F.arc(Ff, rd, ang(S, Ff), ang(K, Ff), "con", lw=2.0)
        H0 = acosd(-tand(phi) * tand(d))
        F.check(f"arc ط ك is the half day-arc (δ={d}°)", abs(((ang(K, Ff) - 90) % 360) - H0) < 1e-9)
        t = acosd((sind(a) - sind(phi) * sind(d)) / (cosd(phi) * cosd(d)))
        F.check(f"arc ط س is the hour angle of the altitude {a}° (δ={d}°)", abs(((ang(S, Ff) - 90) % 360) - t) < 1e-9)
        labs += [(T, "ط", (.03, .08)), (M, "م", (.07, 0)), (Ff, "ف", (.06, -.06)), (Y, "ي", (.07, -.02)),
                 (K, "ك", (-.07, 0)), (S, "س", (-.07, .03))]
    for p, s, dd in labs:
        F.lab(p, s, dd, size=12)
    F.text((ox, -1.32), title, size=12)

def fig28(out, phi=33.0):
    F = Fig(10.5, 3.9)
    analemma(F, 4.6, phi, 0, 35, "الاعتدال")
    analemma(F, 2.3, phi, -20, 25, "الميل الجنوبي")
    analemma(F, 0.0, phi, 20, 40, "الميل الشمالي")
    return F.save(out)

def fig29(out, k=4.0):
    F = Fig(6.0, 5.6)
    AB = 3.0
    da = AB / k
    A = (0, 0); B = (AB, 0); Dd = (0, da); G = (AB, da)
    Hh = (0, da - AB)
    F.line(Dd, G, "con"); F.line(A, B, "con", lw=1.2); F.line(Dd, Hh, "con"); F.line(B, G, "con")
    F.arc(Dd, AB, -90, 0, "con")
    pts = []
    names = "زحطيك"
    marks = "لمسعف"
    for i in range(1, 6):
        q = pol(AB, -90 + 15 * i, Dd)
        m = line_inter(Dd, q, A, B)
        F.line(Dd, q, "con", lw=0.7)
        F.lab(q, names[i - 1], (pol(0.09, -90 + 15 * i)), size=12)
        F.lab(m, marks[i - 1], (0, -0.08), size=12)
        F.check(f"ا{marks[i-1]} = دا · tan {15*i}°", abs(m[0] - da * tand(15 * i)) < 1e-9) if i in (1, 3) else None
    for p, s, d in [(A, "ا", (-.08, 0)), (B, "ب", (.06, -.06)), (Dd, "د", (-.07, .04)), (G, "ج", (.07, .04)),
                    (Hh, "ه", (-.07, -.03))]:
        F.lab(p, s, d, size=12)
    return F.save(out)

def fig30(out):
    F = Fig(5.4, 5.4)
    R = 1.0
    F.circle((0, 0), R, "con")
    F.line((-R, 0), (R, 0), "con"); F.line((0, -R), (0, R), "con")
    Z = pol(R, -45); T = (Z[0], 0); H = (0, Z[1])
    s = Z[0]
    w = 0.07
    # ladders along ز ط and ز ح divided into twelve parts
    F.line(T, Z, "con", lw=1.0); F.line(H, Z, "con", lw=1.0)
    F.line((T[0] - w, 0), (T[0] - w, Z[1] + w), "con", lw=0.8)
    F.line((0, Z[1] + w), (T[0] - w, Z[1] + w), "con", lw=0.8)
    for i in range(1, 13):
        y = -s * i / 12
        F.line((T[0] - w, y), (T[0], y), "con", lw=0.6)
        x = s * i / 12
        F.line((x, Z[1]), (x, Z[1] + w), "con", lw=0.6)
        for j in range(1, 4):
            F.line((T[0], y + s / 48 * j), (T[0] + 0.02, y + s / 48 * j), "redthin")
            F.line((x - s / 48 * j, Z[1]), (x - s / 48 * j, Z[1] - 0.02), "redthin")
        if i % 2 == 0:
            F.text((T[0] - w / 2, y + s / 24), abjad(i), size=7.5)
            F.text((x - s / 24, Z[1] + w / 2), abjad(i), size=7.5)
    F.check("ز is the middle of the quadrant ج د, so the square is 12 by 12", abs(ang(Z) + 45) < 1e-12)
    for p, st, d in [((-R, 0), "ا", (-.07, 0)), ((0, R), "ب", (0, .07)), ((R, 0), "ج", (.07, 0)),
                     ((0, -R), "د", (0, -.08)), ((0, 0), "ه", (-.06, -.06)), (Z, "ز", (.05, -.06)),
                     (T, "ط", (0.0, .07)), (H, "ح", (-.07, 0))]:
        F.lab(p, st, d, size=12)
    return F.save(out)

FIGS = {25: fig25, 26: fig26, 27: fig27, 28: fig28, 29: fig29, 30: fig30}
