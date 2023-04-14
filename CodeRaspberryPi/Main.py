import io
import picamera
import logging
import socketserver
from threading import Condition
from Drivetrain import Drivetrain
from ModeAuto import ModeAuto
from ModeTele import ModeTele
from http.server import BaseHTTPRequestHandler, HTTPServer
#source du tutoriel pour faire apparaitre la video: https://youtu.be/RPZZZ6FSZuk
#Notre page Web,je vais l'ameliorer(personaliser)
PAGE="""\
<html>

<style>

.titreDiv {
    margin: 30px;
    border: black double 10px;
    text-align: center;
    width: auto;
    height: auto;
    background-color: EAEAEA;
}

.cameraDiv {
    margin: 10px;
    border: black solid 3px;
    text-align: center;
    background-color: EAEAEA;
    padding-bottom: 30px;
}


.mouvementDiv {
    margin: 10px;
    border: black ridge 3px;
    text-align: center;
    padding: 20px;
    background-color: EAEAEA;
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

<body style="background-color:C5C5C5">

    <head>
        <title>RecoveryCar Live</title>
    </head>

    <div class="titreDiv">
        <h1 style="text-decoration: underline overline; font-size: 70px;">RecoveryCar</h1>
        <h2 style="color: red;font-size: 50px; text-decoration: underline;">Live</h2>
    </div>
    

<! -- #boite d'image de la camera--> 
    <div class="cameraDiv">
        <h2 style="border: black 2px solid; border-left-width: 0px; border-right-width: 0px; background-color: DCDCDC;">Image en temps réel</h2>
        <img src="stream.mjpg" width="640" height="480" style="border: black inset 2px;"/>
    </div>


<! -- nos differents boutons de deplacement--> 
    <div class="mouvementDiv">
        <form action="/" method="POST">

            <p>
                <input class="bouton" type="submit" name="submit" value="Avant">
            </p>
               
            <p>
                <input class="bouton" type="submit" name="submit" value="Gauche">
                <input class="bouton" type="submit" name="submit" value="Droite">
            </p>

            <p>
                <input class="bouton" type="submit" name="submit" value="Arrière">
            </p>
            
        </form>

    </div>

</body>
</html>
"""
##Adresses ip
host_name='10.150.131.150'
host_name_jg='192.168.2.74'

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

class StreamingHandler(BaseHTTPRequestHandler):
    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
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
    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        post_data = post_data.split("=")[1]
        if post_data == 'Arriere':
            Drivetrain.reculer()
        if post_data=='Avant':
            Drivetrain.avancer()
        print("RecoveryCar en Mode {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url

class StreamingServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution='640x480', framerate=24) as camera:

    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('192.168.2.74', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
