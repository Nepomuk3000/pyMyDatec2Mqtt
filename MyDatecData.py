import json

class MyDatecData:
    CO2CapteurNuit = -1
    CO2CapteurJour = -1
    TemperatureCapteurNuit = -1
    TemperatureCapteurJour = -1
    TemperatureEtalonneeJour = -1
    TemperatureEtalonneeNuit = -1
    TemperatureEcran = -1
    TemperatureEcran = -1
    HygrometrieCapteurNuit = -1
    HygrometrieCapteurJour = -1
    HygrometrieEtalonneeNuit = -1
    HygrometrieEtalonneeJour = -1
    AirExtrait = -1
    AirRejete = -1
    AirExterieur = -1
    AirInsufle = -1
    TempsFiltre = -1
    TempsRestantFiltre = -1
    StatusCode = -1
    Status = "Not set"
    
    @classmethod
    def toJson(cls):
        data = {}
        data['ZoneNuit'] = {}
        data['ZoneNuit']['TemperatureBrute'] = MyDatecData.TemperatureCapteurNuit
        data['ZoneNuit']['TemperatureEtalonnee'] = MyDatecData.TemperatureEtalonneeNuit
        data['ZoneNuit']['HumiditeBrute'] = MyDatecData.HygrometrieCapteurNuit
        data['ZoneNuit']['HumiditeEtalonnee'] = MyDatecData.HygrometrieEtalonneeNuit
        data['ZoneNuit']['COV'] = MyDatecData.CO2CapteurNuit
        
        data['ZoneJour'] = {}
        data['ZoneJour']['TemperatureBrute'] = MyDatecData.TemperatureCapteurJour
        data['ZoneJour']['TemperatureEtalonnee'] = MyDatecData.TemperatureEtalonneeJour
        data['ZoneJour']["TemperatureEcran"] = MyDatecData.TemperatureEcran
        data['ZoneJour']['HumiditeBrute'] = MyDatecData.HygrometrieCapteurJour
        data['ZoneJour']['HumiditeEtalonnee'] = MyDatecData.HygrometrieEtalonneeJour
        data['ZoneJour']['COV'] = MyDatecData.CO2CapteurJour
        
        data['TemperatureAir'] = {}
        data['TemperatureAir']['Extrait'] = MyDatecData.AirExtrait
        data['TemperatureAir']['Rejete'] = MyDatecData.AirRejete
        data['TemperatureAir']['Exterieur'] = MyDatecData.AirExterieur
        data['TemperatureAir']['Insufle'] = MyDatecData.AirInsufle
        
        data['Filtre'] = {}
        data['Filtre']['TempsFiltre'] = MyDatecData.TempsFiltre
        data['Filtre']['TempsRestantFiltre'] = MyDatecData.TempsRestantFiltre
        
        data['Etat'] = {}
        data['Etat']['Code'] = MyDatecData.StatusCode
        data['Etat']['Texte'] = MyDatecData.Status
        
        return json.dumps(data,indent=2)