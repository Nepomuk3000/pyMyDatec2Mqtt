import socket
import binascii
import log
import struct
import json
import threading
import time
import constants
from ModbusFrame import ModbusFrame
from colorama import Fore, Back, Style
from MyDatecData import MyDatecData
        
class ew11Binding:
    showDataChanges = False
    showRegisters = False
    
    def __init__(self, inHost='0.0.0.0', inPort=10004):
            
        # Création du socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Lier le socket à l'adresse et au port spécifiés
        self.server_socket.bind((inHost, inPort))
        self.thread = threading.Thread(target=self.main)
        
        self.mutex = threading.Lock()
        
        self.previousReq = None
        
        self.status = 0
        
        self.precT1ConsigneEcran = -1
        self.precT2ConsigneEcran = -1
        self.precPacConsigneEcran = -1
        self.precColdConsigneEcran = -1
        self.precBoostConsigneEcran = -1
    
    def start(self):
        self.thread.start()
        
    def main(self):
        self.stop = False
        self.server_socket.listen()
        print(f"Serveur en attente de connexion")

        # Accepter la connexion d'un client
        self.client_socket, client_address = self.server_socket.accept()
        print(f"Connexion établie avec {client_address}")

        curFrame = ModbusFrame()
        # Boucle de traitement des données
        precFrame = {}
        while not self.stop :
            # Recevoir les données du client
            data = self.client_socket.recv(1024)
                
            # Si les données sont vides, le client a fermé la connexion
            if not data:
                print("Connexion fermée par le client.")
                break
            
            for byte in data:
                # Ajouter une donnée à la frame actuelle  
                curFrame.add_bytes(byte.to_bytes(1, 'big'))
                ret = curFrame.is_complete()
                
                # Si la frame est complète
                if ret:                    
                    if not curFrame.isRequest:
                        curFrame.request = self.previousReq
                        
                    # Si c'est demandé, afficher les données qui on changées d'une occurence d'une frame à l'autre
                    if ew11Binding.showDataChanges:
                        idx = curFrame.getIdStr()
                        try :
                            if precFrame[idx].crc != curFrame.crc:
                                self.printDataChanges(curFrame, precFrame[idx])
                        except :
                            pass
                        precFrame[idx] = curFrame

                    # Si demandé, afficher les données des frame qui ont des registres renseignés
                    if ew11Binding.showRegisters:
                        if len(curFrame.registersValues) > 0:
                            print(f"{Fore.BLUE}{curFrame.getIdStr()} / {curFrame.startingAddrToStr()}{Style.RESET_ALL}")
                            print(curFrame.registersValues)
                            print(curFrame.registersValuesToHex())
                    
                    # S'il s'agit d'une requête
                    if curFrame.isRequest:
                       self.processRequest(curFrame)
                            
                    else: # S'il s'agit de réponses
                        self.processResponse(curFrame)
                    curFrame = ModbusFrame()

            if ret == False:
                log.warning("ERREUR pas possible d'obtenir une frame valide")
                curFrame = ModbusFrame()
    
    def processRequest(self,curFrame):
        self.previousReq = curFrame            
        # On ne remplace que le slave 247. On ne prépare les réponses qui lui sont associées 
        if curFrame.isId(247):                       
            responseFrame = ModbusFrame()
            responseFrame.isRequest = False
            responseFrame.slave = curFrame.slave
            responseFrame.function = curFrame.function      
            responseFrame.startingAddr = curFrame.startingAddr
            responseFrame.quantity = curFrame.quantity
                                    
            # Traitement des requêtes relatives au slave 247        
            if curFrame.isId(247,3,2):
                self.setTempAndModePDU(responseFrame)
            elif curFrame.isId(247,3,12):
                responseFrame.byteCount = 2
                responseFrame.pdu=b'\x00\x01'
            elif curFrame.isId(247,16,1):   
                statusCode = curFrame.registersValues[0]
                try:
                    statusStr=constants.status[statusCode]
                except:
                    txt="Unknown"
                MyDatecData['Statut']['Etat']['Code']=statusCode
                MyDatecData['Statut']['Etat']['Texte']=statusStr
            data = responseFrame.to_bytes()
            self.client_socket.send(data)
        
        # Traitement de l'information température interne de l'écran
        if curFrame.isId(1,16,9048):
            MyDatecData['Statut']['ZoneJour']['TemperatureEcran'] = curFrame.registersValues[0]/10
            
        elif curFrame.isId(1,16,9070):
            MyDatecData['Statut']['ZoneNuit']['TemperatureEtalonnee'] = curFrame.registersValues[0]/10
            
        elif curFrame.isId(1,16,9071):
            MyDatecData['Statut']['ZoneNuit']['HygrometrieEtalonnee'] = curFrame.registersValues[0]
            
        # Traitement de la consigne de température zone jour par l'écran
        elif curFrame.isId(1,16,16471):  
            bytes_data = struct.pack('<' + 'H' * len(curFrame.registersValues), *curFrame.registersValues)
            bTemperature = struct.pack('BBBB',bytes_data[3],bytes_data[2],bytes_data[1],bytes_data[0])
            temperature = struct.unpack('>f', bTemperature)[0]
            if self.precT1ConsigneEcran != temperature:
                MyDatecData['Consigne']['Temperature']['ZoneJour'] = temperature
                self.precT1ConsigneEcran = temperature
        
        # Traitement de la consigne de température zone nuit par l'écran
        elif curFrame.isId(1,16,16502):
            bytes_data = struct.pack('<' + 'H' * len(curFrame.registersValues), *curFrame.registersValues)
            bTemperature = struct.pack('BBBB',bytes_data[3],bytes_data[2],bytes_data[1],bytes_data[0])
            temperature = struct.unpack('>f', bTemperature)[0]
            if self.precT2ConsigneEcran != temperature:
                MyDatecData['Consigne']['Temperature']['ZoneNuit'] = temperature
                self.precT2ConsigneEcran = temperature
        
        # Traitement de la consigne pac ON / pac OFF par l'écran
        elif curFrame.isId(1,startingAddr=16476):   
            val = curFrame.registersValues[0]
            if self.precPacConsigneEcran != val:
                MyDatecData['Consigne']['Mode']['Pac'] = val
                self.precPacConsigneEcran = val

        # Traitement de la consigne froid / chaud par l'écran
        elif curFrame.isId(startingAddr=16477):
            val = curFrame.registersValues[0]
            if self.precColdConsigneEcran != val:
                MyDatecData['Consigne']['Mode']['Froid'] = val
                self.precColdConsigneEcran = val

        # Traitement de la consigne boost ON / boost OFF par l'écran
        elif curFrame.isId(startingAddr=16478):
            val = curFrame.registersValues[0]
            if self.precBoostConsigneEcran != val:
                MyDatecData['Consigne']['Mode']['Boost'] = val
                self.precBoostConsigneEcran = val        
                
    def processResponse(self,curFrame):  
        
        # Réponse du capteur de la zone Jour
        if curFrame.isId(11,3,4):
            MyDatecData['Statut']['ZoneJour']['TemperatureBrute'] = curFrame.registersValues[0]/10
            MyDatecData['Statut']['ZoneJour']['HygrometrieBrute'] = curFrame.registersValues[1]
            MyDatecData['Statut']['ZoneJour']['COV'] = curFrame.registersValues[2]
        
        # Réponse du capteur de la zone Nuit
        if curFrame.isId(12,3,4):
            MyDatecData['Statut']['ZoneNuit']['TemperatureBrute'] = curFrame.registersValues[0]/10
            MyDatecData['Statut']['ZoneNuit']['HygrometrieBrute'] = curFrame.registersValues[1]
            MyDatecData['Statut']['ZoneNuit']['COV'] = curFrame.registersValues[2]
        
        # Réponse de la VMC concernant les températures en entrée et sortie
        if curFrame.isId(1,3,9002):
            MyDatecData['Statut']['TemperatureAir']['Extrait'] = curFrame.registersValues[2]/10
            MyDatecData['Statut']['TemperatureAir']['Rejete'] = curFrame.registersValues[3]/10
            MyDatecData['Statut']['TemperatureAir']['Exterieur'] = curFrame.registersValues[4]/10
            MyDatecData['Statut']['TemperatureAir']['Insufle'] = curFrame.registersValues[5]/10
        
        if curFrame.isId(1,3,9036):
            MyDatecData['Statut']['Filtre']['TempsRestantFiltre'] = curFrame.registersValues[6]
        
        if curFrame.isId(1,3,16471):
            MyDatecData['Statut']['Filtre']['TempsFiltre'] = curFrame.registersValues[13]
            
        if curFrame.isId(1,3,9053):
            log.error("C'est la trame de consomation ventilation !!!!")
            
        if curFrame.isId(1,3,9051):
            log.error("C'est la trame de consomation chauffage !!!!")
            
        if curFrame.isId(1,3,9055):
            log.error("C'est la trame de consomation freecoolng !!!!")
            
        if curFrame.isId(1,3,9049):
            log.error(f"C'est la trame de consomation raffraichissement !!!! \n{curFrame.registersValues}\n{curFrame.registersValuesToHex()}")


    def printDataChanges(self, curFrame, precFrame):
        print("########################################################################################################################")
        if curFrame.isRequest:
            print("Request")
        else:
            print("Response")
            
        txt = curFrame.startingAddrToStr()
                                
        print (curFrame.slave,curFrame.function,txt)
        print("Previously :", precFrame.registersValuesToHex())
        print("Now        :",curFrame.registersValuesToHex())
        print("########################################################################################################################")

    def setTempAndModePDU(self, responseFrame):
        responseFrame.byteCount = 14
        self.mutex.acquire()
        t1 = MyDatecData['Consigne']['Temperature']['ZoneJour']
        t2 = MyDatecData['Consigne']['Temperature']['ZoneNuit']
        pac = 1 if MyDatecData['Consigne']['Mode']['Pac'] else 0
        froid = 1 if MyDatecData['Consigne']['Mode']['Froid'] else 0
        boost = 1 if MyDatecData['Consigne']['Mode']['Boost'] else 0
        print("T1    =",t1)
        print("T2    =",t2)
        print("Pac   =",pac)
        print("Froid =",froid)
        print("Boost =",boost)
        data = struct.pack("ff",t1,t2)
        pData = struct.unpack('BBBBBBBB',data)
        responseFrame.pdu = struct.pack(">BBBBBBBBHHH",pData[1],pData[0],pData[3],pData[2],
                                                    pData[5],pData[4],pData[7],pData[6],
                                                    pac,froid,boost)
        self.mutex.release()

    def join(self):
        self.thread.join()
        
    def stop(self):
        self.stop = True
        # Fermer les sockets
        self.client_socket.close()
        self.server_socket.close()