
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

    #scanner avec camera et senseur ultrasonique
    #si senseur ultrasonique trouve qqch mais tensor flow trouve rien alors retoune rien, sinon retourne dist trouve        
    def scanner():
        objTrouve = False
        dist = Drivetrain.scannerUltrason()

        #TODO mettre code pour trouver obj ICI

        if not(objTrouve) or dist < 0:
            dist = -1
        
        return dist
        

    #calcule la vitesse du robot avec la puissance dans les moteurs
    def calcTemps(dist, power):
        temps = 0.0
        vitesse = 0.0

        #TODO mettre code pour calculer le temps du trajet ICI

        temps = dist / vitesse
        return temps

    def tournerVersObj():
        #utiliser tensor flow pour tourner vers l'objet
        print("placeholder")


    #Algorithme:
    #https://lucid.app/lucidchart/49f29f3a-0c22-4064-b13e-0cce0266da9b/edit?viewport_loc=-244%2C50%2C2216%2C1054%2C0_0&invitationId=inv_2c8d6370-e1c8-42b7-962f-fb66d02797e6
    def modeAuto(self):
        objetTrouve = False #TODO DEFINIR LA CONDITION POUR QUAND LE ROBOT A TROUVE OBJ ET SE TROUVE A OBJ
        #pour s'assurer que ca roule APRES toggleAuto()
        sleep(0.25)

        print("start")
        
        while self.autoEnabled:
            if self.scanner() > 0.0:
                print("obj trouve")
                self.tournerVersObj()
                dist = self.scanner()
                temps = self.calcTemps(dist)
                Drivetrain.avancerTemps(temps)
            elif self.autoEnabled:
                print("rien trouve")
                Drivetrain.tournerGaucheTemps()
                dist = self.scanner()
                if dist < 0.0 and self.autoEnabled:
                    print("rien trouve a gauche")
                    Drivetrain.tournerDroiteTemps(Drivetrain.SECONDES_POUR_TOURNER_90)
                    dist = self.scanner()
                    if dist < 0.0 and self.autoEnabled:
                        print("rien trouve a droite")
                        Drivetrain.tournerGaucheTemps()
                        Drivetrain.avancerTemps()
