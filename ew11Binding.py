import socket
import binascii
import log
import struct
import json
import threading
from ModbusFrame import ModbusFrame


class ew11Binding:
    def __init__(self, inHost='0.0.0.0', inPort=10004):
        # Création du socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Lier le socket à l'adresse et au port spécifiés
        self.server_socket.bind((inHost, inPort))
        self.thread = threading.Thread(target=self.main)
        
        self.mutex = threading.Lock()
        
        self.prevReq = None
        
        with open('config/config.json', 'r') as jsonfile:
            self.config = json.load(jsonfile)
        
        self.status = 0
    
    def start(self):
        self.thread.start()
        
    def setConfig(self,label,value):
        self.mutex.acquire()
        self.config[label] = value
        with open('config/config.json', 'w') as jsonfile:
            json.dump(self.config, jsonfile, indent=2)
        self.mutex.release()
        
    def main(self):
        self.stop = False
        self.server_socket.listen()
        print(f"Serveur en attente de connexion")

        # Accepter la connexion d'un client
        self.client_socket, client_address = self.server_socket.accept()
        print(f"Connexion établie avec {client_address}")

        curFrame = ModbusFrame()
        # Boucle de traitement des données
        
        
        pduList = []
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
                # Ajouter une donnée à la frame actuelle  
                curFrame.add_bytes(byte.to_bytes(1, 'big'))
                ret = curFrame.is_complete()
                if ret:
                    idx = f"{curFrame.slave}{curFrame.function}{curFrame.startingAddr}{curFrame.isRequest}"
                    try :
                        if pduList[idx] != curFrame.registersValues:
                            print (pduList[idx])
                            print (curFrame.registersValues)
                    except:
                        pass
                    #pduList[idx] = curFrame.registersValues
                    #curFrame.print()   
                    if curFrame.isRequest:
                        self.prevReq = curFrame    
                                                       
                        if curFrame.slave == 247: 
                            responseFrame = ModbusFrame()
                            responseFrame.isRequest = False
                            responseFrame.slave = curFrame.slave
                            responseFrame.function = curFrame.function    
                                    
                            if curFrame.function == 3 : 
                                if curFrame.startingAddr == 2:
                                    self.setTempAndModePDU(responseFrame)
                                elif curFrame.startingAddr == 12:
                                    responseFrame.byteCount = 2
                                    responseFrame.pdu=b'\x00\x01'   
                                            
                            if curFrame.function == 16 : 
                                #curFrame.print()
                                responseFrame.startingAddr = curFrame.startingAddr
                                responseFrame.quantity = curFrame.quantity
                                
                                # Temperature Etalonnée de l’écran
                                if curFrame.startingAddr == 1:
                                    curFrame.print()
                                    status = curFrame.registersValues[0]
                                    print(f"{status}")
                                    #sys.exit(1)
                                # Temperature Etalonnée de l’écran
                                # if curFrame.startingAddr == 9:
                                    #data = struct.pack("<HH",curFrame.registersValues[0],curFrame.registersValues[1])
                                    
                                    #hex_data = binascii.hexlify(data).decode('utf-8')
                                    #print(hex_data)
                                    #print(data)
                                    #temperature = struct.unpack(">F",data)
                                    #print(data)
                                    #sys.exit(1)
                                
                            data = responseFrame.to_bytes()
                            #responseFrame.print()
                            self.client_socket.send(data)
                    else:
                        if curFrame.slave == 1: 
                            if curFrame.function == 3 : 
                                if curFrame.startingAddr == 16471:
                                    self.prevReq.print()
                                    curFrame.print()     
                                
                                
                    curFrame = ModbusFrame()

            if ret == False:
                log.error("ERREUR pas possible d'obtenir une frame valide")
                curFrame = ModbusFrame()

    def setTempAndModePDU(self, responseFrame):
        responseFrame.byteCount = 14
        self.mutex.acquire()
        data = struct.pack("ff",self.config['t1'],self.config['t2'])
        pData = struct.unpack('BBBBBBBB',data)
        responseFrame.pdu = struct.pack(">BBBBBBBBHHH",pData[1],pData[0],pData[3],pData[2],
                                                    pData[5],pData[4],pData[7],pData[6],
                                                    self.config['pac'],self.config['cold'],self.config['boost'])
        self.mutex.release()

    def join(self):
        self.thread.join()
        
    def stop(self):
        self.stop = True
        # Fermer les sockets
        self.client_socket.close()
        self.server_socket.close()