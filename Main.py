import importlib
import json
import RPi.GPIO as GPIO
import time
import threading
import logging
import logging.config
import signal
import sys
from LidarScan import LidarScanner
from InterfaceGraphique2024.INTERFACE.Interface import *
from Globals_Variables import *

class MainCode:
    def __init__(self, json_path="/home/pi/code_principal_2024/Stratégies/StrategieBleuGoTo.json", app=None):
        self.app = app
        self.json_path = json_path
        logging.config.fileConfig(LOGS_CONF_PATH)
        self.logger = logging.getLogger("main_code")
        self.running = False
        self.thread_action = None
        self.lidar_scanner = None
        self.dic_class = {}
        self.data = None

        self.logger.info("Main Code initialized.")

    def init_json(self):
        if self.app == None :
            self.logger.info("Initialisation du JSON...")
            with open(self.json_path) as f:
                self.data = json.load(f)
            self.dic_class = {}
            for module_name in self.data['initialisation']:
                if module_name.startswith('AX12'):
                    module = importlib.import_module('AX12_Python.' + module_name)
                else:
                    module = importlib.import_module(module_name)
                self.logger.info(f"Initialisation de {module}")
                self.dic_class[module_name] = getattr(module, module_name)()
            self.logger.info("JSON initialisé.")
            return True
        else :
            self.logger.info("Initialisation du JSON...")
            with open(self.json_path) as f:
                self.data = json.load(f)
            self.dic_class = {}
            for module_name in self.data['initialisation']:
                if module_name.startswith('AX12'):
                    module = importlib.import_module('AX12_Python.' + module_name)
                else:
                    module = importlib.import_module(module_name)
                self.logger.info(f"Initialisation de {module}")
                self.dic_class[module_name] = getattr(module, module_name)(app=self.app)
            self.logger.info("JSON initialisé.")
            return True

    def actions(self):
        if self.app == None :
            for action in self.data['actions']:
                self.logger.debug(f"Action {action['methode']} de la classe {action['classe']} avec les arguments {action['arguments']}")
                while not(getattr(self.dic_class[action['classe']], action['methode'])(*action['arguments'])):
                    time.sleep(0.1)
        else :
            for action in self.data['actions']:
                self.logger.debug(f"Action {action['methode']} de la classe {action['classe']} avec les arguments {action['arguments']}")
                while not(getattr(self.dic_class[action['classe']], action['methode'])(*action['arguments'])):
                    time.sleep(0.1)

    def check_jack_removed(self):
        if self.app == None :
            jack_state = GPIO.input(PIN_JACK)
            if jack_state == GPIO.HIGH:
                self.logger.info("Jack retiré")
                return True
            else:
                self.logger.debug("Jack non retiré")
                return False
        else :
            jack_state = GPIO.input(PIN_JACK)
            if jack_state == GPIO.HIGH:
                self.logger.info("Jack retiré")
                return True
            else:
                self.logger.debug("Jack non retiré")
                return False

    def signal_handler(self, sig, frame):
        # Arrêter les moteurs
        self.logger.warning("Vous avez appuyé sur Ctrl+C !")
        self.stop()
        sys.exit(0)

    def stop(self):
        if self.app == None :
            self.running = False
            self.logger.info("Arrêt des moteurs")
            self.dic_class['Asserv'].stopmove()
            # Arrêter le scanner Lidar
            self.logger.info("Arrêt du scanner Lidar")
            self.lidar_scanner.stop_lidarScan()
            # self.logger.info("Arrêt du thread Action")
            # if self.thread_action and self.thread_action.is_alive():
            #     self.thread_action.join()
        else :
            self.running = False
            self.logger.info("Arrêt des moteurs")
            self.dic_class['Asserv'].stopmove()
            # Arrêter le scanner Lidar
            self.logger.info("Arrêt du scanner Lidar")
            self.lidar_scanner.stop_lidarScan()
            # self.logger.info("Arrêt du thread Action")
            # if self.thread_action and self.thread_action.is_alive():
            #     self.thread_action.join()


    def run(self):
        if self.app == None :
            self.running = True
            GPIO.setmode(GPIO.BCM)
            self.logger.info("Initialisation broche GPIO Jack")
            GPIO.setup(PIN_JACK, GPIO.IN)

            self.init_json()

            self.logger.info("Initialisation du Lidar")
            self.lidar_scanner = LidarScanner()
            self.logger.info("Don de asserv à Lidar")
            self.lidar_scanner.set_asserv_obj(self.dic_class['Asserv'])

            signal.signal(signal.SIGINT, lambda sig, frame: self.signal_handler(sig,frame))
            signal.signal(signal.SIGTERM, lambda sig, frame: self.signal_handler(sig,frame))

            self.logger.info("Waiting for jack removal...")
            while not self.check_jack_removed():
                time.sleep(0.1)

            time_launch = time.time()
            self.logger.info(f"Démarrage du robot à {time_launch} secondes")

            self.thread_action = threading.Thread(target=self.actions)
            self.thread_action.daemon = True
            lidar_thread = threading.Thread(target=self.lidar_scanner.scan)
            lidar_thread.daemon = True

            self.logger.info("Démarrage du thread de scanner Lidar")
            lidar_thread.start()
            time.sleep(0.5)
            self.logger.info("Démarrage du thread d'actions")
            self.thread_action.start()

            self.logger.info("Démarrage du chrono")

            while time.time() < (time_launch + MATCH_TIME) and self.thread_action.is_alive():
                self.logger.debug(f"Match en cours... (T = {time.time()})")
                time.sleep(0.1)

            self.logger.info("Fin du match ou chrono")

            time.sleep(1)
            self.stop()
        else :
            self.running = True
            GPIO.setmode(GPIO.BCM)
            self.logger.info("Initialisation broche GPIO Jack")
            GPIO.setup(PIN_JACK, GPIO.IN)

            self.init_json()

            self.logger.info("Initialisation du Lidar")
            self.lidar_scanner = LidarScanner(self.app)
            self.logger.info("Don de asserv à Lidar")
            self.lidar_scanner.set_asserv_obj(self.dic_class['Asserv'])

            signal.signal(signal.SIGINT, lambda sig, frame: self.signal_handler(sig,frame))
            signal.signal(signal.SIGTERM, lambda sig, frame: self.signal_handler(sig,frame))

            self.logger.info("Waiting for jack removal...")
            self.app.waiting_jack()
            while not self.check_jack_removed():
                time.sleep(0.1)
            self.app.jack_retired()

            time_launch = time.time()
            self.logger.info(f"Démarrage du robot à {time_launch} secondes")

            self.thread_action = threading.Thread(target=self.actions)
            self.thread_action.daemon = True
            lidar_thread = threading.Thread(target=self.lidar_scanner.scan)
            lidar_thread.daemon = True

            self.logger.info("Démarrage du thread de scanner Lidar")
            lidar_thread.start()
            time.sleep(0.5)
            self.logger.info("Démarrage du thread d'actions")
            self.thread_action.start()

            self.logger.info("Démarrage du chrono")

            while time.time() < (time_launch + MATCH_TIME) and self.thread_action.is_alive():
                self.logger.debug(f"Match en cours... (T = {time.time()})")
                time.sleep(0.1)

            self.logger.info("Fin du match ou chrono")

            time.sleep(1)
            self.stop()

# Utilisation exemple
if __name__ == "__main__":
    main_code = MainCode("/home/pi/code_principal_2024/Stratégies/StrategieBleuGoTo.json")
    main_code.run()
