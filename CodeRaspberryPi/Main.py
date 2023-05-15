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
<html lang="en">
<head>
  <!-- Source thème: https://www.w3schools.com/bootstrap/bootstrap_theme_company.asp -->
  <title>RecoveryCar</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
  <link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

  <style>

  body {
    font: 400 15px Lato, sans-serif;
    line-height: 1.8;
    color: #818181;
  }
  h2 {
    font-size: 24px;
    text-transform: uppercase;
    color: #303030;
    font-weight: 600;
    margin-bottom: 10px;
  }
  h4 {
    font-size: 19px;
    line-height: 1.375em;
    color: #303030;
    font-weight: 400;
    margin-bottom: 30px;
  }
  .onglet{
    background-color: #04AA6D;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            margin-top: 20px;
  }
  .container-fluid {
    padding: 60px 50px;
  }

  .thumbnail {
    padding: 0 0 15px 0;
    border: none;
    border-radius: 0;
  }
  .thumbnail img {
    width: 100%;
    height: 100%;
    margin-bottom: 10px;
  }
  .carousel-control.right, .carousel-control.left {
    background-image: none;
    color: #F60000;
  }
  .carousel-indicators li {
    border-color: #F60000;
  }
  .carousel-indicators li.active {
    background-color: #F60000;
  }
  .item h4 {
    font-size: 19px;
    line-height: 1.375em;
    font-weight: 400;
    font-style: italic;
    margin: 70px 0;
  }
  .item span {
    font-style: normal;
  }



  .panel-footer .btn {
    margin: 15px 0;
    background-color: #F60000;
    color: #fff;
  }
  .navbar {
    margin-bottom: 0;
    background-color:  #00008B;
    z-index: 9999;
    border: 0;
    font-size: 12px !important;
    line-height: 1.42857143 !important;
    letter-spacing: 4px;
    border-radius: 0;
    font-family: Montserrat, sans-serif;
  }
  .navbar li a, .navbar .navbar-brand {
    color: #fff !important;
  }
  .navbar-nav li a:hover, .navbar-nav li.active a {
    color: #F60000 !important;
    background-color: #fff !important;
  }
  .navbar-default .navbar-toggle {
    border-color: transparent;
    color: #fff !important;
  }
  footer .glyphicon {
    font-size: 20px;
    margin-bottom: 20px;
    color: #F60000;
  }




  @keyframes slide {
    0% {
      opacity: 0;
      transform: translateY(70%);
    }
    100% {
      opacity: 1;
      transform: translateY(0%);
    }
  }
  @-webkit-keyframes slide {
    0% {
      opacity: 0;
      -webkit-transform: translateY(70%);
    }
    100% {
      opacity: 1;
      -webkit-transform: translateY(0%);
    }
  }
  @media screen and (max-width: 768px) {
    .col-sm-4 {
      text-align: center;
      margin: 25px 0;
    }
    .btn-lg {
      width: 100%;
      margin-bottom: 35px;
    }
  }
  @media screen and (max-width: 480px) {
    .logo {
      font-size: 150px;
    }
  }
  </style>
</head>

<body id="myPage" data-spy="scroll" data-target=".navbar" data-offset="60" style="text-align: center; background-color: #fff;">

<nav class="navbar navbar-default navbar-fixed-top">
  <div class="container">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#myPage">RecoveryCar</a>
    </div>
    <div class="collapse navbar-collapse" id="myNavbar">
      <ul class="nav navbar-nav navbar-right">
        <form action="/" method="POST">
            <p>
                <input class="onglet" type="submit" name="submit" value="Déconnexion">
                <input class="onglet" type="submit" name="submit" value="Galerie">



            </p>

    </form>
      </ul>
    </div>
  </div>
</nav>


<!-- division pour la camera et les controles -->
<div id="controleRobot" class="container-fluid text-center" style="margin-top: 5px;">

    <div class="row">
      <div class="col-sm-8">
          <div class="thumbnail">
              <img src="stream.mjpg" width="540" height="360" style="border: black inset 1px;"/>
          </div>
        </div>

<div class="col-sm-4">




<!-- nos differents boutons de deplacement -->

<form action="/" method="POST">

                <div style="border: #818181 1px solid; margin-top: 120px; padding: 25px; background-color: #f6f6f6;">

                    <p>
                        <input type="submit;" class="btn btn-primary" value="Mode autonome" style="margin: 7px;">
                    </p>

                    <p>
                      <input type="submit" class="btn btn-default"  value="Avant-Gauche" style="margin: 2px;background-color: #e3e3e3;">
                      <input type="submit" class="btn btn-default" value="Avant" style="margin: 2px;">
                      <input type="submit" class="btn btn-default"  value="Avant-Droite" style="margin: 2px;background-color: #e3e3e3;">
                    </p>


                    <p>
                      <input type="submit" class="btn btn-default"  value="Gauche" style="margin: 5px;">
                      <input type="submit" class="btn btn-default" value="Droite" style="margin: 5px;">
                    </p>

                    <p>
                      <input type="submit" class="btn btn-default"  value="Arrière-Gauche" style="background-color: #e3e3e3;">
                      <input type="submit" class="btn btn-default" value="Arrière" style="margin: 0px;">
                      <input type="submit" class="btn btn-default"  value="Arrière-Droite" style="background-color: #e3e3e3">
                    </p>

                    <p>
                      <input type="submit" class="btn btn-success"value="Prendre photo"; style="margin: 7px;">
                    </p>

</form>
            </div>
          </div>
    </div>

  </form>

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
