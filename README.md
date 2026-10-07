# استيعاب الوجوه الممكنة في صنعة الأسطرلاب — البيروني

دراسة وإعادة رسم للأشكال الخمسة والثمانين من نسخة المكتبة البريطانية Or 5593، مع المعادلات والتعليق.

- `book/out/Istiab_Biruni.docx` — الكتاب (Word). عند فتحه في Word: انقر بالزر الأيمن على جدول المحتويات ← «تحديث الحقل». الخط المستعمل Amiri (مجاني، مرفق في `book/fonts/`).
- `book/figs/ch1.py … ch9.py` — بناء كل شكل بالحساب (Python/matplotlib)، مع اختبارات التحقق.
- `book/text/` — نصوص الدراسة (`*.md`) والتعليق على الأشكال ومعادلاتها (`ft*.py`).
- `figures-atlas/` — صور الأشكال من المخطوط والأطلس الأول.

البناء:

```
cd book
python3 tpl/make_ref.py          # قالب Word العربي
python3 build_figs.py            # الأشكال -> out/fig/*.png و out/checks.json
python3 build_book.py            # الكتاب -> out/Istiab_Biruni.docx
```

المتطلبات: Python 3 مع matplotlib ≥ 3.11 (لتشكيل الحروف العربية)، numpy، pandoc ≥ 3.
