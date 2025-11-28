#!/bin/bash
# DreamTeam For Development - Installation Script
# Copyright (c) 2024 Sean Shin (@seanshin0214)

set -e

echo "=========================================="
echo "  DreamTeam For Development Installer"
echo "  by Sean Shin (@seanshin0214)"
echo "=========================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 현재 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python 버전 확인
echo -e "${YELLOW}[1/5] Python 버전 확인...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python이 설치되어 있지 않습니다.${NC}"
    echo "Python 3.10 이상을 설치해주세요: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✓ Python $PYTHON_VERSION 발견${NC}"

# 가상환경 생성 (선택사항)
echo ""
echo -e "${YELLOW}[2/5] 가상환경 설정...${NC}"
if [ ! -d "venv" ]; then
    read -p "가상환경을 생성하시겠습니까? (y/n): " CREATE_VENV
    if [ "$CREATE_VENV" = "y" ] || [ "$CREATE_VENV" = "Y" ]; then
        $PYTHON_CMD -m venv venv
        echo -e "${GREEN}✓ 가상환경 생성됨${NC}"
        source venv/bin/activate
        echo -e "${GREEN}✓ 가상환경 활성화됨${NC}"
    fi
else
    source venv/bin/activate 2>/dev/null || true
    echo -e "${GREEN}✓ 기존 가상환경 사용${NC}"
fi

# 의존성 설치
echo ""
echo -e "${YELLOW}[3/5] 의존성 설치...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ 의존성 설치 완료${NC}"

# 샘플 데이터 로드
echo ""
echo -e "${YELLOW}[4/5] 샘플 지식 베이스 구축...${NC}"
if [ -d "examples/personas" ]; then
    $PYTHON_CMD src/data_loader.py "examples/personas"
    echo -e "${GREEN}✓ 샘플 데이터 로드 완료${NC}"
else
    echo -e "${YELLOW}⚠ examples/personas 폴더가 없습니다. 나중에 수동으로 로드하세요.${NC}"
fi

# MCP 설정 안내
echo ""
echo -e "${YELLOW}[5/5] MCP 설정 안내${NC}"
echo ""
echo "다음 설정을 MCP 설정 파일에 추가하세요:"
echo ""
echo -e "${GREEN}Claude Code (~/.claude/mcp.json):${NC}"
cat << EOF
{
  "mcpServers": {
    "dreamteam-for-development": {
      "command": "$PYTHON_CMD",
      "args": ["$SCRIPT_DIR/src/server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
EOF

echo ""
echo -e "${GREEN}Claude Desktop (%APPDATA%/Claude/claude_desktop_config.json):${NC}"
echo "위와 동일한 설정 사용"

echo ""
echo "=========================================="
echo -e "${GREEN}✓ 설치 완료!${NC}"
echo ""
echo "슬래시 커맨드 설치 (선택사항):"
echo "  cp claude-code/dreamteam.md ~/.claude/commands/"
echo ""
echo "DreamTeam For Development by Sean Shin"
echo "https://github.com/seanshin0214/dreamteam-for-development"
echo "=========================================="
