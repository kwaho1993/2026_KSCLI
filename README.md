# 2026 면역학회 웹 학회지 만들기

이 프로젝트는 학회지 자료를 PDF와 이미지로 모아 GitHub Pages에서 볼 수 있는 웹 학회지를 만드는 정적 웹 프로젝트입니다. 발표자료와 광고 PDF를 정해진 폴더에 넣고 `generate_metadata.py`를 실행하면, 웹에서 빠르게 열리는 WebP 페이지 이미지, 전체 다운로드용 PDF, QR 코드가 생성됩니다.

## 결과물

- 웹 뷰어: `index.html`
- 웹 뷰어용 페이지 이미지: `book/img/*.webp`
- 웹 뷰어용 목차/페이지 정보: `book/metadata.json`
- 전체 다운로드용 학회지 PDF: `book/journal.pdf`
- GitHub Pages 접속 QR 코드: `qr.png`

## 폴더 구조

```text
.
├── index.html
├── sw.js
├── generate_metadata.py
├── .env
├── qr.png
└── book
    ├── cover
    │   └── 표지 이미지 또는 PDF
    ├── ad
    │   └── 광고 PDF
    ├── papers
    │   └── 발표자료 PDF
    ├── img
    │   └── 자동 생성되는 WebP 이미지
    ├── metadata.json
    └── journal.pdf
```

직접 넣는 원본 자료는 `book/cover`, `book/ad`, `book/papers`에만 둡니다. `book/img`, `book/metadata.json`, `book/journal.pdf`, `qr.png`는 스크립트가 다시 만들 수 있는 산출물입니다.

## 원본 자료 넣는 방법

### 표지

표지는 `book/cover` 폴더에 넣습니다.

사용 가능한 확장자:

- `.png`
- `.jpg`
- `.jpeg`
- `.pdf`

예시:

```text
book/cover/2026_면역검사학회_표지.png
```

표지는 파일명 기준으로 정렬되어 학회지 앞부분에 들어갑니다. 표지를 하나만 쓸 경우 파일명은 자유롭게 두어도 됩니다.

### 광고

광고는 `book/ad` 폴더에 넣습니다.

권장 확장자:

- `.pdf`

광고 순서는 파일명 오름차순입니다. 원하는 순서가 있으면 앞에 번호를 붙입니다.

권장 파일명:

```text
광고01_회사명.pdf
광고02_회사명.pdf
광고03_회사명.pdf
```

예시:

```text
book/ad/광고01_태진엠디.pdf
book/ad/광고02_ROCHE_1.pdf
book/ad/광고13_SYSMEX.pdf
```

광고 PDF가 여러 페이지이면 각 페이지가 순서대로 학회지에 포함됩니다.

### 발표자료

발표자료는 `book/papers` 폴더에 넣습니다.

권장 확장자:

- `.pdf`

발표 순서도 파일명 오름차순입니다. 실제 프로그램 순서와 맞추려면 앞에 연자 번호를 붙입니다.

권장 파일명:

```text
연자01_발표자명_발표제목.pdf
연자02_발표자명_발표제목.pdf
연자03_발표자명_발표제목.pdf
```

예시:

```text
book/papers/연자01_김혜진_KODA_LAB_과_이식검사.pdf
book/papers/연자04_이광호_AI 사용법에 대한 이해.pdf
```

파일명은 웹 목차에도 사용됩니다. `연자01_`, `광고01_` 같은 접두어와 밑줄은 화면에서 보기 좋게 정리됩니다.

## 파일명 규칙

- 순서가 중요한 파일은 `01`, `02`, `03`처럼 두 자리 번호를 붙입니다.
- 한글 파일명은 사용할 수 있습니다.
- 공백도 사용할 수 있지만, 관리와 링크 안정성을 위해 가능하면 밑줄 `_`을 권장합니다.
- 파일명에 `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|` 같은 운영체제 예약 문자는 쓰지 않습니다.
- 같은 이름의 PDF와 이미지가 있으면 생성되는 WebP 파일명이 충돌할 수 있으므로 원본 파일명은 서로 다르게 둡니다.
- GitHub Pages에 올릴 자료는 개별 파일 100MB 미만을 유지합니다. GitHub 일반 저장소는 큰 파일을 거부할 수 있습니다.

## 설정 변경

`.env`에서 생성 옵션을 조정합니다.

```env
AD_RENDER_DPI=150
AD_WEBP_QUALITY=85
PAPER_RENDER_DPI=150
PAPER_WEBP_QUALITY=85
SITE_URL=https://사용자명.github.io/저장소명/
JOURNAL_FILENAME=2026_면역검사학회_학회지.pdf
```

주요 항목:

- `SITE_URL`: GitHub Pages에 공개될 주소입니다. QR 코드에 들어갑니다.
- `JOURNAL_FILENAME`: 웹에서 전체 PDF를 다운로드할 때 보이는 파일명입니다.
- `AD_RENDER_DPI`, `PAPER_RENDER_DPI`: PDF를 이미지로 바꿀 때 해상도입니다. 높이면 선명하지만 파일이 커집니다.
- `AD_WEBP_QUALITY`, `PAPER_WEBP_QUALITY`: WebP 압축 품질입니다. 높이면 선명하지만 로딩이 느려질 수 있습니다.

## 학회지 생성

처음 한 번 의존성을 설치합니다.

