import time
from AX12_Control import AX12_Control

class AX12_Panneau:
    def __init__(self):
        # Initialisation des moteurs avec les IDs id_1 et id_2
        self.AX12_Panneau_Droit = AX12_Control(9, 9600, '/dev/ttyACM1')
        #self.AX12_Panneau_Gauche = AX12_Control(8, 9600, '/dev/ttyACM0')
        self.AX12_Panneau_Droit.connect()
        #self.AX12_Panneau_Gauche.connect()
        self.ramener_AX12_droit()
        
    
    def ramener_AX12_droit(self):
        self.AX12_Panneau_Droit.move(830)
        time.sleep(2)
        return True
    
    def ramener_AX12_gauche(self):  
        self.AX12_Panneau_Gauche.move(415) #à déterminer
        time.sleep(2)
        return True
    
    
    def bouger_panneau_droit(self):
        self.AX12_Panneau_Droit.move(710)
        time.sleep(2)
        return True

    def bouger_panneau_gauche(self):
        self.AX12_Panneau_Gauche.move(415) #à déterminer
        time.sleep(2)
        return True
        
    
    def disconnect(self):
        self.AX12_Panneau_Droit.disconnect()
        self.AX12_Panneau_Gauche.disconnect()
        time.sleep(2)
        return True

# if __name__ == '__main__':
    # AX12_Panneau = AX12_Panneau()
    # AX12_Panneau.bouger_panneau_droit()
    # AX12_Panneau.ramener_AX12_droit()
    # AX12_Panneau.bouger_panneau_gauche()
    # AX12_Panneau.ramener_AX12_gauche()
    # AX12_Panneau.disconnect()