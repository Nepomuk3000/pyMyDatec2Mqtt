import paho.mqtt.client as mqtt
import binascii
from struct import *
import json
import ew11Interface
from MyDatecData import MyDatecData
import threading
import time
from datetime import datetime
import log

def toBool(inByteArray):
    return inByteArray in [b'True',b'true',b'1']

class mqttInterface:
    
    def __init__ (self, inEw11Binding):
        
        # Paramètres du broker MQTT
        broker_address = "192.168.1.107"
        broker_port = 1883
        self.topic = "mydatec/#"
        self.ew11Interface = inEw11Binding
        username = "pi"
        password = "xxxxxxxx"

        # Création d'un client MQTT
        self.client = mqtt.Client()

        # Configuration des callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connexion au broker MQTT
        self.client.username_pw_set(username, password)
        self.client.connect(broker_address, broker_port, 60)

        self.thread = threading.Thread(target=self.sendMqttSatus)
        
        # Boucle principale du client
        self.client.loop_forever()

    # Callback appelée lorsqu'une connexion au broker est établie
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connecté au broker avec le code de retour {rc}")
        # Abonnez-vous au topic
        self.client.subscribe(self.topic)
        self.thread.start()
        
    def sendMqttSatus(self):
        while True:
            dateStr=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            MyDatecData['date']=dateStr
            message = json.dumps(MyDatecData.data,indent=2)
            self.client.publish("mydatec/status", message)
            MyDatecData.save()
            time.sleep(10)

    # Callback appelée lorsqu'un message est reçu du broker
    def on_message(self, client, userdata, msg):
        try:
            if msg.topic == "mydatec/cmd/tJour":
                MyDatecData['Consigne']['Temperature']['ZoneJour'] = float(msg.payload)
            elif msg.topic == "mydatec/cmd/tNuit":
                MyDatecData['Consigne']['Temperature']['ZoneNuit'] = float(msg.payload)
            elif msg.topic == "mydatec/cmd/pac":
                MyDatecData['Consigne']['Mode']['Pac'] = toBool(msg.payload)
            elif msg.topic == "mydatec/cmd/froid":
                MyDatecData['Consigne']['Mode']['Froid'] = toBool(msg.payload)
            elif msg.topic == "mydatec/cmd/boost":
                MyDatecData['Consigne']['Mode']['Boost'] = toBool(msg.payload)
            elif msg.topic == "mydatec/cmd/set":
                self.process_binary_payload(msg.payload)
        except Exception as e:
            log.error(f"Le format de la payload est probblement erroné\nTopic : {msg.topic}\n{msg.payload}")

    # Fonction de traitement des données binaires
    def process_binary_payload(self, binary_data):
        # Ajoutez ici votre logique de traitement pour les données binaires
        # par exemple, décoder les données binaires et effectuer une action en conséquence
        donnees = json.loads(binary_data)
                             
        # Accéder aux données
        t1 =  donnees.get('t1', None)
        t2 =  donnees.get('t2', None)
        pac =  donnees.get('pac', None)
        froid =  donnees.get('froid', None)
        boost =  donnees.get('boost', None)

        if t1 != None :
            MyDatecData['Consigne']['Temperature']['ZoneJour'] = t1
        if t2 != None :
            MyDatecData['Consigne']['Temperature']['ZoneNuit'] = t2
        if pac != None :
            MyDatecData['Consigne']['Mode']['Pac'] = pac
        if froid != None :
            MyDatecData['Consigne']['Mode']['Froid'] = froid
        if boost != None :
            MyDatecData['Consigne']['Mode']['Boost'] = boost

