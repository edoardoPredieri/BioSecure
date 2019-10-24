import shutil
import os
import socketserver
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import threading
from provaCV import FunctionCV



class Listener:
    loginFlag=False
    username=""
    password=""
    subjects = [""]

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
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            post_data = self.rfile.read(content_length) # <--- Gets the data itself
#verificare passw
            self._set_headers()
            functionCV= FunctionCV()
            try:
                functionCV.start()
            except:
                functionCV.start()
            detected = functionCV.getDetected()
            print(post_data)
            ret=("<html><body><pre>" + str(detected) + "</pre></body></html>").encode('ascii')
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
            port = 8080
            addr="localhost"
            server_class=HTTPServer
            handler_class=self.S

            server_address = (addr, port)
            httpd = server_class(server_address, handler_class)
            print(f"Starting httpd server on {addr}:{port}")
            p=threading.Thread(target=httpd.serve_forever)
            p.start()
            
                    
        
