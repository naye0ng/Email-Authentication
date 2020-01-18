# Email Authentication + JWT

- [x] Gmail SMTP, Django를 이용한 이메일 인증 구현
- [x] JWT(Json Web Token)을 이용한 로그인 구현
- [x] Django restframework, framework-jwt 등을 사용하지 않고, 인증 과정을 이해한 뒤 직접 구현
- [x] redis를 사용하여 유효 시간동안 token을 저장



<br/>

## Authentication App

### I. 회원 가입

#### Request

```
[POST] /auth/authentiaction/
```
```json
[header]
{ "Content-Type": "application/json" }
```
```json
[body]
{
    "email": "{email}",
    "password1": "{password}",
    "password2": "{password}",
}
```


#### Response

```json
{ "message": "{email}로 인증 코드를 발송했습니다." }
```

<br/>

### II. 이메일 인증

- 유효한 링크로 요청이 들어오면, 사용자 속성의  `is_activate = True` 로 변경하여 계정을 활성화 시킵니다.
- 해당 링크는 자동으로 리다이렉트됩니다.

#### Request

```
[GET] /auth/authentiaction/?token={token}&uid64={user}
```

#### Response

- 해당 링크의 유효시간은 1분으로 `Redis`에서 자동으로 삭제 됩니다.

```json
{ "message": "유효하지 않은 인증입니다. 다시 진행하세요"}
```

<br/>

## Tokens App

### I. 로그인

#### Request

```
[POST] /token/
```

```json
[header]
{ "Content-Type": "application/json" }
```
```json
[body]
{
    "email": "{email}",
    "password": "{password}",
}
```

#### Response

- 유저정보가 일치한다면, `access_token`과 `refresh token`을 반환합니다.

```json
{
    "access_token": "{access_token}",
    "refresh_token": "{refresh_token}"
}
```

<br/>
### II. 토큰 유효성 검사

#### Request

```
[POST] /token/validate/
```

```json
[header]
{
  "Content-Type": "application/json",
  "Authorization": "{access_token}"
}
```

#### Response

```json
{ "message": "유효한 사용자입니다." }
```

<br />

### III. 토큰 갱신

#### Request

```
[POST] /token/refresh/
```

```json
[header]
{
  "Content-Type": "application/json",
  "Authorization": "{refresh_token}"
}
```

#### Response

```json
{
    "access_token": "{access_token}"
}
```

<br/>



## setup

> - `Python 3.6.7` 버전의 virtualenv 환경에서 작업을 진행합니다.
> - `mysql 8.0.18`과 `redis`를 사용합니다.



#### Install Package

```
pip install -r requirements.txt 
```

#### Database and Email Settings

```
cd Requirements
```
```
mv _db.json db.json & vi db.json
```
```
mv _email.json email.json & vi db.json
```

#### Start App

```
python manage.py runserver
```





