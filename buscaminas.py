#Buscaminas con interfaz gráfica de consola
import os
import random 

class Elemento():
    def __init__(self):
        self.valor = 0

    def __str__(self):
        return self.valor

    def esElemento(self):
        return True

    def esBomba(self):
        return False 

    def valor(self):
        return self.valor 

    def incrementarValor(self):
        self.valor = self.valor + 1


class Bomba(Elemento):
    def __init__(self):
        self.valor = 9

    def esElemento(self):
        return False 

    def esBomba(self):
        return True 

    def incrementarValor(self):
        pass 


class Tablero():
    def __init__(self):
        self.tableroOculto = None 
        self.tableroVisible = None 
        self.filas = None 
        self.columnas = None   
        self.cantMinas = None 
        self.minasOcultas = []

    def eligeDificultad(self):
        bandera = True
        while bandera:
            op = input('Ingrese la dificultad: 1- Fácil 2- Medio 3- Difícil: ')
            if op == '1':
                self.filas = 20
                self.columnas = 50
                self.cantMinas = 40
                bandera = False 
            elif op == '2':
                self.filas = 24
                self.columnas = 60
                self.cantMinas = 50
                bandera = False 
            elif op == '3':
                self.filas = 26
                self.columnas = 75
                self.cantMinas = 70
                bandera = False 
            elif op == '4':
                self.filas = 10
                self.columnas = 10
                self.cantMinas = 2
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
                self.tableroOculto[i].append(elemento)
                self.tableroVisible[i].append('-')

    def colocaMinas(self):    
        numero = 0
        while numero < self.cantMinas: 
            y = random.randint(0,self.filas-1)
            x = random.randint(0,self.columnas-1)
            if self.tableroOculto[y][x].esElemento():
                bombaNueva = Bomba()
                self.tableroOculto[y][x] = bombaNueva 
                numero += 1
                self.minasOcultas.append((y,x))

    def colocaPistas(self):
        for y in range(self.filas):
            for x in range(self.columnas):
                if self.tableroOculto[y][x].esBomba():
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if 0 <= y+i <= self.filas-1 and 0 <= x+j <= self.columnas-1:
                                if self.tableroOculto[y+i][x+j].esElemento():
                                    self.tableroOculto[y+i][x+j].incrementarValor()

    def reemplazaCeros(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tableroVisible[i][j] == 0:
                    self.tableroVisible[i][j] = " "

        return self.tableroVisible

    def reemplazaNueves(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tableroOculto[i][j].esBomba():
                    self.tableroVisible[i][j] = "@"

        return self.tableroVisible

    def tableroOculto(self):
        return self.tableroOculto

    def sTableroOculto(self,tablero):
        self.tableroOculto = tablero 

    def tableroVisible(self):
        return self.tableroVisible

    def sTableroVisible(self,tablero):
        self.tableroVisible = tablero 

    def filas(self):
        return self.filas

    def columnas(self):
        return self.columnas

    def minasOcultas(self):
        return self.minasOcultas


class Buscaminas():
    def __init__(self):
        self.tableros = None
        self.score = 0

    def inicializacion(self):
        self.tableros = Tablero()
        self.tableros.creaTablero()
        self.tableros.colocaMinas()
        self.tableros.colocaPistas()
        
    def muestraTablero(self,tablero):
        if tablero == self.tableros.tableroVisible:
            print()
            for columna in range(self.tableros.columnas+2):
                print('*', end=' ')
            print()
            for fila in tablero:
                print('*',end=" ")
                for elem in fila: 
                    print(elem, end=' ')
                print('*')
            for columna in range(self.tableros.columnas+2):
                print('*', end=' ')
    
    def rellenado(self,y,x,val):
        '''Recorre todas las casillas vecinas y comprueba si son ceros, si es así las descubre, y recorre las vecinas de estas, hasta encontrar casillas con pistas, que también 
        descubre'''

        ceros = [(y,x)]
        while len(ceros) > 0:
            y, x = ceros.pop()
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if 0 <= y+i <= self.tableros.filas -1 and 0 <= x+j <= self.tableros.columnas-1:
                        if self.tableros.tableroVisible[y+i][x+j] == val and self.tableros.tableroOculto[y+i][x+j].valor == 0:
                            self.tableros.tableroVisible[y+i][x+j] = 0
                            self.sumaPuntos(50)
                            if (y+i, x+j) not in ceros:
                                ceros.append((y+i, x+j))
                        else:
                            self.sumaPuntos(60) 
                            self.tableros.tableroVisible[y+i][x+j] = self.tableros.tableroOculto[y+i][x+j].valor
        return self.tableros.tableroVisible

    def tableroCompleto(self,val):
        '''Comprueba si el tablero no tiene ninguna casilla con el valor visible inicial'''
        for y in range(self.tableros.filas ):
            for x in range(self.tableros.columnas):
                if self.tableros.tableroVisible[y][x] == val:
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

    def gTableros(self):
        return self.tableros
    
    def sTableros(self,tableros):
        self.tableros = tableros 

    
    def sumaPuntos(self, unPuntaje):
        self.score = self.score + unPuntaje

    def score(self):
        return self.score


def inicializacion_juego():
    juego = Buscaminas()
    juego.inicializacion()
    juego.presentacion() 
    #Colocamos ficha inicial y mostramos tablero    
    y = random.randint(2, juego.tableros.filas - 3)
    x = random.randint(2, juego.tableros.columnas - 3)
    real = juego.tableros.tableroVisible[y][x]
    juego.tableros.tableroVisible[y][x] = "X"
    os.system("cls")
    print(f"Puntaje: {juego.score} Puntos" )  
    juego.muestraTablero(juego.tableros.tableroVisible)
    minas_marcadas = []
    jugando = True

    return  y, x, real, juego, minas_marcadas, jugando

#Programa principal
os.system("cls")
y, x, real, juego, minasMarcadas, jugando = inicializacion_juego()
listaJugadas = []
r = 's'

#Bucle principal
while r == 's':
    while jugando:
        mov = juego.menu()        
        if mov == "w":
            if y == 0:
                y = 0
            else:
                juego.tableros.tableroVisible[y][x] = real 
                y -= 1
                real = juego.tableros.tableroVisible[y][x]
                juego.tableros.tableroVisible[y][x] = "X"
        elif mov == "s":
            if y == juego.tableros.filas -1:
                y = juego.tableros.filas -1
            else: 
                juego.tableros.tableroVisible[y][x] = real 
                y += 1
                real = juego.tableros.tableroVisible[y][x]
                juego.tableros.tableroVisible[y][x] = "X"
        elif mov == "a":
            if x == 0:
                x = 0
            else: 
                juego.tableros.tableroVisible[y][x] = real 
                x -= 1
                real = juego.tableros.tableroVisible[y][x]
                juego.tableros.tableroVisible[y][x] = "X"
        elif mov == "d":
            if x == juego.tableros.columnas-1:
                x = juego.tableros.columnas-1
            else: 
                juego.tableros.tableroVisible[y][x] = real 
                x += 1
                real = juego.tableros.tableroVisible[y][x]
                juego.tableros.tableroVisible[y][x] = "X"
        elif mov == "b":
            if real == "-":
                juego.tableros.tableroVisible[y][x] = "#"
                real = juego.tableros.tableroVisible[y][x]
                if (y,x) not in minasMarcadas:
                    minasMarcadas.append((y,x))
        elif mov == "v":
            if real == "#":
                juego.tableros.tableroVisible[y][x] = "-"
                real = juego.tableros.tableroVisible[y][x]
                if (y,x) in minasMarcadas:
                    minasMarcadas.remove((y,x))
        elif mov == "m":
            if juego.tableros.tableroOculto[y][x].esBomba():
                juego.tableros.tableroVisible[y][x] = "@"
                jugando = False
            elif juego.tableros.tableroOculto[y][x].valor != 0:
                juego.tableros.gettableroVisible[y][x] = juego.tableros.tableroOculto[y][x].valor
                juego.sumaPuntos(60)
                real = juego.tableros.tableroVisible[y][x]
            elif juego.tableros.tableroOculto[y][x].valor == 0:
                juego.tableros.tableroVisible[y][x] = 0
                juego.tableros.sTableroVisible(juego.rellenado(y,x,"-"))  
                juego.tableros.sTableroVisible(juego.tableros.reemplazaCeros())           
                real = juego.tableros.tableroVisible[y][x]

        os.system("cls")
        print(f"Puntaje: {juego.score} Puntos" )
        juego.muestraTablero(juego.tableros.tableroVisible)
        
        ganas = False 
        
        if juego.tableroCompleto("-") and  sorted(juego.tableros.minasOcultas()) == sorted(minasMarcadas) and real != "-":
            ganas = True 
            jugando = False 
    if not ganas:
        os.system("cls")
        print()  
        juego.tableros.sTableroVisible(juego.tableros.reemplazaNueves()) 
        print(f"|| Puntaje: {juego.score} Puntos Totales ||", end=" ")
        print('    || Has Perdido :( ||')
        juego.muestraTablero(juego.tableros.tableroVisible)
        print()                   
    else:
        os.system("cls")
        print()  
        juego.tableros.sTableroVisible(juego.tableros.reemplazaNueves()) 
        print(f"Puntaje: {juego.score} Puntos Totales", end=" ")
        print('Has GANADO!!!! :)')
        juego.muestraTablero(juego.tableros.tableroVisible)
        print()  
        
    listaJugadas.append(juego.score)
    r = input("Desea continuar? s o n: ")
    if r == 's':        
        y, x, real, juego, minasMarcadas, jugando = inicializacion_juego()

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