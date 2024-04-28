import os
import cv2
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import datetime

face_detector = cv2.CascadeClassifier('attendance_app/resources/haarcascade_frontalface_default.xml')
nimgs = 20

# get a number of total registered users
def totalreg():
    return len(os.listdir('attendance_app/static/faces'))

# extract the face from an image
def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []
    
# Identify face using ML model
def identify_face(facearray):
    model = joblib.load('attendance_app/static/face_recognition_model.pkl')
    return model.predict(facearray)

# A function which trains the model on all the faces available in faces folder
def train_model():
    faces = []
    labels = []
    userlist = os.listdir('attendance_app/static/faces')
    for user in userlist:
        for imgname in os.listdir(f'attendance_app/static/faces/{user}'):
            img = cv2.imread(f'attendance_app/static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'attendance_app/static/face_recognition_model.pkl')


# Our main Face Recognition functionality. 
# This function will run when we click on Mark Attendance Button.
def mark_attendance():
    
    ret = True
    cap = cv2.VideoCapture(0)
    id_number = ''
    while ret:
        ret, frame = cap.read()
        if len(extract_faces(frame)) > 0:
            (x, y, w, h) = extract_faces(frame)[0]
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            id_number = identified_person.split('_')[1]
            employee_name = identified_person.split('_')[0]

            if id_number:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 1)
                cv2.rectangle(frame, (x, y), (x+w, y-40), (0, 255, 0), -1)
                cv2.putText(frame, f'{employee_name}', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
                cv2.rectangle(frame, (x, y), (x+w, y-40), (0, 0, 255), -1)
                cv2.putText(frame, 'Not a Staff', (x+5, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Attendance', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

    return id_number
    

# A function to add a new user.
# This function will run when we add a new user.
def add_new_user(newusername, newuserid):
    userimagefolder = 'attendance_app/static/faces/'+newusername+'_'+str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                name = newusername+'_'+str(i)+'.jpg'
                cv2.imwrite(userimagefolder+'/'+name, frame[y:y+h, x:x+w])
                i += 1
            j += 1
        if j == nimgs*5:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    train_model()