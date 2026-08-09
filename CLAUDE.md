# Gabi Studio — 프로젝트 작업 환경 (gabi-studio)

피아노 스튜디오 **모바일 원페이지**. 바이올린(alice-violin)과 같은 "생활코딩" 레시피 — 정적 HTML + 무료 서비스, 최소 유지보수. (가치관: nas-admin 메모리 `values-appropriate-tech`.)

> **새 세션(Claude)에게**: 이 파일은 워크스페이스 열 때 자동 로드됩니다. 여기가 출처. 사용자 안내는 `README.md`.

## 무엇 / 누구
- 스튜디오 공식명(구글 등록): **Gabi Studio Music & Art** (Langley, BC). 피아노 중심 + 아트.
- **로고 확보**: `assets/logo.png`(블랙, 흰 배경용 — 히어로에 사용), `assets/logo-light.png`(베이지, 어두운 배경용). 원본 3종 `assets/logos/`(ai/pdf/png/jpg). Sempé풍 손그림 + "Gabi Studio Music&Art" 손글씨.
- ⚠️ 폼은 현재 **피아노 경험** 항목 — 브랜드가 music&art라 아트까지 넓힐지 사용자 확인 필요.
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

### HTTPS 상태
- ✅ **라이브** (2026-08-09): https://www.gabistudio.ca/ 200, apex→www 301, Let's Encrypt 인증서, **Enforce HTTPS on**.
- 발급이 ~하루 멈춰 있었음(설정은 정상이었음) → **커스텀 도메인 CNAME 제거→재추가 넛지**로 재트리거해 해결. 다음에 또 멈추면 같은 방법.

### Cloudflare 설정 — ✅ 완료 (프록시 ON, DDoS 보호)
- `www` CNAME → `taehyungalexkim.github.io`, apex A·AAAA → GitHub IP — **전부 Proxied(주황)**.
- **SSL/TLS = Full** (strict 아님 — GitHub 인증서 갱신 삐끗해도 안 죽게), **Always Use HTTPS on**.
- 효과: 무료 플랜 **상시 DDoS 완화(L3/4/7)** + origin GitHub IP 은닉 + 엣지 캐싱. **Cloudflare Web Analytics** 사용 가능.
- ⚠️ GitHub 인증서는 ~90일마다 자동 갱신 — 프록시 뒤라 드물게 갱신 삐끗 가능성. **2026-11초쯤 https 정상인지 한 번 확인** 권장.
- 변경 수단: Zone(Read)+DNS(Edit)+Zone Settings(Edit) 스코프 CF API 토큰 (비밀, 커밋 금지, 사용 후 폐기).

## 디자인 / 구성
- **흰색 계열 고급 톤**: 아이보리(`#fbfaf7`) 배경 + 소프트 차콜 텍스트 + 더스티 블루 포인트(`#7f97a6`) + hairline. 순검정 미사용.
- 폰트: 로고 Caveat / EN 제목 Cormorant Garamond / EN 본문 Nunito Sans / KO Nanum Myeongjo+Noto Sans KR. Sempé 미학 = 타이포 + 가는 선(삽화 없음, 추후 로고 제공).
- **EN/KO 언어 토글**(우상단, localStorage 기억). 텍스트는 `.en`/`.ko` span, body class로 전환.
- **플로팅 하단 메뉴**: About·Location·Contact(소개·오시는 길·문의) + 스크롤스파이.
- 섹션: 히어로 · 소개 · **피아노** · **미술** · 오시는 길(**정적 지도 이미지 + 길찾기 링크**) · 문의 폼. (플로팅 메뉴 5항목, 스크롤스파이.)
- **폼**(Formsubmit AJAX): 학생 이름·나이·학년·연락처·이메일·피아노 경험(select)·레벨/비고.
  - ✅ **활성화 완료** — 엔드포인트 = Formsubmit 별칭 `dc8822359e8161279e6a2414f2114f51` (Gmail로 전송, 소스에 이메일 평문 없음). end-to-end 전송 검증됨.
- 방문 카운터: GoatCounter (코드 미정, `<head>`에 주석 자리표시).

## 상태 / 다음
- 🟡 스켈레톤 배포 단계. 본문은 **로렘 입숨 + 한국어 자리표시**.
- 받아 채울 것: 소개글(EN/KO), 주소(EN/KO)+정적 지도 이미지+길찾기 링크, 로고 파일, GoatCounter 코드.
- 폼: 배포 후 라이브에서 1회 제출 → Gmail의 Activate 링크 클릭 → 별칭 받아 교체.
- 규약: 연락처 평문 소스 노출 0 유지, 변경=커밋=배포.

## 파일
`index.html`, `CNAME`(www.gabistudio.ca), `CLAUDE.md`, (예정) `README.md`, `assets/`(지도·로고).
