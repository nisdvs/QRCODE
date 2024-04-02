import time, serial, sys, os, cv2
from tkinter import Tk, Frame, Label, font, PhotoImage
from scipy import *
from numpy import array
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import json
import locale
from datetime import datetime
import pandas as pd

locale.setlocale(locale.LC_ALL, "pt_BR")
today = datetime.now().strftime('%a')

camera_id = 0
delay = 1
window_name = 'OpenCV pyzbar'

alunos_dict = {}
alunos_data = pd.read_csv('./Lista.csv').to_dict()

for index in range(len(alunos_data.get('nome'))):
    alunos_dict[alunos_data['nome'][index]] = alunos_data['dias'][index].split(',') 

print(alunos_dict)

mGui = Tk()
mGui.geometry('600x600+0+0')
mGui.configure(background="#3a4447")
mGui.state('zoomed')
camFrame = Frame(mGui, width=435, height=475)
camFrame.place(x=100, y=70)
infoFrame = Frame(mGui, width=675, height=475, bg='#667174')
infoFrame.place(x=500, y=70)


cap = cv2.VideoCapture(camera_id)
ret, frame = cap.read()

v1 = Label(camFrame, text="QrCode Video")
v1.place(x=-80, y=-2)

almoco = 'Aponte o QR CODE a câmera para leitura:'
v2 = Label(infoFrame, text=almoco, background='#da251c', foreground='white', font=('Arial', 20, 'bold'))
v2.place(x=59, y=20)
v2.config(borderwidth=2, relief="solid")

def dddd():
    ret, frame = cap.read()
    global almoco
    if ret:
        for d in decode(frame):
            try:
                s = d.data.decode()
                json_data = json.loads(s)
                nome_aluno = json_data['nome']
                dias_almoco = json_data['comida']
                almoco = f'{nome_aluno} NAO LIBERADO(A)'
                if nome_aluno in alunos_dict.keys() and today in dias_almoco and dias_almoco in alunos_dict.values():
                        almoco = f'{nome_aluno} LIBERADO(A)'
                        v2.config(foreground='green') 
                else:
                    almoco = f'{nome_aluno} NAO LIBERADO(A)!'
                    v2.config(foreground='red')
            except Exception as e:
                print(e)
                pass
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    nimg = ImageTk.PhotoImage(image=img)
    
   

    image = Image.open("sesi.png")
    image.thumbnail((150, 150))
    photo = ImageTk.PhotoImage(image)


    image_label = Label(mGui, image=photo)
    image_label.image = photo 


    image_height = image.height 

    image_label.place(x=10, y=645 - image_height)  


    
    v1.n_img = nimg
    v1.configure(image=nimg)
    v2.config(text=almoco)
    
    mGui.after(10, dddd)
dddd()
mGui.mainloop()