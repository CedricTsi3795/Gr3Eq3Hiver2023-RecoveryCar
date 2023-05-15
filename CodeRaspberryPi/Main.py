import io
import picamera
import logging
import socketserver
from threading import Condition
from Drivetrain import Drivetrain
from http.server import BaseHTTPRequestHandler, HTTPServer
from ModeAuto import ModeAuto
import os
import PIL.Image as Image
#****** AVANT de run ce code, s'assurer de d<abord que le terminal est bien sur le dossier contenant les programmes tensorFlow activer l<environnement virtuel
#Dans notre cas, on fait:
#cd /home/cedric/tflite1
#source tflite-env/bin/activate
# classe qui va me etre utilie pour nommer les
class CompteurImage:
    cpt=0
   #on cree notre objet compteur 
CompteurImage= CompteurImage()


#methode qui recupere l'image actuelle et l'analyse. LE Resultat vas dans le fichier Images
def analiserPhotos(imagePath):
    os.system("python3 TFLite_detection_image.py --modeldir=Sample_TFLite_model --image="+imagePath)
    
#analiserPhotos()
# source du tutoriel pour le serveur: 
# Nos page Web,je vais l'ameliorer(personaliser)
##nos differentes pasges
PAGEGALERIE = """
<html>

<style>

header {
    background-color: 070707;
    text-align: center;
}

.onglet {

    border: 2px black inset ;
    color: black;
    padding: 8px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    background-color: black;
    color: white;
    font-family: Verdana, Geneva, Tahoma, sans-serif;

}

.titreDiv {
    margin: 30px;
    border: black double 10px;
    text-align: center;
    width: auto;
    height: auto;
    background-color: EAEAEA;
}

.galerieDiv {

    margin: 40px;
    text-align: center;
    border: black groove 2px;
    background-color: EAEAEA;

    height: auto;
    width: auto;

}

.photo {

    width: 225;
    height: 150;

    margin: 30px;

    border: black 2px groove;

    display: inline-block;



}

.bouton {
    border: 2px black outset ;
    border-radius: 60px;
    color: black;
    padding: 8px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 10px;
    cursor: pointer;
    background-color: DCDCDC;
}




</style>



<head>
    <meta charset="utf-8">
    <title>RecoveryCar Live</title>

    <! definir une image en favicon avec un lien au directory >
    <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
</head>

<! -- Header de la page avec les differents onglets disponibles sur le site -- >

<header>

    <form action="/" method="POST">            
            <p>
                <input class="onglet" type="submit" name="submit" value="Accueil">
                <input class="onglet" type="submit" name="submit" value="Conduite">
                <input class="onglet" type="submit" name="submit" value="Galerie">

            </p>

    </form>

</header>

<body style="background-color:C5C5C5">

    <! -- Tite de la page -- >

    <div class="titreDiv">
        <h1 style="text-decoration: underline overline; font-size: 42px;">RecoveryCar</h1>
        <h2 style="color: red;font-size: 30px; text-decoration: underline;">Live</h2>
    </div>

    <! -- Division de la galerie photos -- >

    <div class="galerieDiv">

        <div class="boutonsAction">

            <h2 style="border: black 2px solid; border-left-width: 0px; border-right-width: 0px; background-color: DCDCDC; font-size: 24px;">Galerie photos</h2>

        </div>


        <p style="display: inline-block;">

            <input class="bouton" type="submit" name="Sélectionner" value="Sélectionner" style="background-color: 0076FF;">
            <input class="bouton" type="submit" name="Télécharger" value="Télécharger" style="background-color: 00FF59;">
            <input class="bouton" type="submit" name="Supprimer" value="Supprimer" style="background-color: red;">
            <input class="bouton" type="submit" name="Annuler" value="Annuler">

        </p>

        <p>
            <img class="photo" >
            <img class="photo" >
            <img class="photo" >
        </p>

        <p>
            <img class="photo" >
            <img class="photo" >
            <img class="photo" >
        </p>

        <p>
            <img class="photo" >
            <img class="photo" >
            <img class="photo" >
        </p>


        <p style="text-align: center; display: inline-block;">

            <input class="bouton" type="submit" name="Page précédente" value="&larr; Page précédente">

            <p class="bouton" style="cursor: default;"> Page # / 10 </p>

                <input class="bouton" type="submit" name="Page suivante" value="Page suivante &rarr;">

        </p>




    </div>






</body>
</html>
"""

