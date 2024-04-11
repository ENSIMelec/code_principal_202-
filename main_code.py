import importlib
import json
import AX12_Pinces

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
            continue





"""
import RPi.GPIO as GPIO
# Numéro de broche GPIO connecté au pin jack 33
PIN_JACK = 33

# Configuration de la broche GPIO en mode d'entrée
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_JACK, GPIO.IN)

# Fonction pour vérifier si le jack a été retiré
def check_jack_removed():
    while True:
        # Lire l'état de la broche GPIO connectée au pin jack
        jack_state = GPIO.input(PIN_JACK)
        # Si l'état du jack est bas (0), cela signifie qu'il a été retiré
        if jack_state == GPIO.LOW:
            print("Le jack a été retiré.")
            return True
        else:
            print("En attente du retrait du jack...")
        time.sleep(1)
    return False

# Fonction pour arrêter le robot après un certain temps
def arreter_apres_temps():
    print("Démarrage du chrono du match")
    time.sleep(10)  # Simulation du temps de match
    print("Fin du match, arrêt du robot")
"""
# Code principal
def main():
    # Initialisation avec le Json
    dic_class,data = init_json("exemple.json")

    # Vérifier si le jack est retiré avant de démarrer le robot
    # check_jack_removed()

    # # Démarrer le thread pour arrêter le robot après un certain temps
    # arret_thread = threading.Thread(target=arreter_apres_temps)
    # arret_thread.start()
   
    #Réalisation des actions 
    actions(dic_class, data['actions'])

    


if __name__ == "__main__":
    main()


