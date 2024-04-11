
import json
import RPi.GPIO as GPIO
import time



def execute_order(order):
    if order['order'] == 'elevate':
        # Appeler la méthode correspondante de la classe AX12_ascenseur
        AX12_ascenseur.elevate()
    elif order['order'] == 'lower':
        # Appeler la méthode correspondante de la classe AX12_ascenseur
        AX12_ascenseur.lower()
    elif order['order'] == 'lower_for_plant':
        # Appeler la méthode correspondante de la classe AX12_ascenseur
        AX12_ascenseur.lower_for_plant()
    elif order['order'] == 'control':
        # Vérifier si la clé 'actuatorPosition' est présente dans l'ordre
        if 'actuatorPosition' in order:
            # Appeler la méthode correspondante de la classe appropriée avec la position spécifiée
            # Supposons que vous ayez une classe appropriée pour le contrôle, par exemple 'ControlClass'
            ControlClass.control(order['actuatorPosition'])
    else:
        print("Ordre inconnu :", order['order'])

# Parcourir chaque ordre dans la liste et l'exécuter
for order in orders:
    execute_order(order)
import json

def lire_fichier_json(nom_fichier):
    with open(nom_fichier, 'r') as f:
        data = json.load(f)
    return data

# Utilisation de la fonction pour lire un fichier JSON
donnees = lire_fichier_json('Blue1Strategy1.json')
print(donnees) 


#liste de toute les action

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

# Code principal
def main():
    # Vérifier si le jack est retiré avant de démarrer le robot
    if not verifier_jack():
        print("Le jack n'est pas retiré, impossible de démarrer le robot")
        return

    # Démarrer le thread pour arrêter le robot après un certain temps
    arret_thread = threading.Thread(target=arreter_apres_temps)
    arret_thread.start()

    # Lire et exécuter les actions à partir du fichier JSON
    lire_et_executer_actions()

if __name__ == "__main__":
    main()
