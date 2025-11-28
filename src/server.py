"""DreamTeam MCP Server - RAG 기반 개발팀 페르소나 지식 검색"""
import os
import sys
from pathlib import Path
from typing import Optional

# Windows stdout/stderr UTF-8 설정
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent))

from vector_store import DreamTeamVectorStore


# 벡터 스토어 - 백그라운드 초기화 (서버 시작 빠르게 + 타임아웃 방지)
DATA_DIR = Path(__file__).parent.parent / "data" / "chroma_db"

import threading
_vector_store = None
_init_lock = threading.Lock()
_init_done = threading.Event()

def _background_init():
    """백그라운드에서 모델 로딩"""
    global _vector_store
    _vector_store = DreamTeamVectorStore(str(DATA_DIR))
    _ = _vector_store.encoder  # SentenceTransformer 로드
    _init_done.set()
    print("벡터 스토어 준비 완료", file=sys.stderr)

# 백그라운드 스레드로 즉시 시작
threading.Thread(target=_background_init, daemon=True).start()

def get_vector_store():
    """벡터 스토어 반환 (초기화 완료 대기)"""
    _init_done.wait()  # 초기화 완료까지 대기
    return _vector_store

# MCP 서버 생성
server = Server("dreamteam-for-development")


# 역할별 설명
ROLE_DESCRIPTIONS = {
    "solution_architect": "시스템 아키텍처, 설계 패턴, 기술 선택 (Dr. Michael Torres)",
    "backend_lead": "백엔드 개발, API 설계, Python/FastAPI (James Park)",
    "frontend_lead": "프론트엔드 개발, React, Next.js, 상태관리 (David Kim)",
    "ai_ml_lead": "AI/ML, RAG, LangChain, 벡터DB (Dr. Lisa Wang)",
    "devops_lead": "CI/CD, Kubernetes, 인프라 자동화 (Kevin Zhang)",
    "security_lead": "보안, 인증/인가, OWASP Top 10 (Robert Chen)",
    "qa_lead": "테스트 전략, 자동화, 품질 관리 (Susan Martinez)",
    "mobile_lead": "모바일 개발, React Native, Flutter (Chris Anderson)",
    "product_manager": "제품 관리, PRD, 로드맵 (Alex Chen)",
    "product_owner": "애자일, 사용자 스토리, 스프린트 (Sarah Kim)",
    "ux_designer": "UX 디자인, 접근성, 디자인 시스템 (Emma Rodriguez)",
    "data_engineer": "데이터 파이프라인, dbt, Airflow (Michelle Liu)",
    "infrastructure_lead": "클라우드 인프라, Terraform, AWS (Mark Stevens)",
    "database_engineer": "데이터베이스 설계, PostgreSQL, 성능 최적화 (Jennifer Wu)",
    "sre_lead": "SRE, SLO/SLI, 모니터링, 인시던트 대응 (Thomas Wright)",
    "technical_writer": "기술 문서화, API 문서, README (Emily Brown)",
    "scrum_master": "스크럼, 회고, 팀 퍼실리테이션 (Ryan O'Brien)",
    "team_collaboration": "팀 협업 시나리오, 워크플로우",
    "quality_standards": "품질 표준, 코드 리뷰 체크리스트",
    "advanced_topics": "고급 주제: Rust/Go, K8s Operator, eBPF",
    "hyperscale_systems": "대규모 시스템: Spanner, Bigtable, TAO",
    "postmortems": "포스트모템, 장애 사례 연구",
}


