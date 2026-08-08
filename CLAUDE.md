# Gabi Studio — 프로젝트 작업 환경 (gabi-studio)

피아노 스튜디오 **모바일 원페이지**. 바이올린(alice-violin)과 같은 "생활코딩" 레시피 — 정적 HTML + 무료 서비스, 최소 유지보수. (가치관: nas-admin 메모리 `values-appropriate-tech`.)

> **새 세션(Claude)에게**: 이 파일은 워크스페이스 열 때 자동 로드됩니다. 여기가 출처. 사용자 안내는 `README.md`.

## 무엇 / 누구
- 스튜디오: **Gabi Studio** (피아노, Vancouver). 로고는 추후 제공 → 현재 텍스트 로고("Gabi. Studio", Caveat 폰트).
- 사용자(나)가 기술 담당, 선생님 무관여가 원칙.
- ⚠️ `~/piano-invoice`(피아노 인보이스 시스템)와 **같은 스튜디오인지 미확인** — 확인되면 브랜딩/이메일 일원화.

## 라이브 / 배포
| 항목 | 값 |
|---|---|
| 도메인 | **www.gabistudio.ca** (apex는 www로 리다이렉트) |
| repo | `TaehyungAlexKim/gabi-studio` (**PUBLIC**) |
| 호스팅 | GitHub Pages (main/root). 배포 = `git push` |
| DNS | Cloudflare (NS: jerry/jocelyn). `www` CNAME → `taehyungalexkim.github.io` |
| 커밋 트레일러 | `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` |

⚠️ **PUBLIC repo — 비밀/평문 이메일 커밋 금지.** (nas-admin(private)과 별개.)

### Cloudflare 설정 (진행 중)
- `www` → CNAME → `taehyungalexkim.github.io` (인증서 발급까진 **회색 구름=DNS only**)
- apex `gabistudio.ca` → **www 리다이렉트**(Redirect Rule)
- SSL/TLS = **Full** (Flexible 금지 — 리다이렉트 루프). 발급 후 Enforce HTTPS.
- 설정 수단: 사용자가 **Zone DNS Edit 스코프 Cloudflare API 토큰** 제공 → curl로 레코드 생성, dig 검증. (토큰=비밀, 커밋 금지.)

## 디자인 / 구성
- **흰색 계열 고급 톤**: 아이보리(`#fbfaf7`) 배경 + 소프트 차콜 텍스트 + 더스티 블루 포인트(`#7f97a6`) + hairline. 순검정 미사용.
- 폰트: 로고 Caveat / EN 제목 Cormorant Garamond / EN 본문 Nunito Sans / KO Nanum Myeongjo+Noto Sans KR. Sempé 미학 = 타이포 + 가는 선(삽화 없음, 추후 로고 제공).
- **EN/KO 언어 토글**(우상단, localStorage 기억). 텍스트는 `.en`/`.ko` span, body class로 전환.
- **플로팅 하단 메뉴**: About·Location·Contact(소개·오시는 길·문의) + 스크롤스파이.
- 섹션: 히어로 · 소개 · 오시는 길(**정적 지도 이미지 + 길찾기 링크**) · 문의 폼.
- **폼**(Formsubmit AJAX): 학생 이름·나이·학년·연락처·이메일·피아노 경험(select)·레벨/비고.
  - 엔드포인트 이메일은 **char-code 조립**(평문 비노출). 활성화 후 **별칭으로 교체**(index.html의 `endpoint` 한 줄).
- 방문 카운터: GoatCounter (코드 미정, `<head>`에 주석 자리표시).

## 상태 / 다음
- 🟡 스켈레톤 배포 단계. 본문은 **로렘 입숨 + 한국어 자리표시**.
- 받아 채울 것: 소개글(EN/KO), 주소(EN/KO)+정적 지도 이미지+길찾기 링크, 로고 파일, GoatCounter 코드.
- 폼: 배포 후 라이브에서 1회 제출 → Gmail의 Activate 링크 클릭 → 별칭 받아 교체.
- 규약: 연락처 평문 소스 노출 0 유지, 변경=커밋=배포.

## 파일
`index.html`, `CNAME`(www.gabistudio.ca), `CLAUDE.md`, (예정) `README.md`, `assets/`(지도·로고).
