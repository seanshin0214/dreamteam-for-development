# DreamTeam For Development MCP Server

> **RAG 기반 개발팀 페르소나 지식 검색 MCP 서버**
>
> 이것은 단순히 "당신은 백엔드 개발자입니다"라고 선언하는 페르소나가 아닙니다.
> 17명의 World-Class 개발팀 전문가의 **실제 지식, 코드 패턴, 의사결정 프레임워크, 체크리스트**가
> 벡터 데이터베이스에 임베딩되어 RAG(Retrieval Augmented Generation)로 검색됩니다.

## Why RAG-based Persona?

### 기존 페르소나의 한계

```
❌ 선언형 페르소나:
"당신은 시니어 백엔드 개발자입니다. FastAPI 전문가입니다."

→ LLM의 기존 지식에만 의존
→ 구체적인 코드 패턴, 체크리스트 없음
→ 조직/팀 특화 지식 반영 불가
```

### DreamTeam의 접근

```
✅ RAG 기반 페르소나:
267KB의 전문 지식이 185개 청크로 분할되어 ChromaDB에 임베딩

→ 질문에 관련된 지식만 정확히 검색
→ 실제 코드 예시, 아키텍처 다이어그램 포함
→ 의사결정 프레임워크, 체크리스트 제공
→ Google/Meta/Amazon 수준의 엔지니어링 지식
```

## 포함된 지식

### 17명의 전문가 페르소나

| 역할 | 전문 분야 | 지식 규모 |
|------|----------|----------|
| Solution Architect | 시스템 아키텍처, 설계 패턴, 기술 선택 | 28KB |
| Backend Lead | Python, FastAPI, 비동기 프로그래밍, API 설계 | 24KB |
| Frontend Lead | React, Next.js, 상태 관리, 성능 최적화 | 21KB |
| AI/ML Lead | RAG, LangChain, 벡터 DB, 프롬프트 엔지니어링 | 26KB |
| DevOps Lead | CI/CD, Kubernetes, Terraform, GitOps | 16KB |
| Security Lead | 인증/인가, OWASP Top 10, 보안 패턴 | 9KB |
| QA Lead | 테스트 전략, Playwright, pytest, k6 | 11KB |
| Mobile Lead | React Native, Flutter, 모바일 최적화 | 11KB |
| Product Manager | PRD, 로드맵, RICE 스코어링, 지표 설계 | 9KB |
| Product Owner | 애자일, 사용자 스토리, 스프린트 관리 | 6KB |
| UX Designer | UX/UI, 접근성, 디자인 시스템 | 8KB |
| Data Engineer | 데이터 파이프라인, dbt, Airflow | 9KB |
| Infrastructure Lead | 클라우드, Terraform, AWS/GCP | 8KB |
| Database Engineer | PostgreSQL, 인덱스 설계, 성능 튜닝 | 5KB |
| SRE Lead | SLO/SLI, 모니터링, 인시던트 대응 | 5KB |
| Technical Writer | API 문서화, README, 기술 문서 | 6KB |
| Scrum Master | 스크럼, 회고, 팀 퍼실리테이션 | 7KB |

### 고급 주제

| 주제 | 내용 |
|------|------|
| Hyperscale Systems | Google Spanner, Meta TAO, Bigtable, Consistent Hashing |
| Advanced Topics | Rust/Go 성능, K8s Operator, eBPF, Module Federation |
| Post-Mortems | AWS S3 장애, Facebook BGP, Cloudflare 사례 분석 |
| Quality Standards | 코드 품질, 성능 기준, 보안 체크리스트 |
| Team Collaboration | 기능 개발, 장애 대응, 기술 부채 해결 시나리오 |

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/seanshin0214/dreamteam-for-development.git
cd dreamteam-for-development
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 지식 베이스 구축

페르소나 마크다운 파일이 있는 디렉토리에서:

```bash
python src/data_loader.py "페르소나_파일_경로"
```

### 4. MCP 서버 등록

**Claude Code** (`~/.claude/mcp.json`):
```json
{
  "mcpServers": {
    "dreamteam-for-development": {
      "command": "python",
      "args": ["경로/src/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

**Claude Desktop** (`%APPDATA%/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "dreamteam-for-development": {
      "command": "python",
      "args": ["경로/src/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

**Cursor / Windsurf / Antigravity**:
각 도구의 `~/.{tool}/mcp.json`에 동일하게 추가

## 사용 가능한 도구

### 1. `search_knowledge`
전체 지식 베이스에서 검색

```
예시: "FastAPI에서 JWT 인증 구현 방법"
→ Security Lead + Backend Lead 지식에서 관련 코드/패턴 반환
```

### 2. `search_by_role`
특정 역할의 지식만 검색

```
예시: role="backend_lead", query="비동기 패턴"
→ Backend Lead의 async/await 패턴, 코드 예시 반환
```

### 3. `list_roles`
사용 가능한 역할 목록 조회

### 4. `get_stats`
벡터 스토어 통계 (문서 수, 역할 수)

## 기술 스택

- **MCP**: Model Context Protocol (Anthropic)
- **Vector Store**: ChromaDB
- **Embedding**: sentence-transformers (all-MiniLM-L6-v2)
- **Language**: Python 3.10+

## RAG vs 선언형 페르소나 비교

| 항목 | 선언형 페르소나 | RAG 기반 (DreamTeam) |
|------|---------------|---------------------|
| 지식 소스 | LLM 사전 학습 | 커스텀 지식 베이스 |
| 컨텍스트 효율 | 전체 로드 | 필요한 청크만 검색 |
| 코드 예시 | LLM 생성 | 검증된 패턴 제공 |
| 크로스 도메인 | 불가 | 여러 역할 지식 통합 |
| 업데이트 | 프롬프트 수정 | 지식 베이스 갱신 |
| 정확도 | 가변적 | 임베딩된 지식 기반 |

## Claude Code 슬래시 커맨드 설정

Claude Code에서 `/dreamteam` 명령어로 바로 사용할 수 있습니다.

### 설치 방법

1. 커맨드 파일 복사:
```bash
# Windows
copy claude-code\dreamteam.md %USERPROFILE%\.claude\commands\

# macOS/Linux
cp claude-code/dreamteam.md ~/.claude/commands/
```

2. Claude Code 재시작

### 사용법

```
/dreamteam FastAPI에서 JWT 인증 구현 방법
/dreamteam Kubernetes 배포 전략
/dreamteam React 성능 최적화
/dreamteam PostgreSQL 인덱스 설계
/dreamteam 인시던트 대응 프로세스
```

이 명령어를 사용하면 자동으로 DreamTeam MCP에서 관련 전문가 지식을 검색하고, 필요한 스킬과 함께 종합적인 답변을 제공합니다.

### 지원 클라이언트

| 클라이언트 | MCP 지원 | 슬래시 커맨드 |
|-----------|---------|--------------|
| Claude Code | ✅ | ✅ `/dreamteam` |
| Claude Desktop | ✅ | ❌ |
| Cursor | ✅ | ❌ |
| Windsurf | ✅ | ❌ |

## 라이선스

MIT License

## Author

Created by @seanshin0214

---

> **"페르소나는 선언이 아니라 지식이다."**
>
> DreamTeam은 17명의 전문가가 실제로 알고 있는 것을 RAG로 검색합니다.
