"""Assemble the book (Markdown) and convert it to Word with pandoc."""
import json, os, re, subprocess, sys, importlib.util, glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
AR_DIG = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
def ar(n): return str(n).translate(AR_DIG)

GROUPS = [
    (1, 6, "الدستور والمدارات"),
    (7, 16, "الأفق والمقنطرات والسموت ورؤوس الكواكب"),
    (17, 24, "العنكبوت وسائر الآلات والأسطرلاب الجنوبي والصفائح الخاصة"),
    (25, 30, "ظهر الأسطرلاب"),
    (31, 43, "المزاجات والأسطرلابات الغريبة"),
    (44, 51, "المسطري والكري والرصدي والمبطّخ"),
    (52, 54, "الأسطرلاب الكامل"),
    (55, 78, "التسطيح التام والقطوع المخروطية"),
    (79, 85, "حُقّ القمر والصفيحة الكسوفية ورؤية الأهلة"),
]

def load_ft():
    FT = {}
    for f in sorted(glob.glob(os.path.join(HERE, "text", "ft*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        FT.update(m.FT)
    return FT

def folio_info():
    raw = json.load(open(os.path.join(HERE, "data", "atlas_raw.json")))
    info = {}
    for o in raw:
        m = re.search(r"f\. ([0-9rv–\- ]+?) · PDF p\. ([0-9, ]+)", o["raw"])
        fol = m.group(1).strip() if m else ""
        pdf = m.group(2).strip() if m else ""
        def conv(x):
            x = x.strip()
            mm = re.match(r"(\d+)([rv])", x)
            return f"{ar(mm.group(1))} {'و' if mm.group(2) == 'r' else 'ظ'}" if mm else x
        fol_ar = " – ".join(conv(x) for x in re.split(r"[–-]", fol)) if fol else ""
        info[o["n"]] = dict(fol=fol_ar, pdf=ar(pdf.replace(" ", "")).replace(",", "، "), ms=o["ms"])
    return info

def figure_section(FT, checks):
    info = folio_info()
    L = ["# الباب الخامس: الأشكال مرسومةً بالحساب، مع معادلاتها والتعليق عليها", "",
         "يُعرض كل شكل على هذا الترتيب: صورته في المخطوط، ثم إعادة رسمه، ثم الشرح، ثم المعادلات، ثم نتيجة التحقق العددي. "
         "والإحالة إلى أوراق نسخة المكتبة البريطانية Or 5593، ويرمز «و» إلى وجه الورقة و«ظ» إلى ظهرها، "
         "ومعها رقم الصفحة في مصوّرة المخطوط.", ""]
    for a, b, gname in GROUPS:
        L += [f"## {gname} (الأشكال {ar(a)}–{ar(b)})", ""]
        for n in range(a, b + 1):
            ft = FT.get(n)
            if not ft:
                continue
            inf = info[n]
            L += [f"### الشكل {ar(n)}: {ft['t']}", ""]
            L += [f"::: {{custom-style=\"Author\"}}", f"من باب «{ft['sec']}» — الورقة {inf['fol']}، صفحة المصوّرة {inf['pdf']}", ":::", ""]
            for k, msimg in enumerate(inf["ms"]):
                cap = "صورة الشكل في المخطوط" + (f" ({ar(k + 1)})" if len(inf["ms"]) > 1 else "")
                L += [f"![{cap}](../figures-atlas/{msimg}){{width={ft.get('msw', '55%')}}}", ""]
            L += [f"![إعادة الرسم بالحساب](out/fig/{n:02d}.png){{width={ft.get('w', '85%')}}}", ""]
            L += ["#### الشرح", ""] + [p.strip() for p in ft["sharh"].strip().split("\n")] + [""]
            if ft.get("eq"):
                L += ["#### المعادلات", ""]
                for e in ft["eq"]:
                    L += [f"$${e}$$", ""]
            ch = checks.get(str(n), [])
            if ch:
                ok = sum(1 for _, o in ch if o)
                L += ["#### التحقق", "", f"اجتاز الشكل {ar(ok)} من {ar(len(ch))} اختبارات عددية"
                      + (f"، منها: {ft['chk']}" if ft.get("chk") else "") + ".", ""]
            if ft.get("note"):
                L += ["::: {custom-style=\"Block Text\"}", "**تنبيه على المخطوط:** " + ft["note"].strip(), ":::", ""]
    return "\n".join(L)

def star_table():
    sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "figs"))
    from figlib import eq_from_ecl
    from ch3 import stars_epoch
    L = ["## ملحق ٣: الكواكب الثابتة المرسومة في العناكب", "",
         "أطوالها من سنة ٢٠٠٠ للميلاد مردودة إلى سنة ٩٩٩ بمقدار المبادرة، وعروضها كما هي، "
         "ثم حُوّلت إلى الميل والمطالع بالميل الكلي $23;35^\\circ$. وهي للرسم لا للرصد.", "",
         "| الكوكب | الطول | العرض | المطالع | الميل |", "|:--|--:|--:|--:|--:|"]
    for n, l, b in stars_epoch():
        a, d = eq_from_ecl(l, b)
        L.append(f"| {n} | ${l:.1f}^\\circ$ | ${b:+.1f}^\\circ$ | ${a:.1f}^\\circ$ | ${d:+.1f}^\\circ$ |")
    return "\n".join(L) + "\n"

def main():
    FT = load_ft()
    checks = json.load(open(os.path.join(OUT, "checks.json")))
    parts = []
    for f in ["00_front.md", "01_biruni.md", "02_kitab.md", "03_tasatih.md", "04_nusakh.md"]:
        parts.append(open(os.path.join(HERE, "text", f)).read())
    parts.append(figure_section(FT, checks))
    for f in ["06_tahqiq.md", "07_malahiq.md"]:
        p = os.path.join(HERE, "text", f)
        if os.path.exists(p):
            parts.append(open(p).read())
    parts.append(star_table())
    parts.append(open(os.path.join(HERE, "text", "08_maraji.md")).read())
    md = "\n\n".join(parts)
    md = md.replace("](../out/fig/", "](out/fig/")
    src = os.path.join(OUT, "book.md")
    open(src, "w").write(md)
    meta = os.path.join(OUT, "meta.yaml")
    open(meta, "w").write('---\nlang: ar\ndir: rtl\ntoc-title: "المحتويات"\n'
        'title: "كتاب استيعاب الوجوه الممكنة في صنعة الأسطرلاب"\n'
        'subtitle: "لأبي الريحان محمد بن أحمد البيروني (٣٦٢ – بعد ٤٤٠ هـ / ٩٧٣ – بعد ١٠٤٨ م): دراسة، وإعادة رسم أشكاله الخمسة والثمانين بالحساب الهندسي، مع معادلاتها والتعليق عليها"\n'
        'author: "اعتمادًا على نسخة المكتبة البريطانية Or 5593"\n---\n')
    target = os.path.join(OUT, sys.argv[1] if len(sys.argv) > 1 else "Istiab_Biruni.docx")
    cmd = ["pandoc", meta, src, "-f", "markdown+native_divs", "--reference-doc", os.path.join(HERE, "tpl", "reference.docx"),
           "--toc", "--toc-depth=2", "--resource-path", HERE, "-o", target]
    subprocess.run(cmd, check=True, cwd=HERE)
    print("wrote", target, "figures with text:", len(FT))

if __name__ == "__main__":
    main()
