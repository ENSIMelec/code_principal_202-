from AX12_Python.AX12_Panneau import AX12_Panneau
import time
import Asserv

AX12_Panneau = AX12_Panneau()
AX12_Panneau.bouger_panneau_droit()
time.sleep(3)
AX12_Panneau.ramener_AX12_droit()

# asserv = Asserv.Asserv()
# asserv.receive_data()