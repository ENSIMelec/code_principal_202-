import serial
import threading

class Asserv:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200, buffer_size=1024):
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
    
    def goto(self, x, y):
        command = f'asserv goto {x} {y}\n'
        self.serial.write(command.encode())
        while (not self.distance_ok):
            continue
        return True
    
    def rotate(self, angle):
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