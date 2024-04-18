import math
from adafruit_rplidar import RPLidar
from Globals_Variables import *

class LidarScanner:
    def __init__(self):
        self.port_name = '/dev/ttyUSB0'
        self.max_distance = 500
        self.deadzone_distance = 150
        self.lidar = RPLidar(None, self.port_name, timeout=3)
        self.alert_triggered = False
        self.alert_counter = 0
        self.alert_limit = 5 #le lidar met 0.6sec/tour
        
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
                        x_coordinate = distance * math.cos(angle * (math.pi / 180))
                        y_coordinate = distance * math.sin(angle_radians)
                        # Filtering by y-coordinate range
                        if -200 <= y_coordinate <= 200:
                            valid_distances[min([359, math.floor(angle)])] = distance
                            
                # Check for objects in the deadzone
                if any(0 < distance <= self.deadzone_distance for distance in valid_distances):
                    #print(f"ALERT: Object detected in the deadzone at {distance} mm! ")
                    self.alert_counter += 1
                    if self.alert_counter >= self.alert_limit and not self.alert_triggered:
                        self.alert_triggered = True
                        detection = True
                        print("You need to stop turn NOW !!!")
                    
                else:
                    #print(f"No objects detected in the deadzone. Nearest object: {distance} mm") 
                    self.alert_counter = 0
                    self.alert_triggered = False
                    
                if(set_stop_lidar):
                    return True

        except KeyboardInterrupt:
            print('Stopping.')
            self.stop_lidarScan()

    def stop_lidarScan(self):
        self.lidar.stop()
        self.lidar.set_pwm(0)
        self.lidar.disconnect()

if __name__ == '__main__':
    # Setup the RPLidar
    lidar_scanner = LidarScanner()
    lidar_scanner.scan()

