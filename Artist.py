# Simple artist class. Stores an artists name
class Artist:

    def __init__(self, name:str):
        self._name = name
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name:str):
        self._name = name