"""Chapter 2 - horizon, almucantars, azimuths and star heads (Figs. 7-16, ff. 12r-20r)."""
from figlib import *

def labels(F, items, size=13):
    for p, s, d in items:
        F.lab(p, s, d, size=size)

def fig07(out, phi=33.0, h=6.0):
    """Horizon and the 6th almucantar by Biruni's construction on the equator circle."""
    F = Fig(4.6, 7.4)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    F.circle(E, 1.0, "fin"); F.circle(E, Re, "fin")
    F.line((-1.0, 0), (1.0, 0), "fin")
    K = (-Re, 0); M = (Re, 0)
    Z = pol(Re, 180 - phi); T = pol(Re, -phi)
    N = pol(Re, 180 - phi - h); Y = pol(Re, -phi + h)
    S = line_inter(K, T, (0, 0), (0, 1)); L = line_inter(K, Z, (0, 0), (0, 1))
    Fq = line_inter(K, Y, (0, 0), (0, 1)); Sd = line_inter(K, N, (0, 0), (0, 1))
    Ain = mid(S, L); Q = mid(Fq, Sd)
    top = L[1] + 0.12
    F.line((0, -1.0), (0, top), "fin", lw=0.8)
    # the board beyond the plate (حد اللوح)
    F.poly([(-0.09, 1.0), (-0.09, top), (0.09, top), (0.09, 1.0)], "con", lw=0.6)
    F.text((0.17, (1.0 + top) / 2 + 0.25), "حد اللوح", size=10, rot=-90)
    F.line(K, L, "con"); F.line(K, Sd, "con"); F.line(K, T, "con"); F.line(K, Y, "con")
    # horizon and almucantar, only inside the plate
    rh = dist(Ain, S); ra_ = dist(Q, Fq)
    F.arc_clip(Ain, rh, inside=[(E, 1.0)], kind="fin", lw=1.3)
    F.arc_clip(Q, ra_, inside=[(E, 1.0)], kind="fin", lw=1.3)
    c0, r0 = P.almucantar(phi, 0); c6, r6 = P.almucantar(phi, h)
    F.close_enough("centre ع of the horizon = midpoint of س ل", Ain[1], c0[1])
    F.close_enough("radius of the horizon", rh, r0)
    F.close_enough("centre ق of the 6th almucantar", Q[1], c6[1])
    F.close_enough("radius of the 6th almucantar", ra_, r6)
    # ends of the horizon and almucantar on the rim (ر ش)
    Rr = circle_circle(Q, ra_, E, 1.0)
    Rp = sorted(Rr, key=lambda p: p[0])
    labels(F, [(K, "ك", (-.07, -.03)), (M, "م", (.07, -.04)), (E, "ه", (.05, .05)),
               (Z, "ز", (-.06, .03)), (N, "ن", (-.05, .06)), (T, "ط", (.04, -.07)), (Y, "ي", (.07, -.02)),
               (S, "س", (.06, -.06)), (Fq, "ف", (-.06, -.05)), (Ain, "ع", (-.07, .0)), (Q, "ق", (-.07, .0)),
               (L, "ل", (-.08, .0)), (Sd, "ص", (-.08, .0)), (Rp[0], "ر", (-.06, .05)), (Rp[1], "ش", (.06, .05))])
    F.dot(Ain, RED, 5); F.dot(Q, RED, 5)
    F.text((0, -1.09), "الشمال", size=10, color=GREY)
    return F.save(out)

