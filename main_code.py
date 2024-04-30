import importlib
import json
import RPi.GPIO as GPIO
import time
import threading
from LidarScan import LidarScanner
from Globals_Variables import *

import logging
import logging.config


# Fonction pour lire et traiter le JSON
def init_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    # Importer les modules d'initialisation
    
    # Importer le module
    dic_class = {}
    for module_name in data['initialisation']:
        if module_name.startswith('AX12'):
            module = importlib.import_module('AX12_Python.' + module_name)
        else:
            module = importlib.import_module(module_name)
        logger.info(f"Initialisation de {module}")
        dic_class[module_name] = getattr(module, module_name)()
    return dic_class, data

def actions(dic_class, actions):
    for action in actions:
        logger.debug(f"Action {action['methode']} de la classe {action['classe']} avec les arguments {action['arguments']}")
        while not( getattr(dic_class[action['classe']], action['methode'])(*action['arguments']) ):
            time.sleep(0.1)

# Fonction pour vérifier si le jack a été retiré
def check_jack_removed():
    # Lire l'état de la broche GPIO connectée au pin jack
    jack_state = GPIO.input(PIN_JACK)
    # Si l'état du jack est bas (0), cela signifie qu'il a été retiré
    if jack_state == GPIO.HIGH:
        logger.info("Jack retiré")
        return True
    else:
        logger.debug("Jack non retiré")
        return False

# Code principal avec conditions sur l'arret en fonction d'obstacle
def main():
    # Définir la configuration des broches GPIO
    GPIO.setmode(GPIO.BCM)
    logger.info("Initialisation broche GPIO Jack")
    GPIO.setup(PIN_JACK, GPIO.IN)

    # Initialisation avec le JSON
    logger.info("Initialisation du JSON")
    dic_class, data = init_json("StrategieBleu.json")

    logger.info("Initialisation du Lidar")
    lidar_scanner = LidarScanner()
    logger.info("Don de asserv à Lidar")
    lidar_scanner.set_asserv_obj(dic_class['Asserv'])
     
    
    # Vérifier si le jack est retiré avant de démarrer le robot
    logger.info("Wainting for jack removal...")
    while not (check_jack_removed()):
        time.sleep(0.1)

    #Seconde a partir de laquelle le robot est partie
    time_lauch = time.time()
    logger.info(f"Démarrage du robot à {time_lauch} secondes")
   
    #Réalisation des actions dans un thread deamon et démarrer le scanner Lidar dans un thread séparé
    thread_action = threading.Thread(target=actions, args=(dic_class, data['actions']))
    thread_action.daemon = True
    
    lidar_thread = threading.Thread(target=lidar_scanner.scan)
    lidar_thread.daemon = True

    logger.info("Démarrage du thread de scanner Lidar")
    lidar_thread.start()
    time.sleep(0.5)
    logger.info("Démarrage du thread d'actions")
    thread_action.start()
    
    logger.info("Démarrage du chrono")
    
    while(time.time() < (time_lauch + MATCH_TIME) and thread_action.is_alive()):
        time.sleep(0.1)
    logger.info("Fin du match ou chrono")
 
    time.sleep(1)
    logger.info("Arrêt du scanner Lidar")
    lidar_scanner.stop_lidarScan()
        
    return 0


if __name__ == "__main__":
    # Charger la configuration de logging
    logging.config.fileConfig('logs.conf')

    # Créer un logger
    logger = logging.getLogger(__name__)
    main()