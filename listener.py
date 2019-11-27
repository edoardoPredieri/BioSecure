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
            
            def contrlPassw(passw):
                f=open("userCredential.txt","r")
                cont = f.readline().strip().split(',')
                while cont[0]!="":
                    if passw==cont[1]:
                        f.close()
                        return True
                    cont = f.readline().strip().split(',')   
                f.close()
                return False

            def getDetected(l):
                ret=""
                maxvalue=0
                for i in l:
                    if l.count(i) > maxvalue:
                        maxvalue=l.count(i)
                        ret=i
                return ret

            def getConfidence(s, ld, lc):
                minvalue=1000
                ret=0
                for i in range(len(ld)):
                    if ld[i]==s and  lc[i] != "" and float(lc[i]) < minvalue:
                        minvalue=float(lc[i])
                        ret=float(lc[i])
                return ret
                    
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self._set_headers()
            
            if contrlPassw(post_data.decode("utf-8").split("=")[1]):
                detectedList=[]
                confidenceList=[]
                for i in range(3):
                    functionCV= FunctionCV()
                    try:
                        functionCV.start()
                    except:
                        try:
                            functionCV.start()
                        except:
                             None   
                    detectedList.append(functionCV.getDetected())
                    confidenceList.append(functionCV.getConfidence())
                    
                print(detectedList)
                print(confidenceList)
                detected=getDetected(detectedList)
                confidence=getConfidence(detected,detectedList, confidenceList)
                print("distance = "+str(confidence))
                if detected=="":
                    ret=("<html><head><title>BioSecure</title><style type='text/css'>.title {position: relative;top: 180px}</style></head><body style='background-color:ff0000'><div id='title' align='center' class='title'><pre><font color='black' size='6' face='helvetica' >WARNING</font></pre></div></body></html>").encode('ascii')
                    self.wfile.write(ret)
                    return
                else:
                    if confidence < threshold:
                        ret=("<html><head><title>BioSecure</title><style type='text/css'>.title {position: relative;top: 180px}</style></head><body style='background-color:99ff66'><div id='title' align='center' class='title'><pre><font color='black' size='6' face='helvetica'>No Problem, your pc is being used by: "+ str(detected) +"</font></pre></div></body></html>").encode('ascii')       
                        self.wfile.write(ret)
                    else:
                        ret=("<html><head><title>BioSecure</title><style type='text/css'>.title {position: relative;top: 180px}</style></head><body style='background-color:ff0000'><div id='title' align='center' class='title'><pre><font color='black' size='6' face='helvetica' >WARNING</font></pre></div></body></html>").encode('ascii')           
                        self.wfile.write(ret)
                        return
            else:
                ret=("<html><body><pre>Wrong Password</pre></body></html>").encode('ascii')     
                self.wfile.write(ret)

    def setFlag(self,flag):
        self.loginFlag=flag
        
    def getFlag(self):
        return self.loginFlag
    
    def setCredential(self, name, passw):
        self.username=name
        self.password=passw
        f=open("userCredential.txt","a")
        f.write(name+",")
        f.write(passw+"\n")
        f.close()
        
    def getName(self):
        return self.username

    def verifyLogin(self, user, passw):
        f=open("userCredential.txt","r")
        cont = f.readline().strip().split(',')
        while cont[0]!="":
            if user==cont[0] and passw==cont[1]:
                self.username=cont[0]
                self.password=cont[1]
                f.close()
                return True
            cont = f.readline().strip().split(',')
        f.close()
        return False

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
        f2.write(name+"(added by "+self.username+"),")
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
