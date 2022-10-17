# cl-server-proj


#### start DB with Docker:

`docker compose up -d db1`

#### access DB:
`docker exec -it db1 psql -U postgres`

#### start Flask server with Docker:
`docker compose up --build flask-app`


