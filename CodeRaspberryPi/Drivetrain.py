from gpiozero import Motor

#Integers pour definir ou les moteurs sont connectes sur le GPIO
#placeholders
pinMoteurAG = 1,2
pinMoteurAD = 3,4
pinMoteurDG = 5,6
pinMoteurDD = 7,8

#moteurs
moteurAG = Motor(pinMoteurAG)
moteurAD = Motor(pinMoteurAD)
moteurDG = Motor(pinMoteurDG)
moteurDD = Motor(pinMoteurDD)

class Drivetrain:

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
        moteurAD.backward(power)
        moteurDG.forward(power)
        moteurDD.backward(power)

    def tournerAvancerG(power = 0.5):
        print("tourne a gauche en avancant")
        power2 = power / 2
        moteurAG.forward(power)
        moteurAD.forward(power2)
        moteurDG.forward(power)
        moteurDD.forward(power2)

    def tournerReculerG(power = 0.5):
        print("tourne a gauche en reculant")
        power2 =  power / 2
        moteurAG.backward(power)
        moteurAD.backward(power2)
        moteurDG.backward(power)
        moteurDD.backward(power2)
    


    def tournerD(power = 0.5):
        print("tourne a droite")
        moteurAG.backward(power)
        moteurAD.forward(power)
        moteurDG.backward(power)
        moteurDD.forward(power)

    def tournerAvancerD(power = 0.5):
        print("tourne a droite en avancant")
        power2 = power / 2
        moteurAG.forward(power2)
        moteurAD.forward(power)
        moteurDG.forward(power2)
        moteurDD.forward(power)
    
    def tournerReculerD(power = 0.5):
        print("tourne a droite en reculant")
        power2 =  power / 2
        moteurAG.backward(power2)
        moteurAD.backward(power)
        moteurDG.backward(power2)
        moteurDD.backward(power)