```powershell
py -m pip install pypdf pymupdf qrcode[pil] python-dotenv
```

자료를 넣은 뒤 프로젝트 루트에서 실행합니다.

```powershell
py generate_metadata.py
```

실행하면 다음 파일이 갱신됩니다.

- `book/img/*.webp`
- `book/metadata.json`
- `book/journal.pdf`
- `qr.png`

`book/img` 폴더는 실행할 때마다 삭제 후 다시 생성됩니다. 이 폴더에는 직접 관리해야 하는 원본 파일을 넣지 마세요.

자료를 추가, 삭제, 교체하거나 `.env`를 수정했다면 반드시 다시 실행합니다.

## 로컬 확인

브라우저 보안 정책 때문에 `index.html`을 파일로 직접 여는 것보다 로컬 서버로 확인하는 것이 좋습니다.

```powershell
py -m http.server 8000
```

브라우저에서 아래 주소를 엽니다.

```text
http://localhost:8000/
```

확인할 항목:

- 첫 화면이 정상적으로 로딩되는지
- 목차 버튼이 열리는지
- 광고와 연자 목차 순서가 맞는지
- 각 PDF 페이지가 잘리지 않고 보이는지
- 전체 PDF 다운로드가 되는지
- 모바일 화면에서 스크롤과 목차가 자연스러운지

## GitHub Pages에 게시하기

이 프로젝트는 루트에 `index.html`이 있으므로 GitHub Pages의 배포 위치를 `main` 브랜치의 `/root`로 설정하는 방식이 가장 단순합니다.

### 1. GitHub 저장소 준비

저장소를 만들고 프로젝트 파일 전체를 커밋합니다.

```powershell
git add .
git commit -m "Publish web journal"
git branch -M main
git remote add origin https://github.com/사용자명/저장소명.git
git push -u origin main
```

이미 원격 저장소가 연결되어 있다면 `remote add`는 생략합니다.

### 2. Pages 설정

GitHub 저장소 화면에서 다음 순서로 설정합니다.

1. `Settings`로 이동합니다.
2. 왼쪽 메뉴에서 `Pages`를 엽니다.
3. `Build and deployment`의 `Source`를 `Deploy from a branch`로 선택합니다.
4. `Branch`를 `main`, 폴더를 `/root`로 선택합니다.
5. `Save`를 누릅니다.

GitHub 공식 문서 기준으로, 선택한 브랜치와 폴더에 변경 사항을 push하면 GitHub Pages가 해당 내용을 게시합니다.

### 3. 공개 주소 확인

일반적인 프로젝트 Pages 주소는 다음 형식입니다.

```text
https://사용자명.github.io/저장소명/
```

예시:

```text
https://kwaho1993.github.io/2026_KSCLI/
```

이 주소가 `.env`의 `SITE_URL`과 같아야 `qr.png`가 올바른 주소로 연결됩니다. 주소를 바꿨다면 `.env`를 수정한 뒤 다시 실행합니다.

```powershell
py generate_metadata.py
git add .
git commit -m "Update site URL"
git push
```

## 업데이트 게시

자료를 수정한 뒤에는 아래 순서로 진행합니다.

```powershell
py generate_metadata.py
py -m http.server 8000
git status
git add .
git commit -m "Update journal materials"
git push
```

GitHub Pages 반영에는 보통 약간의 시간이 걸립니다. 저장소의 `Actions` 탭 또는 `Settings > Pages`에서 배포 상태를 확인할 수 있습니다.

## 주의사항

- `book/img`는 원본을 바탕으로 자동 생성되며, `generate_metadata.py` 실행 시 기존 내용이 삭제됩니다. 직접 보관해야 하는 파일은 넣지 않습니다.
- 파일 순서는 폴더별 파일명 정렬로 결정됩니다. 프로그램 순서를 바꾸려면 파일명 번호를 바꾼 뒤 다시 생성합니다.
- `book/metadata.json`이 없거나 깨지면 웹 뷰어가 열리지 않습니다. 스크립트를 다시 실행합니다.
- `book/journal.pdf`는 WebP 이미지를 다시 PDF로 묶은 파일입니다. 원본 PDF의 텍스트 검색성은 유지되지 않을 수 있습니다.
- 발표자료 PDF가 가로 슬라이드이면 웹에서도 가로 비율로 표시됩니다. 세로 광고와 섞여도 동작하지만 스크롤 길이가 길어질 수 있습니다.
- DPI와 품질을 너무 높이면 GitHub Pages 로딩이 느려지고 저장소 용량이 커집니다. 기본값 `150 DPI`, 품질 `85`부터 확인하는 것을 권장합니다.
- 서비스 워커가 이미지를 캐시하므로, 게시 후 같은 브라우저에서 예전 이미지가 보이면 새로고침하거나 브라우저 캐시를 비웁니다.
- 저장소 이름이나 GitHub 사용자명을 바꾸면 공개 주소도 바뀝니다. `.env`의 `SITE_URL`을 함께 수정하고 QR 코드를 다시 생성합니다.
- GitHub Pages는 정적 파일 호스팅입니다. 서버에서 PDF를 변환하지 않으므로, 변환 작업은 반드시 로컬에서 끝낸 뒤 결과물을 push해야 합니다.

## 참고

- GitHub Pages 배포 소스 설정: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
