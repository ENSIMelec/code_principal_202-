import importlib
import json
import RPi.GPIO as GPIO
import time
import threading
from Lidar import LidarScanner
from Globals_Variables import *


# Fonction pour lire et traiter le JSON
def init_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    # Importer les modules d'initialisation
    
        # Importer le module
    dic_class = {}
    for module_name in data['initialisation']:
        module=importlib.import_module(module_name)
        dic_class[module_name] = getattr(module, module_name)()
    return dic_class,data

def actions(dic_class, actions):
    for action in actions:
        #action['arguments'].insert(0,dic_class[action['classe']]) 
        while not( getattr(dic_class[action['classe']], action['methode'])(*action['arguments']) ):
            time.sleep(0.1)

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

# def lidar_callback():
#     global thread_action
#     global dic_class
#     global data
    
#     print("Message reçu du Lidar. Arrêt des actions en cours...")

#     thread_action.cancel()
    
#     time.sleep(3)
#     thread_action = threading.Thread(target=actions, args=(dic_class, data['actions']))
#     thread_action.start()
#     print("Actions reprises.")

# Code principal avec conditions sur l'arret en fonction d'obsatcle
def main():
    # Définir la configuration des broches GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_JACK, GPIO.IN)

    # Initialisation avec le JSON
    dic_class, data = init_json("Documents/Codes/code_principal_2024/StrategieBleu_droit.json")

    # Vérifier si le jack est retiré avant de démarrer le robot
    while not (check_jack_removed()):
        time.sleep(0.1)


    #Seconde a partir de laquelle le robot est partie
    time_lauch = time.time()
   
    #Réalisation des actions dans un thread deamon et démarrer le scanner Lidar dans un thread séparé
    lidar_scanner = LidarScanner()
    thread_action = threading.Thread(target=actions, args=(dic_class, data['actions']))
    thread_action.daemon = True
    
    lidar_thread = threading.Thread(target=lidar_scanner.scan)
    lidar_thread.daemon = True

    lidar_thread.start()
    time.sleep(0.5)
    thread_action.start()
    
    print("Démarrage du chrono du match")
    
    while(time_lauch < (time_lauch + MATCH_TIME) and thread_action.is_alive()):
        time.sleep(0.1)
    print("Fin du chrono ou du match")
    
    set_stop_lidar = True
    time.sleep(1)
    lidar_scanner.stop_lidarScan()
        
    return 0


if __name__ == "__main__":
    main()