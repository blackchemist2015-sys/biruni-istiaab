"""al-Saghani's 'perfect projection' (التسطيح التام): projection of the sphere onto the plane
of the equator from a point ع on the axis.

Section convention (as in the manuscript's meridian sections): the axis ك ه م is horizontal,
ك (the south pole) on the left, م (the north pole) on the right; the trace of the equator
plane ح ه ي is vertical (ح up).  3-D coordinates: x along the axis toward م, y up the
drawing (the meridian line of the plate), z out of the drawing (east-west of the plate).
A northern astrolabe has its pole of projection on ك's side (x = -e)."""
import math
import numpy as np

def proj(P, e, south=False):
    """Image on the plane x = 0 of the 3-D point P, projected from (∓e, 0, 0)."""
    s = 1 if south else -1
    x, y, z = P
    t = e / (e - s * x) if True else None
    # pole at (s*e, 0, 0); the line pole->P meets x = 0 at parameter u = s*e / (s*e - x)
    u = (s * e) / (s * e - x)
    return (u * y, u * z)

def circle3d(Z, T, n=721):
    """Points of the circle of the sphere perpendicular to the drawing plane whose diameter
    in the section runs from Z to T (2-D points in the drawing)."""
    cx, cy = (Z[0] + T[0]) / 2, (Z[1] + T[1]) / 2
    rho = math.hypot(T[0] - Z[0], T[1] - Z[1]) / 2
    ux, uy = (T[0] - Z[0]) / (2 * rho), (T[1] - Z[1]) / (2 * rho)
    th = np.linspace(0, 2 * math.pi, n)
    return [(cx + rho * math.cos(t) * ux, cy + rho * math.cos(t) * uy, rho * math.sin(t)) for t in th]

def image(Z, T, e, south=False, n=1441):
    """Plate image (y, z) of the circle on Z T; points behind the pole are dropped."""
    s = 1 if south else -1
    out = []
    for P in circle3d(Z, T, n):
        d = s * e - P[0]
        if abs(d) < 1e-6 or (s * e) / d < 0:
            out.append(None)
            continue
        out.append(proj(P, e, south))
    return out

def kind(Z, T, e, south=False):
    """ellipse / parabola / hyperbola according to whether the plane through the pole
    parallel to the equator misses, touches or cuts the circle on Z T."""
    xp = (1 if south else -1) * e
    x1, x2 = sorted((Z[0], T[0]))
    tol = 1e-9
    if abs(xp - x1) < tol or abs(xp - x2) < tol:
        return "parabola"
    return "hyperbola" if x1 < xp < x2 else "ellipse"
