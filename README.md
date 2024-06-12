# Document service

---
## Instalation
1. Clone the repository:

```
$ git clone https://github.com/IlyaTorch/demo-test-task.git
$ cd demo-test-task
```
2. Fill in .env file or use .env_example:
```
$ mv .env_example .env
```

3. Build docker containers:
```
$ docker-compose up -d
```
3. Run migrations:
```
$ docker exec -it documents-app bash
$ python src/manage.py makemigrations app
$ python src/manage.py migrate
```
4. Application started. Navigate to http://127.0.0.1:8000 (documents API is here)

Follow instructions below to run only the application:

1. Repeat steps 1,2 above
2. Create a virtual environment:

```
$ pip install -U pipenv
$ pipenv shell
```

3. Install the dependencies:

```
$ pipenv install --system
```

4. Run server and navigate to http://127.0.0.1:8000 

```
python src/manage.py runserver
```
5. Run migrations:
```
$ python src/manage.py makemigrations app
$ python src/manage.py migrate
```
---
## Endpoints

1. `POST` /api/v1/users/register/ : Sign-up
```
curl --location 'http://127.0.0.1:8000/api/v1/users/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "new_user",
    "password": "some_password",
    "email": "some@mail.ru"

}'
```
2. `POST` /api/v1/users/token/ : Get token 
```
curl --location 'http://127.0.0.1:8000/api/v1/users/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "new_user",
    "password": "some_password"
}'
```
3. `POST` /api/v1/document/ : Create new document **(Auth is required)**
```
curl --location 'http://127.0.0.1:8000/api/v1/document/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "title": "Title",
    "content": "Text Example"
}'
```
4. `GET` /api/v1/document/<id> : Get document detail **(Auth is required)**
```
curl --location 'http://127.0.0.1:8000/api/v1/document/1' \
--header 'Authorization: Bearer <TOKEN>'
```
5. `GET` /api/v1/document/list : Get documents list, filters optional **(Auth is required)**
```
curl --location 'http://127.0.0.1:8000/api/v1/document/list?status=draft' \
--header 'Authorization: Bearer <TOKEN>'
```
6. `DELETE` /api/v1/document/<id>/archive/ : Archive(delete) document **(Auth is required)**
```
curl --location --request DELETE 'http://127.0.0.1:8000/api/v1/document/1/archive/' \
--header 'Authorization: Bearer <TOKEN>'
```
7. `PATCH`|`PUT` /api/v1/document/<id> : Update document **(Auth is required)**
```
curl --location --request PATCH 'http://127.0.0.1:8000/api/v1/document/1/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <TOKEN>' \
--data '{
    "title": "New Title"
}'
```