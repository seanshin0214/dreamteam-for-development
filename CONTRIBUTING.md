# Contributing to DreamTeam For Development

먼저, DreamTeam 프로젝트에 관심을 가져주셔서 감사합니다! 🎉

이 프로젝트는 Sean Shin (@seanshin0214)이 만들고 관리합니다.

## 기여 방법

### 1. 이슈 리포트

버그를 발견하거나 새로운 기능을 제안하고 싶다면:

1. [GitHub Issues](https://github.com/seanshin0214/dreamteam-for-development/issues)에서 기존 이슈 확인
2. 새 이슈 생성 시 다음 정보 포함:
   - 문제 설명 또는 기능 제안
   - 재현 단계 (버그의 경우)
   - 예상 동작 vs 실제 동작
   - 환경 정보 (Python 버전, OS 등)

### 2. Pull Request

코드 기여를 원하시면:

1. 저장소 Fork
2. 새 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

### 3. 페르소나 지식 기여

새로운 전문가 페르소나나 지식을 추가하려면:

1. `examples/personas/` 폴더에 마크다운 파일 작성
2. 다음 형식 준수:

```markdown
# Role Name - Expert Name

> Brief description

## Core Expertise

### Topic 1

```code
example code
```

### Topic 2

...

## Decision Framework

...

## Checklist

- [ ] Item 1
- [ ] Item 2
```

## 코드 스타일

- Python 3.10+ 문법 사용
- Type hints 필수
- Docstring 작성 (Google 스타일)
- Black 포맷터 사용 (`black .`)
- isort로 import 정렬 (`isort .`)

## 테스트

```bash
pip install -e ".[dev]"
pytest
```

## 라이선스

기여하신 코드는 MIT 라이선스로 배포됩니다.
저작권은 원 저자 Sean Shin에게 있으며, 기여자는 Contributors로 인정됩니다.

## 행동 강령

- 서로 존중하고 건설적인 피드백 제공
- 포용적인 언어 사용
- 다양한 관점 존중

## 연락처

- GitHub: [@seanshin0214](https://github.com/seanshin0214)
- 이메일: sshin@geri.kr

감사합니다! 🙏
