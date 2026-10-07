import sys, os, json, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs"))
mods = sys.argv[1:] or [f"ch{i}" for i in range(1, 10)]
res = {}
rp = "out/checks.json"
if os.path.exists(rp): res = json.load(open(rp))
os.makedirs("out/fig", exist_ok=True)
for m in mods:
    M = importlib.import_module(m)
    for n, fn in M.FIGS.items():
        ch = fn(f"out/fig/{n:02d}.png")
        res[str(n)] = ch
        print(n, f"{sum(o for _, o in ch)}/{len(ch)} checks")
json.dump(res, open(rp, "w"), ensure_ascii=False, indent=1)
