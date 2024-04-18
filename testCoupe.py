import RPi.GPIO as GPIO
import time
from Lidar import LidarScanner
from Globals_Variables import *
from Asserv import Asserv
from AX12_Panneau import AX12_Panneau


# Fonction pour vérifier si le jack a été retiré
def check_jack_removed():
        # Lire l'état de la broche GPIO connectée au pin jack
        jack_state = GPIO.input(PIN_JACK)
        # Si l'état du jack est bas (0), cela signifie qu'il a été retiré
        if jack_state == GPIO.HIGH:
            print("Le jack a été retiré.")
            return True
        else:
            print("En attente du retrait du jack...")
            return False
# Code principal avec conditions sur l'arret en fonction d'obsatcle
def main():
    # Définir la configuration des broches GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_JACK, GPIO.IN)

    # Vérifier si le jack est retiré avant de démarrer le robot
    while not (check_jack_removed()):
        time.sleep(0.1)

    #Seconde a partir de laquelle le robot est partie
    time_lauch = time.time()
    
    ax12_panneau = AX12_Panneau()
    asserv = Asserv('/dev/ttyACM0')
    
    # for i in range(0,2001,500):
    #     asserv.goto(i,0.0)
    #     time.sleep(0.5)
    
    #Bleu
    #1erpanneau
    ax12_panneau.bouger_panneau_droit()
    time.sleep(1)
    ax12_panneau.ramener_AX12_droit()
    time.sleep(1)
    asserv.goto(0.0,500.0)
    time.sleep(0.5)
    asserv.goto(0.0,1000.0)
    time.sleep(0.5)
    asserv.goto(0.0,1500.0)
    # time.sleep(0.5)
    # asserv.goto(0.0,1700.0)
    
    # print("Démarrage du chrono du match")
    
    # while(time_lauch < (time_lauch + MATCH_TIME)):
    #     time.sleep(0.1)
    # print("Fin du chrono ou du match")
        
    return 0


if __name__ == "__main__":
    main()