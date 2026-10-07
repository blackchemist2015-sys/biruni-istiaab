"""Convert the Arabic labels inside LaTeX math into Latin (English) notation.

Points of the figures keep their Arabic letters in the drawings and in the prose; in the
equations each letter is written with a fixed Latin capital (table in the book), a segment
between two points is overlined, and Arabic words are replaced by English subscripts."""
import re

LETTERS = {
    "ا": "A", "ب": "B", "ج": "G", "د": "D", "ه": "E", "و": "W", "ز": "Z", "ح": "H", "ط": "T",
    "ي": "Y", "ى": "I", "ك": "K", "ل": "L", "م": "M", "ن": "N", "س": "S", "ع": "O", "ف": "F",
    "ص": "C", "ق": "Q", "ر": "R", "ش": "X", "ت": "U", "ث": "V", "خ": "J", "ذ": "P",
}
# order: longer phrases first
WORDS = [
    ("ميل السمت", r"\iota"), ("الضلع القائم", r"\text{latus rectum}"), ("الضلع المائل", r"\text{transverse side}"),
    ("قطع مكافئ", r"\text{parabola}"), ("زاوية الرأس", r"\beta"), ("زاوية المركز", r"\alpha"),
    ("الدوائر الأربع", r"\text{four circles}"), ("تقاطع الأفقين", r"\text{intersection of the two horizons}"),
    ("خط المراكز", r"\text{line of centres}"), ("درجة الممر", r"\text{culm}"), ("على استقامة", r"\text{collinear}"),
    ("عند المبدأ", r"\text{at the origin}"), ("مركز الأفق", r"\text{horizon centre}"), ("مركز المنطقة", r"\text{ecliptic centre}"),
    ("نقطة الشمال", r"\text{north point}"), ("نقطة المغرب", r"\text{west point}"), ("تحت المركز", r"\text{below the centre}"),
    ("نصف قطرها", r"\text{radius}"), ("نصف قطره", r"\text{radius}"), ("نفسه لكل", r"\text{the same for every}"),
    ("الهلال بين", r"\text{lune between}"), ("من ك:", r"\text{from K:}"), ("الانحراف", r"\psi"),
    ("الأفقي", r"\text{horizontal}"), ("الأفق", r"\text{horizon}"), ("أفق", r"\text{horizon}"),
    ("الصنف", r"\text{type}"), ("العضادة", r"\text{alidade}"), ("القطر", r"\text{diameter}"),
    ("الكوكب", r"\star"), ("المقاربان", r"\text{asymptotes}"), ("(جزء)", r"\text{(parts)}"),
    ("آخره", r"\text{end}"), ("أوله", r"\text{beginning}"), ("جدي", r"\text{Cap}"), ("حمل", r"\text{Ari}"),
    ("سرطان", r"\text{Can}"), ("شمس", r"\text{Sun}"), ("زائد", r"\text{hyperbola}"), ("ناقص", r"\text{ellipse}"),
    ("مكافئ", r"\text{parabola}"), ("زوال", r"\text{noon}"), ("عصر", r"\text{asr}"), ("مستوي", r"\text{dir}"),
    ("معكوس", r"\text{rev}"), ("يومًا", r"\text{days}"),
]

def _latin_points(s):
    s = s.strip()
    letters = s.split()
    if not letters or not all(l in LETTERS for l in letters):
        return None
    lat = "".join(LETTERS[l] for l in letters)
    return r"\mathrm{" + lat + "}" if len(letters) == 1 else r"\overline{\mathrm{" + lat + "}}"

def convert_math(m):
    def text_repl(mo):
        inner = mo.group(1)
        pts = _latin_points(inner)
        if pts is not None:
            return pts
        out = inner
        for a, b in WORDS:
            if a in out:
                out = out.replace(a, "}" + b + r"\text{")
        out = r"\text{" + out + "}"
        out = out.replace(r"\text{}", "").replace(r"\text{ }", r"\ ")
        return out
    m = re.sub(r"\\text\{([^{}]*)\}", text_repl, m)
    # arcs: \widehat{GD} etc. keep; sexagesimal already Latin
    return m

def convert_markdown(md):
    """Convert every $...$ and $$...$$ segment."""
    def disp(mo): return "$$" + convert_math(mo.group(1)) + "$$"
    md = re.sub(r"\$\$(.+?)\$\$", disp, md, flags=re.S)
    def inl(mo): return "$" + convert_math(mo.group(1)) + "$"
    md = re.sub(r"(?<!\$)\$(?!\$)([^$\n]+?)\$", inl, md)
    return md

def leftovers(md):
    bad = []
    for seg in re.findall(r"\$\$(.+?)\$\$", md, flags=re.S) + re.findall(r"(?<!\$)\$(?!\$)([^$\n]+?)\$", md):
        if re.search("[\u0600-\u06ff]", seg):
            bad.append(seg)
    return bad
