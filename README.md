# InTime Shop API Task

## Documentation
- API Documentation file: [docs](docs/api/api.json)
- Swagger interface: [http://localhost:8000/api/doc/](http://localhost:8000/api/doc/)
- Database schema: [dbdiagram.io](https://dbdiagram.io/d/5ff424bb80d742080a351386)
## Docker
- Build
```bash
docker compose up -d --build
# or in older version: docker-compose up -d
```
- Load fixtures
```bash
docker exec -it shop_django python manage.py loaddata docs/fixtures/initial_data.json
```
## Manually
- First, install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
- Then, create database (PostgreSQL):
    ```sql
    CREATE USER <user> WITH PASSWORD <password>;
    CREATE DATABASE <db>;
    ALTER ROLE <user> SET client_encoding TO 'utf8';
    ALTER ROLE <user> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <user> SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE <db> TO <user>;
    ```
- Then, generate JWT keys:
  ```bash
    ssh-keygen -t rsa -b 4096 -m PEM -f jwt-key
    openssl rsa -in jwt-key -pubout -outform PEM -out jwt-key.pub
  ```
- Then, configure settings from `settings-template.ini`:
  ```bash
    cp settings-template.ini settings.ini
  ```
  #### NOTE: Here you should fill `settings.ini` with your own settings
- #### NOTE: If you have `elasticsearch` installed, you should configure it in settings.ini (it's not required for searching you can also use PostgreSQL trigram search)
- Then, migrate database:
  ```bash
  python manage.py migrate
  ```
- Run tests to make sure everything is working:
  ```bash
  python manage.py test
  ```
- Now you can run server:
    ```bash
      python manage.py runserver
    ```
- OPTIONAL: you can load prepared data:
  ```bash
  python manage.py loaddata docs/fixtures/initial_data.json
  # default user
  # username: admin
  # password: secure
  ```