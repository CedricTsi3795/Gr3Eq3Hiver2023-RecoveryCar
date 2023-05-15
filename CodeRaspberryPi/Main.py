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
##nos differentes pages
PAGEPHOTOS = """
<html>

<style>
header {
    background-color: 	#C0C0C0;
    text-align: center;
}
.photo {

    width: 225;
    height: 150;

    margin: 20px;

    border: black 2px groove;

    display: inline-block;



}
.onglet {

    border: 3px black inset ;
    border-radius: 10px;
    color: black;
    padding: 8px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    background-color:#C0C0C0 ;
    color: white;
    font-family: Verdana, Geneva, Tahoma, sans-serif;

}

    .mouvementDiv {
    border: black ridge 3px;
    text-align: center;

    width: auto;
    height: auto;

    margin-top: 40px;

    padding: 8px;
    background-color: #778899;
    display: inline-block;
}

</style>
<! -- Header de la page avec les differents onglets disponibles sur le site -- >
<header>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <title></title>
    <form action="/" method="POST">            
            <p>
                <input class="onglet" type="submit" name="submit" value="Deconnexion">
                <input class="onglet" type="submit" name="submit" value="Conduite">
                
                
            </p>
           
    </form>
</header>


<body style="background-color:#778899">
<! -- division qui montre le logo -- >

    <! -- Titre de la page -- >
<div class="container-fluid p-5   text-center ">
    
        
        <div class="container text-white bg-secondary p-3">
        <dt style=";border: black px solid; border-left-width: 0px; border-right-width: 0px; background-color: #778899; font-size: 24px;">Galerie photo</dt>
        <p style="display: inline-block;">

            <input class="onglet" type="submit" name="Sélectionner" value="Sélectionner" style="background-color: 0076FF;">
            <input class="onglet" type="submit" name="Télécharger" value="Télécharger" style="background-color: 00FF59;">
            <input class="onglet" type="submit" name="Supprimer" value="Supprimer" style="background-color: red;">
            <input class="onglet" type="submit" name="Annuler" value="Annuler">
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

        </p>
        

            
        
        </div>
</div>
    
<! -- division qui regroupe la camera et les boutons -- >

   



</div>

    
</body>

</html>
"""

