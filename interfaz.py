from tkinter import *
from app import *

class Interfaz:

    def __init__(self,root):
        self.frame1 = Frame(root)
        self.frame2 = Frame(root)
        self.frame3 = Frame(root)

        self.fondo_inicio = Canvas(self.frame1)
        self.bot_inicio1 = Button(self.frame1)
        self.bot_inicio2 = Button(self.frame1)
        self.bot_inicio3 = Button(self.frame1)
        self.info_pie = Label(self.frame1)

        self.canvas = Canvas(self.frame2)

        self.fondo_final = Canvas(self.frame3)

        funcion = App(
            self.frame1,self.frame2,
            self.frame3,self.canvas)

#----------------------------------pantalla de inicio----------------------------------
        self.frame1.pack()

        self.img_inicio = funcion.imagen('templates/ob1.png',400,400)
        self.fondo_inicio.config(width=400,height=400)
        self.fondo_inicio.create_image(0,0, anchor='nw', image=self.img_inicio)
        self.fondo_inicio.pack()

        self.bot_inicio1.config(text='Jugar',border=4,command=lambda:funcion.iniciar_juego())
        self.bot_inicio1.place(x=180,y=120)

        self.bot_inicio2.config(text='Opciones',command=lambda:'x')
        self.bot_inicio2.place(x=170,y=180)

        self.bot_inicio3.config(text='Salir',command=lambda:'x')
        self.bot_inicio3.place(x=185,y=240)

        self.info_pie.config(text='By: Olaf Pedersen')
        self.info_pie.place(x=0,y=380)

#---------------------------------pantalla de juego----------------------------------
        self.frame2.pack()
        self.canvas.config(width=400,height=400,bg='black')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", funcion.seleccionar_celda) #El método bind se utiliza para vincular eventos a widgets "<Button-1>" se refiere a un clic del botón izquierdo del ratón.
        self.frame2.forget()     

#----------------------------------pantalla final-------------------------------------
        self.frame3.pack()
        self.img_final = funcion.imagen('templates/ob1.png',400,400)
        self.fondo_final.config(width=400,height=400)
        self.fondo_final.create_image(0,0, anchor='nw', image=self.img_inicio)
        self.fondo_final.pack()
        self.frame3.forget()

#-----------------------------------inicializar Tkinter------------------------------------
if __name__ == "__main__":
    root = Tk()
    juego = Interfaz(root)
    root.mainloop()
