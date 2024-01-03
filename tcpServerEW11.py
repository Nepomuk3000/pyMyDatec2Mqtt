import socket
import binascii
import log
from ModbusFrame import ModbusFrame

# Paramètres du serveur
host = '0.0.0.0'  # Adresse IP du serveur
port = 10004         # Port d'écoute du serveur

# Création du socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Lier le socket à l'adresse et au port spécifiés
server_socket.bind((host, port))

# Mettre le socket en mode écoute
server_socket.listen()

print(f"Serveur en attente de connexion sur {host}:{port}")

# Accepter la connexion d'un client
client_socket, client_address = server_socket.accept()
print(f"Connexion établie avec {client_address}")

curFrame = ModbusFrame()
# Boucle de traitement des données
while True:
    # Recevoir les données du client
    data = client_socket.recv(1024)
        
    # Si les données sont vides, le client a fermé la connexion
    if not data:
        print("Connexion fermée par le client.")
        break
    hex_data = binascii.hexlify(data).decode('utf-8')

    # print("------------Reception de : ",hex_data)

    # Traitement des données une par une
    for byte in data:
        # Retirer l'élément du début de la file d'attente
        ret = curFrame.add_bytes(byte.to_bytes(1, 'big'))
        if ret:
            curFrame.print()
            if curFrame.slave == 247 and curFrame.isRequest:
                log.todo(f"Envoyer la réponse à la demande de trame {curFrame.startingAddr:04X}")
                responseFrame = ModbusFrame()
                responseFrame.isRequest = False
                responseFrame.slave = curFrame.slave
                responseFrame.function = curFrame.function    
                           
                if curFrame.function == 3 : 
                    if curFrame.startingAddr == 2:
                        responseFrame.byteCount = 14
                        responseFrame.pdu=b'\x00\x00\x41\xA0\x00\x00\x41\xB0\x00\x01\x00\x00\x00\x00'
                        
                    elif curFrame.startingAddr == 12:
                        responseFrame.byteCount = 2
                        responseFrame.pdu=b'\x00\x00'   
                                  
                if curFrame.function == 16 : 
                    responseFrame.startingAddr = curFrame.startingAddr
                    responseFrame.quantity = curFrame.quantity
                    
                data = responseFrame.to_bytes()
                responseFrame.print()
                #client_socket.send(data)
                #log.dbg(type(data))
            curFrame = ModbusFrame()

    if ret == False:
        log.error("ERREUR pas possible d'obtenir une frame valide")
        curFrame = ModbusFrame()

# Fermer les sockets
client_socket.close()
server_socket.close()
