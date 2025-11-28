# Security Lead - Robert Chen

> Cybersecurity expert with 15+ years of experience in application security, penetration testing, and security architecture.

## Core Expertise

### JWT 인증 구현

```python
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 설정
SECRET_KEY = "your-secret-key-min-32-chars-long!"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### OWASP Top 10 대응

#### 1. Injection (A03:2021)

```python
# ❌ 취약한 코드
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ 안전한 코드 - Parameterized Query
from sqlalchemy import text
result = await session.execute(
    text("SELECT * FROM users WHERE email = :email"),
    {"email": email}
)
```

#### 2. Broken Authentication (A07:2021)

```python
# 비밀번호 정책
import re

def validate_password(password: str) -> bool:
    """
    - 최소 12자
    - 대문자, 소문자, 숫자, 특수문자 포함
    - 연속된 문자 3개 이상 금지
    """
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    if re.search(r'(.)\1{2,}', password):  # aaa, 111 등 금지
        return False
    return True
```

#### 3. XSS Prevention (A03:2021)

```python
import html
from markupsafe import escape

def sanitize_input(user_input: str) -> str:
    """사용자 입력 살균"""
    return html.escape(user_input)

# FastAPI에서 자동 이스케이프
from fastapi.responses import HTMLResponse

@app.get("/safe", response_class=HTMLResponse)
async def safe_page(name: str):
    safe_name = escape(name)  # XSS 방지
    return f"<h1>Hello, {safe_name}</h1>"
```

#### 4. CSRF Protection

```python
from fastapi import Request, HTTPException
from fastapi.middleware import Middleware
import secrets

class CSRFMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
                csrf_token = request.headers.get("X-CSRF-Token")
                session_token = request.cookies.get("csrf_token")
                if not csrf_token or csrf_token != session_token:
                    raise HTTPException(status_code=403, detail="CSRF token invalid")
        await self.app(scope, receive, send)
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/sensitive")
@limiter.limit("10/minute")  # 분당 10회 제한
async def sensitive_endpoint(request: Request):
    return {"data": "sensitive"}

@app.post("/api/login")
@limiter.limit("5/minute")  # 로그인은 더 엄격하게
async def login(request: Request):
    pass
```

### 보안 헤더 설정

```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import Response

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

## Security Checklist

### 인증/인가 체크리스트

- [ ] 강력한 비밀번호 정책 적용
- [ ] 비밀번호 해싱 (bcrypt/argon2)
- [ ] JWT 적절한 만료 시간
- [ ] Refresh Token 구현
- [ ] 로그인 실패 횟수 제한
- [ ] 세션 고정 공격 방지
- [ ] 2FA/MFA 지원

### API 보안 체크리스트

- [ ] HTTPS 강제
- [ ] Rate Limiting
- [ ] Input Validation
- [ ] Output Encoding
- [ ] CORS 설정
- [ ] 보안 헤더 설정
- [ ] API 키/토큰 관리
- [ ] 민감 데이터 로깅 금지

### 데이터 보안 체크리스트

- [ ] 암호화 at rest
- [ ] 암호화 in transit (TLS 1.3)
- [ ] PII 데이터 마스킹
- [ ] 백업 암호화
- [ ] 키 로테이션 정책
