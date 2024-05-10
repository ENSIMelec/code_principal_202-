import math
from adafruit_rplidar import RPLidar, RPLidarException
from serial import SerialException
from Globals_Variables import *
import logging
import logging.config
import time
from Asserv import Asserv


class LidarScanner(object):
    _instance = None
    def __new__(cls,*args,**kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self,interface=None): 
        
        # Charger la configuration de logging
        logging.config.fileConfig(LOGS_CONF_PATH,disable_existing_loggers=False)

        # Créer un logger
        self.logger = logging.getLogger("Lidar")

        self.interface=interface
        self.port_name = LIDAR_SERIAL
        self.deadzone_distance = 500
        self.lidar = RPLidar(None, self.port_name, timeout=5)
        self.detection = False
        self.logger.info("Lidar initialized.")
        self.asserv = None
        self.enable_lidar = True

        if self.interface != None :
            self.interface.after(0,self.interface.lidar_initialized())

    def set_pwm(self, value):
        self.logger.info(f"Setting PWM value to {value}")
        self.lidar.set_pwm(value)

    def scan(self):
        self.set_pwm(512)
        try:
            for scan in self.lidar.iter_scans():
                if(not(self.enable_lidar)):
                    continue

                for (quality, angle, distance) in scan:
                    angle_radians = angle * (math.pi / 180)
                    # Calculate x-coordinate and y-coordinate based on distance and angle
                    if self.asserv != None:
                        x_coordinate = (distance + ORIGIN_LIDAR) * math.cos(angle_radians) * self.asserv.signeLidar
                    else :
                        x_coordinate = (distance + ORIGIN_LIDAR) * math.cos(angle_radians)
                    y_coordinate = (distance + ORIGIN_LIDAR) * math.sin(angle_radians)
                    
                    if (-200 <= y_coordinate <= 200) and (250 < x_coordinate < 650) and (quality > 14): # Filtering by deadzone distance
                        self.logger.info(f"Object detected in the deadzone at {distance} mm (x)! {angle}°. {quality}")
                        if not self.detection:
                            self.logger.warning(f"Stopping the robot. Object at {x_coordinate} mm (x) and {angle}°")
                            if self.asserv != None:
                                self.asserv.stopmove()
                        self.detection = True
                        self.time_detect = time.time()
                            
                    elif (self.detection) and (time.time() - self.time_detect) > 0.5 :
                        self.logger.info("No more object. Restarting the robot.")
                        if self.asserv != None:
                            self.asserv.restartmove()
                        self.detection = False  
        except RPLidarException as error:
            self.logger.error(f"RPLidarException : {error}")
            self.stop_lidarScan()
            # self.lidar = RPLidar(None, self.port_name, timeout=5)
            # self.scan()
        
        except Exception as error :
            self.logger.error(f"Error in LidarScan: {error}")
            time.sleep(0.1)

        except KeyboardInterrupt:
            self.logger.warning("Stopping the lidar scan. (KeyboardInterrupt)")
            self.stop_lidarScan()

    def stop_lidarScan(self):
        self.logger.info("Stopping the lidar scan.")
        self.lidar.stop_motor()
        self.lidar.stop()
        self.lidar.disconnect()
        
    def set_asserv_obj(self, obj):
        self.asserv = obj

    def disable(self):
        self.enable_lidar = False
        return True

    def enable(self):
        self.enable_lidar = True
        return True

if __name__ == '__main__':
    # Setup the RPLidar
    lidar_scanner = LidarScanner()
    lidar_scanner.disable()
    time.sleep(10)
    lidar_scanner.stop_lidarScan()

