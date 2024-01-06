
from colorama import Fore, Back, Style

def todo(inStr):
    print(f"{Back.YELLOW}{Fore.BLACK}TODO : {inStr}{Style.RESET_ALL}")
    
def error(inStr):
    print(f"{Back.RED}{Fore.BLACK}ERROR : {inStr}{Style.RESET_ALL}")
    with open('err.log', 'a') as errLogFile:
        errLogFile.write(inStr + '\n')

def warning(inStr):
    print(f"{Back.RED}{Fore.BLACK}ERROR : {inStr}{Style.RESET_ALL}")
    
def dbg(inStr):
    print(f"{Back.GREEN}{Fore.BLACK}DBG : {inStr}{Style.RESET_ALL}")