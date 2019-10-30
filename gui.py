from tkinter import filedialog
from tkinter import *
from listener import Listener
from tkinter import messagebox

class Main:
    def start(self):
        self.btn["state"] = "normal"
        listener.start()
        
    def stop(self):
        listener.stop()

    def __init__(self, win):
        photos=[]
        nameI=Entry(win)
        nameI.insert(0, 'Add a new person')
        nameI.place(x=50, y=83)

        def addPhotos():
            for i in range(3):
                name=str(nameI.get())
                upload = Tk()
                upload.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
                photos.append(upload.filename)
                upload.destroy()
            listener.addPhotos(name,photos)
            photos.clear()
            
        self.lbl=Label(win, text="BioSecure", font=("Helvetica", 16))
        self.lbl.place(x=100, y=30)
        
        self.btn=Button(win, text="+",height = 1, command=addPhotos)
        self.btn.place(x=180, y=80)
        
        self.btn=Button(win, text="Logout" , command=win.quit)
        self.btn.place(x=150, y=110)
        self.btn=Button(win, text="Start" ,height = 1, width = 6 , command=self.start)
        self.btn.place(x=70, y=160)
        self.btn=Button(win, text="Stop",height = 1, width = 6 , state="disable", command=self.stop)
        self.btn.place(x=180, y=160)

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
            listener.setCredential(username, passw)
            listener.addPhotos("me",photos)
            photos.clear()
            win.quit()
        
        def addPhotos():
            for i in range(3):
                upload = Tk()
                upload.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
                photos.append(upload.filename)
                upload.destroy()
                self.btn["state"] = "normal"

        self.btn=Button(win, text="+", command=addPhotos)
        self.btn.place(x=160, y=60)
        self.btn=Button(win, text="Back", height = 1, width = 6, command=win.quit)
        self.btn.place(x=40, y=100)
        self.btn=Button(win, text="Confirm", height = 1, width = 6, state="disable", command=confirm)
        self.btn.place(x=110, y=100)


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
            if not listener.verifyLogin(username, passw):
                messagebox.showerror("Error", "Invalid Username or Password")
                return
            win.quit()
            
        self.btn=Button(win, text="Back" ,height = 1, width = 6, command=win.quit)
        self.btn.place(x=40, y=60)
        self.btn=Button(win, text="Confirm" ,height = 1, width = 6, command=confirm)
        self.btn.place(x=110, y=60)
                

class BaseLoginMain:
    def __init__(self, win):
        def login():
            windowL=Tk()
            mywin=LoginForm(windowL)
            windowL.title('LoginForm')
            windowWidth = windowL.winfo_reqwidth()
            windowHeight = windowL.winfo_reqheight()
            positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2 -100)
            positionDown = int(window.winfo_screenheight()/2 - windowHeight/2 -100)
            windowL.geometry("200x100+{}+{}".format(positionRight, positionDown))
            windowL.mainloop()
            windowL.destroy()
            if listener.getFlag:
                win.withdraw()
                windowM=Tk()
                mywin=Main(windowM)
                windowM.title('Main')
                windowWidth = windowM.winfo_reqwidth()
                windowHeight = windowM.winfo_reqheight()
                positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
                positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
                windowM.geometry("300x200+{}+{}".format(positionRight, positionDown))
                windowM.mainloop()
                windowM.destroy()

        def register():
            windowR=Tk()
            mywin=RegisterForm(windowR)
            windowR.title('RegisterForm')
            windowWidth = windowR.winfo_reqwidth()
            windowHeight = windowR.winfo_reqheight()
            positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2 -100)
            positionDown = int(window.winfo_screenheight()/2 - windowHeight/2 -100)
            windowR.geometry("200x150+{}+{}".format(positionRight, positionDown))
            windowR.mainloop()
            windowR.destroy()
            if listener.getFlag:
                win.withdraw()
                windowM=Tk()
                mywin=Main(windowM)
                windowM.title('Main')
                windowWidth = windowM.winfo_reqwidth()
                windowHeight = windowM.winfo_reqheight()
                positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
                positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
                windowM.geometry("300x200+{}+{}".format(positionRight, positionDown))
                windowM.mainloop()
                windowM.destroy()

        
        self.lbl=Label(win, text="BioSecure", font=("Helvetica", 16))
        self.lbl.place(x=100, y=50)
        self.btn=Button(win, text="Login" , command=login, height = 1, width = 6 )
        self.btn.place(x=90, y=100)
        self.btn=Button(win, text="Register" , command=register, height = 1, width = 6 )
        self.btn.place(x=170, y=100)

    
window=Tk()
mywin=BaseLoginMain(window)
listener=Listener()
window.title('Main')
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionRight = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(window.winfo_screenheight()/2 - windowHeight/2)
window.geometry("300x200+{}+{}".format(positionRight, positionDown))
window.mainloop()
