"""
광고 PDF → WebP 이미지 변환 + 전체 페이지 종횡비 추출 → book/metadata.json 저장
GitHub Pages QR 코드 → qr.png 저장

실행: python generate_metadata.py
의존성: pip install pypdf pymupdf qrcode[pil]
"""

import json
from pathlib import Path
from pypdf import PdfReader
import fitz  # pymupdf
from PIL import Image
import qrcode

SITE_URL       = 'https://kwaho1993.github.io/2026_KSCLI/'
AD_IMG_DIR     = Path('book/ad_img')
AD_RENDER_DPI  = 150   # 높일수록 선명하지만 파일 크기 증가
AD_WEBP_QUALITY = 85   # 1-100, 낮출수록 파일 크기 감소

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
    is_ad = path.parent.name == 'ad'
    try:
        ratios = get_page_ratios(path)

        if is_ad:
            img_paths = render_to_webp(path, AD_IMG_DIR, AD_RENDER_DPI, AD_WEBP_QUALITY)
            pages = [
                {"ratio": r, "img": p.as_posix()}
                for r, p in zip(ratios, img_paths)
            ]
            sizes = ' + '.join(f"{p.stat().st_size // 1024}KB" for p in img_paths)
            print(f"  [ad]  {path.name}  ({len(ratios)}p)  →  {sizes}")
        else:
            pages = [{"ratio": r} for r in ratios]
            print(f"  [pdf] {path.name}  ({len(ratios)}p)")

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
