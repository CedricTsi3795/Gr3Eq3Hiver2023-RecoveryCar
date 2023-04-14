
from Drivetrain import Drivetrain
from time import sleep
from gpiozero import DistanceSensor

ultrason = DistanceSensor(echo = 18, trigger = 4)

autoEnabled = True

class ModeAuto:
    def __init__(self):
        self.autoEnabled = True

    def toggleAuto(self):
        if self.autoEnabled:
            self.autoEnabled = False
        else:
            self.autoEnabled = True
        return self.autoEnabled

    def setAutoEnabled(self, bool):
        self.autoEnabled = bool

        
    def scanner():
        print("placeholder")
        objTrouve = False
        dist = 0.0

        #scanner avec camera et senseur ultrasonique
        #mettre code pour trouver obj ICI

        if objTrouve:
            return dist
        else:
            return -1
        

    def calcTemps(dist):
        temps = 0.0

        #mettre code pour calculer le temps du trajet ICI

        return temps
    
    def tournerG45deg():
        TEMPS_ROT_45DEG = 0.0
        Drivetrain.tournerG()
        sleep(TEMPS_ROT_45DEG)
        Drivetrain.stop()

    def tournerD90deg():
        TEMPS_ROT_45DEG = 0.0
        Drivetrain.tournerD()
        sleep(TEMPS_ROT_45DEG)
        Drivetrain.stop()

    def tournerVersObj():
        #utiliser tensor flow pour tourner vers l'objet
        print("placeholder")


    def modeAuto(self):
        #Algorithme: https://lucid.app/lucidchart/49f29f3a-0c22-4064-b13e-0cce0266da9b/edit?viewport_loc=-244%2C50%2C2216%2C1054%2C0_0&invitationId=inv_2c8d6370-e1c8-42b7-962f-fb66d02797e6
        print("start")
        
        while self.autoEnabled:
        
            if self.scanner() > 0.0:
                print("obj trouve")

                self.tournerVersObj()
                dist = self.scanner()
                temps = self.calcTemps(dist)
                Drivetrain.avancer()
                sleep(temps)
                Drivetrain.stop()

            else:
                print("rien trouve")
                self.tournerG45deg()
                dist = self.scanner()

                if dist < 0.0:
                    print("rien trouve a gauche")
                    self.tournerD90deg()
                    dist = self.scanner()

                    if dist < 0.0:
                        print("rien trouve a droite")
                        self.tournerG45deg()
                        Drivetrain.avancer()
                        sleep(2)
                        Drivetrain.stop()
                    
