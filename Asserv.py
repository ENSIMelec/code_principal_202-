import serial
import threading
from Globals_Variables import STM32_SERIAL

class Asserv:
    def __init__(self, port=STM32_SERIAL, baudrate=115200, buffer_size=1024):
        self.started = False
        self.buffer_size = buffer_size
        self.encGauche = [None] * buffer_size
        self.index_encGauche = 0
        self.encDroit = [None] * buffer_size
        self.index_encDroit = 0
        self.vitesse_G = [None] * buffer_size
        self.index_vitesse_G = 0
        self.vitesse_D = [None] * buffer_size
        self.index_vitesse_D = 0
        self.Output_PID_vitesse_G = [None] * buffer_size
        self.index_Output_PID_vitesse_G = 0
        self.Output_PID_vitesse_D = [None] * buffer_size
        self.index_Output_PID_vitesse_D = 0
        self.cmd_vitesse_G = [None] * buffer_size
        self.index_cmd_vitesse_G = 0
        self.cmd_vitesse_D = [None] * buffer_size
        self.index_cmd_vitesse_D = 0
        self.angle = [None] * buffer_size
        self.index_angle = 0
        self.Output_PID_angle = [None] * buffer_size
        self.index_Output_PID_angle = 0
        self.cmd_angle = [None] * buffer_size
        self.index_cmd_angle = 0
        self.distance = [None] * buffer_size
        self.index_distance = 0
        self.Output_PID_distance = [None] * buffer_size
        self.index_Output_PID_distance = 0
        self.cmd_distance = [None] * buffer_size
        self.index_cmd_distance = 0
        self.angle_ok = False
        self.distance_ok = False
        self.x = [None] * buffer_size
        self.index_x = 0
        self.y = [None] * buffer_size
        self.index_y = 0
        self.serial = serial.Serial(port, baudrate)
        self.thread = threading.Thread(target=self.receive_data)
        self.thread.daemon = True
        self.thread.start()
    
    def enable(self): # enable de tout l'asservissement
        command = "asserv enable all\n"
        self.serial.write(command.encode())
        return True
    
    def disable(self): # disable de tout l'asservissement
        command = "asserv disable all\n"
        self.serial.write(command.encode())
        return True

    def reset(self): # reset de tout l'asservissement
        command = "asserv reset all\n"
        self.serial.write(command.encode())
        return True

    def angle_enable(self): # enable de l'asservissement d'angle seulement
        command = "asserv enable angle\n"
        self.serial.write(command.encode())
        return True
    
    def angle_disable(self): # disable de l'asservissement d'angle seulement
        command = "asserv disable angle\n"
        self.serial.write(command.encode())
        return True

    def angle_reset(self): # reset de l'angle
        command = "asserv reset angle\n"
        self.serial.write(command.encode())
        return True

    def dist_enable(self): # enable de l'asservissement de distance seulement
        command = "asserv enable distance\n"
        self.serial.write(command.encode())
        return True
    
    def dist_disable(self): # disable de l'asservissement de distance seulement
        command = "asserv disable distance\n"
        self.serial.write(command.encode())
        return True
    
    def dist_reset(self): # reset de la distance
        command = "asserv reset distance\n"
        self.serial.write(command.encode())
        return True

    def vitesse_droit_enable(self): # enable de l'asservissement vitesse droit seulement
        command = "asserv enable vitesse droit\n"
        self.serial.write(command.encode())
        return True
    
    def vitesse_droit_disable(self): # disable de l'asservissement vitesse droit seulement
        command = "asserv disable vitesse droit\n"
        self.serial.write(command.encode())
        return True

    def vitesse_droit_reset(self): # reset de l'asservissement vitesse droit seulement
        command = "asserv reset vitesse droit\n"
        self.serial.write(command.encode())
        return True

    def vitesse_gauche_enable(self): # enable de l'asservissement vitesse gauche seulement
        command = "asserv enable vitesse gauche\n"
        self.serial.write(command.encode())
        return True
    
    def vitesse_gauche_disable(self): # disable de l'asservissement vitesse gauche seulement
        command = "asserv disable vitesse gauche\n"
        self.serial.write(command.encode())
        return True

    def vitesse_gauche_reset(self): # reset de l'asservissement vitesse gauche seulement
        command = "asserv reset vitesse gauche\n"
        self.serial.write(command.encode())
        return True
    
    def goto(self, x, y): # simple goto x et y en mm
        command = f'asserv goto {x} {y}\n'
        self.serial.write(command.encode())
        while (not self.distance_ok):
            continue
        return True
    
    def rotate(self, angle): # simple rotation de l'angle en degrée
        command = f"asserv rotate {angle}\n"
        self.serial.write(command.encode())
        while (not self.angle_ok):
            continue
        return True
    
    def receive_data(self):
        while True:
            try :
                data = self.serial.readline().decode().strip()
                #print(data)
                if not self.started and data[0] != 'A':
                    continue
                else:
                    self.started = True
                if self.started :
                    if data.startswith("A"): # Valeur du codeur Gauche
                        x = data[1:]
                        self.encGauche[self.index_encGauche] = int(x)
                        self.index_encGauche = (self.index_encGauche + 1) % self.buffer_size
                    elif data.startswith("B"): # Valeur du codeur Droit
                        x = data[1:]
                        self.encDroit[self.index_encDroit] = int(x)
                        self.index_encDroit = (self.index_encDroit + 1) % self.buffer_size
                    elif data.startswith("C"): # Vitesse réel moteur Gauche
                        x = data[1:]
                        self.vitesse_G[self.index_vitesse_G] = float(x)
                        self.index_vitesse_G = (self.index_vitesse_G + 1) % self.buffer_size
                    elif data.startswith("D"): # Vitesse réel moteur Droit
                        x = data[1:]
                        self.vitesse_D[self.index_vitesse_D] = float(x)
                        self.index_vitesse_D = (self.index_vitesse_D + 1) % self.buffer_size
                    elif data.startswith("E"): # Sortie du PID vitesse moteur Gauche
                        x = data[1:]
                        self.Output_PID_vitesse_G[self.index_Output_PID_vitesse_G] = float(x)
                        self.index_Output_PID_vitesse_G = (self.index_Output_PID_vitesse_G + 1) % self.buffer_size
                    elif data.startswith("F"): # Sortie du PID vitesse moteur Droit
                        x = data[1:]
                        self.Output_PID_vitesse_D[self.index_Output_PID_vitesse_D] = float(x)
                        self.index_Output_PID_vitesse_D = (self.index_Output_PID_vitesse_D + 1) % self.buffer_size
                    elif data.startswith("G"): # Consigne de vitesse moteur Gauche
                        x = data[1:]
                        self.cmd_vitesse_G[self.index_cmd_vitesse_G] = float(x)
                        self.index_cmd_vitesse_G = (self.index_cmd_vitesse_G + 1) % self.buffer_size
                    elif data.startswith("H"): # Consigne de vitesse moteur Droit
                        x = data[1:]
                        self.cmd_vitesse_D[self.index_cmd_vitesse_D] = float(x)
                        self.index_cmd_vitesse_D = (self.index_cmd_vitesse_D + 1) % self.buffer_size
                    elif data.startswith("I"): # angle mesurer
                        x = data[1:]
                        self.angle[self.index_angle] = float(x)
                        self.index_angle = (self.index_angle + 1) % self.buffer_size
                    elif data.startswith("J"): # angle PID
                        x = data[1:]
                        self.Output_PID_angle[self.index_Output_PID_angle] = float(x)
                        self.index_Output_PID_angle = (self.index_Output_PID_angle + 1) % self.buffer_size
                    elif data.startswith("K"): # cmd angle
                        x = data[1:]
                        self.cmd_angle[self.index_cmd_angle] = float(x)
                        self.index_cmd_angle = (self.index_cmd_angle + 1) % self.buffer_size
                    elif data.startswith("L"): # distance mesurer
                        x = data[1:]
                        self.distance[self.index_distance] = float(x)
                        self.index_distance = (self.index_distance + 1) % self.buffer_size
                    elif data.startswith("M"): # distance PID
                        x = data[1:]
                        self.Output_PID_distance[self.index_Output_PID_distance] = float(x)
                        self.index_Output_PID_distance = (self.index_Output_PID_distance + 1) % self.buffer_size
                    elif data.startswith("O"): # cmd distance
                        x = data[1:]
                        self.cmd_distance[self.index_cmd_distance] = float(x)
                        self.index_cmd_distance = (self.index_cmd_distance + 1) % self.buffer_size
                    elif data.startswith("P"): # angle ok
                        x = data[1:]
                        self.angle_ok = bool(x)
                    elif data.startswith("Q"): # distance ok 
                        x = data[1:]
                        self.distance_ok = bool(x)
                    elif data.startswith("X"): # position x
                        x = data[1:]
                        self.x[self.index_x] = float(x)
                        self.index_x = (self.index_x + 1) % self.buffer_size
                    elif data.startswith("Y"): # position y
                        x = data[1:]
                        self.y[self.index_y] = float(x)
                        self.index_y = (self.index_y + 1) % self.buffer_size
            except :
                continue

    def get_enc_gauche(self):
        return self.encGauche[self.index_encGauche - 1]

    def get_enc_droit(self):
        return self.encDroit[self.index_encDroit - 1]

    def get_vitesse_g(self):
        return self.vitesse_G[self.index_vitesse_G - 1]

    def get_vitesse_d(self):
        return self.vitesse_D[self.index_vitesse_D - 1]

    def get_output_pid_vitesse_g(self):
        return self.Output_PID_vitesse_G[self.index_Output_PID_vitesse_G - 1]

    def get_output_pid_vitesse_d(self):
        return self.Output_PID_vitesse_D[self.index_Output_PID_vitesse_D - 1]

    def get_cmd_vitesse_g(self):
        return self.cmd_vitesse_G[self.index_cmd_vitesse_G - 1]

    def get_cmd_vitesse_d(self):
        return self.cmd_vitesse_D[self.index_cmd_vitesse_D - 1]

    def get_angle(self):
        return self.angle[self.index_angle - 1]

    def get_output_pid_angle(self):
        return self.Output_PID_angle[self.index_Output_PID_angle - 1]

    def get_cmd_angle(self):
        return self.cmd_angle[self.index_cmd_angle - 1]

    def get_distance(self):
        return self.distance[self.index_distance - 1]

    def get_output_pid_distance(self):
        return self.Output_PID_distance[self.index_Output_PID_distance - 1]

    def get_cmd_distance(self):
        return self.cmd_distance[self.index_cmd_distance - 1]

    def get_x(self):
        return self.x[self.index_x - 1]

    def get_y(self):
        return self.y[self.index_y - 1]

    def is_angle_ok(self):
        return self.angle_ok

    def is_distance_ok(self):
        return self.distance_ok
