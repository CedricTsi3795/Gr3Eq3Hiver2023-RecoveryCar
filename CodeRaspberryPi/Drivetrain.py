
from gpiozero import Motor
from gpiozero import DistanceSensor

#Integers pour definir ou les moteurs sont connectes sur le GPIO
#2 premieres lettres determine l'emplacement du moteur sur le robot
#troisieme lettre determine les pins sur le moteur, F pour forward ou B pour backward

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
ULTRASON_ECHO_PIN = 18
ULTRASON_TRIG_PIN = 4
ULTRASON_MAX_DISTANCE = 0.5 #0.5 metres
ultrason = DistanceSensor(echo = ULTRASON_ECHO_PIN, trigger = ULTRASON_TRIG_PIN, max_distance = ULTRASON_MAX_DISTANCE)

#power default est 0.75 (75%)
#les constantes n'existent pas dans Python, mais la convention pour une constante est mettre la variable en MAJUSCULE
DEFAULT_MOTEUR_POWER = 0.75

class Drivetrain:

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
        power2 = power / 2
        moteurAG.forward(power)
        moteurDG.forward(power)
        moteurAD.forward(power2)
        moteurDD.forward(power2)

    def reculerG(power = DEFAULT_MOTEUR_POWER):
        print("tourne a gauche en reculant")
        power2 =  power / 2
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
        power2 = power / 2
        moteurAD.forward(power)
        moteurDD.forward(power)
        moteurAG.forward(power2)
        moteurDG.forward(power2)
    
    def reculerD(power = DEFAULT_MOTEUR_POWER):
        print("tourne a droite en reculant")
        power2 =  power / 2
        moteurAD.backward(power)
        moteurDD.backward(power)
        moteurAG.backward(power2)
        moteurDG.backward(power2)

    def scannerUltrason():
        dist = ultrason.distance
        if dist > 0:
            return dist
        else:
            return -1

