#!/usr/bin/env python3

import sys
import socket
import selectors
import types
import configparser

import psycopg2
from psycopg2.extras import LogicalReplicationConnection, StopReplication


# Prevent "Broken pipe" on `sent = mysock.sendall((msg.payload.encode()))`
# Investigate this!
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
#




def get_repl_cursor(config):
  try:
    lconnection  = psycopg2.connect (
                    "host=%s user=%s password=%s dbname=%s port=%s" % \
                        (  config.get('postgresql', 'host')
                          ,config.get('postgresql', 'user')
                          ,config.get('postgresql', 'password')
                          ,config.get('postgresql', 'dbname')
                          ,config.get('postgresql', 'port')
                        ),
                     connection_factory = LogicalReplicationConnection)
  except psycopg2.OperationalError as e:
    print('Unable to connect!\n{0}').format(e)
    sys.exit(30)

  lcursor = lconnection.cursor()

  lcursor.start_replication (
    slot_name = config.get('postgresql', 'slot_name')
    ,options = {  'pretty-print':0
                ,'write-in-chunks':0
                ,'include-lsn':1
                ,'format-version':2
              }
    ,decode=True
  )

  print(f"Connected to postgresql {config.get('postgresql', 'host')} db {config.get('postgresql', 'dbname')}")

  return lcursor



def start_socket(config):
  host, port = config.get('socket', 'host'), int(config.get('socket', 'port'))

  lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  lsock.bind((host, port))
  lsock.listen()

  lsock.setblocking(False)
  sel.register(lsock, selectors.EVENT_READ, data=None)

  print(f"Listening on {host} port {port}")



def welcome_client(sock):
  conn, addr = sock.accept()

  conn.setblocking(False)
  data = types.SimpleNamespace(addr=addr)
  events = selectors.EVENT_WRITE
  sel.register(conn, events, data=data)

  print(f"Accepted connection from {addr}")



def send_wal(message, sock):
  if message:
    sent = sock.sendall( message.payload.encode() )
    message.cursor.send_feedback( flush_lsn = message.data_start )




def main():
  config_filename = 'pg_wal2socket.conf'
  config = configparser.ConfigParser()
  if not config.read(config_filename):
    print("Unable to read config file %s" % config_filename)
    exit(20)

  repl_cursor = get_repl_cursor(config)
  start_socket(config)

  try:

    while True:
      events = sel.select(timeout=None)
      for key, mask in events:
        if key.data is None:
          welcome_client(key.fileobj)
        else:
          repl_slot_message = repl_cursor.read_message()
          send_wal(repl_slot_message, key.fileobj)

  except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
  finally:
    sel.close()




if __name__=="__main__":
  sel = selectors.DefaultSelector()
  main()
else:
  exit (1)
