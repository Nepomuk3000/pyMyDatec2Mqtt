import os
import json

class MyDatecDataClass:
    instance = None
    data = {}
    path = os.path.dirname(os.path.abspath(__file__))

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(MyDatecDataClass, cls).__new__(cls)
            cls.instance.load()
        return cls.instance
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
        
    def load(self):
        with open(self.path + '/config/config.json', 'r') as jsonfile:
            self.data = json.load(jsonfile)
        
    def save(self):
        with open(self.path + '/config/config.json', 'w') as jsonfile:
            json.dump(MyDatecData.data, jsonfile, indent=2)
        
MyDatecData = MyDatecDataClass()
