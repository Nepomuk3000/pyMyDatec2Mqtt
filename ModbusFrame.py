import binascii
from colorama import Fore, Back, Style
import constants
import log

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
                log.todo("Traiter les réponses d'erreur de type : 65 83 02 812e")
            elif self.function == 16:
                self.startingAddr = self.data[2] << 8 | self.data[3]
                self.quantity = self.data[4] << 8 | self.data[5]
                if len(self.data) == 8:
                    self.isRequest = False
                    self.startingAddr = self.data[2] << 8 | self.data[3]
                    self.quantity = self.data[4] << 8 | self.data[5]
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
                        log.error(f"Processing Request function {self.function} {self.data:X}")
                else:
                    self.isRequest = False
                    self.byteCount = self.data[2]
                    shortCount = int(self.byteCount / 2)
                    for i in range(shortCount):
                        regVal = self.data[3 + 2 * i] << 8 | self.data[4 + 2 * i]
                        self.registersValues.append(regVal)
              
        return self.isValid
            
        
    def check_CRC(self):
        if len(self.data) < 4:
            return False
        else:
            expectedCRC = self.data[-2] * 256 + self.data[-1]
            dataWithoutCRC = self.data[:-2]

            crc = 0xFFFF  # Initialiser la valeur du CRC

            for byte in dataWithoutCRC:
                index = (crc ^ byte) & 0xFF
                crc = (crc >> 8) ^ constants.crc_table[index]
            self.crc = ((crc & 0xFF) << 8) | ((crc >> 8) & 0xFF)

            return self.crc == expectedCRC

    def print(self):
        hex_data = binascii.hexlify(self.data).decode('utf-8')
        # TODO Mettre un filtre configurable 
        # if self.slave != 247 or self.function != 3:
        #     print("return")
        print("---------------------------------------------------------------------------------------")
        print("-- Données brutees :",hex_data)
        print("--", f"{Back.CYAN}{Fore.BLACK}Request{Style.RESET_ALL}" if self.isRequest else f"{Back.GREEN}{Fore.BLACK}Response{Style.RESET_ALL}")
        print("-- * slave    :",self.slave)
        txt = constants.functions[str(self.function)]
        print("-- * function :",f"{Back.MAGENTA}" if self.function == 16 else f"{Back.BLUE}",self.function,txt,f"{Style.RESET_ALL}")
        if self.isRequest == True:
            txt = constants.registers[str(self.startingAddr)]
            print(f"--   * starting address : 0x{self.startingAddr:04X} ({self.startingAddr})  {txt}")
            print(f"--   * quantity         : {self.quantity}")
            if self.function == 16:
                print(f"--   * byte count       : {self.byteCount}")
                hexa = ' '.join(f"{element:04X}" for element in self.registersValues)
                print(f"--   * registers values : [{hexa}]")
                
        else :
            if self.function < 0x80:
                if self.function == 3:
                    print(f"--   * byte count       : {self.byteCount}")
                    hexa = ' '.join(f"{element:04X}" for element in self.registersValues)
                    print(f"--   * registers values : [{hexa}]")
                else:
                    txt = constants.registers[str(self.startingAddr)]
                    print(f"--   * starting address : 0x{self.startingAddr:04X} ({self.startingAddr}) {txt}")
                    print(f"--   * quantity         : {self.quantity}")
            else:
                log.todo("Traiter les erreurs") 
            
        # print("-- * crc      :","0x{:04X}".format(self.crc))
            
