import tkinter as tk
import cv2,os
import csv
import numpy as np
import pandas as pd
import datetime
import time
from tkinter import messagebox
from tkinter import *
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image

window = tk.Tk()
window.geometry("1150x650")
window.title("Smart Classroom")
style = ThemedStyle(window)
style.set_theme("smog")

image = Image.open('bg.jpg')
image = image.resize((1150, 650), Image.ANTIALIAS)
filename = ImageTk.PhotoImage(image)
background_label = Label(window, image=filename)
background_label.pack()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

x_cord = 50;
y_cord = 20;
checker=0;

# message = tk.Label(window, text="DIT UNIVERSITY" ,bg="white"  ,fg="black"  ,width=20  ,height=2,font=('Times New Roman', 25, 'bold'))
# message.place(x=1150, y=760)

message = tk.Label(window, text="Smart Classroom",fg="goldenrod2",bg='gray25',font=('Times New Roman', 35, 'bold underline'))
message.place(x=400, y=20)

lbl = tk.Label(window, text="Enter Your College ID",width=20  ,height=2  ,fg="black"  ,bg="Pink" ,font=('Times New Roman', 15, ' bold ') )
lbl.place(x=100-x_cord, y=180-y_cord)


txt = tk.Entry(window,width=30,bg="white" ,fg="blue",font=('Times New Roman', 15, ' bold '))
txt.place(x=80-x_cord, y=220-y_cord)

lbl2 = tk.Label(window, text="Enter Your Name",width=20  ,fg="black"  ,bg="pink"    ,height=2 ,font=('Times New Roman', 15, ' bold '))
lbl2.place(x=440-x_cord, y=180-y_cord)

txt2 = tk.Entry(window,width=30  ,bg="white"  ,fg="blue",font=('Times New Roman', 15, ' bold ')  )
txt2.place(x=420-x_cord, y=220-y_cord)

lbl3 = tk.Label(window, text="NOTIFICATION",width=20  ,fg="black"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 15, ' bold '))
lbl3.place(x=820-x_cord, y=180-y_cord)

message = tk.Label(window, text="" ,bg="white"  ,fg="blue"  ,width=30  ,height=1, activebackground = "white" ,font=('Times New Roman', 15, ' bold '))
message.place(x=770-x_cord, y=220-y_cord)

lbl3 = tk.Label(window, text="ATTENDANCE",width=20  ,fg="black"  ,bg="springgreen3"  ,height=1 ,font=('Times New Roman', 25, ' bold '))
lbl3.place(x=60-x_cord, y=550-y_cord)


message2 = tk.Label(window, text="" ,fg="gray26"   ,bg="salmon",activeforeground = "green",width=60  ,height=4  ,font=('times', 15, ' bold '))
message2.place(x=470-x_cord, y=510-y_cord)

lbl4 = tk.Label(window, text="STEP 1",width=20  ,fg="orangered"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
lbl4.place(x=60-x_cord, y=350-y_cord)

lbl5 = tk.Label(window, text="STEP 2",width=20  ,fg="orangered"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
lbl5.place(x=420-x_cord, y=350-y_cord)

lbl6 = tk.Label(window, text="STEP 3",width=20  ,fg="orangered"  ,bg="pink"  ,height=2 ,font=('Times New Roman', 20, ' bold '))
lbl6.place(x=780-x_cord, y=350-y_cord)
 
def clear1():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    if not Id:
        res="Please enter Id"
        message.configure(text = res)
        MsgBox = tk.messagebox.askquestion ("Warning","Please enter roll number properly , press yes if you understood",icon = 'warning')
        if MsgBox == 'no':
            tk.messagebox.showinfo('Your need','Please go through the readme file properly')
    elif not name:
        res="Please enter Name"
        message.configure(text = res)
        MsgBox = tk.messagebox.askquestion ("Warning","Please enter your name properly , press yes if you understood",icon = 'warning')
        if MsgBox == 'no':
            tk.messagebox.showinfo('Your need','Please go through the readme file properly')
        
    elif(is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            while(True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                    #incrementing sample number 
                    sampleNum=sampleNum+1
                    #saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                    #display the frame
                    cv2.imshow('frame',img)
                #wait for 100 miliseconds 
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum>60:
                    break
            cam.release()
            cv2.destroyAllWindows() 
            res = "Images Saved for ID : " + Id +" Name : "+ name
            row = [Id , name]
            with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)
            
    
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.write("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"
    clear1();
    clear2();
    message.configure(text= res)
    tk.messagebox.showinfo('Completed','Your model has been trained successfully!!')
    

def getImagesAndLabels(path):

    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    
    faces=[]

    Ids=[]

    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"))+1
                cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    res=attendance
    message2.configure(text= res)
    res = "Attendance Taken"
    message.configure(text= res)
    tk.messagebox.showinfo('Completed','Congratulations ! Your attendance has been marked successfully for the day!!')
    
def quit_window():
   MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
   if MsgBox == 'yes':
       tk.messagebox.showinfo("Greetings", "Thank You very much for using our software. Have a nice day ahead!!")
       window.destroy()
    
takeImg = tk.Button(window, text="IMAGE CAPTURE BUTTON", command=TakeImages  ,fg="black"  ,bg="dark turquoise"  ,width=25  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
takeImg.place(x=65-x_cord, y=400-y_cord)
trainImg = tk.Button(window, text="MODEL TRAINING BUTTON", command=TrainImages  ,fg="black"  ,bg="dark turquoise"  ,width=25  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
trainImg.place(x=425-x_cord, y=400-y_cord)
trackImg = tk.Button(window, text="ATTENDANCE MARKING BUTTON", command=TrackImages  ,fg="black"  ,bg="peachpuff"  ,width=30  ,height=2, activebackground = "pink" ,font=('Times New Roman', 15, ' bold '))
trackImg.place(x=780-x_cord, y=400-y_cord)
quitWindow = tk.Button(window, text="QUIT", command=quit_window  ,fg="white"  ,bg="red"  ,width=20 ,height=1, activebackground = "pink" ,font=('Times New Roman', 10, ' bold '))
quitWindow.place(x=1020-x_cord, y=630-y_cord)
 
window.mainloop()