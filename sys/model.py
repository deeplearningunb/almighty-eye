#To extract_embeddings function
import imutils
from imutils import paths
import numpy as np
import pickle
import cv2
import os

#to train the DNN
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

def extract_embeddings():

    protoPath = os.path.join("dnn/deploy.prototxt")
    modelPath = os.path.join("dnn/trained_model.caffemodel")

    imagesPaths = list(paths.list_images('dataset'))
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
    DNN = cv2.dnn.readNetFromTorch('openface_DNN_model.small2.v1.t7')


    #Reading names and images from the dataset directory
    names = []
    faces = []
    for i, imagePath in enumerate(imagesPaths):

        name = imagePath.split(os.path.sep)[-2]
        image = cv2.imread(imagePath)
        image = imutils.resize(image , width=600)
        (h, w) = image.shape[:2]
        
        #TODO : BlobFromImage
            #Provide mean subusctraction , scaling and channel swapping
            
        imageBlob = cv2.dnn.blobFromImage(
            image = cv2.resize(image, (300, 300)),
            scalefactor = 1.0, swapRB= False, crop=False)

        #Using the DNN-based face detector localize faces
        detector.setInput(imageBlob)
        detections = detector.forward()


        if len(detections) > 0.8:

            i = np.argmax(detections[0, 0, :, 2])
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = image[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]
                if fW < 20 or fH < 20:
                    continue

                faceBlob = cv2.dnn.blobFromImage(face, 1.0/255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
                DNN.setInput(faceBlob)
                vector = DNN.forward()
                names.append(name)
                faces.append((vector.flatten()))

    data = {'faces': faces, 'names': names}
    fp = open('serializedFiles/faces.pickle', 'wb')
    fp.write(pickle.dumps(data))
    fp.close()
    return data



def train_DNN(data):
    data = pickle.loads(open('serializedFiles/faces.pickle', 'rb').read())

    le = LabelEncoder()
    labels = le.fit_transform(data['names'])

    recognize = SVC(C=1.0 , kernel='linear', probability=True)
    recognize.fit(data['faces'], labels)

    fp = open('serializedFiles/recognize.pickle', 'wb')
    fp.write(pickle.dumps(recognize))
    fp.close()


    fp = open('serializedFiles/le.pickle', "wb")
    fp.write(pickle.dumps(le))
    fp.close()

