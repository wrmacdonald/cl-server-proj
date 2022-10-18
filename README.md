# cl-server-proj

## Running project locally with Docker:

#### 1st: start postgres DB containers:

`docker compose up -d db1`

`docker compose up -d db_test`


#### 2nd: start Flask server:

(will also create necessary tables in database)

`docker compose up --build flask-app`


#### to access DB:

`docker exec -it db1 psql -U postgres`


#### to run unit tests:

Go into the Flask server Docker container CLI & run:

`python -m unittest discover -p unit_tests.py`

