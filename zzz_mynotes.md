# pg_wal2socket

## ENV init
$ alias python=/usr/local/bin/python3

$ source /usr/local/bin/virtualenvwrapper.sh

$ mkvirtualenv pg_wal2socket

$ pip install -r requirements.txt --target .

## PG Preparation

Starts a PG container and changes replication to `logical`.
Still need wal2json installed
```
docker run --name temporary_pg \
   --rm -d \
   -e POSTGRES_HOST_AUTH_METHOD=trust \
   -p5432:5432 postgres:14 ;  \
 sleep 4 ; \
 psql -h 127.0.0.1 -Upostgres postgres -c "alter SYSTEM SET wal_level = logical;" ; \
 sleep 2; docker restart temporary_pg; sleep 2; \
 psql -h 127.0.0.1 -Upostgres postgres -c "show wal_level;"
```


$ cd ~/Documents/NO_BACKUP/myGithubRepos/funwith__pg_recvlogical
$ dck up -d

$ psql -h 127.0.0.1 -Umyuser postgres -p5445
=# select pg_drop_replication_slot('pg_wal2socket');
=# select pg_create_logical_replication_slot('pg_wal2socket', 'wal2json');

$ pgbench -i  -h 127.0.0.1 -Umyuser postgres -p5445


$ cd ~/Documents/NO_BACKUP/myGithubRepos/pg_wal2socket
$ python3 TEST-MEEE.py localhost 8080
$ python3 echo-client.py

## Thanks to
Nathan Jennings for [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)