PAGECONTROLE = """
<style>

header {
    background-color: 070707;
    text-align: center;
}

.onglet {

border: 2px black inset ;
color: black;
padding: 8px 25px;
text-align: center;
text-decoration: none;
display: inline-block;
font-size: 16px;
margin: 4px 2px;
cursor: pointer;
background-color: black;
color: white;
font-family: Verdana, Geneva, Tahoma, sans-serif;

}

.titreDiv {
    margin: 30px;
    border: black double 10px;
    text-align: center;camera=PiCamera()
camera.capture('/home/cedric/Desktop/image1.jpg')
    width: auto;
    height: auto;
    background-color: EAEAEA;
}camera=PiCamera()
camera.capture('/home/cedric/Desktop/image1.jpg')

.cameraDiv {
    margin: 10px;
    margin-left: 50px;
    margin-right: 40px;

    width: 720px;
    height: 560px;

    border: black solid 3px;
    text-align: center;
    background-color: EAEAEA;
    padding-bottom: 0px;
    display: inline-block;
}


.mouvementDiv {
    border: black ridge 3px;
    text-align: center;

    width: auto;
    height: auto;

    margin-top: 10px;

    padding: 25px;
    background-color: EAEAEA;
    display: inline-block;
}

.bouton {
    border: 2px black outset ;
    border-radius: 60px;
    color: black;
    padding: 8px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    background-color: DCDCDC;
}


</style>





<! -- Header de la page avec les differents onglets disponibles sur le site -- >

<header>


    <form action="/" method="POST">            
            <p>
                <input class="onglet" type="submit" name="submit" value="Accueil">
                <input class="onglet" type="submit" name="submit" value="Conduite">
                <input class="onglet" type="submit" name="submit" value="Galerie">

            </p>

    </form>

</header>


<body style="background-color:C5C5C5">

    <! -- Tite de la page -- >

    <div class="titreDiv">
        <h1 style="text-decoration: underline overline; font-size: 42px;">RecoveryCar</h1>
        <h2 style="color: red;font-size: 30px; text-decoration: underline;">Live</h2>
    </div>

<! -- division qui regroupe la camera et les boutons -- >

    <div style="text-align: center;">



<! permet de controler le robot avec les touches du clavier >
        <input type="hidden" name="keypressed" onkeypress="event">




<! -- division d'image de la camera -- > 
        <div class="cameraDiv">

            <h2 style="border: black 2px solid; border-left-width: 0px; border-right-width: 0px; background-color: DCDCDC; font-size: 24px;">Image en temps réel</h2>

            <img src="stream.mjpg" width="630" height="420" style="border: black inset 2px;"/>

        </div>


<! -- division des boutons -- >        
        <div class="mouvementDiv">

            <form action="/" method="POST">

<! -- nos differents boutons de deplacement -- > 

                <p>
                    <input class="bouton" type="submit" name="Mode" value="Autonome" style="background-color: 0076FF;">
                </p>

                <p>
                    <input class="bouton" type="submit" name="Avant G" value="AvantG">
                    <input class="bouton" type="submit" name="Avant" value="Avant">
                    <input class="bouton" type="submit" name="Avant D" value="AvantD">
                </p>


                <p>
                    <input class="bouton" type="submit" name="Gauche" value="Gauche">
                    <input class="bouton" type="submit" name="Droite" value="Droite">
                </p>

                <p>
                    <input class="bouton" type="submit" name="Arriere G" value="ArriereG">
                    <input class="bouton" type="submit" name="Arriere" value="Arriere">
                    <input class="bouton" type="submit" name="Arriere D" value="ArriereD">
                </p>

                <p>
                    <input class="bouton" style="background-color: red; border-color: black;" type="submit" name="Photo" value="Photo">
                </p>

            </form>

        </div>

</div>


</body>
"""
PAGEACCUEIL = """
<html lang="en">
<div class="interaction">
        <form action="/" method="POST">

            <p>
                <input class="bouton" type="submit" name="submit" value="Inscription">
            </p>


        </form>

    </div>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <title></title>
</head>
<body>

    <div class="container-fluid p-5 bg-dark text-white text-center">
        <h1>RecoveryCar</h1>
        <div class="container">
        <h1>Les roues de l'espoir</h1>
            <!--mettre images qui alternent-->
        <p>Un monde infini de possibilites vous attendent</p>
        </div>
    </div>


</body>
</html>
"""

