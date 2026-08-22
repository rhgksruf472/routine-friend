# 루틴프렌드 (RoutineFriend)

헬스장 등록이 부담스러운 홈트 초보자에게, 목표·운동 경험·가용 시간을 입력하면 AI가 맞춤 운동 루틴을 즉석에서 만들어주는 웹 서비스입니다.

| 항목 | 내용 |
|---|---|
| 배포 URL | https://routine-friendtest.vercel.app |
| 페이지 | 홈(`index.html`) / AI 루틴 추천(`routine.html`) / 운동 백과(`encyclopedia.html`) / 소개·문의(`about.html`) |
| 프론트엔드 | 순수 HTML / CSS / JavaScript (프레임워크 없음) |
| 백엔드 | Vercel Serverless Functions (Python) |
| AI | Google Gemini API (`gemini-3.5-flash`), REST 직접 호출 |

## 실행 방법 (로컬)

정적 화면(홈 / 운동 백과 / 소개)은 `index.html` 등을 브라우저로 직접 열어도 확인할 수 있습니다. 다만 **AI 루틴 추천 기능은 서버(`api/routine.py`)가 필요**해서, 로컬에서 전체 기능을 확인하려면 Vercel CLI가 필요합니다.

```bash
npm install -g vercel
vercel dev
```

> Windows 환경에서는 로컬 실행 에뮬레이터(`@vercel/fun`)가 빌드에 쓰인 Python 3.12가 아니라 3.11 문법으로 함수를 실행해 오류가 날 수 있습니다(알려진 제약). AI 기능은 아래 배포 URL에서 확인하는 것을 권장합니다.

## 배포 방법 (Vercel)

1. 이 저장소를 GitHub에 push
2. Vercel 대시보드에서 저장소를 Import (별도 빌드 설정 불필요 — 저장소 루트가 그대로 배포 대상)
3. 환경 변수 `GEMINI_API_KEY` 등록 ([환경 변수 설정](#환경-변수-설정) 참고)
4. Deploy — 이후 `main` 브랜치에 push할 때마다 자동 재배포됩니다.

## 환경 변수 설정

이 프로젝트는 `GEMINI_API_KEY` 하나가 필요합니다. [Google AI Studio](https://ai.google.dev)에서 발급받을 수 있습니다.

**로컬 개발**: 저장소 루트에 `.env` 파일을 만들고 아래처럼 작성합니다.

```
GEMINI_API_KEY=발급받은_키
```

`.env`는 `.gitignore`에 등록되어 있어 git에 커밋되지 않습니다.

**배포 환경**: Vercel 대시보드 → 해당 프로젝트 → Settings → Environment Variables에 `GEMINI_API_KEY`를 등록한 뒤 Redeploy가 필요합니다. 코드(`api/routine.py`)는 `os.environ.get('GEMINI_API_KEY')`로만 키를 읽으며, 코드 어디에도 키 값을 직접 작성하지 않습니다.

## AI 기능 (AI 루틴 추천)

| 구분 | 내용 |
|---|---|
| 입력 | 목표(체중감량/근력/유연성/자세교정), 운동 경험(초급/중급/고급), 하루 가용 시간(15/30/45/60분), 부상·제약 부위(선택) |
| 출력 | 운동 목록(운동명, 세트/횟수 또는 시간, 순서), 예상 소요시간, 주의사항 |
| 실패 처리 | 빈 입력(필수값 누락) 안내 / API 오류(4xx/5xx) 안내 / 응답 지연 시 로딩 표시 + 503(서버 과부하) 최대 3회 자동 재시도 |

## 폴더 구조

```
routine-friend/
├── index.html            # 홈
├── routine.html           # AI 루틴 추천 (핵심 기능)
├── encyclopedia.html      # 운동 백과
├── about.html              # 소개/문의
├── css/style.css           # 공통 스타일 + 반응형(@media)
├── js/main.js               # 여러 페이지가 공유하는 스크립트 자리
├── js/routine.js            # AI 루틴 추천 폼 처리 (fetch, 실패 처리)
├── api/routine.py            # Vercel Serverless Function — Gemini API 호출
├── requirements.txt          # requests
├── .python-version            # Vercel 빌드 Python 버전 고정 (3.12)
└── .gitignore
```

## 보안 주의사항

- API 키는 코드에 직접 작성하지 않고 `os.environ.get()`으로만 읽습니다.
- `.env`는 `.gitignore`에 등록되어 있어 git에 커밋되지 않습니다.
- 인증은 쿼리파라미터가 아닌 **헤더**(`x-goog-api-key`)로 전송합니다.
