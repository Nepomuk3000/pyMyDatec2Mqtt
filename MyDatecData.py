import json

class MyDatecDataClass:
    instance = None
    data = {}
    
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
        with open('config/config.json', 'r') as jsonfile:
            self.data = json.load(jsonfile)
        
    def save(self):
        with open('config/config.json', 'w') as jsonfile:
            json.dump(MyDatecData.data, jsonfile, indent=2)
        
MyDatecData = MyDatecDataClass()