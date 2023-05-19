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
class Galerie:
    page = """
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
      .onglet {
                background-color: #04AA6D;
                color: white;
                padding: 14px 20px;
                margin: 8px 0;
                border: none;
                cursor: pointer;
                margin-top: 20px;
            }
      .jumbotron {
        background-color: #00008B;
        color: #fff;
        padding: 100px 25px;
        font-family: Montserrat, sans-serif;
      }
      .container-fluid {
        padding: 60px 50px;
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
        background-color: #00008B;
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
      .slideanim {visibility:hidden;}
      .slide {
        animation-name: slide;
        -webkit-animation-name: slide;
        animation-duration: 1s;
        -webkit-animation-duration: 1s;
        visibility: visible;
      }

    .img-fluid {
        margin: 30px;
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
                    <input class="onglet" type="submit" name="submit" value="Deconnexion">
                    <input class="onglet" type="submit" name="submit" value="Conduite">

                </p>

            </form>
          </ul>
        </div>
      </div>
    </nav>

    <div id="accueil" class="jumbotron text-center">
      <h1 style="text-shadow:1px 1px 2px black;">RecoveryCar</h1>
      <p style="color: #757575; font-size: 35px; text-shadow: 1px 1px 2px black;">Live</p>
    </div>



    <div id="galeriePhotos" class="container-fluid text-center" style="background-color: #f1f1f1;">

      <h1 style="text-shadow:1px 1px 2px black; color: #404040; padding: 25px; margin-bottom: 30px;">Galerie Photos</h1>

    <!-- définir les images sur le raspberry pi -->
    <img class="img-fluid" src="https://cdn.pixabay.com/photo/2023/05/11/05/40/blackbird-7985552_640.jpg" alt= "imgEUHHH" style=width:700px;height:700px;>
    <img class="img-fluid" src="file:///home/cedric/H23-Gr3-Eq2-RecoveryCar/H23-Gr3-Eq2-RecoveryCar/CodeRaspberryPi/ImagesFichier/image0.jpg" alt= "imgOrrrh" style=width:700px;height:700px;>


    """
#on cree notre objet galerie
galerie=Galerie() 

#Methode qui va nous permettre d'ecrire nos photos dans la page
def ecrireGalerie():
    # chemin d'acces
    folder_dir = "/home/cedric/H23-Gr3-Eq2-RecoveryCar/H23-Gr3-Eq2-RecoveryCar/CodeRaspberryPi/ImagesFichier"
    for fichiers in os.listdir(folder_dir):
        # si c'est une image, on ecrit les informations
        if fichiers.endswith(".jpg"):
            setattr(galerie, 'page', galerie.page + "<img class=" + "img-fluid" + " src=" + str(
                
                "/home/cedric/H23-Gr3-Eq2-RecoveryCar/H23-Gr3-Eq2-RecoveryCar/CodeRaspberryPi/ImagesFichier/image0.jpg")  + " alt=" + "img" + " style=" + "width:700px;height:700px;>")
        # si c'est le fichier txt, on écrit les informations
        #elif fichiers.endswith(".txt"):
          #  f=open(("CodeRaspberryPi/ImagesFichier/"+fichiers),"r")
           # setattr(galerie, 'page', galerie.page + "</h1>" + str(f.readlines()) + "</h1>")


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
                <input class="onglet" type="submit" name="submit" value="Deconnexion">
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



    <div style="border: #818181 1px solid; margin-top: 120px; padding: 25px; background-color: #f6f6f6;">
        <form action="/" method="POST">
            <p>         
                <input type="submit" class="btn btn-primary" name="submit" value="ModeAuto" style="margin: 7px;">
            </p>

            <p>
                <input type="submit" class="btn btn-default" name="submit" value="AvantG" style="margin: 2px;background-color: #e3e3e3">
                <input type="submit" class="btn btn-default" name="submit" value="Avant" style="margin: 2px">
                <input type="submit" class="btn btn-default" name="submit" value="AvantD" style="margin: 2px;background-color: #e3e3e3">
            </p>


            <p>
                <input type="submit" class="btn btn-default" name="submit" value="Gauche" style="margin: 5px">
                <input type="submit" class="btn btn-default" name="submit" value="Droite" style="margin: 5px">
            </p>

            <p>
                <input type="submit" class="btn btn-default"name="submit"  value="ArriereG" style="background-color: #e3e3e3">
                <input type="submit" class="btn btn-default" name="submit"value="Arriere" style="margin: 0px">
                <input type="submit" class="btn btn-default" name="submit" value="ArriereD" style="background-color: #e3e3e3">
            </p>

            <p>
                <input type="submit" class="btn btn-success" name="submit" value="Photo" style="margin: 7px">
            </p>

        </form>
        
    </div>  


