import tkinter as tki
from tkinter import font
import cv2
from PIL import Image, ImageTk
   
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
 
def bt_click():
    print("Click")


    


    



janela = tki.Tk()
janela.title("Almigthy eye")
janela["bg"] = "gray"

janela.bind('<Escape>', lambda e: janela.quit())

arial = font.Font(family='Arial', size=18, weight='normal')

def include_id():
    def show_frame():
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        camera.imgtk = imgtk
        camera.configure(image=imgtk)
        camera.after(10, show_frame)

    window = tki.Toplevel(janela)
    window.geometry("1000x600+150+100")
    camera = tki.Label(window).pack()
    show_frame()


bt_cam = tki.Button(janela, width=19, text="Iniciar Câmera", font=arial,
                bg="LightBlue", highlightbackground="Black",
                highlightcolor="Black", command=bt_click)
bt_cam.place(x=20, y=250)

bt_id = tki.Button(janela, width=19, text="Incluir ID", font=arial,
                bg="LightBlue", highlightbackground="Black",
                highlightcolor="Black", command=include_id)
bt_id.place(x=20, y=300)

#<largura>x<altura>+<dist_esquerda>+<dist_topo>
janela.geometry("1000x600+150+100")

janela.mainloop()
