import cv2
import os
import numpy as np
import shutil


class FunctionCV:
    detected = ""
    confidence= ""
    
    def getDetected(self):
            return self.detected
    def getConfidence(self):
            return self.confidence
    
    def start(self):
        try:
            os.remove("test-data/test1.jpg")
        except:
            None
        
        f=open("subjectList.txt","r")
        subjects = f.read().split(",")

        #function to detect face using OpenCV
        def detect_face(img):
            #convert the test image to gray image as opencv face detector expects gray images
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            #load OpenCV face detector, I am using LBP which is fast
            face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')

            #let's detect multiscale (some images may be closer to camera than others) images
            #result is a list of faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
            
            #if no faces are detected then return original img
            if (len(faces) == 0):
                return None, None
            
            #under the assumption that there will be only one face,
            #extract the face area
            (x, y, w, h) = faces[0]
            
            #return only the face part of the image
            return gray[y:y+w, x:x+h], faces[0]

        #this function will read all persons' training images, detect face from each image
        #and will return two lists of exactly same size, one list 
        # of faces and another list of labels for each face
        def prepare_training_data(data_folder_path):
            
            #------STEP-1--------
            #get the directories (one directory for each subject) in data folder
            dirs = os.listdir(data_folder_path)
            
            #list to hold all subject faces
            faces = []
            #list to hold labels for all subjects
            labels = []
            
            #let's go through each directory and read images within it
            for dir_name in dirs:
                
                #our subject directories start with letter 's' so
                #ignore any non-relevant directories if any
                if not dir_name.startswith("s"):
                    continue;
                    
                #------STEP-2--------
                #extract label number of subject from dir_name
                #format of dir name = slabel
                #, so removing letter 's' from dir_name will give us label
                label = int(dir_name.replace("s", ""))
                
                #build path of directory containin images for current subject subject
                #sample subject_dir_path = "training-data/s1"
                subject_dir_path = data_folder_path + "/" + dir_name
                
                #get the images names that are inside the given subject directory
                subject_images_names = os.listdir(subject_dir_path)
                
                #------STEP-3--------
                #go through each image name, read image, 
                #detect face and add face to list of faces
                for image_name in subject_images_names:
                    
                    #ignore system files like .DS_Store
                    if image_name.startswith("."):
                        continue;
                    
                    #build image path
                    #sample image path = training-data/s1/1.pgm
                    image_path = subject_dir_path + "/" + image_name

                    #read image
                    image = cv2.imread(image_path)
                    
                    #display an image window to show the image 
                   # cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
                   # cv2.waitKey(100)
                    
                    #detect face
                    face, rect = detect_face(image)
                    
                    #------STEP-4--------
                    #for the purpose of this tutorial
                    #we will ignore faces that are not detected
                    if face is not None:
                        #add face to list of faces
                        faces.append(face)
                        #add label for this face
                        labels.append(label)
                    
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            cv2.destroyAllWindows()
            
            return faces, labels

        #data will be in two lists of same size
        #one list will contain all the faces
        #and other list will contain respective labels for each face
        
        faces, labels = prepare_training_data("training-data")
        

        #print total faces and labels
       # print("Total faces: ", len(faces))
     #   print("Total labels: ", len(labels))


        # This was probably the boring part, right? Don't worry, the fun stuff is coming up next. It's time to train our own face recognizer so that once trained it can recognize new faces of the persons it was trained on. Read? Ok then let's train our face recognizer. 

        # ### Train Face Recognizer
        #create our LBPH face recognizer 
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Now that we have initialized our face recognizer and we also have prepared our training data, it's time to train the face recognizer. We will do that by calling the `train(faces-vector, labels-vector)` method of face recognizer. 
        #train our face recognizer of our training faces
        face_recognizer.train(faces, np.array(labels))


        # **Did you notice** that instead of passing `labels` vector directly to face recognizer I am first converting it to **numpy** array? This is because OpenCV expects labels vector to be a `numpy` array. 
        # 
        # Still not satisfied? Want to see some action? Next step is the real action, I promise! 

        # ### Prediction

        # Now comes my favorite part, the prediction part. This is where we actually get to see if our algorithm is actually recognizing our trained subjects's faces or not. We will take two test images of our celeberities, detect faces from each of them and then pass those faces to our trained face recognizer to see if it recognizes them. 
        # 
        # Below are some utility functions that we will use for drawing bounding box (rectangle) around face and putting celeberity name near the face bounding box. 

        # In[8]:

        #function to draw rectangle on image 
        #according to given (x, y) coordinates and 
        #given width and heigh
        def draw_rectangle(img, rect):
            (x, y, w, h) = rect
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        #function to draw text on give image starting from
        #passed (x, y) coordinates. 
        def draw_text(img, text, x, y):
            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


        # First function `draw_rectangle` draws a rectangle on image based on passed rectangle coordinates. It uses OpenCV's built in function `cv2.rectangle(img, topLeftPoint, bottomRightPoint, rgbColor, lineWidth)` to draw rectangle. We will use it to draw a rectangle around the face detected in test image.
        # 
        # Second function `draw_text` uses OpenCV's built in function `cv2.putText(img, text, startPoint, font, fontSize, rgbColor, lineWidth)` to draw text on image. 
        # 
        # Now that we have the drawing functions, we just need to call the face recognizer's `predict(face)` method to test our face recognizer on test images. Following function does the prediction for us.

        # In[9]:

        #this function recognizes the person in image passed
        #and draws a rectangle around detected face with name of the 
        #subject
        def predict(test_img):
            #make a copy of the image as we don't want to chang original image
            img = test_img.copy()
            #detect face from the image
            face, rect = detect_face(img)

            #predict the image using our face recognizer 
            label, confidence = face_recognizer.predict(face)

            #get name of respective label returned by face recognizer
            label_text = subjects[label]
            
            self.detected=label_text            
            return label, confidence

        # Now that we have the prediction function well defined, next step is to actually call this function on our test images and display those test images to see if our face recognizer correctly recognized them. So let's do it. This is what we have been waiting for. 

        def takeSnapshotDark():
            key = cv2. waitKey(1)
            webcam = cv2.VideoCapture(0)
            while True:     
                check, frame = webcam.read() 
                key = cv2.waitKey(1)
                cv2.imwrite(filename='test1.jpg', img=frame)
                cv2.destroyAllWindows()
                break
            shutil.move("test1.jpg", "test-data")

        def takeSnapshotLight():
            camera_port = 0 
            ramp_frames = 30 
            camera = cv2.VideoCapture(camera_port)
            def get_image():
                 retval, im = camera.read()
                 return im 
            for i in range(ramp_frames):
                temp = camera.read()

            camera_capture = get_image()
            filename = "test1.jpg"
            cv2.imwrite(filename,camera_capture)
            del(camera)
            shutil.move("test1.jpg", "test-data")
        


        try:
            takeSnapshotLight()
            
            #load test images
            test_img1 = cv2.imread("test-data/test1.jpg")

            #perform a prediction
            pos, self.confidence = predict(test_img1)
        except:
            os.remove("test-data/test1.jpg")
            takeSnapshotDark()
            
            #load test images
            test_img1 = cv2.imread("test-data/test1.jpg")

            #perform a prediction
            pos, self.confidence = predict(test_img1)
        
        filelist = os.listdir("training-data/"+"s"+str(pos)) 
        number_files = len(filelist)
        threshold = 100/number_files
        
        
        if self.confidence < threshold:
            os.rename("test-data/test1.jpg", "test-data/"+str(number_files)+".jpg")
            shutil.move("test-data/"+str(number_files)+".jpg","training-data/"+"s"+str(pos))
        else:
            os.remove("test-data/test1.jpg")
        
        cv2.destroyAllWindows()
        return True

