
from gpiozero import Motor
from gpiozero import DistanceSensor
from time import sleep

#Integers pour definir ou les moteurs sont connectes sur le GPIO
#les constantes n'existent pas dans Python, mais la convention pour une constante est mettre la variable en MAJUSCULE

#cable vert sur 11, cable bleu sur 12
AVNT_GAUC_FORW_PINMOTEUR = 11
AVNT_GAUC_BACK_PINMOTEUR = 12

#cable mauve sur 9, cable brun sur 10
AVNT_DROT_FORW_PINMOTEUR = 9
AVNT_DROT_BACK_PINMOTEUR = 10

#cable bleu sur 13, cable vert sur 14
DERR_GAUC_FORW_PINMOTEUR = 16
DERR_GAUC_BACK_PINMOTEUR = 18

#cable jaune sur 18, cable orange sur 16
DERR_DROT_FORW_PINMOTEUR = 13
DERR_DROT_BACK_PINMOTEUR = 14

#moteurs
moteurAG = Motor(AVNT_GAUC_FORW_PINMOTEUR, AVNT_GAUC_BACK_PINMOTEUR)
moteurAD = Motor(AVNT_DROT_FORW_PINMOTEUR, AVNT_DROT_BACK_PINMOTEUR)
moteurDG = Motor(DERR_GAUC_FORW_PINMOTEUR, DERR_GAUC_BACK_PINMOTEUR)
moteurDD = Motor(DERR_DROT_FORW_PINMOTEUR, DERR_DROT_BACK_PINMOTEUR)

#numero des pins placeholder
ULTRASON_ECHO_PIN = 5
ULTRASON_TRIG_PIN = 4
ULTRASON_MAX_DISTANCE = 0.5 #0.5 metres
ULTRASON_NB_MESURES = 50
ultrason = DistanceSensor(echo = ULTRASON_ECHO_PIN, trigger = ULTRASON_TRIG_PIN, max_distance = ULTRASON_MAX_DISTANCE)

DEFAULT_MOTEUR_POWER = 1

def avancer(power = DEFAULT_MOTEUR_POWER):
    print("avance")
    moteurAG.forward(power)
    moteurAD.forward(power)
    moteurDG.forward(power)
    moteurDD.forward(power)
    
def reculer(power = DEFAULT_MOTEUR_POWER):
    print("recule")
    moteurAG.backward(power)
    moteurAD.backward(power)
    moteurDG.backward(power)
    moteurDD.backward(power)

def stop():
    moteurAG.stop()
    moteurAD.stop()
    moteurDG.stop()
    moteurDD.stop()
    

def tournerG(power = DEFAULT_MOTEUR_POWER):
    print("tourne a gauche")
    moteurAG.forward(power)
    moteurDG.forward(power)
    moteurAD.backward(power)
    moteurDD.backward(power)

def avancerG(power = DEFAULT_MOTEUR_POWER):
    print("tourne a gauche en avancant")
    power2 = power * 0.75
    moteurAG.forward(power)
    moteurDG.forward(power)
    moteurAD.forward(power2)
    moteurDD.forward(power2)

def reculerG(power = DEFAULT_MOTEUR_POWER):
    print("tourne a gauche en reculant")
    power2 =  power * 0.75
    moteurAG.backward(power)
    moteurDG.backward(power)
    moteurAD.backward(power2)
    moteurDD.backward(power2)
    

def tournerD(power = DEFAULT_MOTEUR_POWER):
    print("tourne a droite")
    moteurAD.forward(power)
    moteurDD.forward(power)
    moteurAG.backward(power)
    moteurDG.backward(power)

def avancerD(power = DEFAULT_MOTEUR_POWER):
    print("tourne a droite en avancant")
    power2 = power * 0.75
    moteurAD.forward(power)
    moteurDD.forward(power)
    moteurAG.forward(power2)
    moteurDG.forward(power2)
    
def reculerD(power = DEFAULT_MOTEUR_POWER):
    print("tourne a droite en reculant")
    power2 =  power * 0.75
    moteurAD.backward(power)
    moteurDD.backward(power)
    moteurAG.backward(power2)
    moteurDG.backward(power2)

class Drivetrain:

    SECONDES_POUR_MOUVEMENT_DEFAUT = 2
        
    SECONDES_POUR_TOURNER_45 = 2
    SECONDES_POUR_TOURNER_90 = 2.5
    SECONDES_POUR_TOURNER_180 = 3

    def avancerTemps(tempsSecondes = SECONDES_POUR_MOUVEMENT_DEFAUT):
        avancer()
        sleep(tempsSecondes)
        stop()

    def avancerGaucheTemps(tempsSecondes = SECONDES_POUR_MOUVEMENT_DEFAUT):
        avancerG()
        sleep(tempsSecondes)
        stop()

    def avancerDroiteTemps(tempsSecondes = SECONDES_POUR_MOUVEMENT_DEFAUT):
        avancerD()
        sleep(tempsSecondes)
        stop()


    def reculerTemps(tempsSecondes = SECONDES_POUR_MOUVEMENT_DEFAUT):
        reculer()
        sleep(tempsSecondes)
        stop()

    def reculerGaucheTemps(tempsSecondes = SECONDES_POUR_MOUVEMENT_DEFAUT):
        reculerG()
        sleep(tempsSecondes)
        stop()

    def reculerDroiteTemps(tempsSecondes = SECONDES_POUR_MOUVEMENT_DEFAUT):
        reculerD()
        sleep(tempsSecondes)
        stop()


    def tournerGaucheTemps(tempsSecondes = SECONDES_POUR_TOURNER_45):
        tournerG()
        sleep(tempsSecondes)
        stop()

    def tournerDroiteTemps(tempsSecondes = SECONDES_POUR_TOURNER_45):
        tournerD()
        sleep(tempsSecondes)
        stop()

    #mesure la distance ULTRASON_NB_MESURES fois et fait la moyenne
    #le senseur ultrasonique est tres sensible et fait des erreurs constamment
    def scannerUltrason():
        dist = 0
        sum = 0
        for i in range(ULTRASON_NB_MESURES + 1):
            sum += ultrason.distance
        dist = sum / ULTRASON_NB_MESURES

        if dist < ULTRASON_MAX_DISTANCE:
            return dist
        else:
            return -1
