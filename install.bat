@echo off
REM DreamTeam For Development - Windows Installation Script
REM Copyright (c) 2024 Sean Shin (@seanshin0214)

echo ==========================================
echo   DreamTeam For Development Installer
echo   by Sean Shin (@seanshin0214)
echo ==========================================
echo.

REM 현재 디렉토리 저장
set SCRIPT_DIR=%~dp0

REM Python 확인
echo [1/5] Python 버전 확인...
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python이 설치되어 있지 않습니다.
    echo Python 3.10 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo [OK] Python 발견
echo.

REM 가상환경 생성
echo [2/5] 가상환경 설정...
if not exist "venv" (
    set /p CREATE_VENV="가상환경을 생성하시겠습니까? (y/n): "
    if /i "%CREATE_VENV%"=="y" (
        python -m venv venv
        echo [OK] 가상환경 생성됨
        call venv\Scripts\activate.bat
        echo [OK] 가상환경 활성화됨
    )
) else (
    call venv\Scripts\activate.bat 2>nul
    echo [OK] 기존 가상환경 사용
)
echo.

REM 의존성 설치
echo [3/5] 의존성 설치...
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo [OK] 의존성 설치 완료
echo.

REM 샘플 데이터 로드
echo [4/5] 샘플 지식 베이스 구축...
if exist "examples\personas" (
    python src\data_loader.py "examples\personas"
    echo [OK] 샘플 데이터 로드 완료
) else (
    echo [WARN] examples\personas 폴더가 없습니다.
)
echo.

REM MCP 설정 안내
echo [5/5] MCP 설정 안내
echo.
echo 다음 설정을 MCP 설정 파일에 추가하세요:
echo.
echo Claude Code (%%USERPROFILE%%\.claude\mcp.json):
echo {
echo   "mcpServers": {
echo     "dreamteam-for-development": {
echo       "command": "python",
echo       "args": ["%SCRIPT_DIR%src\server.py"],
echo       "env": {
echo         "PYTHONIOENCODING": "utf-8",
echo         "PYTHONUTF8": "1"
echo       }
echo     }
echo   }
echo }
echo.
echo Claude Desktop (%%APPDATA%%\Claude\claude_desktop_config.json):
echo 위와 동일한 설정 사용
echo.
echo ==========================================
echo [OK] 설치 완료!
echo.
echo 슬래시 커맨드 설치 (선택사항):
echo   copy claude-code\dreamteam.md %%USERPROFILE%%\.claude\commands\
echo.
echo DreamTeam For Development by Sean Shin
echo https://github.com/seanshin0214/dreamteam-for-development
echo ==========================================
pause
