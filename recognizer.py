from ast import While
import cv2
from cv2 import *
import numpy as np
import face_recognition
import os
import time
from sendmail import send
from tkinter.messagebox import askyesno, showinfo

path = 'total_images'
images = []
classnames = []
mylist = os.listdir(path)
id = 0
print(mylist)

for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    images.append(curimg)
    classnames.append(os.path.splitext(cl)[0])
print(classnames)

def findencodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

encodelistknown = findencodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgs = cv2.resize(img,dsize=(30,30))
    imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facescurframe = face_recognition.face_locations(imgs)
    encodescurframe = face_recognition.face_encodings(img, facescurframe)

    for encodeface, faceLoc in zip(encodescurframe, facescurframe):
        matches = face_recognition.compare_faces(encodelistknown, encodeface)
        faceDis = face_recognition.face_distance(encodelistknown, encodeface)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classnames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),int(0.7))

        else:
            y1, x2, y2, x1 = faceLoc
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0), cv2.FILLED)
            # time.sleep(5)
            # cv2.putText(img,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),int(0.7))
            ret,frame = cap.read() # return a single frame in variable `frame`

            # while(True):
                # cv2.imshow('img1',frame) #display the captured image
            cv2.imwrite('Unrecognised'+str(1)+'.jpg', frame)
            # cv2.imwrite('./total_images/Unrecognised'+str(1)+'.jpg', frame)
                    # cv2.destroyAllWindows()
                    # break
            # time.sleep(300)
            send()
            answer = askyesno(title='Add Image', message='Would you like to add the image to the dataset?')
            if answer:
                old_path = r'/Unrecognised1.jpg'
                new_path = r'/total_images/Unrecognised1.jpg'
                os.rename(old_path, new_path)
                showinfo(title='Image Added', message='Image addition was successful.')
            else:
                cap.release()
                if os.path.exists("/home/cycobot/Desktop/A.S.S/Unrecognised1.jpg"):
                    os.remove("/home/cycobot/Desktop/A.S.S/nrecognised1.jpg")
            cap.release()

    cv2.imshow('webcam', img)
    cv2.waitKey(1)