
class Listener:
    loginFlag=False
    Globalnome="default"
    
    def setName(self,name):
        self.Globalnome=name
        
    def getName(self):
        return self.Globalnome