# 
# /*************************************/
# /*******Envoie des données************/
# /*************************************/
# void sendData()
# {
	# Serial.print("A"); // Valeur du codeur Gauche
	# Serial.println(last_encGauche);
	# Serial.print("B"); // Valeur du codeur Droit
	# Serial.println(last_encDroit);
	# Serial.print("C"); // Vitesse réel moteur Gauche
	# Serial.println(vitesse_G, 5);
	# Serial.print("D"); // Vitesse réel moteur Droit
	# Serial.println(vitesse_D, 5);
	# Serial.print("E"); // Sortie du PID vitesse moteur Gauche
	# Serial.println(Output_PID_vitesse_G, 5);
	# Serial.print("F"); // Sortie du PID vitesse moteur Droit
	# Serial.println(Output_PID_vitesse_D, 5);
	# Serial.print("G"); // Consigne de vitesse moteur Gauche
	# Serial.println(cmd_vitesse_G, 5);
	# Serial.print("H"); // Consigne de vitesse moteur Droit
	# Serial.println(cmd_vitesse_D, 5);
	# Serial.print("I"); // angle mesurer
	# Serial.println(angle, 5);
	# Serial.print("J"); // angle PID
	# Serial.println(Output_PID_angle);
	# Serial.print("K");
	# Serial.println(cmd_angle, 5);
	# Serial.print("L"); // distance mesurer
	# Serial.println(distance, 5);
	# Serial.print("M"); // distance PID
	# Serial.println(Output_PID_distance, 5);
	# Serial.print("O"); // cmd distance
	# Serial.println(cmd_distance, 5);
	# Serial.print("P"); // angle ok
	# Serial.println(angle_ok);
	# Serial.print("Q"); // distance ok
	# Serial.println(distance_ok);
	# Serial.print("X"); // position x
	# Serial.println(x);
	# Serial.print("Y"); // position y
	# Serial.println(y);
