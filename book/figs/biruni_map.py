"""Schematic map of al-Biruni's journey (places approximate, for orientation only)."""
from figlib import *

CASPIAN = [(46.7,44.3),(47.5,45.6),(49.2,46.4),(51.3,47.0),(53.1,46.9),(53.0,45.3),(52.4,44.6),(51.4,43.6),(51.2,43.2),
           (52.5,42.0),(53.0,40.7),(54.0,40.5),(52.9,39.9),(53.6,39.0),(53.9,37.3),(52.5,36.7),(50.5,37.1),(49.0,37.6),
           (48.9,38.5),(49.5,40.3),(48.6,41.8),(47.5,42.9)]
ARAL = [(58.3,45.5),(59.2,46.6),(61.0,46.6),(61.8,45.3),(61.5,44.1),(60.1,43.6),(58.6,44.2)]
JAYHUN = [(59.6,43.6),(60.0,42.2),(60.9,41.5),(61.6,40.6),(63.6,39.1),(65.2,37.8),(67.3,37.2),(69.0,37.1),(71.0,37.0)]
SAYHUN = [(61.2,45.9),(63.5,45.0),(65.5,44.3),(67.5,43.6),(68.8,41.5),(69.5,40.9),(71.0,40.8),(72.5,40.7)]
SINDH = [(74.5,35.4),(73.0,34.3),(72.3,33.9),(71.8,32.6),(71.3,30.6),(70.5,29.0),(68.9,27.5),(68.3,25.4),(67.6,24.3)]

PLACES = {
    "كاث": (61.0, 41.4), "الجرجانية": (59.15, 42.3), "الري": (51.4, 35.6), "جرجان": (55.2, 37.25),
    "غزنة": (68.4, 33.55), "بخارى": (64.4, 39.8), "سمرقند": (66.97, 39.65), "نندنة": (73.2, 32.7),
    "لاهور": (74.35, 31.55), "الملتان": (71.5, 30.2), "بغداد": (44.4, 33.3), "مرو": (61.8, 37.6), "نيسابور": (58.8, 36.2),
}
ROUTE = [("كاث", "الري", "١", 0.28), ("الري", "كاث", "٢", 0.28), ("كاث", "جرجان", "٣", 0.0), ("جرجان", "الجرجانية", "٤", -0.3),
         ("الجرجانية", "غزنة", "٥", -0.15), ("غزنة", "نندنة", "٦", 0.2)]

def fig_map(out):
    F = Fig(8.6, 6.4)
    k = math.cos(38 * D)
    T = lambda p: (p[0] * k, p[1])
    for lo in range(45, 80, 5):
        F.line(T((lo, 23)), T((lo, 48)), "aux", lw=0.35)
        F.text(T((lo, 22.3)), f"{lo}°", size=7, color=GREY)
    for la in range(25, 50, 5):
        F.line(T((43, la)), T((77, la)), "aux", lw=0.35)
        F.text(T((42.2, la)), f"{la}°", size=7, color=GREY)
    for poly in (CASPIAN, ARAL):
        pts = [T(p) for p in poly]
        F.fill(pts, color="#dfe9ef", z=0); F.poly(pts, "thin", closed=True, lw=0.6)
    for riv in (JAYHUN, SAYHUN, SINDH):
        xs, ys = zip(*[T(p) for p in riv]); F.ax.plot(xs, ys, color="#6d8fa6", lw=1.0, zorder=1)
    F.text(T((50.4, 41.8)), "بحر الخزر", size=10, color="#4b6b80")
    F.text(T((60.0, 45.2)), "بحيرة خوارزم", size=9, color="#4b6b80")
    F.text(T((64.4, 38.4)), "جيحون", size=9, color="#4b6b80", rot=35)
    F.text(T((70.0, 28.0)), "نهر السند", size=9, color="#4b6b80", rot=-60)
    for a, b, n, rad in ROUTE:
        p, q = T(PLACES[a]), T(PLACES[b])
        F.ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="->", color=RED, lw=1.4, shrinkA=6, shrinkB=6,
                       connectionstyle=f"arc3,rad={rad}"), zorder=4)
        m = mid(p, q); dx, dy = q[0] - p[0], q[1] - p[1]
        # the arc bulges to the right of p->q by rad * |pq|
        off = (dy * rad + (0.0 if rad else 0.35), -dx * rad + (0.0 if rad else 0.35))
        LP = {"١": (58.6, 36.6), "٢": (54.6, 40.3), "٣": (58.9, 38.6), "٤": (56.3, 41.2), "٥": (66.6, 37.9), "٦": (71.0, 33.7)}
        F.text(T(LP[n]), n, size=13, color=RED, bold=True)
    for nm, p in PLACES.items():
        main = nm in ("كاث", "الجرجانية", "الري", "جرجان", "غزنة", "نندنة")
        F.dot(T(p), RED if main else BLACK, 9 if main else 5)
        F.text((T(p)[0], T(p)[1] + 0.55), nm, size=11 if main else 9, color=BLACK if main else GREY, bold=main)
    F.ax.set_xlim(42 * k, 77.5 * k); F.ax.set_ylim(22, 48)
    return F.save(out)

FIGS = {}
if __name__ == "__main__":
    fig_map("out/fig/map.png")
