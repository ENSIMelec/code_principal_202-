import math
from adafruit_rplidar import RPLidar
from serial import SerialException
from Globals_Variables import *

class LidarScanner:
    def __init__(self):
        self.port_name = LIDAR_SERIAL
        self.max_distance = 700
        self.deadzone_distance = 500
        self.lidar = RPLidar(None, self.port_name, timeout=5)
        self.alert_triggered = False
        self.alert_counter = 0
        self.alert_limit = 1 #le lidar met 0.6sec/tour
        
    def set_pwm(self, value):
        self.lidar.set_pwm(value)

    def scan(self):
        global detection
        global set_stop_lidar
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
                        x_coordinate = (distance + ORIGIN_LIDAR) * math.cos(angle * (math.pi / 180))
                        y_coordinate = (distance + ORIGIN_LIDAR) * math.sin(angle_radians)
                        # Filtering by y-coordinate range
                        if -200 <= y_coordinate <= 200:
                            # -150<x_coordinates*signeLidar<500
                            valid_distances[min([359, math.floor(angle)])] = distance
                            
                # Check for objects in the deadzone
                if any(0 < distance <= self.deadzone_distance for distance in valid_distances):
                    #print(f"ALERT: Object detected in the deadzone at {distance} mm! ")
                    self.alert_counter += 1
                    if self.alert_counter >= self.alert_limit and not self.alert_triggered:
                        self.alert_triggered = True
                        detection = True
                        # appeler com pour Killian
                        print("You need to stop turn NOW !!!")
                        print("A une distance", x_coordinate)
                
                elif detection :
                    detection = False
                    # appeler com pour Killian  
                else:
                    #print(f"No objects detected in the deadzone. Nearest object: {distance} mm") 
                    self.alert_counter = 0
                    self.alert_triggered = False
                    
                if(set_stop_lidar):
                    return True

        except SerialException:
            print('Error: Lidar device disconnected or multiple access on port.')
            self.stop_lidarScan()

    def stop_lidarScan(self):
        self.lidar.stop_motor()
        self.lidar.disconnect()

if __name__ == '__main__':
    # Setup the RPLidar
    lidar_scanner = LidarScanner()
    #lidar_scanner.scan()
    lidar_scanner.stop_lidarScan()

