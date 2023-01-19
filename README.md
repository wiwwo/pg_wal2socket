# pg_wal2socket

---
Send Postgresql WAL content to socket.
<br>AKA
<br>Stream Postgresql database changes to TCP socket.

I've seen other solutions around, but they relied on LISTEN/NOTIFY, which has some limitations.
<br>This solution uses native Logical replication and wal2json plugin to stream database changes via sockets.
<br>
<br>Far from being "production ready", but not *that* far.
It just works.
<br><br>
IMPORTANT: use of this code in business context is strictly forbidden unless with explicit consent.


---
### Small HOWTO

Change config file.

Terminal 1:

```
$ python3 pg_wal2socket.py
```


Terminal 2:

```
$ python3 pg_wal2socket-client.py localhost 8080
```


Terminal 3:

```
$ pgbench -i  -h 127.0.0.1 -Uuser db 
```


---
### Requisites

* A running Postgresql, with logical replication enabled and wal2json plugin enabled
* A logical replication slot, as in `select pg_create_logical_replication_slot('pg_wal2socket', 'wal2json');`
* python 3.10
* psycopg2-binary==2.9.1



---
### Thanks to
Nathan Jennings for [Socket Programming in Python (Guide)](https://realpython.com/python-sockets/)

