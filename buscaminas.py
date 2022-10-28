import matplotlib.pyplot as plt
import random
import math


class Casilla:
    def __init__(self):
        self.Visible = False            #Indica si la casilla es visible o no para el usuario
        self.TieneMina = False          #Indica si hay colocada una mina en esa posición
        self.MinaMarcada = False        #Indica si el jugador marcó una mina en esa posición
        self.NumMinasAdyacentes = 0     #Numero de minas en las casillas adyacentes, para pintar el numero

class Buscaminas:
    def __init__(self, tam, numMinas):
        self.Tamanio= tam               #Tamaño del tablero (Cuadrado)
        self.Tablero=[]                 #Matriz de casillas
        self.Pendientes = tam*tam       #Numero de celdas que quedan por visualizarse 
        self.Estado= ""                 #"P" = Perdido/ "G" = Ganado / "" = En juego
        self.XError = None              #Fila de la casilla que produjo el error (al perder)        
        self.YError = None              #Columna de la casilla que produjo el error (al perder)
        for fila in range(tam):
            f = []
            for j in range(tam):
                f.append(Casilla())
            self.Tablero.append(f)

        num = 0
        while num < numMinas:
            rndx = random.randint(0,tam - 1)
            rndy = random.randint(0,tam - 1)
            if not self.Tablero[rndx][rndy].TieneMina:
                self.Tablero[rndx][rndy].TieneMina = True 
                filaIni = max(rndx-1,0)
                filaFin = min(rndx+1,tam-1)
                colIni = max(rndy-1,0)
                colFin = min(rndy+1,tam-1)
                for i in range(filaIni, filaFin+1, 1):
                    for j in range(colIni,colFin+1,1):
                        if i!= rndx or j != rndy:
                            self.Tablero[i][j].NumMinasAdyacentes +=1
                num += 1
        
    def Pintar(self):
        if self.Estado == "G":
            plt.suptitle("Has Ganado!!!")
        elif self.Estado == "P":
            plt.suptitle("Has Perdido!!")
        else: 
            plt.suptitle("Pendientes: " + str(self.Pendientes))

        for n in range(self.Tamanio+1):
            plt.plot ([0,self.Tamanio],[n,n], color="black",linewidth=1)
            plt.plot ([n,n],[0,self.Tamanio], color="black",linewidth=1)
        
        for i in range(self.Tamanio):
            for j in range(self.Tamanio):
                px = j + 0.5
                py = self.Tamanio - (i + 0.5)
                if self.Tablero[i][j].Visible:
                    if self.XError == i and self.YError == j:
                        plt.plot([px],[py],linestyle='None', marker='.',markersize=11,color='red')
                    elif self.Tablero[i][j].MinaMarcada:
                        plt.plot([px],[py], linestyle='None', marker='.',markersize=8,color='blue')
                    elif self.Tablero[i][j].TieneMina:
                        plt.plot([px],[py], linestyle='None', marker='.',markersize=8,color='orange')
                    else:
                        if self.Tablero[i][j].NumMinasAdyacentes != 0:
                            plt.text(px,py,str(self.Tablero[i][j].NumMinasAdyacentes), horizontalalignment = 'center', verticalalignment = 'center', color = 'gray', fontsize=12)
                else: 
                    plt.plot([px],[py], linestyle='None', marker='.',markersize=4,color='black')   
             
    def Limpiar(self,x,y):
        CLimpiar = [[x,y]]
        while len(CLimpiar) != 0:
            [x,y] = CLimpiar.pop(0)
            for i in range(max(x-1,0), min(x+1,self.Tamanio-1) + 1, 1):
                for j in range(max(y-1,0), min(y+1,self.Tamanio - 1) + 1, 1):
                    if not self.Tablero[i][j].Visible and not self.Tablero[i][j].TieneMina:
                        self.Pendientes -= 1
                        self.Tablero[i][j].Visible =True 
                        if self.Tablero[i][j].NumMinasAdyacentes == 0: CLimpiar.append([i,j])    

    def on_click (self,event):
        y = math.floor(event.xdata)
        x = self.Tamanio - math.floor(event.ydata) - 1
        if str(event.button) == "MouseButton.LEFT":
            if self.Tablero[x][y].TieneMina:
                self.Estado = "P"
                self.XError = x 
                self.YError = y
                for i in range(self.Tamanio):
                    for j in range(self.Tamanio):
                        self.Tablero[i][j].Visible = True 
            elif not self.Tablero[x][y].Visible:
                self.Tablero[x][y].Visible = True 
                self.Pendientes -= 1
                self.Limpiar(x,y)
        elif str(event.button) == "MouseButton.RIGHT":
            VAntes = self.Tablero[x][y].Visible
            self.Tablero[x][y].MinaMarcada = not self.Tablero[x][y].MinaMarcada
            if self.Tablero[x][y].MinaMarcada: self.Tablero[x][y].Visible = True 
            if VAntes and not self.Tablero[x][y].Visible: self.Pendientes += 1
            if not VAntes and self.Tablero[x][y].Visible: self.Pendientes -= 1
        if self.Pendientes == 0 : self.Estado = "G"
        plt.clf()
        self.Pintar()
        plt.draw()
        
#Programa principal

busca= Buscaminas(8, 15)
plt.connect('button_press_event',busca.on_click)
plt.ion()
busca.Pintar()
plt.draw()
plt.pause(100)
#plt.show()