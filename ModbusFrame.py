import binascii
from colorama import Fore, Back, Style
import constants
import log
import struct

class ModbusFrame:
    def __init__(self):
        self.data = b''
        self.isValid = False
        self.isRequest = False
        self.request = None
        
        self.slave = -1
        self.function = -1
        self.crc = -1
        
        self.quantity = 0
        self.startingAddr = -1
        
        self.byteCount = -1
        self.registersValues = []
        
        self.pdu = b''

    def to_bytes(self):
        if not self.isRequest:
            if self.function == 3:
                self.data = struct.pack('@BBB', self.slave, self.function, self.byteCount)
                self.data += self.pdu
                shortCount = int(self.byteCount / 2)
                for i in range(shortCount):
                    regVal = self.data[3 + 2 * i] << 8 | self.data[4 + 2 * i]
                    self.registersValues.append(regVal)
            else:
                self.data = struct.pack('>BBHH', self.slave, self.function, self.startingAddr, self.quantity )
            self.data += self.calculate_CRC(self.data).to_bytes(2, byteorder='big')  

            return self.data
        
    def is_complete(self):
        self.isValid = self.check_CRC()
        
        if (self.isValid):
            self.slave=self.data[0]
            self.function=self.data[1]
            if self.function > 0x80:
                self.isRequest = False
                hex_response = binascii.hexlify(self.data).decode('utf-8')  
                log.todo(f"Traiter les réponses d'erreur de type : {hex_response}")
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
    
    def add_bytes(self,inByte):
        self.data += inByte            
        
    def calculate_CRC(self,data):
        crc = 0xFFFF  # Initialiser la valeur du CRC

        for byte in data:
            index = (crc ^ byte) & 0xFF
            crc = (crc >> 8) ^ constants.crc_table[index]
        return ((crc & 0xFF) << 8) | ((crc >> 8) & 0xFF)
        
    def check_CRC(self):
        if len(self.data) < 4:
            return False
        else:
            expectedCRC = self.data[-2] * 256 + self.data[-1]
            dataWithoutCRC = self.data[:-2]
            self.crc = self.calculate_CRC(dataWithoutCRC)

            return self.crc == expectedCRC
        
    def registersValuesToHex(self):
        return ' '.join(f"{element:04X}" for element in self.registersValues)

    def getIdStr(self):
        if self.isRequest:
            addr = self.startingAddr
        else:
            try:
                addr = self.request.startingAddr
            except:
                addr = -1
        return f"{self.slave}_{self.function}_{addr}_{self.isRequest}"

    def isId(self,slave=None,function=None,startingAddr=None):
        ret = True
        if slave:
            ret &= self.slave == slave
        if function:
            ret &= self.function == function
        if startingAddr:
            if self.isRequest:
                ret &= self.startingAddr == startingAddr
            else:
                try:
                    ret &= self.request.startingAddr == startingAddr
                except:
                    ret = False
        return ret

    def print(self,slave=None,function=None,startingAddr=None):
        if not self.isId(slave,function,startingAddr):
            return
        hex_data = binascii.hexlify(self.data).decode('utf-8')
        # TODO Mettre un filtre configurable 
        #if self.startingAddr != 16471:
        #     print("return")
        
        
        print("---------------------------------------------------------------------------------------")
        print("-- Données brutees :",hex_data)
        print("--", f"{Back.CYAN}{Fore.BLACK}Request{Style.RESET_ALL}" if self.isRequest else f"{Back.GREEN}{Fore.BLACK}Response{Style.RESET_ALL}")
        print("-- * slave    :",self.slave)
        txt = constants.functions[str(self.function)]
        print("-- * function :",f"{Back.MAGENTA}" if self.function == 16 else f"{Back.BLUE}",self.function,txt,f"{Style.RESET_ALL}")
        if self.isRequest == True:
            strStartingAddr = self.startingAddrToStr()
            print(f"--   * starting address : {strStartingAddr}")

            print(f"--   * quantity         : {self.quantity}")
            if self.function == 16:
                print(f"--   * byte count       : {self.byteCount}")
                print(f"--   * registers values : [{self.registersValues}]")
                print(f"--                        [{self.registersValuesToHex()}]")
                
        else :
            if self.function < 0x80:
                if self.function == 3:
                    print(f"--   * byte count       : {self.byteCount}")
                    print(f"--   * registers values : [{self.registersValues}]")
                    print(f"--                        [{self.registersValuesToHex()}]")
                else:
                    try:
                        txt = constants.registers[self.slave][self.startingAddr]
                    except:
                        txt = f"Unknown register name for slave {self.slave} address : 0x{self.startingAddr:04X} ({self.startingAddr})"
                        log.error(txt)
                    print(f"--   * starting address : 0x{self.startingAddr:04X} ({self.startingAddr}) {txt}")
                    print(f"--   * quantity         : {self.quantity}")
            else:
                log.todo("Traiter les erreurs") 
                
    def startingAddrToStr(self):
        if self.isRequest:
            startingAddr = self.startingAddr
        else:
            if not self.request:
                log.error(f"No request for response {self.getIdStr()}")
                startingAddr = -1
            else:
                startingAddr = self.request.startingAddr
            
        try:
            txt = constants.registers[self.slave][startingAddr]
        except:
            txt = f"Unknown register name for slave {self.slave} address : 0x{startingAddr:04X} ({self.startingAddr})"
            log.error(txt)
        return (f"0x{startingAddr:04X} ({startingAddr})  {txt}")
            
        # print("-- * crc      :","0x{:04X}".format(self.crc))
            
