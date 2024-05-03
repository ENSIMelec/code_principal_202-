import math
from adafruit_rplidar import RPLidar
from serial import SerialException
from Globals_Variables import *
import logging
import logging.config
import time
from Asserv import Asserv

       
class LidarScanner:
    def __init__(self): 
        
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH)

        # Créer un logger
        self.logger = logging.getLogger("Lidarscan")

        self.port_name = LIDAR_SERIAL
        self.deadzone_distance = 500
        self.lidar = RPLidar(None, self.port_name, timeout=5)
        self.detection = False
        self.logger.info("Lidar initialized.")
        

    def set_pwm(self, value):
        self.logger.info(f"Setting PWM value to {value}")
        self.lidar.set_pwm(value)

    def scan(self):
        self.set_pwm(512)
        try:
            for scan in self.lidar.iter_scans():
                for (quality, angle, distance) in scan:
                    angle_radians = angle * (math.pi / 180)
                    # Calculate x-coordinate and y-coordinate based on distance and angle
                    x_coordinate = (distance + ORIGIN_LIDAR) * math.cos(angle_radians) * self.asserv.signeLidar
                    y_coordinate = (distance + ORIGIN_LIDAR) * math.sin(angle_radians)
                    
                    if (-200 <= y_coordinate <= 200) and (50 < x_coordinate < 650) and (quality > 10): # Filtering by deadzone distance
                        self.logger.info(f"Object detected in the deadzone at {distance} mm (x)! {angle}°. {quality}")
                        if not self.detection:
                            self.logger.warning(f"Stopping the robot. Object at {x_coordinate} mm (x) and {angle}°")
                            self.asserv.stopmove()
                        self.detection = True
                        self.time_detect = time.time()
                            
                    elif (self.detection) and (time.time() - self.time_detect) > 0.5 :
                        self.logger.info("No more object. Restarting the robot.")
                        self.asserv.restartmove()
                        self.detection = False  

        except KeyboardInterrupt:
            self.logger.warning("Stopping the lidar scan. (KeyboardInterrupt)")
            self.stop_lidarScan()

    def stop_lidarScan(self):
        self.logger.info("Stopping the lidar scan.")
        self.lidar.stop_motor()
        self.lidar.disconnect()
        
    def set_asserv_obj(self, obj):
        self.asserv = obj

if __name__ == '__main__':
    # Setup the RPLidar
    lidar_scanner = LidarScanner()
    lidar_scanner.scan()
    lidar_scanner.stop_lidarScan()