def plate_33(F, P, phi, step=6, hours=True, cancer=True, numbers=True):
    E = (0, 0)
    F.circle(E, 1.0, "fin", lw=1.3)
    rc = P.r_decl(EPS)
    if cancer: F.circle(E, rc, "fin", lw=0.8)
    F.circle(E, P.Re, "fin", lw=0.8)
    F.line((-1, 0), (1, 0), "fin", lw=0.8); F.line((0, -1), (0, 1), "fin", lw=0.8)
    for h in range(0, 90, step):
        c, r = P.almucantar(phi, h)
        F.arc_clip(c, r, inside=[(E, 1.0)], kind="fin" if h == 0 else "con",
                   lw=1.4 if h == 0 else 0.7)
    Z = P.zenith(phi)
    F.circle(Z, 0.012, "con")
    if numbers:
        for h in range(step, 84, step):
            c, r = P.almucantar(phi, h)
            pts = circle_circle(c, r, E, 0.93)
            if pts:
                for p in pts:
                    F.text(p, abjad(h), size=10, color=BLACK)
            else:
                F.text((c[0] - r + 0.03, c[1]), abjad(h), size=7, color=RED)
    if hours:
        # the twelve seasonal (unequal) hours of the night, below the horizon, between
        # the circle of Cancer and the rim (circle of Capricorn), numbered from the west
        decs = np.linspace(-EPS, EPS, 41)
        lines = []
        for k in range(13):
            pts = []
            for d in decs:
                H0 = acosd(-tand(phi) * tand(d))
                N = 180 - H0
                H = H0 + k * 2 * N / 12
                pts.append(P.eq(H, d))
            lines.append(pts)
            if 0 < k < 12:
                xs, ys = zip(*pts)
                F.curve(xs, ys, "con", lw=0.7)
        for k in range(12):
            d = 0.0
            H0 = acosd(-tand(phi) * tand(-EPS * 0.55)); N = 180 - H0
            p = P.eq(H0 + (k + 0.5) * 2 * N / 12, -EPS * 0.55)
            F.text(p, abjad(k + 1), size=11)
        c, r = P.almucantar(phi, 0)
        F.check("hour line 6 is the lower meridian (midnight)",
                all(abs(p[0]) < 1e-9 for p in lines[6]))
        F.check("hour lines 0 and 12 lie on the horizon",
                all(abs(dist(p, c) - r) < 1e-9 for p in lines[0] + lines[12]))
    return Z

def fig08(out, phi=33.0):
    F = Fig(6.2, 6.4)
    P = Plate(1.0)
    Z = plate_33(F, P, phi)
    F.lab(Z, "ص", (0.04, 0.03), size=11)
    F.text((0, -0.36), "عرضه لج", size=13)
    F.text((0, 1.06), "الجنوب", size=11); F.text((0, -1.07), "الشمال", size=11)
    F.text((-1.08, 0.06), "المشرق", size=11, rot=90); F.text((1.07, 0.06), "المغرب", size=11, rot=-90)
    return F.save(out)

