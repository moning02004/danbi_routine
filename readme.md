## 1. 설계

Routine 은 개인적인 목표를 다루는 것이기에 Routine 에 관한 API 호출은 모두 인가된 사용자에게만 접근할 수 있게 하였습니다.



###routine 조회

- 목록: GET /routines
- 단건: GET /routines/{routine_id}



###routine 생성

- POST /routines



###routine 수정

*routine_id 가 Optional 로 지정되어 있었지만 의도와는 다르게 다른 routine 이 수정될 수 있어 URL 에 포함시켰습니다.*

- PATCH /routines/{routine_id}



###routine 삭제

- DELETE /routines/{routine_id}



###routine 완료

*Routine 의 완료를 위한 API 를 추가했습니다.*

- PATCH /routines/{routine_id}/complete