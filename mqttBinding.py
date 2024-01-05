import paho.mqtt.client as mqtt
import binascii
from struct import *
import json
from ew11Binding import ew11Binding


class mqttBinding:
    
    def __init__ (self, inEw11Binding):
        
        # Paramètres du broker MQTT
        broker_address = "192.168.1.107"
        broker_port = 1883
        self.topic = "mydatec/#"
        self.ew11Binding = inEw11Binding
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

        # Boucle principale du client
        self.client.loop_forever()

    # Callback appelée lorsqu'une connexion au broker est établie
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connecté au broker avec le code de retour {rc}")
        # Abonnez-vous au topic
        self.client.subscribe(self.topic)

    # Callback appelée lorsqu'un message est reçu du broker
    def on_message(self, client, userdata, msg):
        #print(f"Message reçu du topic {msg.topic}: {msg.payload}")
        # Traitement des données binaires
        self.process_binary_payload(msg.payload)

    # Fonction de traitement des données binaires
    def process_binary_payload(self, binary_data):
        # Ajoutez ici votre logique de traitement pour les données binaires
        # par exemple, décoder les données binaires et effectuer une action en conséquence
        hex_data = binascii.hexlify(binary_data).decode('utf-8')
        print("Traitement des données binaires : ", binary_data)
        
        
        donnees = json.loads(binary_data)
                             
                             
        # Accéder aux données
        t1 =  donnees.get('t1', None)
        t2 =  donnees.get('t2', None)
        pac =  donnees.get('pac', None)
        cold =  donnees.get('cold', None)
        boost =  donnees.get('boost', None)
        
        
        if t1:
            self.ew11Binding.setConfig("t1",t1)
        if t2:
            self.ew11Binding.setConfig("t2",t2)
        if pac:
            self.ew11Binding.setConfig("pac",pac)
        if cold:
            self.ew11Binding.setConfig("cold",cold)
        if boost:
            self.ew11Binding.setConfig("boost",boost)
        # Afficher les données
        print(f"T1: {t1}, T2: {t2}, pac: {pac}, cold: {cold}, boost: {boost}")

