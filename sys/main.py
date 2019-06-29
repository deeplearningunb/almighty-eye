from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import model

model.extract_embeddings()
model.train_DNN()


protoPath = os.path.join("dnn/deploy.prototxt")
modelPath = os.path.join("dnn/trained_model.caffemodel")
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
DNN = cv2.dnn.readNetFromTorch('openface_DNN_model.small2.v1.t7')
recognizer = pickle.loads(open('serializedFiles/recognizer.pickle', 'rb').read())
le = pickle.loads(open('serializedFiles/le.pickle', 'rb').read())

def iniciar_camera():
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

    fps = FPS().start()

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=600)
        (h, w) = frame.shape[:2]
        imageBlob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)
        detector.setInput(imageBlob)
        detections = detector.forward()

        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.6:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = frame[startY:endY, startX:endX]
                (fH, fW) = face.shape[:2]

                if fW < 20 or fH < 20:
                    continue

                faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                                                 (96, 96), (0, 0, 0), swapRB=True, crop=False)
                DNN.setInput(faceBlob)
                vec = DNN.forward()
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                text = "{}: {:.2f}%".format(name, proba * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              (0, 0, 255), 2)
                cv2.putText(frame, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        fps.update()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break


    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()


#iniciar_camera()

import tkinter as tki
from tkinter import font
import cv2
from PIL import Image, ImageTk
    
def bt_click():
    print("Click")

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    camera.imgtk = imgtk
    camera.configure(image=imgtk)
    camera.after(10, show_frame)
    

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


janela = tki.Tk()
janela.title("Almigthy eye")
janela["bg"] = "gray"

camera = tki.Label(janela)
camera.place(x=300, y=70)

janela.bind('<Escape>', lambda e: janela.quit())

arial = font.Font(family='Arial', size=18, weight='normal')

bt_cam = tki.Button(janela, width=19, text="Iniciar Câmera", font=arial,
                bg="LightBlue", highlightbackground="Black",
                highlightcolor="Black", command=iniciar_camera)
bt_cam.place(x=20, y=250)

bt_id = tki.Button(janela, width=19, text="Incluir ID", font=arial,
                bg="LightBlue", highlightbackground="Black",
                highlightcolor="Black", command=show_frame)
bt_id.place(x=20, y=300)

#<largura>x<altura>+<dist_esquerda>+<dist_topo>
janela.geometry("1000x600+150+100")

janela.mainloop()
