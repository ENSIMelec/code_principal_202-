import math
import pygame
from Asserv import Asserv
from AX12 import AX12_Ascenseur, AX12_Pince, AX12_Panneau
pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True

asserv = Asserv()

ascenceur = AX12_Ascenseur()
ascenceur_bas = True

pince = AX12_Pince()
pince_ouverte = True
pince_en_fermeture = False

panneau = AX12_Panneau()
panneau_ouvert_droit = False
panneau_ouvert_gauche = False

def joystick_to_pwm(x, y):
    """ Convertit les valeurs du joystick (x, y) en deux valeurs PWM (gauche, droite) entre -255 et 255 """
    pwm_max = 255
    if y > 0:
        x = -x
    pwm_gauche = int((x - y) * pwm_max)
    pwm_droit = int((-y - x) * pwm_max)
    
    # Limiter les valeurs de PWM à l'intervalle [-255, 255]
    pwm_gauche = max(min(pwm_gauche, pwm_max), -pwm_max)
    pwm_droit = max(min(pwm_droit, pwm_max), -pwm_max)
    
    return pwm_gauche, pwm_droit

def joystick_to_radians(x, y):
    """ Convertit les valeurs du joystick (x, y) en radians """
    angle_radians = math.atan2(x, -y)  # On utilise -y pour correspondre à l'orientation du joystick
    return angle_radians

def gachette_to_pwm(x,signe):
    """ Convertit les valeurs de la gachette (x) en pwm """
    pwm_max = 255
    pwm = (x+1)/2 * pwm_max * signe
    return pwm

# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize the appended joystick (-1 means last array item)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print ("Detected joystick "),joysticks[-1].get_name(),"'"
while keepPlaying:
    clock.tick(60)
    for event in pygame.event.get():
        # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                print ("A")
                if pince_ouverte and not pince_en_fermeture:
                    pince.close_pince()
                    pince_ouverte = False
                    pince_en_fermeture = True
                elif not pince_ouverte and pince_en_fermeture:
                    pince.close_pince(1024)
                    pince_ouverte = False
                    pince_en_fermeture = False
                elif not pince_ouverte and not pince_en_fermeture:
                    pince.open_pince()
                    pince_ouverte = True
                    pince_en_fermeture = False
            elif event.button == 1:
                print ("B")
                if ascenceur_bas:
                    ascenceur.elevate()
                else :
                    ascenceur.lower()
                ascenceur_bas = not ascenceur_bas
            elif event.button == 2:
                print ("X")
            elif event.button == 3:
                print ("Y")
            elif event.button == 4:
                print ("double carré (au milieu)")
            elif event.button == 5:
                print ("bouton xbox")
            elif event.button == 6:
                print ("bouton menu je pense")
            elif event.button == 7:
                print ("Joystick gauche pressed")
            elif event.button == 8:
                print ("Joystick droit pressed")
            elif event.button == 9:
                print ("LB")
                if panneau_ouvert_gauche:
                    panneau.ramener_AX12_gauche()
                else :
                    panneau.bouger_panneau_gauche()
                panneau_ouvert_gauche = not panneau_ouvert_gauche
            elif event.button == 10:
                print ("RB")
                if panneau_ouvert_droit:
                    panneau.ramener_AX12_droit()
                else :
                    panneau.bouger_panneau_droit()
                panneau_ouvert_droit = not panneau_ouvert_droit
            elif event.button == 11:
                print ("haut")
                asserv.rotate(0)
            elif event.button == 12:
                print ("bas")
                asserv.rotate(-PI)
            elif event.button == 13:
                print ("gauche")
                asserv.rotate(-PI/2)
            elif event.button == 14:
                print ("droite")
                asserv.rotate(PI/2)
            elif event.button == 15:
                print ("bouton partage je pense")

        if event.type == pygame.JOYAXISMOTION:
            # left stick
            if event.axis in [0, 1]:  # Axe X ou Y du joystick gauche
                # On récupère les valeurs de l'axe X (event.axis == 0) et Y (event.axis == 1)
                value_x = joysticks[0].get_axis(0)
                value_y = joysticks[0].get_axis(1)
                if abs(value_x) > 0.50 or abs(value_y) > 0.50:
                    # On affiche les valeurs
                    print(f"Joystick gauche X: {value_x:.2f}, Y: {value_y:.2f}") # Conversion en PWM
                    # Conversion en radians
                    angle_radians = joystick_to_radians(value_x, value_y)
                    
                    print(f"Angle en radians: {angle_radians:.4f}")

            # right stick
            if event.axis in [2, 3]:  # Axe X ou Y du joystick gauche
                # On récupère les valeurs de l'axe X (event.axis == 0) et Y (event.axis == 1)
                value_x1 = joysticks[0].get_axis(2)
                value_y1 = joysticks[0].get_axis(3)
                # On affiche les valeurs
                print(f"Joystick droit X: {value_x1:.2f}, Y: {value_y1:.2f}")
                pwm_gauche, pwm_droit = joystick_to_pwm(value_x1, value_y1)
                
                print(f"Valeur PWM moteur gauche: {pwm_gauche}, moteur droit: {pwm_droit}")
                

            if event.axis == 4:
                value_left = joysticks[0].get_axis(4)
                print(f"gachette gauche {value_left:.2f}")
                pwm = gachette_to_pwm(value_left,-1)
                print(f"Valeur PWM: {pwm:.0f}")
            if event.axis == 5:
                value_right = joysticks[0].get_axis(5)
                print(f"gachette droite {value_right:.2f}")
                pwm = gachette_to_pwm(value_right,1)
                print(f"Valeur PWM: {pwm:.0f}")