@server.list_tools()
async def list_tools():
    """사용 가능한 도구 목록 반환"""
    return [
        Tool(
            name="search_knowledge",
            description="""DreamTeam 개발팀의 전문 지식을 검색합니다.

17명의 전문가 페르소나 지식 + 고급 주제 포함:
- Solution Architect, Backend/Frontend Lead
- AI/ML, DevOps, Security, QA, Mobile Lead
- PM, PO, UX Designer, Data/DB Engineer
- Infrastructure, SRE, Tech Writer, Scrum Master
- Hyperscale Systems, Post-Mortems 등

사용 예시:
- "FastAPI에서 JWT 인증 구현 방법"
- "Kubernetes 배포 전략"
- "React 성능 최적화"
- "PostgreSQL 인덱스 설계"
- "인시던트 대응 프로세스"
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색할 질문 또는 주제"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "반환할 결과 수 (기본: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_by_role",
            description="""특정 역할의 전문가 지식만 검색합니다.

사용 가능한 역할:
- solution_architect: 시스템 아키텍처, 설계 패턴
- backend_lead: 백엔드, API, Python/FastAPI
- frontend_lead: React, Next.js, 상태관리
- ai_ml_lead: AI/ML, RAG, LangChain
- devops_lead: CI/CD, Kubernetes
- security_lead: 보안, 인증, OWASP
- qa_lead: 테스트, QA
- mobile_lead: React Native, Flutter
- product_manager: PM, PRD
- product_owner: 애자일, 스토리
- ux_designer: UX, 접근성
- data_engineer: 데이터 파이프라인
- infrastructure_lead: 클라우드, Terraform
- database_engineer: DB 설계, 최적화
- sre_lead: SRE, 모니터링
- technical_writer: 문서화
- scrum_master: 스크럼, 회고
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색할 질문"
                    },
                    "role": {
                        "type": "string",
                        "description": "역할 ID (예: backend_lead, security_lead)",
                        "enum": list(ROLE_DESCRIPTIONS.keys())
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "반환할 결과 수 (기본: 5)",
                        "default": 5
                    }
                },
                "required": ["query", "role"]
            }
        ),
        Tool(
            name="list_roles",
            description="사용 가능한 모든 전문가 역할 목록을 표시합니다.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_stats",
            description="벡터 스토어의 통계 정보를 반환합니다.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """도구 실행"""

    if name == "search_knowledge":
        query = arguments.get("query", "")
        n_results = arguments.get("n_results", 5)

        results = get_vector_store().search(query, n_results=n_results)

        if not results:
            return [TextContent(
                type="text",
                text=f"'{query}'에 대한 결과를 찾을 수 없습니다."
            )]

        output = f"## 🔍 '{query}' 검색 결과\n\n"
        for i, r in enumerate(results, 1):
            role_name = r["metadata"].get("role_name", "Unknown")
            output += f"### [{i}] {role_name}\n"
            output += f"**관련도**: {1 - r['distance']:.2%}\n\n"
            output += f"{r['content']}\n\n"
            output += "---\n\n"

        return [TextContent(type="text", text=output)]

    elif name == "search_by_role":
        query = arguments.get("query", "")
        role = arguments.get("role", "")
        n_results = arguments.get("n_results", 5)

        if role not in ROLE_DESCRIPTIONS:
            return [TextContent(
                type="text",
                text=f"알 수 없는 역할: {role}\n\n사용 가능한 역할:\n" +
                     "\n".join(f"- {k}: {v}" for k, v in ROLE_DESCRIPTIONS.items())
            )]

        results = get_vector_store().search_by_role(query, role, n_results=n_results)

        if not results:
            return [TextContent(
                type="text",
                text=f"'{role}'의 '{query}'에 대한 결과를 찾을 수 없습니다."
            )]

        role_desc = ROLE_DESCRIPTIONS.get(role, role)
        output = f"## 🎯 [{role_desc}] '{query}' 검색 결과\n\n"
        for i, r in enumerate(results, 1):
            output += f"### [{i}] 관련도: {1 - r['distance']:.2%}\n\n"
            output += f"{r['content']}\n\n"
            output += "---\n\n"

        return [TextContent(type="text", text=output)]

    elif name == "list_roles":
        output = "## 👥 DreamTeam 전문가 역할\n\n"
        output += "| 역할 ID | 설명 |\n|---------|------|\n"
        for role_id, desc in ROLE_DESCRIPTIONS.items():
            output += f"| `{role_id}` | {desc} |\n"

        stored_roles = get_vector_store().get_all_roles()
        output += f"\n\n**저장된 역할 수**: {len(stored_roles)}"

        return [TextContent(type="text", text=output)]

    elif name == "get_stats":
        doc_count = get_vector_store().get_document_count()
        roles = get_vector_store().get_all_roles()

        output = "## 📊 DreamTeam 지식 베이스 통계\n\n"
        output += f"- **총 문서 청크 수**: {doc_count}\n"
        output += f"- **등록된 역할 수**: {len(roles)}\n"
        output += f"- **역할 목록**: {', '.join(roles)}\n"

        return [TextContent(type="text", text=output)]

    else:
        return [TextContent(
            type="text",
            text=f"알 수 없는 도구: {name}"
        )]


async def main():
    """MCP 서버 실행"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
