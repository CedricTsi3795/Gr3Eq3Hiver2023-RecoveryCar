
from Drivetrain import Drivetrain
from time import sleep

class ModeTele:
    def __init__(self):
        self.teleEnabled = True

    avancer = False
    reculer = False

    droite = False
    droiteAvancer = False
    droiteReculer = False

    gauche = False
    gaucheAvancer = False
    gaucheReculer = False

    def toggleTele(self):
        if self.teleEnabled:
            self.teleEnabled = False
        else:
            self.teleEnabled = True
        return self.teleEnabled


    def setTeleEnabled(self, bool):
        self.teleEnabled = bool


    def setAvancer(self, bool = False):
        self.avancer = bool
    def setReculer(self, bool = False):
        self.reculer = bool

    def setDroite(self, bool = False):
        self.droite = bool
    def setDroiteAvancer(self, bool = False):
        self.droiteAvancer = bool
    def setDroiteReculer(self, bool = False):
        self.droiteReculer = bool

    def setGauche(self, bool = False):
        self.gauche = bool
    def setGaucheAvancer(self, bool = False):
        self.gaucheAvancer = bool
    def setGaucheReculer(self, bool = False):
        self.gaucheReculer = bool
    

    def modeTele(self):

        #pour s'assurer que ca roule APRES toggleTele()
        sleep(0.25)

        while self.teleEnabled:
            if self.avancer:
                Drivetrain.avancer()

            elif self.reculer:
                Drivetrain.reculer()
                
            elif self.droite:
                Drivetrain.tournerD()
            elif self.droiteAvancer:
                Drivetrain.avancerD()
            elif self.droiteReculer:
                Drivetrain.reculerD()
                    
            elif self.gauche:
                Drivetrain.tournerG()
            elif self.gaucheAvancer:
                Drivetrain.avancerG()
            elif self.gaucheReculer:
                Drivetrain.reculerG()

            else:
                Drivetrain.stop()
        