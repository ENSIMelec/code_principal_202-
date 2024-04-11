import importlib
import json
import RPi.GPIO as GPIO
import time
import threading
# Numéro de broche GPIO connecté au pin jack 33
PIN_JACK = 33
MATCH_TIME = 100


# Fonction pour lire et traiter le JSON
def init_json(json_file):
    with open(json_file) as f:
        data = json.load(f)
    # Importer les modules d'initialisation
    
        # Importer le module
    dic_class = {}
    for module_name in data['initialisation']:
        module=importlib.import_module(module_name)
        dic_class[module_name] = getattr(module, module_name)
    return dic_class,data

def actions(dic_class, actions):
    for action in actions:
        action['arguments'].insert(0,dic_class[action['classe']]) 
        while not( getattr(dic_class[action['classe']], action['methode'])(*action['arguments']) ):
            time.sleep(0.1)






# Fonction pour vérifier si le jack a été retiré
def check_jack_removed():
        # Lire l'état de la broche GPIO connectée au pin jack
        jack_state = GPIO.input(PIN_JACK)
        # Si l'état du jack est bas (0), cela signifie qu'il a été retiré
        if jack_state == GPIO.LOW:
            print("Le jack a été retiré.")
            return True
        else:
            print("En attente du retrait du jack...")
            return False

# Fonction pour arrêter le robot après un certain temps
def arreter_apres_temps():
    print("Démarrage du chrono du match")
    time.sleep(MATCH_TIME)  # Simulation du temps de match
    print("Fin du match, arrêt du robot")


# Code principal
def main():
    #definition GPIO entrée
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_JACK, GPIO.IN)

    # Initialisation avec le Json
    dic_class,data = init_json("exemple.json")

    # Vérifier si le jack est retiré avant de démarrer le robot
    while(not(check_jack_removed())):
        time.sleep(0.1)

    #Seconde a partir de laquelle le robot est partie
    time_lauch = time.time()
   
    #Réalisation des actions dans un thread deamon
    thread_action = threading.Thread(target=actions, args=(dic_class, data['actions']))
    thread_action.setDaemon(True)
    thread_action.start()

    print("Démarrage du chrono du match")
    
    while(time_lauch < (time_lauch + MATCH_TIME) and thread_action.is_alive()):
        time.sleep(0.1)
    print("Fin du chrono ou du match")
    return 0

    
main()


