
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

functions = {
    '3':'Read Holding Registers',
    '16':'Write Multiple Registers',
    '131':'ERREUR'
}

status = {
    0:'Ventilation',
    1:'Tempo Chauffage',
    2:'Chauffage',
    3:'Free Cooling',
    4:'AD 4',
    5:'AD 5',
    6:'Dégivrage',
    7:'AD',
    8:'AD',
    9:'ERR 2 Sécurité HP'
}

registers = {
    1:{
        9002:'R Ref Programme Smart',
        9004:'R Température Etalonnée Air Extrait',
        9005:'R Température Etalonnée Air Rejeté',
        9006:'R Température Etalonnée Air Neuf',
        9007:'R Température Etalonnée Air Insufflé',
        9036:'R Consigne recalculée Ecran Principal',
        9038:'R Mode de fonctionnement',
        9039:'R Température Etalonnée Ecran',
        9041:'R Temps restant GV Extraction',
        9042:'R Temps restant timer filtre',
        9043:'R&W Reset Timer Filtre',
        9049:'R Consommation Rafraichissement',
        9051:'R Consommation Chauffage',
        9053:'R Consommation Ventilation',
        9055:'R Consommation Freecooling',
        9070:'R Température Etalonnée Sensair',
        9071:'R Hygrométrie Etalonnée Sensair',
        9072:'R Information Manu / Ref Prog.',
        9076:'R ON / OFF fonction LED Sensair',
        9077:'R CO2 Eq. Capteur Sensair Bar Graph',
        9078:'R Consigne recalculée Zone Sensair',
        9080:'R Information Manu / Ref Prog.',
        
        16383:'R&W MANU / PROG status',
        16385:'R&W Reset Valeurs Usine',
        16406:'R&W Valeur débit de recyclage',
        16427:'R Nb démarrage Chaud',
        16429:'R Nb démarrage Froid',
        16443:'R&W Vitesse U076',
        16445:'R&W Vitesse U071',
        16447:'R&W Vitesse U176',
        16449:'R&W Vitesse U171',
        16451:'R&W Vitesse U276',
        16453:'R&W Vitesse U271',
        16455:'R&W Vitesse U376',
        16457:'R&W Vitesse U371',
        16471:'R&W Température de consigne',
        16473:'R&W Valeur de réduction de consigne',
        16475:'R&W Choix du programme',
        16476:'R&W ON / OFF status',
        16477:'R&W HIVER / ETE status',
        16478:'R&W ECO / BOOST status',
        16479:'R&W Appoint Intégré status',
        16480:'R&W Ecart Appoint N°1',
        16482:'R&W Ecart Appoint N°2',
        16484:'R&W Timer Filtre',
        16485:'R&W GV Extraction status',
        16491:'R&W Etalonnage sonde temp. Ecran',
        16493:'R&W Temps montée V1 à V2',
        16494:'R&W Temperature Mode V0',
        16499:'R&W ON / OFF Led Sensair Status',
        16501:'R&W Temps montée V1 à V2',
        16502:'R&W Température de consigne zone Sensair',
        16504:'R&W Temperature Mode V0',
        16487:'Time schedule 4 status',
        16488:'Time schedule 5 status',
        16489:'Time schedule 1 status',
        16490:'Time schedule 2 status',
        9048:'Screen Internal temperature',
        9057:'Ecran Comm. check',
        9070:'Température Etalonnée Sensair',
        9071:'Hygrométrie Etalonnée Sensair',
        9104:'AD',
        9105:'AD',
        9106:'AD',
        9111:'AD'
    },
    11:{
        4:'R Température Etalonnée Sensair Z1',
        9:'Etalonnage Humidité Sensair Z1',
        13:'Sensair Z1 Comm. Check',
        16:'AD'
    },
    12:{
        4:'R Température Etalonnée Sensair Z2',
        8:'R&W Etalonnage Temp. Sensair Z2',
        13:'Sensair Z1 Comm. Check',
        16:'AD'
    },
    101:{
        4:'R Dde Chaud ou Froid Zone Ecran',
        5:'R Réchauffeur Zone Ecran',
        6:'EZAir 1 Comm Check',
        7:'EZAir 1 Registre Programme',
        35:'AD'  
    },
    102:{
        4:'R Dde Chaud ou Froid Zone Sensair',
        5:'R Réchauffeur Zone Sensair',
        6:'EZAir 2 Comm Check',
        7:'EZAir 2 Registre Programme',
        35:'AD' 
    },
    247:{
        1:'Valeur du mode de fonctionnement (envoi sur device distant)',
        2:'R&W Température de consigne zone Ecran',
        4:'R&W Température de consigne zone Sensair',
        6:'R&W ON / OFF status',
        7:'R&W HIVER / ETE status',
        8:'R&W ECO / BOOST status',
        9:'Temperature Etalonnée de l’écran (envoi sur device distant)',
        11:'Temperature Etalonnée du Sensair (envoi sur device distant)',
        12:'R&W MANU / PROG status',
        14:'AD',
        15:'AD',
        16:'AD',
    }
}