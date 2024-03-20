# Notes RESTful API
RESTful API for working with notes
## How to run
- Clone this repository
- Create file `.env-non-dev` with contents:
    ```
    DBMS_NAME=postgresql
    DB_USER=<Replace with your DB username>
    DB_PASSWORD=<Replace with your DB password>
    DB_HOST=0.0.0.0
    DB_PORT=5432
    DB_NAME=<Replace with your DB name>

    POSTGRES_USER=<Replace with your DB username>
    POSTGRES_PASSWORD=<Replace with your DB password>
    POSTGRES_DB=<Replace with your DB name>
    ```
- Run `docker-compose up`
