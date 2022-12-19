#!/usr/bin/env python3

# Copied from https://docs.air-q.com, which you can, of course, only access
# after purchasing a device and entering the serial number. 🤦🏻‍♂️

import sys
import base64
import json
import http.client
from Crypto.Cipher import AES

SENSOR = sys.argv[1]
PASSWORD = sys.argv[2]

def unpad(data):
  return data[:-ord(data[-1])]

def decodeMessage(msgb64):
  msg = base64.b64decode(msgb64)

  # Generate AES key of length 32 from air-Q password.
  key = PASSWORD.encode('utf-8')
  if len(key) < 32:
    for i in range(32-len(key)):
      key += b'0'
  elif len(key) > 32:
    key = key[:32]

  # Decode AES256.
  cipher = AES.new(key=key, mode=AES.MODE_CBC, IV=msg[:16])
  return unpad(cipher.decrypt(msg[16:]).decode('utf-8'))

connection = http.client.HTTPConnection(SENSOR)

connection.request('GET', '/data')
contents = connection.getresponse()

msg = json.loads(contents.read())
msg['content'] = json.loads(decodeMessage(msg['content']))
print(json.dumps(msg['content']))

connection.close()
