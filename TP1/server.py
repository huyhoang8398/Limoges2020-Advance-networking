import sys
import os
import socket

adresse_hote = ''
numero_port = 6688
ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
ma_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ma_socket.bind((adresse_hote, numero_port))
ma_socket.listen(socket.SOMAXCONN)

while 1:
    (nouvelle_connexion, depuis) = ma_socket.accept()
    print("Nouvelle connexion depuis ", depuis)
    nouvelle_connexion.sendall(b'Bienvenu\n')
    pid = os.fork()
    if (pid):
      while 1:
        ligne = nouvelle_connexion.recv(1000)
        print("<:", str(ligne, encoding='UTF-8'))
        if not ligne:
          break
    else:
      while 1:
        clavier = input(':>')
        if not clavier:
          break
        nouvelle_connexion.sendall(bytes(clavier, encoding='UTF-8'))
    nouvelle_connexion.close()
ma_socket.close()
