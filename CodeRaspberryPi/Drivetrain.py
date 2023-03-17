
from gpiozero import Motor
from gpiozero import DistanceSensor
from picamera import PiCamera

#Integers pour definir ou les moteurs sont connectes sur le GPIO
#2 premieres lettres determine l'emplacement du moteur sur le robot
#troisieme lettre determine les pins sur le moteur, F pour forward ou B pour backward
#chiffres placeholders
AGFpinMoteur = 1
AGBpinMoteur = 2

ADFpinMoteur = 3
ADBpinMoteur = 4

DGFpinMoteur = 5
DGBpinMoteur = 6

DDFpinMoteur = 7
DDBpinMoteur = 8

#moteurs
moteurAG = Motor(AGFpinMoteur, AGBpinMoteur)
moteurAD = Motor(ADFpinMoteur, ADBpinMoteur)
moteurDG = Motor(DGFpinMoteur, DGBpinMoteur)
moteurDD = Motor(DDFpinMoteur, DDBpinMoteur)

senseurPinEcho = 18
senseurPinTrigger = 17

senseurUltrasonique = DistanceSensor(echo = senseurPinEcho, trigger = senseurPinTrigger)

class Drivetrain:
#power default est 0.5 (50%)

    def avancer(power = 0.5):
        print("avance")
        moteurAG.forward(power)
        moteurAD.forward(power)
        moteurDG.forward(power)
        moteurDD.forward(power)
    
    def reculer(power = 0.5):
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
    


    def tournerG(power = 0.5):
        print("tourne a gauche")
        moteurAG.forward(power)
        moteurDG.forward(power)
        moteurAD.backward(power)
        moteurDD.backward(power)

    def avancerG(power = 0.5):
        print("tourne a gauche en avancant")
        power2 = power / 2
        moteurAG.forward(power)
        moteurDG.forward(power)
        moteurAD.forward(power2)
        moteurDD.forward(power2)

    def reculerG(power = 0.5):
        print("tourne a gauche en reculant")
        power2 =  power / 2
        moteurAG.backward(power)
        moteurDG.backward(power)
        moteurAD.backward(power2)
        moteurDD.backward(power2)
    


    def tournerD(power = 0.5):
        print("tourne a droite")
        moteurAD.forward(power)
        moteurDD.forward(power)
        moteurAG.backward(power)
        moteurDG.backward(power)

    def avancerD(power = 0.5):
        print("tourne a droite en avancant")
        power2 = power / 2
        moteurAD.forward(power)
        moteurDD.forward(power)
        moteurAG.forward(power2)
        moteurDG.forward(power2)
    
    def reculerD(power = 0.5):
        print("tourne a droite en reculant")
        power2 =  power / 2
        moteurAD.backward(power)
        moteurDD.backward(power)
        moteurAG.backward(power2)
        moteurDG.backward(power2)