"""
PAGEACCUEIL = """
<html>
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
            font-family: Arial, Helvetica, sans-serif;
        }

        /*  source pur le bouton de connexion: https://www.w3schools.com/howto/howto_css_login_form.asp */


        <
        style >
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

        .onglet {
            background-color: #04AA6D;
            color: white;
            padding: 14px 20px;
            margin: 8px 0;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }

        .jumbotron {
            background-color: #00008B;
            color: #fff;
            padding: 100px 25px;
            font-family: Montserrat, sans-serif;
        }

        .container-fluid {
            padding: 60px 50px;
        }

        .bg-grey {
            background-color: #f6f6f6;
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
            background-color: #00008B;
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

        .slide {
            animation-name: slide;
            -webkit-animation-name: slide;
            animation-duration: 1s;
            -webkit-animation-duration: 1s;
            visibility: visible;
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


        /* Full-width input fields */
        input[type=text], input[type=password] {
            width: 100%;
            padding: 12px 20px;
            margin: 8px 0;
            display: inline-block;
            border: 1px solid #ccc;
            box-sizing: border-box;
        }

        /* Set a style for all buttons */
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

        /* Extra styles for the cancel button */
        .cancelbtn {
            width: auto;
            padding: 10px 18px;
            background-color: #f44336;
        }

        /* Center the image and position the close button */


        .container {
            padding: 16px;
        }

        span.psw {
            float: right;
            padding-top: 16px;
        }

        /* The Modal (background) */
        .modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1; /* Sit on top */
            left: 0;
            top: 0;
            width: 100%; /* Full width */
            height: 100%; /* Full height */
            overflow: auto; /* Enable scroll if needed */
            background-color: #00008B; /* Fallback color */
            background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
            padding-top: 60px;
        }

        /* Modal Content/Box */
        .modal-content {
            background-color: #fefefe;
            margin: 5% auto 15% auto; /* 5% from the top, 15% from the bottom and centered */
            border: 1px solid #888;
            width: 80%; /* Could be more or less, depending on screen size */
        }


        .close:hover,
        .close:focus {
            color: red;
            cursor: pointer;
        }

        /* Add Zoom Animation */
        .animate {
            -webkit-animation: animatezoom 0.6s;
            animation: animatezoom 0.6s
        }

        @-webkit-keyframes animatezoom {
            from {
                -webkit-transform: scale(0)
            }
            to {
                -webkit-transform: scale(1)
            }
        }

        @keyframes animatezoom {
            from {
                transform: scale(0)
            }
            to {
                transform: scale(1)
            }
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

        /* Le bouton de connexion--> */

    </style>
</head>
<body data-spy="scroll" data-target=".navbar" data-offset="60" style="text-align: center; background-color: #fff;">

<nav class="navbar navbar-default navbar-fixed-top">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand">RecoveryCar</a>
        </div>
        <div class="collapse navbar-collapse" id="myNavbar">
            <ul class="nav navbar-nav navbar-right">
                <button onclick="document.getElementById('id01').style.display='block'" style="width:auto;">Connexion
                </button>


                </form>
            </ul>
        </div>
    </div>
</nav>

<div class="jumbotron text-center">
    <h1 style="text-shadow:1px 1px 2px black;">RecoveryCar</h1>
    <p style="color: #757575; font-size: 35px; text-shadow: 1px 1px 2px black;">Live</p>
</div>


<!-- Carrousel -->
<!-- Source : https://www.w3schools.com/bootstrap/bootstrap_theme_company.asp -->

<div class="container-fluid text-center bg-grey" style="margin: 100px; padding: 50px;">
    <h2>À propos</h2>
    <div id="myCarousel" class="carousel slide text-center" data-ride="carousel">
        <!-- Indicators -->
        <ol class="carousel-indicators">
            <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
            <li data-target="#myCarousel" data-slide-to="1"></li>
            <li data-target="#myCarousel" data-slide-to="2"></li>
        </ol>

        <!-- Wrapper for slides -->
        <div class="carousel-inner" role="listbox">
            <div class="item active">
                <h4 style="font-size: smaller;"><span style="font-size: large;"> Objectif du RecoveryCar</span>
                    <br><br>Le Recovery Car est un véhicule motorisé qui se déplace dans son environnement muni d'une
                    caméra.<br>Grâce à sa petite taille, il peut se déplacer dans des endroits étroits généralement
                    inaccessibles aux êtres humains.</h4>
            </div>
            <div class="item">
                <h4 style="font-size: smaller;"><span style="font-size: large;">Vision en temps réel</span>
                    <br><br>Le RecoveryCar est munis d'une caméra permettant d'avoir un retour d'images et de prendre
                    des photos en direct.</h4>
            </div>
            <div class="item">
                <h4 style="font-size: smaller;"><span style="font-size: large;">Analyse de l'environnement</span>
                    <br><br>Le RecoveryCar est aussi munis d'un logiciel de reconnaissance d'objets.<br>Il est donc en
                    mesure d'analyser l'environnement qui l'entoure.</h4>
            </div>
        </div>

        <!-- Left and right controls -->
        <a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
            <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
            <span class="sr-only">Previous</span>
        </a>
        <a class="right carousel-control" href="#myCarousel" role="button" data-slide="next">
            <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
            <span class="sr-only">Next</span>
        </a>
    </div>
</div>



<div id="id01" class="modal">

    <form class="modal-content animate"style="background-color:#87CEFA" action="/" method="POST">

        <div class="container">
            <label for="uname"style="color:#000000"><b>Indentifiant</b></label>
            <input type="text" placeholder="Entrez votre identifiant" name="uname" required>

            <label for="psw"style="color:#000000"><b>mot de Passe</b></label>
            <input type="password" placeholder="Entrez votre mot de passe" name="psw" required>
             <p>
                <input class="onglet" type="submit" name="submit" value="Connexion">


            </p>

        </div>

        <div class="container" style="background-color:#87CEFA">
            <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">
                Annuler
            </button>
        </div>
    </form>

</div>

<script>
    // Get the modal
    var modal = document.getElementById('id01');

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
</script>

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
            self.send_header('Location', '/index.html')
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
            content = galerie.page.encode('utf-8')
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
        l=1
        etat = ''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8") 
        print(post_data,"!!!!!")
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
                    #on l' analyse
                    img.save('/home/cedric/Desktop/image'+str(CompteurImage.cpt)+'.jpg')
                    #'image vient egalement dans le projet et on s en sert pour l affichage
                    analiserPhotos('/home/cedric/Desktop/image'+str(CompteurImage.cpt)+'.jpg')
                    #on modifie le compteur d image
                    setattr(CompteurImage,'cpt',CompteurImage.cpt+1)
            #on l'ecrit dans notre page galerie
            ecrireGalerie()
           #cause des erreurs 
        elif post_data == 'ModeAuto':
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
            ecrireGalerie()
            etat = '/Galerie'
        elif post_data == 'Connexion':
            # voici comment on va changer de page
            etat = '/controle'
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