PAGECONTROLE = """
<style>
header {
    background-color: 	#C0C0C0;
    text-align: center;
}
.onglet {

    border: 3px black inset ;
    border-radius: 10px;
    color: black;
    padding: 8px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    background-color:#C0C0C0 ;
    color: white;
    font-family: Verdana, Geneva, Tahoma, sans-serif;

}
.bouton {
    border: 2px black outset ;
    border-radius: 50px;
    color: black;
    padding: 2px px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 13px;
    margin: 2px;
    cursor: pointer;
    background-color: DCDCDC;
}
    .mouvementDiv {
    border: black ridge 3px;
    text-align: center;

    width: auto;
    height: auto;

    margin-top: 40px;

    padding: 8px;
    background-color: #778899;
    display: inline-block;
}

</style>
<! -- Header de la page avec les differents onglets disponibles sur le site -- >
<header>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <title></title>
    <form action="/" method="POST">            
            <p>
                <input class="onglet" type="submit" name="submit" value="Deconnexion">
                <input class="onglet" type="submit" name="submit" value="Galerie">
                
            </p>
           
    </form>
</header>


<body style="background-color:#778899">
<! -- division qui montre le logo -- >
<div class="container-fluid p-5 bg-secondary p-3 text-white text-center">
        
        <div class="container">
        <h1 style="text-decoration: ; font-size: 42px;">RecoveryCar</h1>
        <h2 style="color: red;font-size: 30px; text-decoration: underline;">Live</h2>
        <h3 style="text-decoration: ; font-size: 15px;">La suite entre vos mains</h1<3>
        </div>
    </div>
    <! -- Titre de la page -- >
<div class="container-fluid p-5   text-center ">
    
        
        <div class="container text-white bg-secondary p-3">
        <dt style=";border: black px solid; border-left-width: 0px; border-right-width: 0px; background-color: #778899; font-size: 24px;">Image en temps réel</dt>

            <img src="stream.mjpg" width="630" height="420" style="border: black inset 2px;"/>
            <! -- division des boutons -- >  
            <! -- nos differents boutons de deplacement -- >
        <div class="mouvementDiv">

            <form action="/" method="POST">

 

                <p>
                    <input class="bouton" type="submit" name="Mode" value="Autonome" style="background-color: 0076FF;">
                </p>

                <p>
                    <input class="bouton" type="submit" name="Avant" value="Avant">
                </p>
               

                <p>
                    <input class="bouton" type="submit" name="Gauche" value="Gauche">
                    <input class="bouton" type="submit" name="Droite" value="Droite">
                </p>

                <p>
                    <input class="bouton" type="submit" name="Arriere" value="Arriere">
                </p>
            
                <p>
                    <input class="bouton" style="background-color: red; border-color: black;" type="submit" name="Photo" value="Photo">
                </p>

            </form>

        </div>
        </div>
</div>
    
<! -- division qui regroupe la camera et les boutons -- >

   



</div>

    
</body>



"""
PAGEACCUEIL = """
<html lang="en">
<div class="interaction">
        <form action="/" method="POST">

            <p>
                <input class="bouton" type="submit" name="submit" value="Connexion">
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
        <p>Un monde infini  vous attend</p>
        </div>
    </div>
    <div class="container-fluid bg-secondary p-3 mt-3 text-center">
             <div id="demo" class="carousel slide" data-bs-ride="carousel">

  <!-- Indicators/dots -->
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#demo" data-bs-slide-to="0" class="active"></button>
    <button type="button" data-bs-target="#demo" data-bs-slide-to="1"></button>
    <button type="button" data-bs-target="#demo" data-bs-slide-to="2"></button>
  </div>
  
  <!-- The slideshow/carousel -->
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="https://cdn.pixabay.com/photo/2012/11/28/09/08/mars-67522_1280.jpg" alt="Los Angeles" class="d-block" style="width:100%; height=100">
    </div>
    <div class="carousel-item">
      <img src="https://cdn.pixabay.com/photo/2019/04/12/23/32/tank-caterpillar-4123566_1280.jpg" alt="Chicago" class="d-block" style="width:100%; height=100">
    </div>
    <div class="carousel-item">
      <img src="https://cdn.pixabay.com/photo/2016/03/04/19/36/gears-1236578_1280.jpg" alt="New York" class="d-block" style="width:100%; height=100">
    </div>
  </div>
  
  <!-- Left and right controls/icons -->
  <button class="carousel-control-prev" type="button" data-bs-target="#demo" data-bs-slide="prev">
    <span class="carousel-control-prev-icon"></span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#demo" data-bs-slide="next">
    <span class="carousel-control-next-icon"></span>
  </button>
</div> 
    </div>
 

<div class="container-fluid mt-3">
  <h3>Un projet indépendant</h3>
  <p>The following example shows how to create a basic carousel with indicators and controls.</p>
</div>


</body>
</html>
"""
# source:https://www.w3schools.com/howto/howto_css_login_form.asp
PAGECONNEXION = """
<html lang="en">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {font-family: Arial, Helvetica, sans-serif;}
form {border: 3px solid #f1f1f1;}

input[type=text], input[type=password] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

button {
  background-color: #04AA6D;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}

button:hover {
  opacity: 0.8;
}

.cancelbtn {
  width: auto;
  padding: 10px 18px;
  background-color: #f44336;
}





.container {
  padding: 16px;
}

span.psw {
  float: right;
  padding-top: 16px;
}

/* Change styles for span and cancel button on extra small screens */
@media screen and (max-width: 300px) {
  span.psw {
     display: block;
     float: none;
  }
  .cancelbtn {
     width: 100%;
  }
}
</style>
</head>
<style>
p {
  border: 2px solid powderblue;
  margin: 100px;
}
</style>
<div class="mt-4 p-5 bg-success p-3 text-white rounded">
    <h1>Inscription</h1>
    <form action="/" method="POST">    <div class="mb-3 ">
      <label for="uname"><b>Identifiant</b></label>
    <input type="text" placeholder="Entrez votre identifiant" name="uname" required>
    </div>
    <div class="mb-3">
      <label for="pwd" class="form-label">Mot de passe:</label>
      <input type="password" class="form-control" id="psw" placeholder="Entez votre mot de passe" name="psw" required>
    </div>

    <p>
            
            <button type="submit" class="btn btn-primary"value="Valider">Valider</button>
    </p>
  
  </form>

            

  
</div>
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
            content = PAGEPHOTOS.encode('utf-8')
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
        elif self.path == '/connexion.html':
            # on ecrit nos pages ici
            content = PAGECONNEXION.encode('utf-8')
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
        l=1
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
            #enlever inscription
        elif post_data == 'Inscription':
            etat = '/controle'
        elif post_data == 'Conduite':
            etat = '/controle'
        elif post_data == 'Accueil':
            etat = '/index'
        elif post_data == 'Galerie':
            etat = '/Galerie'
        elif post_data == 'Connexion':
            # voici comment on va changer de page
            etat = '/connexion'
        elif post_data == 'Deconnexion':
            etat = '/index'
        elif post_data == 'Valider':
            etat = '/controle'
        else:  
            #Mettre ça dans une méthode
            dernierscars=''
            longeur=len(post_data)
            counter = 0
            for c in post_data:  
                counter += 1  
                if longeur-counter<4:
                    dernierscars+=c
            print("chars extraits sont",dernierscars)
            if dernierscars=="&psw":
                etat='/controle'
                print("wow")
                
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
