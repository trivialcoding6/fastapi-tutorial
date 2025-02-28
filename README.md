# FastAPI Todo API

이 프로젝트는 FastAPI 환경 세팅을 위한 tutorial 로 간단한 todo API를 구현한 프로젝트입니다.

## 기능

- Todo 항목 생성
- 단일 Todo 항목 조회
- 모든 Todo 항목 조회 (상태별 필터링 가능)
- Todo 항목 업데이트
- Todo 항목 삭제

## 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **SQLAlchemy**: ORM(Object-Relational Mapping)
- **Pydantic**: 데이터 검증 및 설정 관리
- **PostgreSQL**: 데이터베이스
- **Alembic**: 데이터베이스 마이그레이션
- **Pytest**: 테스트 프레임워크
- **Loguru**: 로깅 라이브러리

## 프로젝트 구조

```
├── app
│   ├── api # API 라우터 및 엔드포인트
│   ├── core # 핵심 설정 및 유틸리티
│   ├── crud # 데이터베이스 CRUD 작업
│   ├── db # 데이터베이스 연결 및 세션 관리
│   ├── models SQLAlchemy 모델
│   ├── schemas # Pydantic 스키마
│   ├── services # 비즈니스 로직
│   └── tests # 테스트 코드
│   ├── main.py
├── migrations # Alembic 마이그레이션 파일
│   ├── env.py
├── poetry.lock
├── pyproject.toml
├── alembic.ini  # Alembic 설정
└── pytest.ini  # Pytest 설정
```

## 설치 및 실행

### 필수 조건

- Python 3.11 이상
- PostgreSQL
- Poetry

### 환경 설정

1. 저장소 클론:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Poetry를 사용하여 의존성 설치:

```bash
poetry install
```

3. `.env` 파일 생성:

```
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SYNC_DATABASE_URL=postgresql://user:password@localhost/dbname
DB_ECHO_LOG=False
```

### 데이터베이스 마이그레이션
