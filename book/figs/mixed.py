"""Mixed retes (المزاجات).

Every sign keeps the sector of its right ascensions whichever ecliptic it is taken from; the
northern ecliptic (projection from the south pole) and the southern ecliptic (projection from
the north pole) differ only in putting a sign inside or outside the equator:
  northern sign (Aries..Virgo):   northern ecliptic -> inside,  southern ecliptic -> outside
  southern sign (Libra..Pisces):  northern ecliptic -> outside, southern ecliptic -> inside
so a mixed rete is fixed by the set of signs drawn outside the equator.
"""
from figlib import *

SIGN_ABBR = ["حمل", "ثور", "جوزا", "سرطان", "أسد", "سنبلة", "ميزان", "عقرب", "قوس", "جدي", "دلو", "حوت"]

def sign_piece(sign, outside, eps=EPS):
    """Return ('N' or 'S') and a function lam -> point (rim radius 1)."""
    north_sign = sign < 6
    use_N = (north_sign and not outside) or ((not north_sign) and outside)
    P = Plate(1.0, eps=eps, south=not use_N)
    if use_N:
        f = lambda lam: P.star(ra(lam, eps), decl(lam, eps))
    else:
        # southern projection with the rim on the circle of Cancer: same scale as the northern
        # one whose rim is Capricorn (both rims are the tropics)
        f = lambda lam: P.star(ra(lam, eps), decl(lam, eps))
    return ("N" if use_N else "S"), f, P

def ecl_circle(use_N, eps=EPS):
    P = Plate(1.0, eps=eps, south=not use_N)
    pts = [P.star(ra(l, eps), decl(l, eps)) for l in (0, 90, 180)]
    return circle3(*pts)

def rot_pt(p, rot, c=(0, 0), s=1.0):
    x, y = p
    return (c[0] + s * (x * cosd(rot) - y * sind(rot)), c[1] + s * (x * sind(rot) + y * cosd(rot)))

def draw_band(F, sign, outside, rot=0, c=(0, 0), s=1.0, w=0.085, label=True, size=7.5, kind="con", ticks=True):
    use, f, P = sign_piece(sign, outside)
    cc, rr = ecl_circle(use == "N")
    lam = np.linspace(sign * 30, sign * 30 + 30, 61)
    pts = [f(l) for l in lam]
    # inner edge: the band lies on the side of the ecliptic toward its own centre
    inner = [pol(rr - w, ang(p, cc), cc) for p in pts]
    T = lambda q: rot_pt(q, rot, c, s)
    xs, ys = zip(*[T(p) for p in pts]); F.curve(xs, ys, kind, lw=0.9)
    xs, ys = zip(*[T(p) for p in inner]); F.curve(xs, ys, kind, lw=0.9)
    for p, q in ((pts[0], inner[0]), (pts[-1], inner[-1])):
        F.line(T(p), T(q), kind, lw=0.9)
    if ticks:
        for i in range(2, 60, 2):
            q = pol(rr - w * (0.3 if i % 10 else 0.5), ang(pts[i], cc), cc)
            F.line(T(pts[i]), T(q), "redthin" if kind == "con" else "thin")
    if label:
        m = pol(rr - w * 0.68, ang(pts[30], cc), cc)
        a = ang(T(m), T(cc))
        F.rtext(T(m), SIGN_ABBR[sign], a, size=size, color=BLACK)
    return T(pts[0]), T(pts[-1]), T(inner[0]), T(inner[-1])

def mixed_rete(F, outside, rot=0, c=(0, 0), s=1.0, w=0.085, spokes=True, size=7.5, rim=True, ticks=True):
    """Draw a mixed rete; `outside` = set of sign indices kept outside the equator."""
    if rim:
        F.circle(c, s, "con", lw=1.0)
    F.circle(c, 0.07 * s, "con", lw=0.9)
    ends = {}
    for sg in range(12):
        ends[sg] = draw_band(F, sg, sg in outside, rot, c, s, w, size=size, ticks=ticks)
    # supports: where an inside piece meets an outside piece, a radial bar joins them
    if spokes:
        for sg in range(12):
            nx = (sg + 1) % 12
            if (sg in outside) != (nx in outside):
                p1 = ends[sg][1]; p2 = ends[nx][0]
                a = ang(p1, c)
                r1 = dist(p1, c); r2 = dist(p2, c)
                F.line(pol(min(r1, r2) - w * s, a, c), pol(s, a, c), "con", lw=0.7)
    return ends
