from ew11Interface import ew11Interface
from mqttInterface import mqttInterface

myServer = ew11Interface()

myServer.start()

mqtt = mqttInterface(myServer)


myServer.join()

