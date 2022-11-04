#Buscaminas con interfaz gráfica de consola

import random
import os 


class Celda():
    def __init__(self):
        self.valor_oculto = None 
        self.valor_visible = None 

    def es_celda(self):
        return True

    def es_bomba(self):
        return False

    def set_valores(self):
        self.valor_oculto = 0
        self.valor_visible = '-'

    def incrementar_val(self):
        self.valor_oculto += 1


class Bomba(Celda):

    def es_celda(self):
        return False

    def es_bomba(self):
        return True 
    
    def set_valores(self):
        self.valor_oculto = 9
        self.valor_visible = '@'

        

class Tablero():
    def __init__(self,filas,columnas,cantMinas):
        self.tablero_oculto = None 
        self.tablero_visible = None 
        self.fila = filas
        self.columna = columnas  
        self.cantMinas = cantMinas
        self.minasOcultas = []

    def crea_tablero(self):
        self.tablero_oculto = []
        self.tablero_visible = []
        for i in range(self.fila):
            self.tablero_oculto.append([])
            self.tablero_visible.append([])
            for j in range(self.columna):
                celda = Celda()
                celda.set_valores()
                self.tablero_oculto[i].append(celda)
                self.tablero_visible[i].append('-')  

    def coloca_minas(self):    
        numero = 0
        while numero < self.cantMinas: 
            y = random.randint(0,self.fila-1)
            x = random.randint(0,self.columna-1)
            if self.tablero_oculto[y][x].valor_oculto != 9:
                bomba_nueva = Bomba()
                bomba_nueva.set_valores()
                self.tablero_oculto[y][x] = bomba_nueva
                numero += 1
                self.minasOcultas.append((y,x))

    def coloca_pistas(self):
        for y in range(self.fila):
            for x in range(self.columna):
                if self.tablero_oculto[y][x].valor_oculto == 9:
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if 0 <= y+i <= self.fila-1 and 0 <= x+j <= self.columna-1:
                                if self.tablero_oculto[y+i][x+j].valor_oculto != 9:
                                    self.tablero_oculto[y+i][x+j].incrementar_val()

class Buscaminas():
    def __init__(self,tableros):
        self.tablero = tableros

    def muestra_tablero(self,tablero):
        if tablero == self.tablero.tablero_visible:
            for fila in tablero:
                print(end=" ")
                for elem in fila: 
                    print(elem, end=' ')
                print()
        else: 
            for fila in tablero:
                print(end=" ")
                for elem in fila: 
                    print(elem.valor_oculto, end=' ')
                print()

    def rellenado(self,y,x,val):
        '''Recorre todas las casillas vecinas y comprueba si son ceros, si es así las descubre, y recorre las vecinas de estas, hasta encontrar casillas con pistas, que también 
        descubre'''

        ceros = [(y,x)]
        while len(ceros) > 0:
            y, x = ceros.pop()
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if 0 <= y+i <= self.tablero.fila-1 and 0 <= x+j <= self.tablero.columna-1:
                        if self.tablero.tablero_visible[y+i][x+j] == val and self.tablero.tablero_oculto[y+i][x+j].valor_oculto == 0:
                            self.tablero.tablero_visible[y+i][x+j] = " "
                            if (y+i, x+j) not in ceros:
                                ceros.append((y+i, x+j))
                        else: 
                            self.tablero.tablero_visible[y+i][x+j] = self.tablero.tablero_oculto[y+i][x+j].valor_oculto
        return self.tablero.tablero_visible

    def tablero_completo(self,tablero,fil,col,val):
        '''Comprueba si el tablero no tiene ninguna casilla con el valor visible inicial'''
        for y in range(fil):
            for x in range(col):
                if tablero[y][x] == val:
                    return False 
        return True

#Funciones para la presentación del juego
def presentacion():
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

def inicializacion_juego(filas,columnas,cant_bombas):
    tableros = Tablero(filas,columnas,cant_bombas)
    tableros.crea_tablero()
    tableros.coloca_minas()
    tableros.coloca_pistas()
    presentacion()
    #Colocamos ficha inicial y mostramos tablero    
    y = random.randint(2, filas-3)
    x = random.randint(2, columnas-3)
    real = tableros.tablero_visible[y][x]
    tableros.tablero_visible[y][x] = "X"
    os.system("cls")
    juego = Buscaminas(tableros)   
    juego.muestra_tablero(juego.tablero.tablero_visible)
    minas_marcadas = []
    jugando = True

    return tableros, y, x, real, juego, minas_marcadas, jugando

