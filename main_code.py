
import json
"""
import threading
import time

# Fonction pour exécuter une action
def executer_action(action, parametres):
    if action == "avancer":
        print("Action : Avancer avec distance =", parametres.get("distance", 0), "et vitesse =", parametres.get("vitesse", 0))
    elif action == "reculer":
        print("Action : Reculer avec distance =", parametres.get("distance", 0), "et vitesse =", parametres.get("vitesse", 0))
    elif action == "rotation":
        print("Action : Rotation de", parametres.get("angle", 0), "degrés")
    elif action == "actionneur":
        print("Action : Actionneur avec position =", parametres.get("position", 0))
    elif action == "ascenseur_descend":
        print("Action : Descendre l'ascenseur")
    elif action == "ascenseur_monte":
        print("Action : Monter l'ascenseur")
    elif action == "pince_fermeture":
        print("Action : Fermer la pince")
    elif action == "pince_ouverture":
        print("Action : Ouvrir la pince")
    else:
        print("Action non reconnue")
"""
import json

def lire_fichier_json(nom_fichier):
    with open(nom_fichier, 'r') as f:
        data = json.load(f)
    return data

# Utilisation de la fonction pour lire un fichier JSON
donnees = lire_fichier_json('Blue1Strategy1.json')
print(donnees) 

"""
# Fonction pour vérifier si le jack est retiré
def verifier_jack():
    print("Vérification si le jack est retiré")
    time.sleep(2)  # Simulation de la vérification
    return True  # Supposons que le jack est retiré

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
"""