# 
	# Update_IT = false;
# }
# /*************************************/
# /*************************************/
# /*************************************/

# //         chprintf(outputStream,"Usage :");
# //         chprintf(outputStream," - asserv wheelcalib \r\n");
# //         chprintf(outputStream," - asserv enablemotor 0|1\r\n");
# //         chprintf(outputStream," - asserv enablepolar 0|1\r\n");
# //         chprintf(outputStream," - asserv coders \r\n");
# //         chprintf(outputStream," - asserv reset \r\n");
# //         chprintf(outputStream," - asserv motorspeed [r|l] speed \r\n");
# //         chprintf(outputStream," -------------- \r\n");
# //         chprintf(outputStream," - asserv wheelspeedstep [r|l] [speed] [steptime] \r\n"); 
# //         chprintf(outputStream," -------------- \r\n");
# //         chprintf(outputStream," - asserv robotfwspeedstep [speed] [step time]\r\n"); 
# //         chprintf(outputStream," - asserv robotangspeedstep [speed][step time] \r\n"); 
# //         chprintf(outputStream," - asserv speedcontrol [r|l] [Kp] [Ki] \r\n"); 
# //         chprintf(outputStream," - asserv angleacc delta_speed \r\n"); 
# //         chprintf(outputStream," - asserv distacc delta_speed \r\n"); 
# //         chprintf(outputStream," -------------------\r\n"); 
# //         chprintf(outputStream," - asserv addangle angle_rad \r\n");
# //         chprintf(outputStream," - asserv anglereset\r\n");
# //         chprintf(outputStream," - asserv anglecontrol Kp\r\n");
# //         chprintf(outputStream," ------------------- \r\n");
# //         chprintf(outputStream," - asserv adddist mm \r\n");
# //         chprintf(outputStream," - asserv distreset\r\n");
# //         chprintf(outputStream," - asserv distcontrol Kp\r\n");
# //         chprintf(outputStream," -------------- \r\n");
# //         chprintf(outputStream," - asserv addgoto X Y\r\n");
# //         chprintf(outputStream," - asserv gototest\r\n");
# //         chprintf(outputStream," -------------- \r\n");
# //         chprintf(outputStream," - asserv pll freq\r\n");

