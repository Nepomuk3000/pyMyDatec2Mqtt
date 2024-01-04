import socket
import binascii
import log
import struct
import time
import threading
from ModbusFrame import ModbusFrame


class tcpServer:
    def __init__(self, inHost='0.0.0.0', inPort=10004):
        # Création du socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Lier le socket à l'adresse et au port spécifiés
        self.server_socket.bind((inHost, inPort))
        self.thread = threading.Thread(target=self.main)
        
        self.mutex = threading.Lock()
        
        self.t1 = 18
        self.t2 = 18
        self.pac = 0
        self.cold = 0
        self.boost = 0
    
    def start(self):
        self.thread.start()
        
    def setT1(self,inVal):
        self.mutex.acquire()
        self.t1 = inVal
        self.mutew.release()
        
    def setT2(self,inVal):
        self.mutex.acquire()
        self.t2 = inVal
        self.mutew.release()
        
    def setPAC(self,inVal):
        self.mutex.acquire()
        self.pac = inVal
        self.mutew.release()
        
    def setCold(self,inVal):
        self.mutex.acquire()
        self.cold = inVal
        self.mutew.release()
        
    def setBoost(self,inVal):
        self.mutex.acquire()
        self.boost = inVal
        self.mutew.release()
        
    def main(self):
        self.stop = False
        self.server_socket.listen()
        print(f"Serveur en attente de connexion")

        # Accepter la connexion d'un client
        self.client_socket, client_address = self.server_socket.accept()
        print(f"Connexion établie avec {client_address}")

        curFrame = ModbusFrame()
        # Boucle de traitement des données
        while not self.stop :
            # Recevoir les données du client
            data = self.client_socket.recv(1024)
                
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
                        if curFrame.function == 3:
                            log.todo(f"Envoyer la réponse à la demande de trame {curFrame.startingAddr:04X}")
                            responseFrame = ModbusFrame()
                            responseFrame.isRequest = False
                            responseFrame.slave = curFrame.slave
                            responseFrame.function = curFrame.function    
                                    
                            if curFrame.function == 3 : 
                                if curFrame.startingAddr == 2:
                                    responseFrame.byteCount = 14
                                    log.todo("Positionner les températures et modes à envoyer ICI")
                                    self.mutex.acquire()
                                    data = struct.pack("ff",self.t1,self.t2)
                                    pData = struct.unpack('BBBBBBBB',data)
                                    responseFrame.pdu = struct.pack(">BBBBBBBBHHH",pData[1],pData[0],pData[3],pData[2],
                                                    pData[5],pData[4],pData[7],pData[6],
                                                    self.pac,self.cold,self.boost)
                                    self.mutex.release()
                                elif curFrame.startingAddr == 12:
                                    responseFrame.byteCount = 2
                                    responseFrame.pdu=b'\x00\x00'   
                                            
                            if curFrame.function == 16 : 
                                responseFrame.startingAddr = curFrame.startingAddr
                                responseFrame.quantity = curFrame.quantity
                                
                            data = responseFrame.to_bytes()
                            responseFrame.print()
                            #sys.exit(1)
                            self.client_socket.send(data)
                            #log.dbg(type(data))
                    curFrame = ModbusFrame()

            if ret == False:
                log.error("ERREUR pas possible d'obtenir une frame valide")
                curFrame = ModbusFrame()

    def join(self):
        self.thread.join()
        
    def stop(self):
        self.stop = True
        # Fermer les sockets
        self.client_socket.close()
        self.server_socket.close()