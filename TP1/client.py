import os
import socket
import sys

adresse_serveur = 'localhost'
numero_port = 6688
ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  ma_socket.connect((adresse_serveur, numero_port))
except:
  print("probleme de connexion")
sys.exit(1)
pid = os.fork()
if (pid):
  while 1:
    ligne = ma_socket.recv(1000)
    print(str(ligne, encoding='UTF-8'))
    if not ligne:
      break
else:
  while 1:
    clavier = input(':>')
    if not clavier:
      break
    ma_socket.sendall(bytes(clavier+'\n', encoding='UTF-8'))
ma_socket.close()
