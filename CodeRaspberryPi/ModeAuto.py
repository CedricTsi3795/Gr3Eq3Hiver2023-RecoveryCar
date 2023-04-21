
from Drivetrain import Drivetrain
from time import sleep
from flask import Flask

app = Flask(__name__)

@app.route('/PagesHTML/')
def index():
    return render_template('PageControle.html')

class ModeAuto:
    def __init__(self):
        self.autoEnabled = False

    @app.route('/Mode/')
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

        #mettre code pour trouver obj ICI

        if not(objTrouve) or dist < 0:
            dist = -1
        
        return dist
        

    #calcule la vitesse du robot avec la puissance dans les moteurs
    def calcTemps(dist, power):
        temps = 0.0
        vitesse = 0.0

        #mettre code pour calculer le temps du trajet ICI

        temps = dist / vitesse
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


    #Algorithme: https://lucid.app/lucidchart/49f29f3a-0c22-4064-b13e-0cce0266da9b/edit?viewport_loc=-244%2C50%2C2216%2C1054%2C0_0&invitationId=inv_2c8d6370-e1c8-42b7-962f-fb66d02797e6
    @app.route('/Mode/')
    def modeAuto(self):
        
        #pour s'assurer que ca roule APRES toggleAuto()
        sleep(0.25)

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
                    
