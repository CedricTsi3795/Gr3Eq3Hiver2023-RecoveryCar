import io
from gpiozero import Motor
from time import sleep
import picamera
import logging
import socketserver
from threading import Condition
from http.server import BaseHTTPRequestHandler, HTTPServer
#source du tutoriel pour faire apparaitre la video:https://youtu.be/RPZZZ6FSZuk
#Notre page Web,je vais l'ameliorer(personaliser)
PAGE="""\
<html>

<body
style="width:960px; margin: 20px auto;">
<h1>RecoveryCar en action</h1>
<p>Bonjour, monsieur {}</p>
<form action="/" method="POST">
<! -- nos differents boutons de deplacement--> 
    Mouvement :
    <input type="submit" name="submit" value="Avant">
    <input type="submit" name="submit" value="Arriere">
    
    </form>
<head>
<title>Vision en temps reel</title>
</head>
<! -- #boite d'image de la camera--> 
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""
##Adresses ip
host_name='10.150.131.150'
host_name_jg='192.168.2.74'


moteurAvantDroite = Motor(9,10) #cable mauve sur 9, cable brun sur 10
moteurAvantGauche = Motor(11,12) #cable vert sur 11, cable bleu sur 12
moteurDerriereDroite = Motor(13,14) #cable bleu sur 13, cable vert sur 14
moteurDerriereGauche = Motor(16,18) #cable jaune sur 18, cable orange sur 16


##methodes pour bougerla voiture(incomplet)
def avancer():
    print("forward")
    moteurAvantDroite.forward()
    moteurAvantGauche.forward()
    moteurDerriereDroite.forward()
    moteurDerriereGauche.forward()
    sleep(1)

    print("stop")
    moteurAvantDroite.stop()
    moteurAvantGauche.stop()
    moteurDerriereDroite.stop()
    moteurDerriereGauche.stop()

def reculer():
    print("backwards")
    moteurAvantDroite.backward()
    moteurAvantGauche.backward()
    moteurDerriereDroite.backward()
    moteurDerriereGauche.backward()
    sleep(1)

    print("stop")
    moteurAvantDroite.stop()
    moteurAvantGauche.stop()
    moteurDerriereDroite.stop()
    moteurDerriereGauche.stop()

    

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
            reculer()
        if post_data=='Avant':
            avancer()
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