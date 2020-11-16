import sys
import os
import socket
import select

adresse_hote = ''
numero_port = 6688


def lecture_ligne(ma_socket):
  ligne = b''
  while 1:
    caractere_courant = ma_socket.recv(1)
    if not caractere_courant:
      break
    if caractere_courant == b'\r':
      caractere_suivant = ma_socket.recv(1)
      if caractere_suivant == b'\n':
        break
      ligne += caractere_courant + caractere_suivant
      continue
    if caractere_courant == b'\n':
      break
    ligne += caractere_courant
  return ligne

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
ma_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ma_socket.bind((adresse_hote, numero_port))
ma_socket.listen(socket.SOMAXCONN)

surveillance = [ma_socket]
while 1:
  (evnt_entree, evnt_sortie, evnt_exception) = select.select(surveillance, [], [])
  for un_evenement in evnt_entree:
    if (un_evenement == ma_socket):
        # il y a une demande de connexion
      nouvelle_connexion, depuis = ma_socket.accept()
      print("Nouvelle connexion depuis ", depuis)
      nouvelle_connexion.sendall(b'Bienvenu\n')
      surveillance.append(nouvelle_connexion)
      continue
    # sinon cela concerne une socket connectée à un client
    ligne = un_evenement.recv(1024)
    if not ligne:
      surveillance.remove(un_evenement)  # le client s'est déconnecté
    else:
      print(un_evenement.getpeername(), ':', ligne)
    # envoyer la ligne a tous les clients, etc
      for desc in surveillance:
        if (desc != ma_socket) and (desc != un_evenement):
          desc.sendall(bytes(str(un_evenement.getpeername()), encoding='UTF-8')+b': '+ligne)

connexion.close()
ma_socket.close()