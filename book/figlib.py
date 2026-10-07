"""Drawing and geometry toolkit for the Istīʿāb figures.

Every figure is built from the geometry the text describes, never traced.
Conventions follow the manuscript (BL Or 5593): red ink for construction
lines, black for the finished (engraved) lines; south (the meridian
toward the handle) is UP, east on the LEFT, as on an astrolabe plate.
"""
import math, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Arc, Polygon, Circle as MCircle
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.abspath(__file__))
for f in ("Amiri-Regular.ttf", "Amiri-Bold.ttf"):
    fm.fontManager.addfont(os.path.join(HERE, "fonts", f))
plt.rcParams["font.family"] = "Amiri"
plt.rcParams["mathtext.fontset"] = "stix"

EPS = 23 + 35 / 60          # al-Bīrūnī's obliquity 23;35°
RED = "#b3261e"
BLACK = "#111111"
GREY = "#8a8a8a"
D = math.pi / 180

def ar(s):
    # matplotlib >= 3.11 shapes and orders Arabic itself (libraqm)
    return s

def sind(a): return math.sin(a * D)
def cosd(a): return math.cos(a * D)
def tand(a): return math.tan(a * D)
def atand(x): return math.atan(x) / D
def asind(x): return math.asin(max(-1, min(1, x))) / D
def acosd(x): return math.acos(max(-1, min(1, x))) / D

def pol(r, a, c=(0, 0)):
    """Point at distance r, angle a (degrees, counter-clockwise from +x)."""
    return (c[0] + r * cosd(a), c[1] + r * sind(a))

def dist(p, q): return math.hypot(p[0] - q[0], p[1] - q[1])
def mid(p, q): return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
def ang(p, c=(0, 0)): return math.degrees(math.atan2(p[1] - c[1], p[0] - c[0]))

def line_inter(p1, p2, p3, p4):
    """Intersection of line p1p2 with line p3p4."""
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-14:
        return None
    a = x1 * y2 - y1 * x2; b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)

