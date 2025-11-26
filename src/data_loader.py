"""DreamTeam 페르소나 파일을 벡터 스토어에 로드하는 스크립트"""
import os
import re
from pathlib import Path
from typing import List, Tuple
from vector_store import DreamTeamVectorStore


# 파일명에서 역할 추출을 위한 매핑
ROLE_MAPPING = {
    "01_Solution_Architect": ("solution_architect", "Solution Architect - Dr. Michael Torres"),
    "02_Backend_Lead": ("backend_lead", "Backend Lead - James Park"),
    "03_Frontend_Lead": ("frontend_lead", "Frontend Lead - David Kim"),
    "04_AI_ML_Lead": ("ai_ml_lead", "AI/ML Lead - Dr. Lisa Wang"),
    "05_DevOps_Lead": ("devops_lead", "DevOps Lead - Kevin Zhang"),
    "06_Security_Lead": ("security_lead", "Security Lead - Robert Chen"),
    "07_QA_Lead": ("qa_lead", "QA Lead - Susan Martinez"),
    "08_Mobile_Lead": ("mobile_lead", "Mobile Lead - Chris Anderson"),
    "09_Product_Manager": ("product_manager", "Product Manager - Alex Chen"),
    "10_Product_Owner": ("product_owner", "Product Owner - Sarah Kim"),
    "11_UX_Designer": ("ux_designer", "UX Designer - Emma Rodriguez"),
    "12_Data_Engineer": ("data_engineer", "Data Engineer - Michelle Liu"),
    "13_Infrastructure_Lead": ("infrastructure_lead", "Infrastructure Lead - Mark Stevens"),
    "14_Database_Engineer": ("database_engineer", "Database Engineer - Jennifer Wu"),
    "15_SRE_Lead": ("sre_lead", "SRE Lead - Thomas Wright"),
    "16_Technical_Writer": ("technical_writer", "Technical Writer - Emily Brown"),
    "17_Scrum_Master": ("scrum_master", "Scrum Master - Ryan O'Brien"),
    "18_Team_Collaboration": ("team_collaboration", "Team Collaboration Scenarios"),
    "19_Quality_Standards": ("quality_standards", "Quality Standards Summary"),
    "20_Advanced_Topics": ("advanced_topics", "Advanced Topics"),
    "21_Hyperscale_Systems": ("hyperscale_systems", "Hyperscale Systems"),
    "22_PostMortems": ("postmortems", "Post-Mortems & War Stories"),
    "00_README": ("overview", "Team Overview"),
}


def get_role_info(filename: str) -> Tuple[str, str]:
    """파일명에서 역할 정보 추출"""
    for prefix, (role_id, role_name) in ROLE_MAPPING.items():
        if filename.startswith(prefix):
            return role_id, role_name
    return "general", "General Knowledge"


def chunk_document(content: str, chunk_size: int = 1500, overlap: int = 200) -> List[str]:
    """문서를 청크로 분할

    마크다운 헤더(#, ##, ###)를 기준으로 의미 있게 분할
    """
    chunks = []

    # 섹션별로 분할 (## 또는 ### 헤더 기준)
    sections = re.split(r'\n(?=#{2,3}\s)', content)

    current_chunk = ""
    for section in sections:
        section = section.strip()
        if not section:
            continue

        # 섹션이 chunk_size보다 작으면 현재 청크에 추가
        if len(current_chunk) + len(section) < chunk_size:
            current_chunk += "\n\n" + section if current_chunk else section
        else:
            # 현재 청크 저장
            if current_chunk:
                chunks.append(current_chunk.strip())

            # 섹션 자체가 너무 크면 더 작게 분할
            if len(section) > chunk_size:
                # 코드 블록 기준으로 분할 시도
                parts = re.split(r'\n(?=```)', section)
                for part in parts:
                    if len(part) > chunk_size:
                        # 그래도 크면 강제 분할
                        for i in range(0, len(part), chunk_size - overlap):
                            chunks.append(part[i:i + chunk_size].strip())
                    else:
                        chunks.append(part.strip())
                current_chunk = ""
            else:
                current_chunk = section

    # 마지막 청크 저장
    if current_chunk:
        chunks.append(current_chunk.strip())

    return [c for c in chunks if len(c) > 50]  # 너무 짧은 청크 제외


def load_persona_files(source_dir: str, vector_store: DreamTeamVectorStore) -> int:
    """페르소나 파일들을 벡터 스토어에 로드

    Args:
        source_dir: 페르소나 마크다운 파일이 있는 디렉토리
        vector_store: DreamTeamVectorStore 인스턴스
    Returns:
        로드된 청크 수
    """
    source_path = Path(source_dir)
    if not source_path.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    all_documents = []
    total_chunks = 0

    # 모든 마크다운 파일 처리
    md_files = sorted(source_path.glob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    for md_file in md_files:
        filename = md_file.stem
        role_id, role_name = get_role_info(filename)

        print(f"Processing: {filename} -> {role_name}")

        # 파일 읽기
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 청크로 분할
        chunks = chunk_document(content)
        print(f"  - Created {len(chunks)} chunks")

        # 문서 객체 생성
        for i, chunk in enumerate(chunks):
            doc = {
                "id": f"{role_id}_{i:04d}",
                "content": chunk,
                "metadata": {
                    "role": role_id,
                    "role_name": role_name,
                    "source_file": filename,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            }
            all_documents.append(doc)

        total_chunks += len(chunks)

    # 벡터 스토어에 추가
    if all_documents:
        vector_store.add_documents(all_documents)
        print(f"\nTotal: Loaded {total_chunks} chunks from {len(md_files)} files")

    return total_chunks


if __name__ == "__main__":
    import sys

    # 소스 디렉토리 (페르소나 파일 위치)
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    else:
        source_dir = r"C:\Users\sshin\OneDrive - Global Education Research Institutute\바탕 화면\개발자팀 페르소나팀"

    # 벡터 스토어 초기화
    script_dir = Path(__file__).parent.parent
    db_path = script_dir / "data" / "chroma_db"
    vector_store = DreamTeamVectorStore(str(db_path))

    # 기존 데이터 클리어 (옵션)
    print("Clearing existing data...")
    vector_store.clear()

    # 파일 로드
    print(f"\nLoading files from: {source_dir}")
    chunk_count = load_persona_files(source_dir, vector_store)

    print(f"\n=== Load Complete ===")
    print(f"Total documents in store: {vector_store.get_document_count()}")
    print(f"Available roles: {vector_store.get_all_roles()}")
