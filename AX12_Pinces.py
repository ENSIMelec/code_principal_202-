import time
import os
from dynamixel_sdk import *
from AX12_Control import AX12_Control

class AX12_Pinces:
    def __init__(self):
        # Initialisation des moteurs avec les IDs 3 et 5
        self.ax12_motor_1 = AX12_Control(3, 9600, '/dev/ttyACM0')
        self.ax12_motor_2 = AX12_Control(5, 9600, '/dev/ttyACM0')
        self.angle_ajustement_ax12_motor_1 = 580
        self.angle_ajustement_ax12_motor_2 = 140
        self.continuer_ajustement_motor_1 = True
        self.continuer_ajustement_motor_2 = True

    def initialize_motors(self):
        # On leur donne une position initiale
        self.ax12_motor_1.connect()
        self.ax12_motor_2.connect()

        self.ax12_motor_1.move(580)  # environ 170°
        self.ax12_motor_2.move(140) 


    def open_pince(self):
        # Ouvrir la pince
        self.ax12_motor_1.move(470) # à peu près 135°
        self.ax12_motor_2.move(270) 

        
    def open_pince_stepbystep(self):
        self.continuer_ajustement_motor_1 = True
        self.continuer_ajustement_motor_2 = True
        while self.continuer_ajustement_motor_1 or self.continuer_ajustement_motor_2:
            if self.angle_ajustement_ax12_motor_1 > 470:
                self.angle_ajustement_ax12_motor_1 -= 10
                self.ax12_motor_1.move(self.angle_ajustement_ax12_motor_1)
            else:
                self.continuer_ajustement_motor_1 = False
                
            if self.angle_ajustement_ax12_motor_2 < 270:
                self.angle_ajustement_ax12_motor_2 += 10
                self.ax12_motor_2.move(self.angle_ajustement_ax12_motor_2)
            else:
                self.continuer_ajustement_motor_2 = False

    def close_pince(self):
        
        # Fermer la pince
        self.ax12_motor_1.move(580) 
        self.ax12_motor_2.move(140) 

        load_threshold = 150  # Définir le seuil de charge de travail approprié

        # Fermer la pince progressivement jusqu'à rencontrer une résistance
        while self.continuer_ajustement_motor_1 or self.continuer_ajustement_motor_2:
            time.sleep(0.75)
            # Obtenez la charge de travail actuelle des moteurs
            load_motor_1 = self.ax12_motor_1.read_load()
            load_motor_2 = self.ax12_motor_2.read_load()

            if load_motor_1 < load_threshold:
                self.angle_ajustement_ax12_motor_1 += 10
                self.ax12_motor_1.move(self.angle_ajustement_ax12_motor_1)
                print(f"Ajustement du moteur {self.ax12_motor_1.DXL_ID} effectué")
            else:
                print(f"Ajustement du moteur {self.ax12_motor_1.DXL_ID} suffisant")
                self.continuer_ajustement_motor_1 = False


            if load_motor_2 < load_threshold:
                self.angle_ajustement_ax12_motor_2 -= 10
                self.ax12_motor_2.move(self.angle_ajustement_ax12_motor_2)
                print(f"Ajustement du moteur {self.ax12_motor_2.DXL_ID} effectué")
            else:
                print(f"Ajustement du moteur {self.ax12_motor_2.DXL_ID} suffisant")
                self.continuer_ajustement_motor_2 = False

                
                
    def run(self):
        self.initialize_motors()
        self.open_pince()
        self.close_pince()
        self.open_pince_stepbystep()

# # Exemple d'utilisation
# if __name__ == "__main__":
#     pince = AX12_Pinces()
#     pince.run()