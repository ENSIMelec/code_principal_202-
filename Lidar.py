import math
from adafruit_rplidar import RPLidar
from serial import SerialException
from Globals_Variables import *
import logging
import logging.config

       
class LidarScanner:
    def __init__(self): 
        
        # Charger la configuration de logging
        logging.config.fileConfig('logs.conf')

        # Créer un logger
        self.logger = logging.getLogger(__name__)

        self.port_name = LIDAR_SERIAL
        self.max_distance = 700
        self.deadzone_distance = 500
        self.lidar = RPLidar(None, self.port_name, timeout=5)
        self.alert_triggered = False
        self.alert_counter = 0
        self.alert_limit = 1 #le lidar met 0.6sec/tour
        self.detection = False
        self.logger.info("Lidar initialized.")
        

    def set_pwm(self, value):
        self.logger.info(f"Setting PWM value to {value}")
        self.lidar.set_pwm(value)

    def scan(self):
        self.set_pwm(512)
        try:
            for scan in self.lidar.iter_scans():
                # Initialize an empty list to store valid distances
                valid_distances = [0] * 360
                for (_, angle, distance) in scan:
                    if distance <= self.max_distance:  # Filtering by maximum distance
                        # Convert angle to radians for y-coordinate calculation
                        angle_radians = angle * (math.pi / 180)
                        # Calculate y-coordinate based on distance and angle
                        x_coordinate = (distance + ORIGIN_LIDAR) * math.cos(angle_radians)
                        y_coordinate = (distance + ORIGIN_LIDAR) * math.sin(angle_radians)
                        # Filtering by y-coordinate range
                        if -200 <= y_coordinate <= 200:
                            # -150<x_coordinates*signeLidar<500
                            valid_distances[min([359, math.floor(angle)])] = distance
                            
                # Check for objects in the deadzone
                if any(0 < distance <= self.deadzone_distance for distance in valid_distances):
                    self.logger.debug(f"Object detected in the deadzone at {x_coordinate} mm (x)! {angle}° counter: {self.alert_counter}")
                    self.alert_counter += 1
                    if self.alert_counter >= self.alert_limit and not self.alert_triggered:
                        self.alert_triggered = True
                        self.detection = True
                        # self.asserv.stopmove()
                        # appeler com pour Killian
                        self.logger.info("Stopping the robot. Object at {x_coordinate} mm (x) and {angle}°")
                
                elif self.detection :
                    self.logger.info("No more object. Restarting the robot.")
                    # self.asserv.restartmove()
                    self.detection = False
                    # appeler com pour Killian  
                    
                else:
                    #logger.debug(f"No objects detected in the deadzone. Nearest object: {distance} mm") 
                    self.alert_counter = 0
                    self.alert_triggered = False
                    
                if(set_stop_lidar):
                    return True

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
    #lidar_scanner.stop_lidarScan()

