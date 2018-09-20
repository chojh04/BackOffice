## Project ##

- admin 관리자 페이지 개발

## 환경구성 

- python 2.7
- flask
- gentelella template
- bootstrap 3
- jquery
- redis


## Member & Role (bitbucket ID)

- developer
        - 황상현 (sanghyun5468@gmail.com)


## Install / Development

git clone -b back_office https://sanghyunhwang@bitbucket.org/openny/kpcadmin.git
cd kpcadmin/KpcAdmin

# Install dependencies
pip install requirements

# set redis (default)

window redis download
https://github.com/MSOpenTech/redis/releases

linux redis download
https://redis.io/download


## 확인중인 사항 ##
    - 없음

## commit history ##

### 2017-02-14
    - 최초 commit
    -


### 2017-02-17
    - dist, js 폴더 삭제
    - datatable column order 제거
    - 파일 업로드시 back_office server forword
    - nav.py nav.html file fullname 으로 변경