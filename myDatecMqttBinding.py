from ew11Binding import ew11Binding
from mqttBinding import mqttBinding

myServer = ew11Binding()

myServer.start()

mqtt = mqttBinding(myServer)


myServer.join()

