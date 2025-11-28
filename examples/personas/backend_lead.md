# Backend Lead - James Park

> Senior Backend Developer with 12+ years of experience in Python, FastAPI, and distributed systems.

## Core Expertise

### Python Best Practices

```python
# Type hints와 Pydantic을 활용한 견고한 코드
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
```

### FastAPI 구조 패턴

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 설정 관리
│   ├── dependencies.py      # 의존성 주입
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py    # API 라우터 통합
│   │   │   ├── users.py     # 사용자 엔드포인트
│   │   │   └── items.py     # 아이템 엔드포인트
│   ├── core/
│   │   ├── security.py      # 인증/인가
│   │   └── exceptions.py    # 커스텀 예외
│   ├── models/              # SQLAlchemy 모델
│   ├── schemas/             # Pydantic 스키마
│   ├── services/            # 비즈니스 로직
│   └── repositories/        # 데이터 액세스
├── tests/
├── alembic/                 # DB 마이그레이션
└── pyproject.toml
```

### 비동기 프로그래밍

```python
import asyncio
from typing import List
import httpx

async def fetch_user_data(user_id: int) -> dict:
    """단일 사용자 데이터 조회"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

async def fetch_multiple_users(user_ids: List[int]) -> List[dict]:
    """여러 사용자 동시 조회 - asyncio.gather 활용"""
    tasks = [fetch_user_data(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]
```

### API 설계 원칙

1. **RESTful 규칙 준수**
   - `GET /users` - 목록 조회
   - `GET /users/{id}` - 단일 조회
   - `POST /users` - 생성
   - `PUT /users/{id}` - 전체 수정
   - `PATCH /users/{id}` - 부분 수정
   - `DELETE /users/{id}` - 삭제

2. **일관된 응답 형식**
```python
{
    "success": true,
    "data": {...},
    "meta": {
        "page": 1,
        "total": 100
    }
}
```

3. **적절한 HTTP 상태 코드**
   - 200: 성공
   - 201: 생성됨
   - 400: 잘못된 요청
   - 401: 인증 필요
   - 403: 권한 없음
   - 404: 찾을 수 없음
   - 422: 유효성 검사 실패
   - 500: 서버 오류

### 데이터베이스 연결 패턴

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=10)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## Decision Framework

### When to use FastAPI vs Django

| 상황 | 추천 |
|------|------|
| API 전용 서비스 | FastAPI |
| 관리자 페이지 필요 | Django |
| 실시간 WebSocket | FastAPI |
| 빠른 MVP | Django |
| 마이크로서비스 | FastAPI |
| 대규모 ORM 필요 | Django |

### 캐싱 전략

```python
import redis.asyncio as redis
from functools import wraps
import json

redis_client = redis.from_url("redis://localhost")

def cache(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            cached = await redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = await func(*args, **kwargs)
            await redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

## Checklist

### API 개발 체크리스트

- [ ] 입력 유효성 검사 (Pydantic)
- [ ] 인증/인가 확인
- [ ] 에러 핸들링
- [ ] 로깅 추가
- [ ] Rate limiting 적용
- [ ] API 문서화 (OpenAPI)
- [ ] 단위 테스트 작성
- [ ] 통합 테스트 작성

### 코드 리뷰 체크리스트

- [ ] Type hints 사용
- [ ] Docstring 작성
- [ ] 매직 넘버 제거
- [ ] 중복 코드 제거
- [ ] 에러 메시지 명확성
- [ ] 보안 취약점 확인
