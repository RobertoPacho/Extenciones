import sqlite3
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from PIL import Image, ImageTk
import os
import ast
import re
from tkinter import ttk

ancho=0
alto=0
panelImagenes=''
lienzo1=''
cpanel=1
#conexion con la base de datos
con = sqlite3.connect('BaseDatos/AraSuite.db')
cursorObj = con.cursor()

#Ubicamos los archivos que se encuentran en la base de datos
ruta = 'images/'

listaCarpeta = os.listdir(ruta)

#Creamos la ventana Principal en donde se mostrara todo el contenido
ventana = tk.Tk()
ventana.title("PICTOGRAMAS")
ventana.configure(bg='white')
ventana.grid_propagate(False)
#Identificamos la resolucion de la pantalla
def dimensiones():
    global ancho,alto
    #ancho = GetSystemMetrics(0) - 30
    #alto = GetSystemMetrics(1) - 150
    ancho = ventana.winfo_width()-30
    alto = ventana.winfo_height()-130

#highlightbackground='black', highlightthicknes=0.
panelscroll = tk.Frame(ventana)
panelscroll.place(y=70)
scrollbar=tk.Scrollbar(panelscroll)
panelscroll.grid_propagate(False)

def scrll_panel():
    global panelImagenes,ancho,alto,lienzo1
    dimensiones()
    #Usamos canvas como lienzo
    lienzo1=tk.Canvas(panelscroll,width=ancho, height=alto,background="black",yscrollcommand=scrollbar.set)
    scrollbar.config(command=lienzo1.yview)
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
    scrollbar.grid_propagate(False)#evitamos

    #Panel que ejecuta el scrollbar
    panelImagenes = tk.Frame(lienzo1,width=ancho, height=alto,background="blue")
    lienzo1.pack(side="left",fill="both",expand=True)
    lienzo1.grid_propagate(False)
    lienzo1.create_window(0,60,window=panelImagenes)
    return lienzo1

#extraemos todos los lenguajes disponibles en la base de datos
sql="select name from language"
cursorObj.execute(sql)
#etiquetamos el estado lenguajes aplicando tipos de letra y tamaño
fontStyle = tkFont.Font(family="Lucida Grande", size=12)
lenguaje=tk.Label(ventana,text='Idiomas:', font=fontStyle,bg='white')
lenguaje.place(x=40,y=2)

#Mostramos todos los lenguajes extraidos en el comboBox
comboBoxLenguaje = ttk.Combobox(ventana,values=cursorObj.fetchall(), justify='center')
comboBoxLenguaje.place(x=40, y=25)
comboBoxLenguaje.current(0)

#extraemos todos los tipos de imagenes disponibles de la base de datos
sql="select name from type"
cursorObj.execute(sql)

#etiquetamos la posicion en donde se mostrara los tipos de imagenes
tipo=tk.Label(ventana,text='Imagenes tipo:', font=fontStyle,bg='white')
tipo.place(x=200,y=2)

#Mostramos todos los tipos de imagenes disponibles en el comboBox
comboBoxTipo = ttk.Combobox(ventana,values=cursorObj.fetchall(),justify='center')
comboBoxTipo.place(x=200,y=25)
comboBoxTipo.current(6)


class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master = master
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth() - pad, master.winfo_screenheight() - pad))
        master.bind('<Escape>', self.toggle_geom)

    def toggle_geom(self, event):
        geom = self.master.winfo_geometry()
        print(geom, self._geom)
        self.master.geometry(self._geom)
        self._geom = geom

#Funcion que nos indicara el numero de paneles o limitar los paneles
def contador():
    global cuenta
    cuenta += 1


columna = 0
fila = 0
cuenta = 0

#funcion esta ejecuta
def paneles(event):
    global columna,cursor,fila,cuenta,ancho,panelImagenes,lienzo1,cpanel
    contador()
    print(cuenta)
    if(cuenta==1 & cpanel==1):
        scrll_panel()


    datos = ventana.winfo_width()

    npanes=round(ancho/135)
    #npanes=ancho//135
    print(npanes)
    if ancho == ancho:
        if columna == npanes:
            fila += 1
            columna = 0


    #codigo del panel contenedor label en donde se ingresara la imagen a mostrar
    panel = tk.Frame(panelImagenes, width=80, height=130, highlightbackground='black', highlightthicknes=0.5)
    panel.grid(row=fila, column=columna, padx=5, pady=3, ipadx=20, ipady=20)
    txto = Entry(panel, fg='black', bg='white', justify='center')
    txto.place(x=1, y=147, width=115)

    #Metodo compara el texto ingresado con la base de datos y existe mustra la imagen uvicada en la carpera de imagenes
    def imgpaneles(event):
        if comboBoxTipo.current() == 6:
            sql = "select name from main where word='" + txto.get() + "' and idL=" + str(
                comboBoxLenguaje.current()) + "  order by name desc"
        else:
            sql = "select name from main where word='" + txto.get() + "' and idL=" + str(
                comboBoxLenguaje.current()) + " and idT=" + str(comboBoxTipo.current()) + "  order by name desc"
        #sql = "select name from main where word='" + txto.get() + "' order by name desc"
        cursorObj.execute(sql)
        for name in cursorObj.fetchall():
            nombre = re.compile(r"\[.*\]")
            res = [ast.literal_eval(e) if isinstance(e, str) and nombre.fullmatch(e) else e for e in name]
            palabra1 = str(res)
            for item in listaCarpeta:
                palabra = "['" + item + "']"
                if palabra1 == palabra:
                    imagenB = "images/"+item
                    img = Image.open(imagenB)
                    new_img = img.resize((110, 140))
                    render = ImageTk.PhotoImage(new_img)
                    img1 = Label(panel, image=render)
                    img1.image = render
                    img1.place(x=1, y=1)

    columna += 1
    ventana.bind('<Key>', imgpaneles)
    ventana.bind('<Tab>', paneles)
    ventana.update()
    lienzo1.config(scrollregion=lienzo1.bbox("all"))

#Funcion que permire reconstruir el panel contenedor de imagenes
def generar(ventana):
    global columna,fila,cuenta,panelImagenes,cpanel
    columna = 0
    fila = 0
    cuenta = 0
    cpanel=2
    scrll_panel()

    return panelImagenes

#Funcion que permite eliminar todos los paneles creados
def limpiar():
    global panelImagenes
    global lienzo1
    panelImagenes.destroy()
    lienzo1.destroy()
    panelImagenes=generar(lienzo1)

#creacion y estilo del boton para limpiar
imgb = Image.open('limpiar.png')
new_imgb = imgb.resize((35, 40))
render1 = ImageTk.PhotoImage(new_imgb)
boton = Button(ventana, text="limpiar", command=limpiar,image=render1, bg='white')
boton.place(x=450, y=5)


ventana.bind('<Tab>', paneles)
ventana.update()
app = FullScreenApp(ventana)
ventana.mainloop()