def fig09(out):
    """Division of the ecliptic in the rete with the dastur; north at the top as on f.13v."""
    F = Fig(6.0, 6.0)
    P = Plate(0.82)
    rot = lambda p: (-p[0], -p[1])          # Capricorn toward the south (bottom)
    E = (0, 0)
    Rd = 1.0
    F.circle(E, Rd, "con", lw=0.9)          # the dastur
    F.circle(E, 0.82, "fin")                 # rim of the rete = circle of Capricorn
    F.circle(E, P.Re, "fin", lw=0.7); F.circle(E, P.r_decl(EPS), "fin", lw=0.7)
    c, r = P.ecliptic(); c = rot(c)
    F.circle(c, r, "fin", lw=1.3)
    F.line((-Rd, 0), (Rd, 0), "con", lw=0.7); F.line((0, -Rd), (0, Rd), "con", lw=0.7)
    # sign divisions of the dastur on its eastern half (right), by right ascension
    R1, R2, R3 = 0.89, 0.94, 0.985
    F.arc(E, R1, -90, 90, "con", lw=0.8); F.arc(E, R2, -90, 90, "con", lw=0.6)
    for lam in range(270, 451, 30):
        a = ra(lam % 360) - 180 + 180          # rotated: Aries on the east (right)
        F.line(pol(R1, a), pol(Rd, a), "con", lw=0.8)
        if lam < 450:
            am = ra((lam + 15) % 360)
            F.rtext(pol((R2 + R3) / 2, am), SIGNS[((lam + 15) % 360) // 30], am, size=9, color=RED)
        for d in range(5, 30, 5):
            if lam + d < 450:
                ad = ra((lam + d) % 360)
                F.line(pol(R1, ad), pol(R2, ad), "redthin")
    # the bevelled alidade on the ends of Capricorn and Aquarius
    pts = {}
    for lam, l1, l2 in [(300, "ط", "ي"), (330, "ل", "ن")]:
        a = ra(lam)
        p1 = pol(Rd, a); p2 = pol(Rd, a + 180)
        F.line(p1, p2, "con", lw=0.7)
        q = [x for x in line_circle(p1, p2, c, r)]
        A = rot(P.ecl_point(lam)); B = rot(P.ecl_point(lam - 180))
        F.check(f"the alidade through the centre at RA {a:.2f}° meets the ecliptic at λ={lam}° and λ={lam-180}°",
                min(dist(A, x) for x in q) < 1e-9 and min(dist(B, x) for x in q) < 1e-9)
        pts[l1] = A; pts[l2] = B
    H = rot(P.ecl_point(270)); Zz = rot(P.ecl_point(90)); K = rot(P.ecl_point(0)); M = rot(P.ecl_point(180))
    labels(F, [(E, "ه", (.05, .05)), (H, "ح", (0, -.06)), (Zz, "ز", (.0, .06)), (K, "ك", (-.06, .04)),
               (M, "م", (-.06, .04)), (pts["ط"], "ط", (.06, -.02)), (pts["ي"], "ي", (-.05, .05)),
               (pts["ل"], "ل", (.06, .0)), (pts["ن"], "ن", (-.05, .05))])
    for p in (H, Zz, K, M, pts["ط"], pts["ي"], pts["ل"], pts["ن"]):
        F.dot(p, BLACK, 5)
    F.text((0, 1.06), "الشمال", size=11); F.text((0, -1.07), "الجنوب", size=11)
    F.text((1.08, 0), "المشرق", size=11, rot=-90); F.text((-1.08, 0), "المغرب", size=11, rot=90)
    return F.save(out)

def fig10(out, dN=20.0, dS=15.0):
    F = Fig(5.2, 5.6)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    F.circle(E, Re, "fin")                                   # equator ط ك ل م
    c, r = P.ecliptic(); F.circle(c, r, "fin", lw=0.9)       # ecliptic
    F.line((-1.0, 0), (1.0, 0), "fin", lw=0.8)
    T = (0, Re); K = (-Re, 0); L = (0, -Re); M = (Re, 0)
    Hh = (0, c[1] + r)
    Q = pol(Re, 90 - dN)              # arc ط ق to the right = northern declination
    N = pol(Re, 90 + dS)              # arc ط ن to the left = southern declination
    S = line_inter(K, Q, (0, 0), (0, 1)); A = line_inter(K, N, (0, 0), (0, 1))
    F.line(K, Q, "con"); F.line(K, A, "con")
    F.line((0, -1.0), (0, max(Hh[1], A[1]) + 0.05), "fin", lw=0.8)
    F.circle(E, dist(E, S), "fin", lw=0.8)
    F.circle(E, dist(E, A), "fin", lw=0.8)
    F.close_enough("ه س = radius of the northern star's day-circle", dist(E, S), P.r_decl(dN))
    F.close_enough("ه ع = radius of the southern star's day-circle", dist(E, A), P.r_decl(-dS))
    labels(F, [(E, "ه", (0.05, 0.06)), (T, "ط", (0.05, 0.05)), (K, "ك", (-0.07, -0.03)),
               (L, "ل", (0.05, -0.06)), (M, "م", (0.07, -0.04)), (Hh, "ح", (0, 0.07)),
               (Q, "ق", (0.06, 0.04)), (N, "ن", (-0.06, 0.04)), (S, "س", (-0.06, 0.04)),
               (A, "ع", (0.06, 0.04))])
    return F.save(out)

def fig11(out, dN=20.0, dS=15.0, lamN=62.0, lamS=312.0):
    """Habash's way: star heads from the declination and the culminating degree."""
    F = Fig(5.0, 6.0)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    c, r = P.ecliptic()
    F.circle(c, r, "fin"); F.circle(E, Re, "fin")
    F.line((-Re * 1.02, 0), (Re * 1.02, 0), "fin", lw=0.7)
    F.line((0, c[1] + r), (0, -Re), "fin", lw=0.7)
    # northern star: culminating degree ش (on the ecliptic), ه ش produced to the equator at ط
    Sh = P.ecl_point(lamN); a = ang(Sh)
    T = pol(Re, a)
    Nn = pol(Re, a + 90)                       # ط ن a quadrant
    Q = pol(Re, a - dN)                        # ط ق = declination, away from ن
    A = line_inter(Nn, Q, E, T)
    F.line(E, T, "con"); F.line(Nn, Q, "con")
    F.close_enough("ه ع = distance of the northern star's head", dist(E, A), P.r_decl(dN))
    # southern star: culminating degree ي, ه س ي; س ز = declination, س ص a quadrant
    Yy = P.ecl_point(lamS); b = ang(Yy)
    S = pol(Re, b)
    Sd = pol(Re, b - 90)
    Z = pol(Re, b - dS)                        # س ز = declination, toward ص
    Fp = line_inter(Sd, Z, E, S)
    F.line(E, Fp, "con"); F.line(Sd, Fp, "con")
    F.close_enough("ه ف = distance of the southern star's head", dist(E, Fp), P.r_decl(-dS))
    F.dot(A, RED, 6); F.dot(Fp, RED, 6)
    labels(F, [(E, "ه", (.06, .04)), (Sh, "ش", (-.06, .02)), (T, "ط", (-.03, -.07)), (Nn, "ن", (.07, -.02)),
               (Q, "ق", (-.06, -.04)), (A, "ع", (.06, -.02)), (Yy, "ي", (-.06, .05)), (S, "س", (-.07, .0)),
               (Sd, "ص", (.07, .0)), (Z, "ز", (.03, .07)), (Fp, "ف", (-.06, .03)),
               ((0, c[1] + r), "ح", (0, .07))])
    return F.save(out)

def azimuth_base(F, P, phi):
    Re = P.Re
    E = (0, 0)
    F.circle(E, Re, "fin")
    c0, r0 = P.almucantar(phi, 0)
    F.arc_clip(c0, r0, inside=[((0, 0), Re * 1.45)], kind="fin", lw=1.2)
    F.line((-Re, 0), (Re, 0), "fin", lw=0.6)
    return c0, r0

def fig12(out, phi=33.0, A=30.0):
    F = Fig(5.6, 6.0)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    c0, r0 = azimuth_base(F, P, phi)
    T = (0, Re); K = (-Re, 0); M = (Re, 0); L = (0, -Re)
    Z = pol(Re, 90 - phi)                         # arc ط ز = latitude
    S_ = line_inter(K, Z, (0, 0), (0, 1))         # zenith ص
    Nad = P.nadir(phi)
    Ain = mid(S_, Nad)                            # centre of the prime vertical
    rpv = dist(Ain, S_)
    F.circle(Ain, rpv, "con")
    F.line(K, Z, "con")
    F.line((-1.15, Ain[1]), (1.15, Ain[1]), "con")      # line of centres
    F.line((0, Re + 0.05), (0, Nad[1]), "fin", lw=0.6)
    Fp = pol(rpv, -90 + 2 * A, Ain)                    # arc ح ف = twice the azimuth
    Q = line_inter(S_, Fp, (0, Ain[1]), (1, Ain[1]))
    F.line(S_, Fp, "con")
    ca, ra_ = P.azimuth(phi, 90 - A)
    F.close_enough("ص is the zenith", S_[1], P.zenith(phi)[1])
    F.close_enough("ق is the centre of the azimuth circle", Q[0], ca[0], 1e-6)
    F.arc_clip(Q, dist(Q, S_), inside=[(E, Re * 1.3)], kind="aux", lw=0.7)
    Sx = (0, c0[1] - r0)
    labels(F, [(T, "ط", (0, .07)), (Z, "ز", (.05, .05)), (S_, "ص", (-.06, .04)), (E, "ه", (-.05, .05)),
               (K, "ك", (-.06, .04)), (M, "م", (.06, .04)), (Sx, "س", (-.06, -.04)), (Ain, "ع", (-.06, -.05)),
               (L, "ل", (-.06, -.05)), (Fp, "ف", (.06, -.03)), (Q, "ق", (.04, -.07)), (Nad, "ح", (0, -.08))])
    return F.save(out)

def fig13(out, phi=33.0, A=30.0):
    F = Fig(5.4, 5.6)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    F.circle(E, Re, "fin")
    F.line((-Re, 0), (Re, 0), "fin", lw=0.7)
    S_ = P.zenith(phi); Nad = P.nadir(phi); Ain = mid(S_, Nad)
    F.line((0, Re + 0.06), (0, -Re - 0.04), "fin", lw=0.7)
    F.line((-1.15, Ain[1]), (1.15, Ain[1]), "con")
    rs = 0.62 * Re                                        # a circle of any radius about the zenith
    F.circle(S_, rs, "fin", lw=0.8)
    A_ = (S_[0], S_[1] - rs); B = pol(rs, -90 + A, S_)
    Gp = (S_[0] + rs, S_[1]); Dp = (S_[0] - rs, S_[1])
    Q = line_inter(S_, B, (0, Ain[1]), (1, Ain[1]))
    F.line(S_, Q, "con")
    ca, _ = P.azimuth(phi, 90 - A)
    F.close_enough("ص ب produced meets the line of centres at the same centre ق", Q[0], ca[0], 1e-6)
    labels(F, [((0, Re), "ط", (0.05, -0.06)), (S_, "ص", (-0.06, 0.03)), (A_, "ا", (-0.05, -0.04)),
               (B, "ب", (0.06, -0.02)), (Gp, "ج", (0.06, 0.03)), (Dp, "د", (-0.06, 0.03)),
               (E, "ه", (-0.05, -0.05)), ((-Re, 0), "ك", (-0.07, 0)), ((Re, 0), "م", (0.07, 0)),
               ((0, Ain[1]), "ع", (-0.06, 0.04)), (Q, "ق", (0.05, -0.07)), ((0, -Re), "ز", (0.05, -0.06))])
    return F.save(out)

def fig14(out, phi=33.0, A=25.0):
    F = Fig(5.4, 5.6)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    c0, r0 = azimuth_base(F, P, phi)
    S_ = P.zenith(phi); Nad = P.nadir(phi); Ain = mid(S_, Nad)
    F.line((0, Re + 0.05), (0, -Re - 0.03), "fin", lw=0.7)
    F.line((-1.1, Ain[1]), (1.1, Ain[1]), "con")
    L = (0, -Re)
    Aq = pol(Re, -90 + A)                 # arc ل ا = the distance of the azimuth from the meridian
    hits = line_circle(S_, Aq, c0, r0)
    B = min(hits, key=lambda p: dist(p, Aq))
    F.line(S_, Aq, "con")
    ca, rr = P.azimuth(phi, 180 - A)      # azimuth measured from the north point
    F.check("ب lies on the azimuth circle whose centre is on the line of centres",
            abs(dist(ca, B) - rr) < 1e-9)
    F.arc_clip(ca, rr, inside=[(E, Re * 1.25)], kind="aux", lw=0.7)
    labels(F, [((0, Re), "ط", (0, .07)), (S_, "ص", (-.06, .03)), (E, "ه", (-.05, .05)),
               ((-Re, 0), "ك", (-.07, .03)), ((Re, 0), "م", (.07, .03)), (B, "ب", (.05, -.05)),
               ((0, Ain[1]), "ع", (-.06, -.04)), (L, "ل", (-.05, -.07)), (Aq, "ا", (.05, -.06))])
    return F.save(out)

def ecl_coord_circles(P):
    """Great circles of ecliptic longitude pass through the projected ecliptic pole."""
    pole = P.star(270, 90 - P.eps)
    return pole

def fig15(out):
    F = Fig(5.6, 6.4)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    c, r = P.ecliptic()
    F.circle(c, r, "fin"); F.circle(E, Re, "fin")
    F.line((-Re, 0), (Re, 0), "fin", lw=0.7); F.line((0, c[1] + r), (0, -Re * 1.15), "fin", lw=0.7)
    pole = ecl_coord_circles(P)
    F.close_enough("ص (pole of the ecliptic) lies at the zenith of latitude 90−ε", pole[1], P.zenith(90 - EPS)[1])
    out_pts = {}
    for lam, beta, l_e, l_s in [(200, 6, "ج", "د"), (97, -10, "ي", "س")]:
        ra_, de = eq_from_ecl(lam, 0); e_pt = P.star(ra_, de)
        ra2, de2 = eq_from_ecl(lam, beta); s_pt = P.star(ra2, de2)
        ra3, de3 = eq_from_ecl(lam, 40); x_pt = P.star(ra3, de3)
        cc, rr = circle3(pole, e_pt, x_pt)
        F.arc_clip(cc, rr, inside=[(E, 1.45)], kind="con", lw=0.9)
        F.check(f"the head of the star (λ={lam}°, β={beta}°) lies on its circle of longitude",
                abs(dist(cc, s_pt) - rr) < 1e-9)
        F.check(f"its ecliptic point lies on the ecliptic", abs(dist(c, e_pt) - r) < 1e-9)
        F.dot(s_pt, RED, 6); F.dot(e_pt, BLACK, 5)
        out_pts[l_e] = e_pt; out_pts[l_s] = s_pt
    labels(F, [((0, c[1] + r), "ح", (0, .07)), ((-Re, 0), "ك", (-.07, -.02)), ((Re, 0), "م", (.07, -.03)),
               (E, "ه", (.05, -.05)), (pole, "ص", (-.06, .03)), ((0, c[1] - r), "ز", (.05, -.06)),
               ((0, Re), "ط", (.05, .05)),
               (out_pts["ج"], "ج", (.07, .05)), (out_pts["د"], "د", (-.07, -.03)),
               (out_pts["ي"], "ي", (.06, .02)), (out_pts["س"], "س", (.06, -.03))])
    return F.save(out)

def fig16(out, d=10.0):
    F = Fig(5.0, 5.6)
    P = Plate(1.0)
    Re = P.Re
    E = (0, 0)
    c, r = P.ecliptic()
    F.circle(E, Re, "fin"); F.circle(c, r, "fin")
    K = (-Re, 0); M = (Re, 0)
    F.line(K, M, "fin", lw=0.7)
    phi_ = 90 - EPS                     # the ecliptic as the horizon of latitude 90 − ε
    A = pol(Re, 180 - phi_); B = pol(Re, -phi_)
    Rh = line_inter(K, A, (0, 0), (0, 1)); Bh = line_inter(K, B, (0, 0), (0, 1))
    F.close_enough("ك ا meets the meridian at the top of the ecliptic (ح)", Rh[1], c[1] + r)
    F.close_enough("ك ب meets the meridian at the bottom of the ecliptic (ر)", Bh[1], c[1] - r)
    G = pol(Re, 180 - phi_ + d); Dd = pol(Re, -phi_ - d)     # opposite to the altitude side
    S = line_inter(K, G, (0, 0), (0, 1)); Ai = line_inter(K, Dd, (0, 0), (0, 1))
    Fc = mid(S, Ai)
    F.circle(Fc, dist(Fc, S), "con")
    F.line(K, S, "con"); F.line(K, Rh, "con"); F.line(K, Ai, "con"); F.line(K, Bh, "con")
    F.line((0, S[1] + .03), (0, Ai[1] - 0.1), "fin", lw=0.7)
    # check against the depression almucantar of a horizon of latitude 90-ε
    cc, rr = P.almucantar(phi_, -d)
    F.close_enough("radius of the 10th almucantar of depression", dist(Fc, S), rr)
    F.close_enough("its centre", Fc[1], cc[1])
    labels(F, [(S, "س", (0, .07)), ((0, c[1] + r), "ح", (.06, .03)), ((0, Re), "ط", (.06, .04)),
               (A, "ا", (-.03, .06)), (G, "ج", (-.06, .04)), (K, "ك", (-.07, 0)), (M, "م", (.07, 0)),
               (E, "ه", (.05, .05)), ((0, c[1] - r), "ر", (.05, .05)), (Ai, "ع", (.05, -.03)),
               (B, "ب", (.06, -.03)), (Dd, "د", (.03, -.07)), ((0, -Re), "ل", (-.05, -.06))])
    F.dot(Fc, RED, 4)
    return F.save(out)

FIGS = {7: fig07, 8: fig08, 9: fig09, 10: fig10, 11: fig11, 12: fig12, 13: fig13, 14: fig14, 15: fig15, 16: fig16}
