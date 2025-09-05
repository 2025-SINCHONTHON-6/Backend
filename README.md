# Backend
2025-SINCHONTHON-6 Backend

차(Tea) 취향 테스트/기록 서비스 TeaBTI의 백엔드입니다. Django Rest Framework 기반으로, 차 추천, 기록, 챌린지 기록 등의 API를 제공합니다.

✨ 서비스 소개

추천: 사용자가 선택한 기분(mood)과 맛(taste)에 따라 조건에 맞는 차 목록을 추천하는 API를 제공합니다.

기록: 차를 마신 경험(느낌, 코멘트)을 생성하고 조회하는 API를 제공합니다.

챌린지 기록: 전체 기록을 기반으로 다양한 챌린지(마신 횟수, 종류 등)의 현재 달성도를 계산하여 제공하는 API를 제공합니다.

🧰 기술 스택

Framework: DRF

Database : SQLite3

Deploy : PythonAnywhere

👥 팀원 소개
이름   역할
황규리  BE
설영은  BE
고선태  BE

🗂 폴더 구조
Backend/                   # Git Repository Root
└── Dsichonsix/            # Django Project Root
    ├── shinchonsix/      # 메인 프로젝트 
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── challenges/        # 챌린지 앱
    │   ├── data/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── checkers.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── recommendations/   # 추천 앱
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   └── ...
    ├── teas/              # 차 정보 앱
    │   ├── data/
    │   ├── migrations/
    │   ├── __init__.py
    │   ├── admin.py
    │   └── ...
    ├── .gitignore
    ├── db.sqlite3
    ├── manage.py
    ├── README.md
    └── requirements.txt

🚀 실행 방법
요구 사항

Python 3.9+

pip

🚀 설치 & 로컬 실행
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 데이터베이스 초기화
python manage.py migrate

# (선택) 초기 데이터 로드
python manage.py loaddata teas/data/teas_teacategory.json
python manage.py loaddata teas/data/teas_tea.json
python manage.py loaddata challenges/data/challenges_challenge.json

# 개발 서버 실행
python manage.py runserver

🔑 API 엔드포인트 개요
GET /recommendations/filter/mood?mood={mood}: 기분에 맞는 맛 필터링 데이터 조회

GET /recommendations/filter/taste?taste_id={taste_id}: 맛에 맞는 최종 차 추천 목록 조회

POST /challenges/recommendations/recent/: '마셔볼래요' 선택한 차 등록

GET /challenges/recommendations/recent/: '마셔볼래요' 선택한 차 목록 조회

POST /challenges/log/: 기록(리뷰) 등록

GET /challenges/status/: 전체 챌린지 진행 현황 조회

GET /challenges/logs/dates/: 전체 기록 날짜 조회

GET /challenges/records/daily?created_at=YYYY-MM-DD: 특정 날짜의 나의 차 기록 조회

네, 제공해주신 모든 모델 코드를 반영하여 README.md 파일의 데이터 모델 파트를 완성해 드릴게요.

💾 데이터 모델
teas app
1. TeaCategory

id: 카테고리 ID (PK)

name: 카테고리 이름

mood: 기분 이름

2. Tea

id: 차 ID (PK)

name: 차 이름

description: 차 설명

tea_category: TeaCategory 참조 (FK)

taste: 차 맛

taste_id: URL용 맛 ID

challenges app
3. Challenge

id: 챌린지 ID (PK)

title: 챌린지 제목

description: 챌린지 설명

challenge_type: 챌린지 종류 (DRINK_COUNT, RECORD_COUNT 등)

4. TeaLogs

id: 로그 ID (PK)

tea: teas.Tea 참조 (FK)

created_at: 차 마신 날짜

feeling: 평가 (좋았어요, 그냥그래요, 별로에요)

comment: 코멘트

🧩 개발 메모

- 초기 데이터는 각 앱의 data 폴더 내 JSON 파일을 통해 관리됩니다.

