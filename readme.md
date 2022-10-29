# 1. 사용자에 대한 API

|API URL|Method|기능|설명|
|---|---|---|---|
|/users|POST|회원가입|비밀번로 8자리 이상이며 영문, 숫자, 특수기호를 모두 포함해야 합니다.|
|/users/token|POST|JWT 토큰 발급|인증을 위한 access token, refresh token을 발급합니다.|
|/users/refresh|POST|JWT 토큰 refresh|access token 을 새로 발급합니다.|
|/users/expire|POST|JWT refresh 토큰 발급|refresh 토큰을 만료시켜 access token 을 재발급받지 못하도록 합니다.|

## 1-1. 로그아웃
로그아웃에 대한 기능은 세션을 통한 인증일 때, 필요한 기능으로 보여집니다. 
하지만 JWT 로 구현했기 때문에 토큰을 재발급 받을 수 없도록 하는 것이 로그아웃과 비슷한 기능이라고 생각했습니다.


# 2. Routine에 대한 API

|API URL|Method|기능|설명|
|---|---|---|---|
|/routines|GET|사용자의 routine 리스트 조회|date get parameter 를 주어 특정 날짜에 대한 routine 리스트를 가져옵니다.|
|/routines|POST|routine 생성|routine 을 생성합니다.|
|/routines/{routine_id}|GET|routine 단건 조회|routine_id 의 routine 을 가져옵니다. |
|/routines/{routine_id}|PATCH|routine 수정|routine_id 의 routine 을 수정합니다.|
|/routines/{routine_id}/delete|PATCH|routine 제거|routine_id 의 routine 컬럼 중 is_deleted 를 True 로 저장합니다.|
|/routines/{routine_id}/result|PATCH|routine 결과 수정|routine 의 결과를 수정합니다.|

## 2-1. 구현 설명
인증을 통해 어떤 사용자의 routine 을 반환해야하는 지 구현하였고, routine_id를 URL 에 명시하여 어떤 routine 을 조회하려고 하는 지 구현했습니다.