def elige_dificultad():
    bandera = True
    while bandera:
        op = input('Ingrese la dificultad: 1- Fácil 2- Medio 3- Difícil: ')
        if op == '1':
            filas = 15
            columnas = 15
            cant_bombas = 10
            bandera = False 
        elif op == '2':
            filas = 20
            columnas = 20
            cant_bombas = 20
            bandera = False 
        elif op == '3':
            filas = 30
            columnas = 30
            cant_bombas = 35
            bandera = False 
        else:
            print('Opción ingresada incorrecta')

    return filas,columnas,cant_bombas


#Función que tiene el menú de movimiento
def menu():
    '''Devuelve el movimiento u opción elegida por el usuario'''

    print()
    opcion = input("¿w/a/s/d  - m - b/v? ")
    return opcion

#Programa principal
filas,columnas,cant_bombas = elige_dificultad()

tableros, y, x, real, juego, minas_marcadas, jugando = inicializacion_juego(filas,columnas,cant_bombas)

#Bucle principal
r = 's'

while r == 's':
    while jugando:
        mov = menu()        
        if mov == "w":
            if y == 0:
                y = 0
            else:
                tableros.tablero_visible[y][x] = real 
                y -= 1
                real = tableros.tablero_visible[y][x]
                tableros.tablero_visible[y][x] = "X"
        elif mov == "s":
            if y == filas-1:
                y = filas-1
            else: 
                tableros.tablero_visible[y][x] = real 
                y += 1
                real = tableros.tablero_visible[y][x]
                tableros.tablero_visible[y][x] = "X"
        elif mov == "a":
            if x == 0:
                x = 0
            else: 
                tableros.tablero_visible[y][x] = real 
                x -= 1
                real = tableros.tablero_visible[y][x]
                tableros.tablero_visible[y][x] = "X"
        elif mov == "d":
            if x == columnas-1:
                x = columnas-1
            else: 
                tableros.tablero_visible[y][x] = real 
                x += 1
                real = tableros.tablero_visible[y][x]
                tableros.tablero_visible[y][x] = "X"
        elif mov == "b":
            if real == "-":
                tableros.tablero_visible[y][x] = "#"
                real = tableros.tablero_visible[y][x]
                if (y,x) not in minas_marcadas:
                    minas_marcadas.append((y,x))
        elif mov == "v":
            if real == "#":
                tableros.tablero_visible[y][x] = "-"
                real = tableros.tablero_visible[y][x]
                if (y,x) in minas_marcadas:
                    minas_marcadas.remove((y,x))
        elif mov == "m":
            if tableros.tablero_oculto[y][x].valor_oculto == 9:
                tableros.tablero_visible[y][x] = "@"
                jugando = False
            elif tableros.tablero_oculto[y][x].valor_oculto != 0:
                tableros.tablero_visible[y][x] = tableros.tablero_oculto[y][x].valor_oculto
                real = tableros.tablero_visible[y][x]
            elif tableros.tablero_oculto[y][x].valor_oculto == 0:
                tableros.tablero_visible[y][x] = 0
                tableros.tablero_visible = juego.rellenado(y,x,"-")            
                real = tableros.tablero_visible[y][x]

        os.system("cls")
        
        juego.muestra_tablero(tableros.tablero_visible)
        
        ganas = False 
        
        if juego.tablero_completo(tableros.tablero_visible,filas,columnas,"-") and  sorted(tableros.minasOcultas) == sorted(minas_marcadas) and real != "-":
            ganas = True 
            jugando = False 
    if not ganas:
        print("************************************")
        print("------------------------------------")
        print("             HAS PERDIDO            ")
        print("------------------------------------")
    else: 
        print("------------------------------------")
        print("             HAS GANADO!!           ")
        print("------------------------------------")
        
    r = input("Desea continuar? s o n: ")
    if r == 's':
        filas,columnas,cant_bombas = elige_dificultad()
        tableros, y, x, real, juego, minas_marcadas, jugando = inicializacion_juego(filas,columnas,cant_bombas)