def line_circle(p, q, c, r):
    """Intersections of line pq with circle (c, r), ordered along p->q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    fx, fy = p[0] - c[0], p[1] - c[1]
    A = dx * dx + dy * dy; B = 2 * (fx * dx + fy * dy); C = fx * fx + fy * fy - r * r
    disc = B * B - 4 * A * C
    if disc < 0:
        return []
    s = math.sqrt(disc)
    ts = sorted([(-B - s) / (2 * A), (-B + s) / (2 * A)])
    return [(p[0] + t * dx, p[1] + t * dy) for t in ts]

def circle_circle(c1, r1, c2, r2):
    d = dist(c1, c2)
    if d > r1 + r2 or d < abs(r1 - r2) or d == 0:
        return []
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(0, r1 * r1 - a * a))
    xm = c1[0] + a * (c2[0] - c1[0]) / d; ym = c1[1] + a * (c2[1] - c1[1]) / d
    return [(xm + h * (c2[1] - c1[1]) / d, ym - h * (c2[0] - c1[0]) / d),
            (xm - h * (c2[1] - c1[1]) / d, ym + h * (c2[0] - c1[0]) / d)]

def circle3(p1, p2, p3):
    """Centre and radius of the circle through three points."""
    ax, ay = p1; bx, by = p2; cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    uy = ((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    return (ux, uy), dist((ux, uy), p1)

def collinear(p, q, r, tol=1e-6):
    return abs((q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])) < tol * max(1, dist(p, q) * dist(p, r))

# ---------------------------------------------------------------- astrolabe
class Plate:
    """Stereographic projection of the celestial sphere onto the plane of the equator.
    Northern astrolabe: pole of projection = south celestial pole.  Southern: north pole.
    R = radius of the rim (Capricorn on the northern, Cancer on the southern astrolabe).
    Plate coordinates: the upper meridian (south point of the horizon) is +y, east is -x,
    hour angle H counted westward from the upper meridian."""
    def __init__(self, R=1.0, eps=EPS, south=False):
        self.R = R; self.eps = eps; self.south = south
        self.Re = R * tand(45 - eps / 2)   # radius of the equator (circle of Aries)

    def eq(self, H, dec):
        """Plate point of the sphere point with hour angle H and declination dec."""
        s = -1 if self.south else 1
        k = self.Re * cosd(dec) / (1 + s * sind(dec))
        return (k * sind(H), k * cosd(H))

    def r_decl(self, d):
        s = -1 if self.south else 1
        return self.Re * cosd(d) / (1 + s * sind(d))

    def hor(self, phi, h, A):
        """Plate point of altitude h, azimuth A (from the south point, westward)."""
        sd = sind(phi) * sind(h) - cosd(phi) * cosd(h) * cosd(A)
        dec = asind(sd)
        H = math.degrees(math.atan2(sind(A) * cosd(h), cosd(A) * cosd(h) * sind(phi) + sind(h) * cosd(phi)))
        return self.eq(H, dec)

    def almucantar(self, phi, h):
        c, r = circle3(self.hor(phi, h, 0), self.hor(phi, h, 90), self.hor(phi, h, 180))
        return c, r

    def zenith(self, phi): return self.eq(0, phi)
    def nadir(self, phi): return self.eq(180, -phi)

    def azimuth(self, phi, A):
        """Vertical circle through azimuth A (from the south point): centre, radius."""
        return circle3(self.zenith(phi), self.hor(phi, 0, A), self.hor(phi, 30, A))

    def ecliptic(self, ra0=0):
        """Ecliptic circle when the vernal point lies at hour angle ra0 west of the meridian
        is not needed: the rete is drawn with the solstices on the meridian (Capricorn up).
        Returns centre, radius for the standard rete orientation."""
        p1 = self.ecl_point(270); p2 = self.ecl_point(90); p3 = self.ecl_point(0)
        return circle3(p1, p2, p3)

    def ecl_point(self, lam, H0=None):
        """Point of the ecliptic of longitude lam with the beginning of Capricorn on the
        upper meridian (rete in its drawing position).  RA grows counter-clockwise from Aries
        on the east (left) side."""
        a = ra(lam, self.eps); d = decl(lam, self.eps)
        # Capricorn (RA 270) on the upper meridian: hour angle H = RA - 270 ... east = -x
        H = (270 - a)
        return self.eq(H, d)

    def star(self, ra_, dec):
        H = 270 - ra_
        return self.eq(H, dec)

def decl(lam, eps=EPS):
    """Declination of ecliptic longitude lam."""
    return asind(sind(eps) * sind(lam))

def ra(lam, eps=EPS):
    """Right ascension of ecliptic longitude lam (0..360)."""
    a = math.degrees(math.atan2(cosd(eps) * sind(lam), cosd(lam)))
    return a % 360

def eq_from_ecl(lam, beta, eps=EPS):
    """(RA, Dec) from ecliptic longitude/latitude."""
    x = cosd(beta) * cosd(lam)
    y = cosd(beta) * sind(lam) * cosd(eps) - sind(beta) * sind(eps)
    z = cosd(beta) * sind(lam) * sind(eps) + sind(beta) * cosd(eps)
    return math.degrees(math.atan2(y, x)) % 360, asind(z)

# ---------------------------------------------------------------- drawing
class Fig:
    def __init__(self, w=6, h=6, lim=None):
        self.f, self.ax = plt.subplots(figsize=(w, h))
        self.ax.set_aspect("equal"); self.ax.axis("off")
        self.lim = lim
        self.checks = []

    # primitives --------------------------------------------------------
    def _st(self, kind, lw):
        if kind == "con": return dict(color=RED, lw=lw or 0.8, ls="-")
        if kind == "fin": return dict(color=BLACK, lw=lw or 1.1, ls="-")
        if kind == "aux": return dict(color=GREY, lw=lw or 0.7, ls=(0, (4, 3)))
        if kind == "dot": return dict(color=BLACK, lw=lw or 0.8, ls=(0, (1, 2)))
        if kind == "reddash": return dict(color=RED, lw=lw or 0.8, ls=(0, (4, 3)))
        if kind == "thin": return dict(color=BLACK, lw=lw or 0.5, ls="-")
        if kind == "redthin": return dict(color=RED, lw=lw or 0.45, ls="-")
        raise ValueError(kind)

    def line(self, p, q, kind="fin", lw=None, z=2):
        st = self._st(kind, lw)
        self.ax.plot([p[0], q[0]], [p[1], q[1]], solid_capstyle="round", zorder=z, **st)

    def poly(self, pts, kind="fin", lw=None, closed=False, z=2):
        st = self._st(kind, lw)
        pts = list(pts)
        if closed: pts = pts + [pts[0]]
        xs, ys = zip(*pts)
        self.ax.plot(xs, ys, zorder=z, **st)

    def fill(self, pts, color="#f2e9d8", z=0, alpha=1.0):
        self.ax.add_patch(Polygon(pts, closed=True, fc=color, ec="none", zorder=z, alpha=alpha))

    def circle(self, c, r, kind="fin", lw=None, z=2):
        st = self._st(kind, lw)
        self.ax.add_patch(MCircle(c, r, fill=False, ec=st["color"], lw=st["lw"], ls=st["ls"], zorder=z))

    def arc(self, c, r, a1, a2, kind="fin", lw=None, z=2):
        """Arc from angle a1 to a2 counter-clockwise (degrees)."""
        st = self._st(kind, lw)
        a2 = a1 + ((a2 - a1) % 360 or 360) if a2 != a1 else a1 + 360
        t = np.linspace(a1, a2, max(8, int(abs(a2 - a1) * 2)))
        self.ax.plot(c[0] + r * np.cos(t * D), c[1] + r * np.sin(t * D), zorder=z, **st)

    def arc_clip(self, c, r, inside=None, outside=None, kind="fin", lw=None, n=1440, z=2):
        """Draw the parts of circle (c,r) inside every circle of `inside` and outside every circle of `outside`."""
        t = np.linspace(0, 2 * math.pi, n + 1)
        x = c[0] + r * np.cos(t); y = c[1] + r * np.sin(t)
        ok = np.ones_like(t, dtype=bool)
        for (cc, rr) in inside or []:
            ok &= (x - cc[0]) ** 2 + (y - cc[1]) ** 2 <= rr * rr + 1e-12
        for (cc, rr) in outside or []:
            ok &= (x - cc[0]) ** 2 + (y - cc[1]) ** 2 >= rr * rr - 1e-12
        self._runs(x, y, ok, kind, lw, z)

    def arc_component(self, c, r, through, okf, kind="fin", lw=None, n=4000, z=2):
        """Draw only the connected piece of circle (c,r) that passes through `through`
        and on which okf(x, y) holds.  Returns the two end points."""
        a0 = math.atan2(through[1] - c[1], through[0] - c[0])
        t = np.linspace(-math.pi, math.pi, n + 1)
        def P_(u): return (c[0] + r * math.cos(a0 + u), c[1] + r * math.sin(a0 + u))
        lo = 0; hi = 0
        i0 = n // 2
        j = i0
        while j < n and okf(*P_(t[j + 1])): j += 1
        k = i0
        while k > 0 and okf(*P_(t[k - 1])): k -= 1
        us = t[k:j + 1]
        self.ax.plot(c[0] + r * np.cos(a0 + us), c[1] + r * np.sin(a0 + us), zorder=z, **self._st(kind, lw))
        return P_(t[k]), P_(t[j])

    def curve(self, xs, ys, kind="fin", lw=None, z=2):
        self.ax.plot(xs, ys, zorder=z, **self._st(kind, lw))

    def curve_clip(self, xs, ys, ok, kind="fin", lw=None, z=2):
        self._runs(np.asarray(xs), np.asarray(ys), np.asarray(ok), kind, lw, z)

    def _runs(self, x, y, ok, kind, lw, z):
        st = self._st(kind, lw)
        i = 0; n = len(x)
        while i < n:
            if ok[i]:
                j = i
                while j + 1 < n and ok[j + 1]: j += 1
                if j > i: self.ax.plot(x[i:j + 1], y[i:j + 1], zorder=z, **st)
                i = j + 1
            else:
                i += 1

    def dot(self, p, color=BLACK, s=7, z=5):
        self.ax.plot([p[0]], [p[1]], "o", ms=s ** 0.5 * 1.2, color=color, zorder=z)

    def text(self, p, s, size=11, color=BLACK, ha="center", va="center", rot=0, z=6, bold=False):
        self.ax.text(p[0], p[1], ar(s), fontsize=size, color=color, ha=ha, va=va, rotation=rot,
                     rotation_mode="anchor", zorder=z, fontweight="bold" if bold else "normal")

    def rtext(self, p, s, a, size=10, color=BLACK):
        """Text written tangentially at polar angle a, kept readable (never upside down)."""
        rot = (a - 90) % 360
        if 90 < rot < 270: rot -= 180
        self.text(p, s, size=size, color=color, rot=rot)

    def lab(self, p, s, d=(0, 0), size=12, color=BLACK, dotit=False):
        """Letter label offset by d from point p (as the copyist writes them beside the point)."""
        if dotit: self.dot(p, color=color)
        self.text((p[0] + d[0], p[1] + d[1]), s, size=size, color=color)

    def latex(self, p, s, size=10, color=BLACK, ha="center"):
        self.ax.text(p[0], p[1], s, fontsize=size, color=color, ha=ha, va="center", zorder=6)

    def ticks(self, c, r1, r2, a0, a1, step, kind="thin", lw=None):
        a = a0
        while a <= a1 + 1e-9:
            self.line(pol(r1, a, c), pol(r2, a, c), kind=kind, lw=lw)
            a += step

    def ring_numbers(self, c, r, labels, a0, step, size=8, color=BLACK, upright=False, sense=1):
        """Write labels around a ring starting at angle a0, every `step` degrees (sense=+1 ccw)."""
        for i, s in enumerate(labels):
            a = a0 + sense * i * step
            p = pol(r, a, c)
            rot = 0 if upright else (a - 90)
            self.text(p, s, size=size, color=color, rot=rot, ha="center", va="center")

    # checks --------------------------------------------------------------
    def check(self, desc, ok):
        self.checks.append((desc, bool(ok)))
        if not ok:
            print("  !! CHECK FAILED:", desc)

    def close_enough(self, desc, a, b, tol=1e-6):
        self.check(f"{desc} ({a:.6g} ≈ {b:.6g})", abs(a - b) < tol * max(1, abs(b)))

    def save(self, path, pad=0.05, dpi=220):
        if self.lim:
            x0, x1, y0, y1 = self.lim
            self.ax.set_xlim(x0, x1); self.ax.set_ylim(y0, y1)
        self.f.savefig(path, dpi=dpi, bbox_inches="tight", pad_inches=pad, facecolor="white")
        plt.close(self.f)
        return self.checks

ABJAD = ["ا","ب","ج","د","ه","و","ز","ح","ط","ي","ك","ل","م","ن","س","ع","ف","ص","ق","ر","ش","ت","ث","خ","ذ","ض","ظ","غ"]
ABJAD_VAL = [1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000]

def abjad(n):
    """Abjad numeral for 1..999 as written on instruments (e.g. 15 -> يه)."""
    if n == 0: return "٠"
    out = ""
    for v, l in sorted(zip(ABJAD_VAL, ABJAD), reverse=True):
        while n >= v:
            # 15 and 16 are written يه and يو in the abjad of the instruments
            out += l; n -= v
    return out

SIGNS = ["الحمل","الثور","الجوزاء","السرطان","الأسد","السنبلة","الميزان","العقرب","القوس","الجدي","الدلو","الحوت"]
SIGNS_S = ["حمل","ثور","جوزا","سرطان","أسد","سنبلة","ميزان","عقرب","قوس","جدي","دلو","حوت"]
