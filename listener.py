import shutil
import os
import socketserver
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading
from provaCV import FunctionCV

threshold = 70

class Listener:
    loginFlag=False
    username=""
    password=""
    subjects = [""]
    stop=True

    class S(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def _html(self, message):
            f=open("site/index.html","r")
            content=f.read()
            return content.encode("utf8")

        def do_GET(self):
            self._set_headers()
            self.wfile.write(self._html("hi!"))

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            f=open("userCredential.txt","r")
            self._set_headers()
            
            if post_data.decode("utf-8").split("=")[1] == f.read().split(",")[1]:
                functionCV= FunctionCV()
                try:
                    functionCV.start()
                except:
                    try:
                        functionCV.start()
                    except:
                        try:
                            functionCV.start()
                        except:
                            ret=("<html><head><title>BioSecure</title><style type='text/css'>.title {position: relative;top: 180px}</style></head><body style='background-color:ff0000'><div id='title' align='center' class='title'><pre><font color='black' size='6' face='helvetica' >WARNING</font></pre></div></body></html>").encode('ascii')
                            f.close()
                            self.wfile.write(ret)
                            return
                detected = functionCV.getDetected()
                confidence = functionCV.getConfidence()
                print(confidence)
                if confidence < threshold:
                    ret=("<html><head><title>BioSecure</title><style type='text/css'>.title {position: relative;top: 180px}</style></head><body style='background-color:99ff66'><div id='title' align='center' class='title'><pre><font color='black' size='6' face='helvetica'>No Problem, your pc is being used by: "+ str(detected) +"</font></pre></div></body></html>").encode('ascii')
                    f.close()
                    self.wfile.write(ret)
                else:
                    ret=("<html><head><title>BioSecure</title><style type='text/css'>.title {position: relative;top: 180px}</style></head><body style='background-color:ff0000'><div id='title' align='center' class='title'><pre><font color='black' size='6' face='helvetica' >WARNING</font></pre></div></body></html>").encode('ascii')
                    f.close()
                    self.wfile.write(ret)
                    return
            else:
                ret=("<html><body><pre>Wrong Password</pre></body></html>").encode('ascii')
                f.close()
                self.wfile.write(ret)

    def setFlag(self,flag):
        self.loginFlag=flag
        
    def getFlag(self):
        return self.loginFlag
    
    def setCredential(self, name, passw):
        self.username=name
        self.password=passw
        f=open("userCredential.txt","w")
        f.write(name+",")
        f.write(passw)
        f.close()
        
    def getName(self):
        return self.username

    def verifyLogin(self, user, passw):
        f=open("userCredential.txt","r")
        cont = f.readline().strip().split(',')
        self.username=cont[0]
        self.password=cont[1]
        f.close()
        return user == self.username and passw == self.password

    def addPhotos(self, name, photos):
        self.subjects.append(name)
        dirs = os.listdir("training-data")

        val=0
        for i in range(0, len(dirs)):
            val+=1

        folder_path="training-data/s"+str(val+1)
        os.mkdir(folder_path)
          
        for i in range(0,len(photos)):
            tmp = photos[i].split("/")
            photo_name=tmp[len(tmp)-1]
            shutil.move(photos[i], folder_path)
            os.rename(folder_path+"/"+photo_name, folder_path+"/"+str(i)+".jpg")
        
        f2=open("subjectList.txt","a")
        f2.write(","+name)
        f2.close()
        
    def start(self):
            self.stop = False
            port = 8080
            addr=socket.gethostbyname(socket.gethostname())
            server_class=HTTPServer
            handler_class=self.S
            server_address = (addr, port)
            httpd = server_class(server_address, handler_class)
            print(f"Starting httpd server on {addr}:{port}")
            p=threading.Thread(target=httpd.serve_forever)
            p.start()

    def stop(self):
            self.stop = True
                    
        
