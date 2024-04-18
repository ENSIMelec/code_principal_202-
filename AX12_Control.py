import os
import time
from dynamixel_sdk import *

class AX12_Control:
    def __init__(self, dxl_id, baudrate, devicename):
        self.DXL_ID = dxl_id
        self.BAUDRATE = baudrate
        self.DEVICENAME = devicename
        self.portHandler = PortHandler(self.DEVICENAME)
        self.packetHandler = PacketHandler(1.0) # Protocol version 1.0
        self.torque_limit = 1023
        self.ADDR_MX_PRESENT_POSITION = 132
        
    def connect(self):
        if self.portHandler.openPort():
            print("Port ouvert avec succès")
        else:
            print("Échec de l'ouverture du port")
            print("Appuyez sur une touche pour terminer...")
            getch()
            quit()

        if self.portHandler.setBaudRate(self.BAUDRATE):
            print("Vitesse du port modifiée avec succès")
        else:
            print("Échec de modification de la vitesse du port")
            print("Appuyez sur une touche pour terminer...")
            getch()
            quit()

        dxl_model_number, dxl_comm_result, dxl_error = self.packetHandler.ping(self.portHandler, self.DXL_ID)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("[ID:%03d] Ping réussi. Numéro de modèle du Dynamixel : %d" % (self.DXL_ID, dxl_model_number))
        
        self.packetHandler.write1ByteTxRx(self.portHandler, self.DXL_ID, 24, 1)  # Adresse pour activer le mode de torque

    def move(self, position):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, 30, position)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print(f"Position du moteur {self.DXL_ID} réglée à {position} avec succès")
            
    def read_load(self):
        dxl_present_load, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, 40)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print(f"Load du moteur {self.DXL_ID}: {dxl_present_load}")
        return dxl_present_load
    

    def write(self, address, value):
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.DXL_ID, address, value)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print(f"Écriture réussie à l'adresse {address} avec la valeur {value}")

        
    def read_present_position(self):
        while 1:
        # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.DXL_ID, self.ADDR_MX_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            print("[ID:%03d] PresPos:%03d" % (self.DXL_ID, dxl_present_position))
        return dxl_present_position

        
    def disconnect(self):
        self.portHandler.closePort()

#Exemple d'utilisation


# Actionneurs panneaux solaires
#for _ in range(6):
#   ax12.move(520)
#   time.sleep(5)

#    ax12.move(615)
#    time.sleep(3)

#    ax12.move(520)
#    time.sleep(5)

#ax12.disconnect()
