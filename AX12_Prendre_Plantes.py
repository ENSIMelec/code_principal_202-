import time
from AX12_Pinces import AX12_Pinces
from AX12_Ascenseur import AX12_Ascenseur
from Asserv import Asserv


def prendre_plante():
    # Initialisation des instances des classes AX12_Pinces et AX12_Ascenseur
    ax12_pinces = AX12_Pinces()
    ax12_ascenseur = AX12_Ascenseur()
    asserv = Asserv('/dev/ttyACM1')
    
    asserv.goto(300.0,0.0)
    # Ouvrir la pince pour prendre les plantes
    ax12_pinces.open_pince()
    
    # Fermer la pince pour prendre les plantes
    ax12_pinces.close_pince()

    # Monter l'ascenseur
    ax12_ascenseur.elevate()
    
    asserv.goto(300.0,0.0)

    # Descendre l'ascenseur
    ax12_ascenseur.lower_for_plant()

    # Ouvrir à nouveau la pince pour déposer les plantes
    ax12_pinces.open_pince_stepbystep()
    
    # Monter l'ascenseur
    ax12_ascenseur.elevate()
    #reculer
    asserv.goto(300.0,0.0)

    # Fermer la pince à nouveau
    ax12_pinces.close_pince()
    
    #retour zone
    asserv.goto(300.0,0.0)


if __name__ == "__main__":
    # Prendre les plantes
    prendre_plante()

