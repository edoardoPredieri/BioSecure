from tkinter import filedialog
from tkinter import *
from listener import Listener

loginFlag=False
'''

class Listener:
    loginFlag=False
    Globalnome="default"
    
    def setName(self,name):
        self.Globalnome=name
        
    def getName(self):
        return self.Globalnome
'''

class Main:
    def start(self):
        print("start")
        
    def stop(self):
        print("stop")

    def __init__(self, win):
        photos=[]
        nameI=Entry(win)
        nameI.place(x=10, y=50)

        def addPhotos():
            for i in range(3):
                name=str(nameI.get())
    
                upload = Tk()
                upload.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
                photos.append(upload.filename)
                upload.destroy()

            print(name)
            for i in photos:
                print(i)

        
        self.lbl=Label(win, text="BioSecure", font=("Helvetica", 16))
        self.lbl.place(x=60, y=50)
        
        self.btn=Button(win, text="+", command=addPhotos)
        self.btn.place(x=100, y=50)
        
        self.btn=Button(win, text="Logout" , command=win.quit)
        self.btn.place(x=150, y=60)
        self.btn=Button(win, text="Start" , command=self.start)
        self.btn.place(x=80, y=80)
        self.btn=Button(win, text="Stop" , command=self.stop)
        self.btn.place(x=150, y=80)

class RegisterForm:
    def __init__(self, win):
        self.usernameL=Label(win, text="Username").grid(row=0)
        self.passwL=Label(win, text="Passw").grid(row=1)
        usernameI=Entry(win)
        usernameI.grid(row=0, column=1)
        passwI=Entry(win)
        passwI.grid(row=1, column=1)
        usernameI.insert(0,"")
        passwI.insert(0,"")
        self.lbl=Label(win, text="Insert at least 3 photos", font=("Helvetica", 8))
        self.lbl.place(x=40, y=60)
        photos=[]

        def confirm():
            username = str(usernameI.get())
            passw = str(passwI.get())
            for i in photos:
                print(i)
            print(username+" "+passw+" "+"me")
            listener.setName(username)
            win.quit()

        self.btn=Button(win, text="Confirm",state="disable", command=confirm)
        
        self.btn.place(x=100, y=100)
        
        def addPhotos():
            for i in range(3):
                upload = Tk()
                upload.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
                photos.append(upload.filename)
                upload.destroy()
                self.btn["state"] = "normal"

        self.btn=Button(win, text="+", command=addPhotos)
        self.btn.place(x=160, y=60)
        self.btn=Button(win, text="Back", command=win.quit)
        self.btn.place(x=30, y=100)
        self.btn=Button(win, text="Confirm",state="disable", command=confirm)
        self.btn.place(x=100, y=100)


class LoginForm:
    def __init__(self, win):
        self.usernameL=Label(win, text="Username").grid(row=0)
        self.passwL=Label(win, text="Passw").grid(row=1)
        usernameI=Entry(win)
        usernameI.grid(row=0, column=1)
        passwI=Entry(win)
        passwI.grid(row=1, column=1)
        usernameI.insert(0,"")
        passwI.insert(0,"")

        def confirm():
            username = str(usernameI.get())
            passw = str(passwI.get())
            print(username+" "+passw)
            win.quit()
        
       
        self.btn=Button(win, text="Back", command=win.quit)
        self.btn.place(x=30, y=60)
        self.btn=Button(win, text="Confirm", command=confirm)
        self.btn.place(x=100, y=60)
                

class BaseLoginMain:
    def __init__(self, win):
        def login():
            windowL=Tk()
            mywin=LoginForm(windowL)
            windowL.title('LoginForm')
            windowL.geometry("200x100+10+10")
            windowL.mainloop()
            windowL.destroy()

            print(listener.getName)
            if loginFlag:
                win.withdraw()
                windowM=Tk()
                mywin=Main(windowM)
                windowM.title('Main')
                windowM.geometry("300x100+10+10")
                windowM.mainloop()
                windowM.destroy()

        def register():
            windowR=Tk()
            mywin=RegisterForm(windowR)
            windowR.title('RegisterForm')
            windowR.geometry("200x200+10+10")
            windowR.mainloop()
            windowR.destroy()
           
            name=listener.getName()
            print(name)
            if loginFlag:
                win.withdraw()
                windowM=Tk()
                mywin=Main(windowM)
                windowM.title('Main')
                windowM.geometry("300x100+10+10")
                windowM.mainloop()
                windowM.destroy()

        
        self.lbl=Label(win, text="BioSecure", font=("Helvetica", 16))
        self.lbl.place(x=60, y=50)
        self.btn=Button(win, text="Login" , command=login)
        self.btn.place(x=80, y=100)
        self.btn=Button(win, text="Register" , command=register)
        self.btn.place(x=150, y=100)

    
window=Tk()
mywin=BaseLoginMain(window)
listener=Listener()
window.title('Main')
window.geometry("300x200+10+10")
window.mainloop()
