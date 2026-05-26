"""
PDF 페이지 종횡비를 추출해 book/metadata.json 으로 저장하고,
GitHub Pages QR 코드를 qr.png 로 저장합니다.
실행: python generate_metadata.py
의존성: pip install pypdf qrcode[pil]
"""

import json
from pathlib import Path
from pypdf import PdfReader
import qrcode

SITE_URL = 'https://kwaho1993.github.io/2026_KSCLI/'

# book/ 하위 PDF를 재귀 탐색 — ad/ → papers/ 순, 각 폴더 내 파일명 정렬
DIR_ORDER = {'ad': 0, 'papers': 1}

pdf_files = sorted(
    Path('book').rglob('*.pdf'),
    key=lambda p: (DIR_ORDER.get(p.parent.name, 99), p.name),
)

# ── metadata.json ─────────────────────────────────────────────────────────────

def extract_ratios(path: Path) -> list[float]:
    reader = PdfReader(path)
    ratios = []
    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        if page.rotation in (90, 270):
            w, h = h, w
        ratios.append(round(h / w, 6))
    return ratios

metadata = []
for path in pdf_files:
    try:
        ratios = extract_ratios(path)
        metadata.append({"url": path.as_posix(), "ratios": ratios})
        print(f"  {path.name}  ({len(ratios)}p)")
    except Exception as e:
        print(f"  FAIL  {path.name}: {e}")

out = Path('book/metadata.json')
out.write_text(json.dumps(metadata, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f"\n→ {out}  ({out.stat().st_size:,} bytes)")

# ── QR 코드 ───────────────────────────────────────────────────────────────────

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
qr.add_data(SITE_URL)
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save('qr.png')
print(f"→ qr.png  ({Path('qr.png').stat().st_size:,} bytes)  {SITE_URL}")
