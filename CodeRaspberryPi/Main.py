
import Drivetrain
import keyboard

drivetrain = Drivetrain.Drivetrain

avancer = False
reculer = False
droite = False
gauche = False

def keyboardPress():
    global avancer
    global reculer
    global droite
    global gauche

    avancer = keyboard.is_pressed("w")
    reculer = keyboard.is_pressed("s")
    droite = keyboard.is_pressed("d")
    gauche = keyboard.is_pressed("a")

while True:
    keyboardPress()
    if avancer:
        if droite:
            drivetrain.tournerAvancerD()
        elif gauche:
            drivetrain.tournerAvancerG()
        elif reculer:
            drivetrain.stop()
        else:
            drivetrain.avancer()

    elif reculer:
        if droite:
            drivetrain.tournerReculerD()
        elif gauche:
            drivetrain.tournerReculerG()
        elif avancer:
            drivetrain.stop()
        else:
            drivetrain.reculer()
        
    elif droite:
        if avancer:
            drivetrain.tournerAvancerD()
        elif reculer:
            drivetrain.tournerReculerD()
        elif gauche:
            drivetrain.stop()
        else:
            drivetrain.tournerD()
            
    elif gauche:
        if avancer:
            drivetrain.tournerAvancerG()
        elif reculer:
            drivetrain.tournerReculerG()
        elif droite:
            drivetrain.stop()
        else:
            drivetrain.tournerG()

    else:
        drivetrain.stop()