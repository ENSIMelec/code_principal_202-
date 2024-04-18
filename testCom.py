import time
from Asserv import Asserv
from AX12_Pinces import AX12_Pinces
from AX12_Ascenseur import AX12_Ascenseur


asserv = Asserv('/dev/ttyACM1')
asserv.goto(300.0,0.0)
time.sleep(0.5)
asserv.goto(600.0,0.0)