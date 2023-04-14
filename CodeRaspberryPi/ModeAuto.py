
from Drivetrain import Drivetrain

drivetrain = Drivetrain

autoEnabled = True

def toggleAuto():
    global autoEnabled
    if autoEnabled:
        autoEnabled = False
    else:
        autoEnabled = True
    return autoEnabled

def setAutoEnabled(bool):
    global autoEnabled
    autoEnabled = bool

def modeAuto():
    while autoEnabled:
        print("placeholder")