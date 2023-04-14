
from gpiozero import Motor

#Integers pour definir ou les moteurs sont connectes sur le GPIO
#2 premieres lettres determine l'emplacement du moteur sur le robot
#troisieme lettre determine les pins sur le moteur, F pour forward ou B pour backward
#chiffres placeholders
#cable vert sur 11, cable bleu sur 12
AGFpinMoteur = 11
AGBpinMoteur = 12

#cable mauve sur 9, cable brun sur 10
ADFpinMoteur = 9
ADBpinMoteur = 10

#cable bleu sur 13, cable vert sur 14
DGFpinMoteur = 16
DGBpinMoteur = 18

#cable jaune sur 18, cable orange sur 16
DDFpinMoteur = 13
DDBpinMoteur = 14

#moteurs
moteurAG = Motor(AGFpinMoteur, AGBpinMoteur)
moteurAD = Motor(ADFpinMoteur, ADBpinMoteur)
moteurDG = Motor(DGFpinMoteur, DGBpinMoteur)
moteurDD = Motor(DDFpinMoteur, DDBpinMoteur)

class Drivetrain:
    #power default est 0.75 (75%)
    #les constantes n'existent pas dans Python, mais la convention pour une constante est mettre la variable en MAJUSCULE
    DEFAULT_POWER = 0.75

    def avancer(power = DEFAULT_POWER):
        print("avance")
        moteurAG.forward(power)
        moteurAD.forward(power)
        moteurDG.forward(power)
        moteurDD.forward(power)
    
    def reculer(power = DEFAULT_POWER):
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
    


    def tournerG(power = DEFAULT_POWER):
        print("tourne a gauche")
        moteurAG.forward(power)
        moteurDG.forward(power)
        moteurAD.backward(power)
        moteurDD.backward(power)

    def avancerG(power = DEFAULT_POWER):
        print("tourne a gauche en avancant")
        power2 = power / 2
        moteurAG.forward(power)
        moteurDG.forward(power)
        moteurAD.forward(power2)
        moteurDD.forward(power2)

    def reculerG(power = DEFAULT_POWER):
        print("tourne a gauche en reculant")
        power2 =  power / 2
        moteurAG.backward(power)
        moteurDG.backward(power)
        moteurAD.backward(power2)
        moteurDD.backward(power2)
    


    def tournerD(power = DEFAULT_POWER):
        print("tourne a droite")
        moteurAD.forward(power)
        moteurDD.forward(power)
        moteurAG.backward(power)
        moteurDG.backward(power)

    def avancerD(power = DEFAULT_POWER):
        print("tourne a droite en avancant")
        power2 = power / 2
        moteurAD.forward(power)
        moteurDD.forward(power)
        moteurAG.forward(power2)
        moteurDG.forward(power2)
    
    def reculerD(power = DEFAULT_POWER):
        print("tourne a droite en reculant")
        power2 =  power / 2
        moteurAD.backward(power)
        moteurDD.backward(power)
        moteurAG.backward(power2)
        moteurDG.backward(power2)

