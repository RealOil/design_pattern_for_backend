# 1주차
## 기술 목표
- Service 코드에서 DB / 외부 API / 트랜잭션 코드 제거
- 생성자 기반 DI 구조 이해
- Repository와 Service의 역할 경계 명확화

## 사고 목표
- "이 클래스는 왜 이것을 알고 있는가?"를 설명할 수 있다.
- 패턴을 *도입해야 하는 순간*을 감지할 수 있다.

## 실습
### 1. 일부러 나쁜 코드 만들기

**목적**: 왜 이 구조가 위험한지 느끼기

- Service 클래스에서 다음을 직접 처리한다
    - DB 세션 생성
    - SQL 실행
    - 트랜잭션 commit / rollback
- 의도적으로 아래 특징을 가진 코드를 작성한다.
    - Service 안에 SQL 또는 ORM 코드 존재
    - 테스트시 DB 없이는 실행 불가

- **질문**
    - 이 Service는 몇 가지 이유로 변경될 수 있는가?
    - DB 구현이 바뀌면, 이 파일은 얼마나 수정해야 하는가?
    - 테스트를 작성하려면 무엇을 가짜로 만들어야 하는가?

| 이 질문에 답하는 것이 **DI / Repository**의 출발점

### 2. DI(Dependency Injection) 도입

- DI의 핵심: "이 클래스는 무엇을 '사용'하지만, 무엇을 '생성'하지는 않는다."

- Service에서 DB 객체 생성 코드 제거
- 생성자를 통해 의존성 주입
- 예시 개념
    - X `service` 내부에서 `Repository` 생성
    - O 외부에서 `Repository`를 만들어 `Service`에 주입
- 체크 포인트
    - Service 코드에 `new`, `Session()`, `connect()` 같은 코드가 남아있는가?
    - Service는 이제 인터페이스에만 의존하는가?
- AI와 일할 때
    - "이 Service는 구현체를 직접 생성하고 있어 테스트와 교체가 어렵습니다. Repository 인터페이스를 만들고 DI 구조로 바꾸세요."

### 3. Repository 도입

- Repository의 역할
    - 도메인이 DB를 모르게 한다
    - SQL/ORM을 한 곳에 가둔다
- Repository 인터페이스 정의
- DB 접근 코드를 Repository로 이동
- 가장 중요한 경계 질문
    - Repository가 비즈니스 판단(if/else)을 하고 있는가?
    - 아니면 데이터 접근만 담당하고 있는가?
    - Repository가 두꺼워지면 -> 그건 Service 책임을 침범한 것

### 4. Unit of Work는 정말 필요한가?

- Unit of Work의 존재 이유
    - 여러 Repository를 사용하는 하나의 비즈니스 흐름을 **하나의 트랜잭션으로 묶기 위함**
- 사고 실험
    - Service에서 Repository A, B를 동시에 사용한다면?
    - A 성공, B 실패 시 데이터는 어떻게 되는가?
- 판단 기준 정리
    - 다음 중 2개 이상이면 UoW 고려
        - 하나의 유스케이스에서 Repository가 2개 이상 사용됨
        - 트랜잭션 경계가 Service마다 다름
        - 실패 시 롤백 규칙이 복잡함

## 정리
### 반드시 문장으로 정리해보기

1. DI가 없을 때 생기는 실제 문제 2가지
2. Repository가 해결해주는 문제 2가지
3. "이 프로젝트에서는 UoW가 필요/불필요하다"는 결론과 이유

### 30분 강의 자료 관점

| "디자인 패턴은 구조를 예쁘게 만들기 위한 것이 아니라 변경 비용을 줄이기 위한 도구다"

-  DI -> 테스트와 교체 비용 감소
- Repository -> 도메인 보호
- UoW -> 실패 시 일관성  유지