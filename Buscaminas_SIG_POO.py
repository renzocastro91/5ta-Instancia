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

    def es_pista(self):
        return False 

    def set_valores(self):
        self.valor_oculto = 0
        self.valor_visible = '-'


class Bomba(Celda):
    def __init__(self):
        pass 

    def es_celda(self):
        return False

    def es_bomba(self):
        return True 

    def es_pista(self):
        return False
    
    def set_valores(self):
        self.valor_oculto = 9
        self.valor_visible = '@'


class Pista(Celda):
    def __init__(self):
        pass 

    def es_celda(self):
        return False

    def es_bomba(self):
        return False 

    def es_pista(self):
        return True

        

class Buscaminas():
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
                self.tablero_oculto[i].append(0)
                self.tablero_visible[i].append('-')  

    def coloca_minas(self):    
        numero = 0
        while numero < self.cantMinas: 
            y = random.randint(0,self.fila-1)
            x = random.randint(0,self.columna-1)
            if self.tablero_oculto[y][x] != 9:
                self.tablero_oculto[y][x] = 9
                numero += 1
                self.minasOcultas.append((y,x))

    def coloca_pistas(self):
        for y in range(self.fila):
            for x in range(self.columna):
                if self.tablero_oculto[y][x]== 9:
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if 0 <= y+i <= self.fila-1 and 0 <= x+j <= self.columna-1:
                                if self.tablero_oculto[y+i][x+j] != 9:
                                    self.tablero_oculto[y+i][x+j] += 1

class Interfaz():
    def __init__(self,buscaminas):
        self.tablero = buscaminas

    def muestra_tablero(self,tablero):
        for fila in tablero:
            print(end=" ")
            for elem in fila: 
                print(elem, end=' ')
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
                        if self.tablero.tablero_visible[y+i][x+j] == val and self.tablero.tablero_oculto[y+i][x+j] == 0:
                            self.tablero.tablero_visible[y+i][x+j] = 0
                            if (y+i, x+j) not in ceros:
                                ceros.append((y+i, x+j))
                        else: 
                            self.tablero.tablero_visible[y+i][x+j] = self.tablero.tablero_oculto[y+i][x+j]
        return self.tablero.tablero_visible
#Programa principal

tableros = Buscaminas(15,15,10)
tableros.crea_tablero()

tableros.coloca_minas()
tableros.coloca_pistas()
interfaz = Interfaz(tableros)
interfaz.muestra_tablero(interfaz.tablero.tablero_oculto)
