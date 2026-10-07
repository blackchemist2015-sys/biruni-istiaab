"""Build tpl/reference.docx: Arabic (RTL) styles in Amiri, A4 pages, page numbers in the footer."""
import re, subprocess, zipfile, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "pandoc-default.docx")
OUT = os.path.join(HERE, "reference.docx")
subprocess.run(["pandoc", "-o", SRC, "--print-default-data-file", "reference.docx"], check=True)

FONT = "Amiri"
INK = "7A1E14"          # the manuscript's red ink, darkened

zin = zipfile.ZipFile(SRC)
files = {n: zin.read(n) for n in zin.namelist()}

s = files["word/styles.xml"].decode()
fonts = f'<w:rFonts w:ascii="{FONT}" w:hAnsi="{FONT}" w:eastAsia="{FONT}" w:cs="{FONT}" />'
s = re.sub(r'<w:rFonts [^>]*/>', fonts, s)
s = s.replace('<w:sz w:val="24" />\n        <w:szCs w:val="24" />', '<w:sz w:val="28" />\n        <w:szCs w:val="28" />')
s = s.replace('<w:lang w:val="en-US" w:eastAsia="en-US" w:bidi="ar-SA" />', '<w:rtl /><w:lang w:val="ar-SA" w:eastAsia="en-US" w:bidi="ar-SA" />')
s = s.replace('<w:pPrDefault>\n      <w:pPr>\n        <w:spacing w:after="200" />',
              '<w:pPrDefault>\n      <w:pPr>\n        <w:bidi />\n        <w:jc w:val="both" />\n        <w:spacing w:after="120" w:line="312" w:lineRule="auto" />')
# colours and sizes of headings and title
s = re.sub(r'<w:color [^>]*/>', f'<w:color w:val="{INK}" />', s)
def setsize(sid, half_points):
    global s
    m = re.search(r'(<w:style [^>]*w:styleId="%s".*?</w:style>)' % sid, s, re.S)
    if not m: return
    blk = m.group(1)
    nb = re.sub(r'<w:sz w:val="\d+" />', f'<w:sz w:val="{half_points}" />', blk)
    nb = re.sub(r'<w:szCs w:val="\d+" />', f'<w:szCs w:val="{half_points}" />', nb)
    if '<w:sz ' not in nb:
        nb = nb.replace('</w:rPr>', f'<w:sz w:val="{half_points}" /><w:szCs w:val="{half_points}" /></w:rPr>')
    if '<w:bCs' not in nb and '<w:b />' in nb:
        nb = nb.replace('<w:b />', '<w:b /><w:bCs />')
    s = s.replace(blk, nb)
for sid, sz in (("Title", 52), ("Subtitle", 34), ("Heading1", 40), ("Heading2", 34), ("Heading3", 30), ("Heading4", 28)):
    setsize(sid, sz)
# headings: centred chapter titles, page break before Heading 1
s = re.sub(r'(<w:style [^>]*w:styleId="Heading1".*?<w:pPr>)', r'\1<w:pageBreakBefore /><w:jc w:val="center" />', s, count=1, flags=re.S)
# captions centred, not italic
s = re.sub(r'(<w:style [^>]*w:styleId="Caption".*?</w:style>)',
           lambda m: re.sub(r'<w:i />', '', m.group(1)).replace('<w:pPr>', '<w:pPr><w:jc w:val="center" />'), s, count=1, flags=re.S)
s = re.sub(r'(<w:style [^>]*w:styleId="ImageCaption".*?)</w:style>',
           r'\1<w:pPr><w:jc w:val="center" /></w:pPr><w:rPr><w:sz w:val="22" /><w:szCs w:val="22" /><w:color w:val="555555" /></w:rPr></w:style>', s, count=1, flags=re.S)
s = re.sub(r'(<w:style [^>]*w:styleId="CaptionedFigure".*?)</w:style>', r'\1<w:pPr><w:jc w:val="center" /><w:keepNext /></w:pPr></w:style>', s, count=1, flags=re.S)
s = re.sub(r'(<w:style [^>]*w:styleId="Figure".*?)</w:style>', r'\1<w:pPr><w:jc w:val="center" /><w:keepNext /></w:pPr></w:style>', s, count=1, flags=re.S)
s = re.sub(r'(<w:style [^>]*w:styleId="BlockText".*?)</w:style>',
           r'\1<w:pPr><w:ind w:left="567" w:right="567" /><w:shd w:val="clear" w:color="auto" w:fill="F6F1E7" /></w:pPr></w:style>', s, count=1, flags=re.S)
files["word/styles.xml"] = s.encode()

# footer with the page number
footer = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
          '<w:p><w:pPr><w:bidi /><w:jc w:val="center" /></w:pPr>'
          '<w:r><w:fldChar w:fldCharType="begin" /></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
          '<w:r><w:fldChar w:fldCharType="separate" /></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end" /></w:r>'
          '</w:p></w:ftr>')
files["word/footer1.xml"] = footer.encode()
rels = files["word/_rels/document.xml.rels"].decode()
rels = rels.replace('</Relationships>',
    '<Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/></Relationships>')
files["word/_rels/document.xml.rels"] = rels.encode()
ct = files["[Content_Types].xml"].decode()
ct = ct.replace('</Types>', '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
files["[Content_Types].xml"] = ct.encode()
d = files["word/document.xml"].decode()
sect = ('<w:sectPr><w:footerReference w:type="default" r:id="rIdFooter1" />'
        '<w:pgSz w:w="11906" w:h="16838" /><w:pgMar w:top="1418" w:right="1304" w:bottom="1304" w:left="1304" w:header="709" w:footer="567" w:gutter="0" />'
        '<w:bidi /></w:sectPr>')
d = re.sub(r'<w:sectPr.*?</w:sectPr>', sect, d, flags=re.S) if '<w:sectPr' in d else d.replace('</w:body>', sect + '</w:body>')
if 'xmlns:r=' not in d[:2000]:
    d = d.replace('<w:document ', '<w:document xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
files["word/document.xml"] = d.encode()

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zo:
    for n, b in files.items():
        zo.writestr(n, b)
os.remove(SRC)
print("wrote", OUT)
