## Set up webapp:
```sh
$ pip install -r requirements.txt
```
## Set up postgresql:
```sh
$ docker run -e POSTGRES_DB=practica -p 5732:5432 -v $PWD/data:/var/lib/postgresql/data -d postgres
```
##### Create db user:
```sh
$ docker exec -it <docker_id> psql -U postgres
```
In psql run this comands:
```psql
create user "user";
```
```psql
alter user "user" with encrypted password '1234';
```
```psql
grant all privileges on database practica to "user";
```

## Run db:
```sh
$ docker run -e POSTGRES_DB=practica -p 5732:5432 -v $PWD/data:/var/lib/postgresql/data -d postgres
```
## Run webapp:
```sh
$ python manage.py runserver
```
