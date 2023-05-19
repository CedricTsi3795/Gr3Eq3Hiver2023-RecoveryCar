
from Drivetrain import Drivetrain
from time import sleep

class ModeAuto:
    autoEnabled = False
    def __init__(self):
        self.autoEnabled = False

    def toggleAuto(self):
        if self.autoEnabled:
            self.autoEnabled = False
        else:
            self.autoEnabled = True
        return self.autoEnabled

    def setAutoEnabled(self, bool):
        self.autoEnabled = bool

    #calcule la vitesse du robot avec la puissance dans les moteurs
    def calcTemps(dist, power):
        temps = 0.0
        vitesse = 0.0

        #mettre code pour calculer le temps du trajet ICI

        temps = dist / vitesse
        return temps


    #Algorithme:
    #https://lucid.app/lucidchart/49f29f3a-0c22-4064-b13e-0cce0266da9b/edit?viewport_loc=-244%2C50%2C2216%2C1054%2C0_0&invitationId=inv_2c8d6370-e1c8-42b7-962f-fb66d02797e6
    def modeAuto(self):

        print("start")
        
        while self.autoEnabled:
            if Drivetrain.scannerUltrason() != -1:
                Drivetrain.avancerTemps()

            else:
                Drivetrain.tournerDroiteTemps(Drivetrain.SECONDES_POUR_TOURNER_90)

                if Drivetrain.scannerUltrason() != -1:
                    Drivetrain.avancerTemps()
                else:
                    Drivetrain.tournerGaucheTemps(Drivetrain.SECONDES_POUR_TOURNER_180)
                    