import socket
import sys
from collections import deque
import binascii
from colorama import Fore, Back, Style

def todo(inStr):
    print(f"{Back.YELLOW}{Fore.BLACK}TODO : {inStr}{Style.RESET_ALL}")
    
def error(inStr):
    print(f"{Back.RED}{Fore.BLACK}ERROR : {inStr}{Style.RESET_ALL}")
    
def dbg(inStr):
    print(f"{Back.GREEN}{Fore.BLACK}DBG : {inStr}{Style.RESET_ALL}")

class ModbusFrame:
    def __init__(self):
        self.data = b''
        self.isValid = False
        self.isRequest = False
        
        self.slave = -1
        self.function = -1
        self.crc = -1
        
        self.quantity = 0
        self.startingAddr = -1
        
        self.byteCount = -1
        self.registersValues = []
        
    def to_bytes(self):
        """Convertir la trame Modbus en une séquence d'octets."""
        frame_bytes = bytes([self.address, self.function_code]) + self.data
        return frame_bytes
    
    def add_bytes(self,inByte):
        self.data += inByte
        self.isValid = self.check_CRC()
        
        if (self.isValid):
            self.slave=self.data[0]
            self.function=self.data[1]
            if self.function > 0x80:
                self.isRequest = False
                todo("Traiter les réponses d'erreur de type : 65 83 02 812e")
            elif self.function == 16:
                self.startingAddr = self.data[2] << 8 | self.data[3]
                self.quantity = self.data[4] << 8 | self.data[5]
                if len(self.data) == 8:
                    self.isRequest = False
                else:
                    self.isRequest = True
                    self.byteCount = self.data[6]
                    for i in range(self.quantity):
                        regVal = self.data[7 + 2 * i] << 8 | self.data[8 + 2 * i]
                        self.registersValues.append(regVal)
            else:
                if len(self.data) != 5 + self.data[2]:
                    try:
                        self.isRequest = True
                        self.startingAddr = self.data[2] << 8 | self.data[3]
                        self.quantity = self.data[4] << 8 | self.data[5]
                    except:
                        error(f"Processing Request function {self.function} {self.data:X}")
                else:
                    self.isRequest = False
                    todo("Traiter les réponses de fonction 1")
              
        return self.isValid
            
        
    def check_CRC(self):
        if len(self.data) < 4:
            return False
        else:
            expectedCRC = self.data[-2] * 256 + self.data[-1]
            dataWithoutCRC = self.data[:-2]
      
            crc_table = [
                0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
                0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
                0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
                0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
                0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
                0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
                0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
                0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
                0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
                0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
                0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
                0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
                0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
                0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
                0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
                0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
                0xa001, 0x60c0, 0x6180, 0xa141, 0x6300, 0xa3c1, 0xa281, 0x6240,
                0x6600, 0xa6c1, 0xa781, 0x6740, 0xa501, 0x65c0, 0x6480, 0xa441, 
                0x6c00, 0xacc1, 0xad81, 0x6d40, 0xaf01, 0x6fc0, 0x6e80, 0xae41, 
                0xaa01, 0x6ac0, 0x6b80, 0xab41, 0x6900, 0xa9c1, 0xa881, 0x6840, 
                0x7800, 0xb8c1, 0xb981, 0x7940, 0xbb01, 0x7bc0, 0x7a80, 0xba41, 
                0xbe01, 0x7ec0, 0x7f80, 0xbf41, 0x7d00, 0xbdc1, 0xbc81, 0x7c40, 
                0xb401, 0x74c0, 0x7580, 0xb541, 0x7700, 0xb7c1, 0xb681, 0x7640, 
                0x7200, 0xb2c1, 0xb381, 0x7340, 0xb101, 0x71c0, 0x7080, 0xb041, 
                0x5000, 0x90c1, 0x9181, 0x5140, 0x9301, 0x53c0, 0x5280, 0x9241, 
                0x9601, 0x56c0, 0x5780, 0x9741, 0x5500, 0x95c1, 0x9481, 0x5440, 
                0x9c01, 0x5cc0, 0x5d80, 0x9d41, 0x5f00, 0x9fc1, 0x9e81, 0x5e40, 
                0x5a00, 0x9ac1, 0x9b81, 0x5b40, 0x9901, 0x59c0, 0x5880, 0x9841, 
                0x8801, 0x48c0, 0x4980, 0x8941, 0x4b00, 0x8bc1, 0x8a81, 0x4a40, 
                0x4e00, 0x8ec1, 0x8f81, 0x4f40, 0x8d01, 0x4dc0, 0x4c80, 0x8c41, 
                0x4400, 0x84c1, 0x8581, 0x4540, 0x8701, 0x47c0, 0x4680, 0x8641, 
                0x8201, 0x42c0, 0x4380, 0x8341, 0x4100, 0x81c1, 0x8081, 0x4040 
            ]

            crc = 0xFFFF  # Initialiser la valeur du CRC

            for byte in dataWithoutCRC:
                index = (crc ^ byte) & 0xFF
                crc = (crc >> 8) ^ crc_table[index]
            self.crc = ((crc & 0xFF) << 8) | ((crc >> 8) & 0xFF)

            return self.crc == expectedCRC

    def print(self):
        hex_data = binascii.hexlify(curFrame.data).decode('utf-8')
        print("-----------------------------")
        print("-- Données brutees :",hex_data)
        print("--", f"{Fore.YELLOW}Request{Style.RESET_ALL}" if curFrame.isRequest else f"{Fore.GREEN}Response{Style.RESET_ALL}")
        print("-- * slave    :",self.slave)
        print("-- * function :",self.function)
        if curFrame.isRequest == True:
            print(f"--   * starting address : 0x{self.startingAddr:04X} ({self.startingAddr})")
            print(f"--   * quantity         : {self.quantity}")
            if curFrame.function == 16:
                print(f"--   * byte count       : {self.byteCount}")
                hexa = ' '.join(f"{element:04X}" for element in self.registersValues)
                print(f"--   * registers values : [{hexa}]")
                
        else :
            todo("Afficher les réponses")
            
        print("-- * crc      :","0x{:04X}".format(self.crc))
            


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
            curFrame = ModbusFrame()

    if ret == False:
        print ("ERREUR pas possible d'obtenir une frame valide")
        curFrame = ModbusFrame()

# Fermer les sockets
client_socket.close()
server_socket.close()
