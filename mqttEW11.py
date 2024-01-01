import paho.mqtt.client as mqtt
import binascii
from struct import *

# Paramètres du broker MQTT
broker_address = "192.168.1.107"
broker_port = 1883
topic = "ew11/up"
username = "pi"
password = "2oyfexeo"

# Callback appelée lorsqu'une connexion au broker est établie
def on_connect(client, userdata, flags, rc):
    print(f"Connecté au broker avec le code de retour {rc}")
    # Abonnez-vous au topic
    client.subscribe(topic)

# Callback appelée lorsqu'un message est reçu du broker
def on_message(client, userdata, msg):
    #print(f"Message reçu du topic {msg.topic}: {msg.payload}")
    # Traitement des données binaires
    process_binary_payload(msg.payload)

# Fonction de traitement des données binaires
def process_binary_payload(binary_data):
    # Ajoutez ici votre logique de traitement pour les données binaires
    # par exemple, décoder les données binaires et effectuer une action en conséquence
    hex_data = binascii.hexlify(binary_data).decode('utf-8')
    if (len(binary_data) > 4):
        print(len(binary_data))
        myTuple = unpack('!BBH',binary_data[:4])
        print("Traitement des données binaires : ", myTuple, hex_data)

# Création d'un client MQTT
client = mqtt.Client()

# Configuration des callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connexion au broker MQTT
client.username_pw_set(username, password)
client.connect(broker_address, broker_port, 60)

# Boucle principale du client
client.loop_forever()

