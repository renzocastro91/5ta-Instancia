#Buscaminas con interfaz gráfica de consola
import os
import random 

class Elemento():
    def __init__(self):
        self.valor = None 

    def __str__(self):
        return self.valor

    def esElemento(self):
        return True

    def esBomba(self):
        return False 

    def setValor(self):
        self.valor = 0

    def getValor(self):
        return self.valor 

    def incrementarValor(self):
        self.valor = self.valor + 1
        
class Bomba(Elemento):
    def __init__(self):
        pass 

    def esElemento(self):
        return False 

    def esBomba(self):
        return True 
    
    def setValor(self):
        self.valor = 9

    def incrementarValor(self):
        pass 


class Celda():
    def __init__(self):
        self.celda = None 

    def __str__(self):
        return self.celda

    def getCelda(self):
        return self.celda
    
    def setCelda(self,unElemento):
        self.celda = unElemento 

class Tablero():
    def __init__(self):
        self.tableroOculto = None 
        self.tableroVisible = None 
        self.filas = None 
        self.columnas = None   
        self.cantMinas = None 
        self.minasOcultas = []
        self.dificultad = None

    def eligeDificultad(self):
        bandera = True
        while bandera:
            op = input('Ingrese la dificultad: 1- Fácil 2- Medio 3- Difícil: ')
            if op == '1':
                self.filas = 20
                self.columnas = 35
                self.cantMinas = 30
                bandera = False 
            elif op == '2':
                self.filas = 35
                self.columnas = 45
                self.cantMinas = 50
                bandera = False 
            elif op == '3':
                self.filas = 45
                self.columnas = 55
                self.cantMinas = 60
                bandera = False 
            else:
                print('Opción ingresada incorrecta') 

    def creaTablero(self):
        self.eligeDificultad()
        self.tableroOculto = []
        self.tableroVisible = []
        for i in range(self.filas):
            self.tableroOculto.append([])
            self.tableroVisible.append([])
            for j in range(self.columnas):
                elemento = Elemento()
                elemento.setValor()
                celda = Celda()
                celda.setCelda(elemento)
                self.tableroOculto[i].append(celda)
                self.tableroVisible[i].append('-')

    def colocaMinas(self):    
        numero = 0
        while numero < self.cantMinas: 
            y = random.randint(0,self.filas-1)
            x = random.randint(0,self.columnas-1)
            if self.tableroOculto[y][x].getCelda().getValor() != 9:
                bombaNueva = Bomba()
                bombaNueva.setValor()
                celda = Celda()
                celda.setCelda(bombaNueva)
                self.tableroOculto[y][x] = celda 
                numero += 1
                self.minasOcultas.append((y,x))

    def colocaPistas(self):
        for y in range(self.filas):
            for x in range(self.columnas):
                if self.tableroOculto[y][x].getCelda().getValor() == 9:
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if 0 <= y+i <= self.filas-1 and 0 <= x+j <= self.columnas-1:
                                if self.tableroOculto[y+i][x+j].getCelda().getValor() != 9:
                                    self.tableroOculto[y+i][x+j].getCelda().incrementarValor()

    def reemplazaCeros(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tableroVisible[i][j] == 0:
                    self.tableroVisible[i][j] = " "

        return self.tableroVisible

    def reemplazaNueves(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tableroOculto[i][j].getCelda().getValor() == 9:
                    self.tableroVisible[i][j] = "@"

        return self.tableroVisible
    
    def getTableroOculto(self):
        return self.tableroOculto

    def getTableroVisible(self):
        return self.tableroVisible

    def getFilas(self):
        return self.filas

    def getColumnas(self):
        return self.columnas

    def getMinasOcultas(self):
        return self.minasOcultas


class Buscaminas():
    def __init__(self,tableros):
        self.tableros = tableros 
        self.score = None 

    def muestraTablero(self,tablero):
        if tablero == self.tableros.getTableroVisible():
            print()
            for columna in range(self.tableros.getColumnas()+2):
                print('*', end=' ')
            print()
            for fila in tablero:
                print('*',end=" ")
                for elem in fila: 
                    print(elem, end=' ')
                print('*')
            for columna in range(self.tableros.getColumnas()+2):
                print('*', end=' ')
        else:
            print() 
            for fila in tablero:
                print('*',end=" ")
                for elem in fila: 
                    print(elem.getCelda().getValor(), end=' ')
                print('*')
            for columna in range(self.tableros.getColumnas()+2):
                print('*', end=' ')
    
    def rellenado(self,y,x,val):
        '''Recorre todas las casillas vecinas y comprueba si son ceros, si es así las descubre, y recorre las vecinas de estas, hasta encontrar casillas con pistas, que también 
        descubre'''

        ceros = [(y,x)]
        while len(ceros) > 0:
            y, x = ceros.pop()
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if 0 <= y+i <= self.tableros.getFilas()-1 and 0 <= x+j <= self.tableros.getColumnas()-1:
                        if self.tableros.getTableroVisible()[y+i][x+j] == val and self.tableros.getTableroOculto()[y+i][x+j].getCelda().getValor() == 0:
                            self.tableros.getTableroVisible()[y+i][x+j] = 0
                            self.sumaPuntos()
                            if (y+i, x+j) not in ceros:
                                ceros.append((y+i, x+j))
                        else: 
                            self.tableros.getTableroVisible()[y+i][x+j] = self.tableros.getTableroOculto()[y+i][x+j].getCelda().getValor()
        return self.tableros.getTableroVisible()

    def tableroCompleto(self,tablero,fil,col,val):
        '''Comprueba si el tablero no tiene ninguna casilla con el valor visible inicial'''
        for y in range(fil):
            for x in range(col):
                if tablero[y][x] == val:
                    return False 
        return True

    def presentacion(self):
        '''Pantalla de presentación'''

        os.system("cls")

        print("*****************************************************")
        print("*                                                   *")
        print("*                    BUSCAMINAS                     *")
        print("*                                                   *")
        print("*                 w/a/s/d - Moverse                 *")
        print("*                                                   *")
        print("*                     m - mostrar                   *")
        print("*                                                   *")
        print("*               b/v - marcar/desmarcar              *")
        print("*                                                   *")
        print("*****************************************************")
        print()
        input("'Enter' para empezar... ")

    def menu(self):
        '''Devuelve el movimiento u opción elegida por el usuario'''

        print()
        opcion = input("¿w/a/s/d  - m - b/v? ")
        return opcion

    def getTableros(self):
        return self.tableros

    def setScore(self):
        self.score = 0
    
    def sumaPuntos(self):
        self.score = self.score + 100

    def getScore(self):
        return self.score

def inicializacion_juego():
    tableros = Tablero()
    tableros.creaTablero()
    tableros.colocaMinas()
    tableros.colocaPistas()
    juego = Buscaminas(tableros)
    juego.setScore()
    juego.presentacion() 
    #Colocamos ficha inicial y mostramos tablero    
    y = random.randint(2, tableros.getFilas()-3)
    x = random.randint(2, tableros.getColumnas()-3)
    real = juego.getTableros().getTableroVisible()[y][x]
    juego.getTableros().getTableroVisible()[y][x] = "X"
    os.system("cls")
    print(f"Puntaje: {juego.getScore()} Puntos" )  
    juego.muestraTablero(juego.getTableros().getTableroVisible())
    minas_marcadas = []
    jugando = True

    return tableros, y, x, real, juego, minas_marcadas, jugando


#Programa principal
os.system("cls")
tableros, y, x, real, juego, minasMarcadas, jugando = inicializacion_juego()
listaJugadas = []

#Bucle principal
r = 's'

while r == 's':
    while jugando:
        mov = juego.menu()        
        if mov == "w":
            if y == 0:
                y = 0
            else:
                juego.getTableros().getTableroVisible()[y][x] = real 
                y -= 1
                real = juego.getTableros().getTableroVisible()[y][x]
                juego.getTableros().getTableroVisible()[y][x] = "X"
        elif mov == "s":
            if y == tableros.getFilas()-1:
                y = tableros.getFilas()-1
            else: 
                juego.getTableros().getTableroVisible()[y][x] = real 
                y += 1
                real = juego.getTableros().getTableroVisible()[y][x]
                juego.getTableros().getTableroVisible()[y][x] = "X"
        elif mov == "a":
            if x == 0:
                x = 0
            else: 
                juego.getTableros().getTableroVisible()[y][x] = real 
                x -= 1
                real = juego.getTableros().getTableroVisible()[y][x]
                juego.getTableros().getTableroVisible()[y][x] = "X"
        elif mov == "d":
            if x == tableros.getColumnas()-1:
                x = tableros.getColumnas()-1
            else: 
                juego.getTableros().getTableroVisible()[y][x] = real 
                x += 1
                real = juego.getTableros().getTableroVisible()[y][x]
                juego.getTableros().getTableroVisible()[y][x] = "X"
        elif mov == "b":
            if real == "-":
                juego.getTableros().getTableroVisible()[y][x] = "#"
                real = juego.getTableros().getTableroVisible()[y][x]
                if (y,x) not in minasMarcadas:
                    minasMarcadas.append((y,x))
        elif mov == "v":
            if real == "#":
                juego.getTableros().getTableroVisible()[y][x] = "-"
                real = juego.getTableros().getTableroVisible()[y][x]
                if (y,x) in minasMarcadas:
                    minasMarcadas.remove((y,x))
        elif mov == "m":
            if juego.getTableros().getTableroOculto()[y][x].getCelda().getValor() == 9:
                juego.getTableros().getTableroVisible()[y][x] = "@"
                jugando = False
            elif juego.getTableros().getTableroOculto()[y][x].getCelda().getValor() != 0:
                juego.getTableros().getTableroVisible()[y][x] = juego.getTableros().getTableroOculto()[y][x].getCelda().getValor()
                real = juego.getTableros().getTableroVisible()[y][x]
            elif juego.getTableros().getTableroOculto()[y][x].getCelda().getValor() == 0:
                juego.getTableros().getTableroVisible()[y][x] = 0
                juego.tableros.tableroVisible = juego.rellenado(y,x,"-")
                juego.tableros.tableroVisible = tableros.reemplazaCeros()          
                real = juego.getTableros().getTableroVisible()[y][x]

        os.system("cls")
        print(f"Puntaje: {juego.getScore()} Puntos" )
        juego.muestraTablero(juego.getTableros().getTableroVisible())
        
        ganas = False 
        
        if juego.tableroCompleto(juego.getTableros().getTableroVisible(),tableros.getFilas(),tableros.getColumnas(),"-") and  sorted(tableros.getMinasOcultas()) == sorted(minasMarcadas) and real != "-":
            ganas = True 
            jugando = False 
    if not ganas:
        os.system("cls")
        print()  
        juego.tableros.tableroVisible = tableros.reemplazaNueves()
        print(f"|| Puntaje: {juego.getScore()} Puntos Totales ||", end=" ")
        print('    || Has Perdido :( ||')
        juego.muestraTablero(juego.getTableros().getTableroVisible())
        print()                   
    else:
        os.system("cls")
        print()  
        juego.tableros.tableroVisible = tableros.reemplazaNueves()
        print(f"Puntaje: {juego.getScore()} Puntos Totales", end=" ")
        print('Has GANADO!!!! :)')
        juego.muestraTablero(juego.getTableros().getTableroVisible())
        print()  
        
    listaJugadas.append(juego.getScore())
    r = input("Desea continuar? s o n: ")
    if r == 's':        
        tableros, y, x, real, juego, minasMarcadas, jugando = inicializacion_juego()

print("---------------------------------------------------------------------------------")
print("Muchas gracias por Jugar")
cont = 1
print("---------------------------------------------------------------------------------")
print("Top de Jugadas")
print("---------------------------------------------------------------------------------")
listaJugadas.sort(reverse=True)
for jug in listaJugadas:    
    print(f"Top N° {cont}: {jug} Puntos")
    cont += 1