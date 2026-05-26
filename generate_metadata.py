"""
모든 PDF → WebP 이미지 변환 → book/metadata.json 저장
GitHub Pages QR 코드 → qr.png 저장

실행: python generate_metadata.py
의존성: pip install pypdf pymupdf qrcode[pil] python-dotenv
설정:  .env 파일에서 DPI, 품질, URL 조정
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader
import fitz
from PIL import Image
import qrcode

load_dotenv()

SITE_URL          = os.getenv('SITE_URL',          'https://kwaho1993.github.io/2026_KSCLI/')
AD_RENDER_DPI     = int(os.getenv('AD_RENDER_DPI',     '150'))
AD_WEBP_QUALITY   = int(os.getenv('AD_WEBP_QUALITY',   '85'))
PAPER_RENDER_DPI  = int(os.getenv('PAPER_RENDER_DPI',  '150'))
PAPER_WEBP_QUALITY = int(os.getenv('PAPER_WEBP_QUALITY', '85'))

IMG_DIR   = Path('book/img')
DIR_ORDER = {'ad': 0, 'papers': 1}

pdf_files = sorted(
    Path('book').rglob('*.pdf'),
    key=lambda p: (DIR_ORDER.get(p.parent.name, 99), p.name),
)

print(f'설정: 광고 {AD_RENDER_DPI}DPI/q{AD_WEBP_QUALITY}  논문 {PAPER_RENDER_DPI}DPI/q{PAPER_WEBP_QUALITY}')
print(f'      URL: {SITE_URL}')
print()

# ── 헬퍼 ─────────────────────────────────────────────────────────────────────

def get_page_ratios(path: Path) -> list[float]:
    reader = PdfReader(path)
    ratios = []
    for page in reader.pages:
        w = float(page.mediabox.width)
        h = float(page.mediabox.height)
        if page.rotation in (90, 270):
            w, h = h, w
        ratios.append(round(h / w, 6))
    return ratios

def render_to_webp(pdf_path: Path, out_dir: Path, dpi: int, quality: int) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    paths = []
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), alpha=False)
        img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        out_path = out_dir / f"{pdf_path.stem}_p{i + 1}.webp"
        img.save(out_path, 'WEBP', quality=quality, method=6)
        paths.append(out_path)
    doc.close()
    return paths

# ── metadata.json ─────────────────────────────────────────────────────────────

metadata = []
for path in pdf_files:
    is_ad = path.parent.name == 'ad'
    dpi     = AD_RENDER_DPI    if is_ad else PAPER_RENDER_DPI
    quality = AD_WEBP_QUALITY  if is_ad else PAPER_WEBP_QUALITY
    tag     = 'ad ' if is_ad else 'pdf'
    try:
        ratios    = get_page_ratios(path)
        img_paths = render_to_webp(path, IMG_DIR, dpi, quality)
        pages     = [{"ratio": r, "img": p.as_posix()} for r, p in zip(ratios, img_paths)]
        total_kb  = sum(p.stat().st_size for p in img_paths) // 1024
        print(f'  [{tag}] {path.name}  ({len(ratios)}p)  {total_kb}KB')
        metadata.append({"url": path.as_posix(), "pages": pages})
    except Exception as e:
        print(f'  FAIL  {path.name}: {e}')

out = Path('book/metadata.json')
out.write_text(json.dumps(metadata, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f'\n→ {out}  ({out.stat().st_size:,} bytes)')

# ── QR 코드 ───────────────────────────────────────────────────────────────────

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
qr.add_data(SITE_URL)
qr.make(fit=True)
qr.make_image(fill_color='black', back_color='white').save('qr.png')
print(f'→ qr.png  ({Path("qr.png").stat().st_size:,} bytes)  {SITE_URL}')
