
from Drivetrain import Drivetrain
import keyboard

drivetrain = Drivetrain

teleEnabled = True

avancer = False
reculer = False
droite = False
gauche = False

def toggleTele():
    global teleEnabled
    if teleEnabled:
        teleEnabled = False
    else:
        teleEnabled = True
    return teleEnabled

def setTeleEnabled(bool):
    global teleEnabled
    teleEnabled = bool


def keyboardPress():
    global avancer
    global reculer
    global droite
    global gauche

    avancer = keyboard.is_pressed("w") or keyboard.is_pressed("up arrow")
    reculer = keyboard.is_pressed("s") or keyboard.is_pressed("down arrow")
    droite = keyboard.is_pressed("d") or keyboard.is_pressed("right arrow")
    gauche = keyboard.is_pressed("a") or keyboard.is_pressed("left arrow")

    if avancer and reculer:
        avancer = False
        reculer = False
    if droite and gauche:
        droite = False
        gauche = False

def modeTele():
    global teleEnabled
    while teleEnabled:
        keyboardPress()
        if avancer:
            if droite:
                drivetrain.avancerD()
            elif gauche:
                drivetrain.avancerG()
            else:
                drivetrain.avancer()

        elif reculer:
            if droite:
                drivetrain.reculerD()
            elif gauche:
                drivetrain.reculerG()
            else:
                drivetrain.reculer()
            
        elif droite:
            if avancer:
                drivetrain.avancerD()
            elif reculer:
                drivetrain.reculerD()
            else:
                drivetrain.tournerD()
                
        elif gauche:
            if avancer:
                drivetrain.avancerG()
            elif reculer:
                drivetrain.reculerG()
            else:
                drivetrain.tournerG()

        else:
            drivetrain.stop()