# /*
#   * Commande / Caractères à envoyer sur la série / Paramètres / Effets obtenus

#   g%x#%y\n / Goto / x, y : entiers, en mm /Le robot se déplace au point de
# 	coordonnée (x, y). Il tourne vers le point, puis avance en ligne droite.
# 	L'angle est sans cesse corrigé pour bien viser le point voulu. 

#   e%x#%y\n / goto Enchaîné / x, y : entiers, en mm / Idem que le Goto, sauf que 
#   	lorsque le robot est proche du point d'arrivée (x, y), on s'autorise à 
# 	enchaîner directement la consigne suivante si c'est un Goto ou un Goto
# 	enchaîné, sans marquer d'arrêt.

#   v%d\n / aVancer / d : entier, en mm / Fait avancer le robot de d mm, tout
#   	droit 

#   t%a\n / Tourner / a : entier, en degrées / Fait tourner le robot de a degrées.
#   	Le robot tournera dans le sens trigonométrique : si a est positif, il tourne
# 	à gauche, et vice-versa. 

#   f%x#%y\n / faire Face / x, y : entiers, en mm / Fait tourner le robot pour être
# 	en face du point de coordonnées (x, y). En gros, ça réalise la première partie
# 	d'un Goto : on se tourne vers le point cible, mais on avance pas. 

#   h / Halte ! / Arrêt d'urgence ! Le robot est ensuite systématiquement asservi à
#   	sa position actuelle. Cela devrait suffire à arrêter le robot correctement. La
# 	seule commande acceptée par la suite sera un Reset de l'arrêt d'urgence : toute
# 	autre commande sera ignorée. 

#   r / Reset de l'arrêt d'urgence / Remet le robot dans son fonctionnement normal 
#   	après un arrêt d'urgence. Les commandes en cours au moment de l'arrêt d'urgence 
# 	NE sont PAS reprises. Si le robot n'est pas en arrêt d'urgence, cette commande 
# 	n'a aucun effet.

#   p / get Position / Récupère la position et le cap du robot sur la connexion i2c, 
#   	sous la forme de 3 types float (3 * 4 bytes), avec x, y, et a les coordonnées et
# 	l'angle du robot. S%x#%y#%a\n / set Position / applique la nouvelle position du robot

#   z / avance de 20 cm
#   s / recule de 20 cm
#   q / tourne de 45° (gauche)
#   d / tourne de -45° (droite)

#   M / modifie la valeur d'un paramètre / name, value
#   R / réinitialiser l'asserv
#   D / dump la config du robot
#   G / lire la valeur d'un paramètre / name
#   L / recharge la config config.txt
#   W / sauvegarde la config courante  config~1.txt = config.default.txt

#   I / Active les actions dans la boucle d'asservissement (odo + managers)
#   ! / Stoppe actions dans la boucle d'asservissement
#   K / desactive le consignController et le commandManager
#   J / reactive le consignController et le commandManager

#   + / applique une valeur +1 sur les moteurs LEFT
#   - / applique une valeur -1 sur les moteurs LEFT
#   */