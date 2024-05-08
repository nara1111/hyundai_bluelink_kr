## 소개 ##

[Hyundai-Kia-Connect/kia_uvo](https://github.com/Hyundai-Kia-Connect/kia_uvo) 프로젝트를 기반으로 한국의 현대 블루링크 API에 맞추어 변경하는 프로젝트. 코드 변경의 상당부분은 [Claude.ai](https://claude.ai)의 도움을 받았다.

AI의 도움을 받았다는 언급에서 눈치 챘겠지만, 전업개발자의 작품이 아닌데다가 한국의 경우, 현대차그룹 차원에서 CCS(Connected Car Service) 관련한 명확한 과금전략을 가지고 있어 외국과 달리 커뮤니티를 기반으로 한 프로젝트가 성공하기 어려운 환경이다. 따라서 본 프로젝트의 사용범위는 어디까지나 개인이 보유한 현대자동차의 상태 확인 등에 한정하며, API를 호출하기 위한 코드 외 API 그 자체와 호출을 통해 수집한 정보 등은 모두 현대차그룹의 것 또는 현대차그룹과 CCS 가입자 간 개인정보 약정에 의한 것이므로 제3자 등이 이 관계에 개입하였을때 발생할 수 있는 법적 제도적 문제에 대해서는 본 개발자는 책임질 수 없음을 분명히 밝혀두고자 한다.

## 로그 확인 ##

```

logger:

  default: warning

  logs:

    custom_components.hyundai_bluelink_kr: debug

```