##Adresses ip
host_name = '10.150.134.79'
host_name_jg = '192.168.2.74'


#envoie les frames a afficher
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

#classe qui gere le streaming
class StreamingHandler(BaseHTTPRequestHandler):
    
    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()
    #dit quoi afficher en fonction de ce qui est demande
    def do_GET(self):
        
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/controle.html')
            self.end_headers()
        elif self.path == '/index.html':
            # on ecrit nos pages ici
            content = PAGEACCUEIL.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/Galerie.html':
            # on ecrit nos pages ici
            content = PAGEGALERIE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/controle.html':
            # on ecrit nos pages ici
            content = PAGECONTROLE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)

        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))

        else:
            self.send_error(404)
            self.end_headers()
    #dit quoi faire en fonction de l<information envoyee par les pages web
    def do_POST(self):
    
        etat = ''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8") 
        post_data = post_data.split("=")[1]
        
        if ModeAuto.autoEnabled == False:
            if post_data == 'Avant':
                Drivetrain.avancerTemps()
                etat = '/controle'
                
                                    
            elif post_data == 'AvantG':
                Drivetrain.avancerGaucheTemps()
                etat = '/controle'
            elif post_data == 'AvantD':
                Drivetrain.avancerDroiteTemps()
                etat = '/controle'
                
            elif post_data == 'Gauche':
                Drivetrain.tournerGaucheTemps()
                etat = '/controle'
            elif post_data == 'Droite':
                Drivetrain.tournerDroiteTemps()
                etat = '/controle'

            elif post_data == 'Arriere':
                Drivetrain.reculerTemps()
                etat = '/controle'
            elif post_data == 'ArriereG':
                Drivetrain.reculerGaucheTemps()
                etat = '/controle'
            elif post_data == 'ArriereD':
                Drivetrain.reculerDroiteTemps()
                etat = '/controle'

        if post_data == 'Photo':
            print('correct')
            etat = '/controle'
            #***************mettre dans une methode
            with output.condition:
                    #on prend La frame de la video
                    frame2 = output.frame
                    #on la transforme de bytes a image
                    img=Image.open(io.BytesIO(frame2))
                    #on la sauvegarde
                    img.save('/home/cedric/Desktop/image'+str(CompteurImage.cpt)+'.jpg')
                    analiserPhotos('/home/cedric/Desktop/image'+str(CompteurImage.cpt)+'.jpg')
                    #on modifie le compteur d image
                    setattr(CompteurImage,'cpt',CompteurImage.cpt+1)
            
        elif post_data == 'Autonome':
            ModeAuto.toggleAuto(self)
            etat = '/controle'
        elif post_data == 'Inscription':
            etat = '/controle'
        elif post_data == 'Conduite':
            etat = '/controle'
        elif post_data == 'Accueil':
            etat = '/index'
        elif post_data == 'Galerie':
            etat = '/Galerie'
        else:  # je vais retirer cette ligne à la fin, c'est juste pour éviter que le site crash à chaque fois qu'on clique sur un bouton pour lequel on a encore rien prévu
            self._redirect('/')
        print("RecoveryCar en Mode {}".format(post_data))
        print(etat)
        self.send_response(301)
        # Ici, on envoit nos inforamtions au path auquel mène le bouton aui a été cliqué
        self.send_header('Location', etat + '.html')
        self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = (host_name_jg, 8000)
        server = StreamingServer(address, StreamingHandler)
        print("lancement")
        server.serve_forever()
    finally:
        camera.stop_recording()
