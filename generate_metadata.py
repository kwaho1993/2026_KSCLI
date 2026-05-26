"""
모든 PDF → WebP 이미지 변환 → book/metadata.json 저장
GitHub Pages QR 코드 → qr.png 저장

실행: python generate_metadata.py
의존성: pip install pypdf pymupdf qrcode[pil]
"""

import json
from pathlib import Path
from pypdf import PdfReader
import fitz
from PIL import Image
import qrcode

SITE_URL     = 'https://kwaho1993.github.io/2026_KSCLI/'
IMG_DIR      = Path('book/img')
RENDER_DPI   = 150   # 높일수록 선명, 파일 크기 증가
WEBP_QUALITY = 85    # 1-100

DIR_ORDER = {'ad': 0, 'papers': 1}

pdf_files = sorted(
    Path('book').rglob('*.pdf'),
    key=lambda p: (DIR_ORDER.get(p.parent.name, 99), p.name),
)

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
    try:
        ratios = get_page_ratios(path)
        img_paths = render_to_webp(path, IMG_DIR, RENDER_DPI, WEBP_QUALITY)
        pages = [
            {"ratio": r, "img": p.as_posix()}
            for r, p in zip(ratios, img_paths)
        ]
        total_kb = sum(p.stat().st_size for p in img_paths) // 1024
        tag = 'ad ' if path.parent.name == 'ad' else 'pdf'
        print(f"  [{tag}] {path.name}  ({len(ratios)}p)  {total_kb}KB")
        metadata.append({"url": path.as_posix(), "pages": pages})
    except Exception as e:
        print(f"  FAIL  {path.name}: {e}")

out = Path('book/metadata.json')
out.write_text(json.dumps(metadata, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(f"\n→ {out}  ({out.stat().st_size:,} bytes)")

# ── QR 코드 ───────────────────────────────────────────────────────────────────

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
qr.add_data(SITE_URL)
qr.make(fit=True)
qr.make_image(fill_color='black', back_color='white').save('qr.png')
print(f"→ qr.png  ({Path('qr.png').stat().st_size:,} bytes)  {SITE_URL}")
