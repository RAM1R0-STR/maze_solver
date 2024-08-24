import matplotlib.pyplot as plt
import numpy as np
import time

#CLASE CURSOR - DEFINE Y MANIPULA EL MOVIMIENTO ---->
class cursor:
    def __init__(self, sentido, char, posActual):
        self.sentido = sentido # En que sentido esta apuntando el personaje
        self.char = char # Caracter que representa el personaje en la impresion
        self.posActual = posActual # Posicion actual del personaje
        self.direccion = ("arriba", "izquierda", "abajo", "derecha") # Todas las direcciones posibles que puede tomar el personaje
        self.camino = [posActual]  # Almacenar el camino recorrido
        self.visitados = set([posActual])  # Para evitar ciclos

    #Define el siguiente movimiento del personaje
    def movimiento(self, direccion):
        if direccion == "arriba":
            return (self.posActual[0] - 1, self.posActual[1])
        elif direccion == "izquierda":
            return (self.posActual[0], self.posActual[1] - 1)
        elif direccion == "abajo":
            return (self.posActual[0] + 1, self.posActual[1])
        elif direccion == "derecha":
            return (self.posActual[0], self.posActual[1] + 1)

    #Devuelve True si el personaje pudo avanzar y modifica su nueva posicion
    def avanzar(self, lab, muros):
        #CAMBIOS DE DIRECCION ---->
        for direccion in self.direccion:
            posSiguiente = self.movimiento(direccion)
            #EVALUACION DE POSICION VALIDA ---->
            if(posSiguiente not in muros and 
                posSiguiente[0]<=len(lab[0])-1 and posSiguiente[1]<=len(lab[0])-1 and
                lab[posSiguiente[0]][posSiguiente[1]] != self.char and
                posSiguiente not in self.visitados and
                lab[posSiguiente[0]][posSiguiente[1]] != 'X' and posSiguiente[0]>=0 and 
                posSiguiente[1]>=0):
            #<---- EVALUACION DE POSICION VALIDA
                
                # Almacena la posicion valida
                self.posActual = posSiguiente
                self.camino.append(posSiguiente)
                self.visitados.add(posSiguiente)
                return True
        #<---- CAMBIOS DE DIRECCION
        return False  # No se pudo avanzar
#<---- CLASE CURSOR - DEFINE Y MANIPULA EL MOVIMIENTO

    #Evaluamos si es posible el retroceso y retrocedemos
    def retroceder(self):
        if len(self.camino) > 1:
            self.camino.pop()  # Retrocede un paso
            self.posActual = self.camino[-1]  # Retrocede la posición actual
            return True
        return False  # No hay más camino a retroceder

#Genera una lista de los muros del laberinto
def enlistarMuros(lab):
    muros_l = []
    for x in range(len(lab)):
        for y in range(len(lab[x])):
            if lab[x][y] == "X":
                muros_l.append((x, y))
    return muros_l

#Ubica la coordenada de la salida en el laberinto
def ubicarSalida(lab):
    ubiSalida = (0,0)
    for x in range(len(lab)):
        for y in range(len(lab[x])):
            if lab[x][y] == "S":
                ubiSalida=(x,y)
    return ubiSalida

#Ubica la coordenada de la entrada en el laberinto
def ubicarEntrada(lab):
    ubiEntrada = (0,0)
    for x in range(len(lab)):
        for y in range(len(lab[x])):
            if lab[x][y] == "E":
                ubiEntrada=(x,y)
    return ubiEntrada

#Realiza las impresiones del laberinto por la terminal
def imprimir(ubi, lab, char):
    for y in range(len(lab)):
        for x in range(len(lab[y])):
            if((y,x)==ubi):
                lab[y][x]=char
        print(lab[y])
    print("\n ")
    return lab

#FUNCION QUE DIBUJA EL RECORRIDO ---->
def display_lab(lab_graph, cursor_posicion):
    display_lab = lab_graph.copy()
    display_lab[cursor_posicion[0], cursor_posicion[1]] = 2  # Marcar la posición del jugador
    plt.imshow(display_lab, cmap="cividis", origin="upper")
    plt.xticks([]), plt.yticks([])
    plt.show()
#<---- FUNCION QUE DIBUJA EL RECORRIDO

#FUNCION PRINCIPAL PARA ENCONTRAR LA SALIDA ---->
def escape(lab,character):
    #GRAFICAR DIMENSIONES, OBSTACULOS Y MATRIZ DEL LABERINTO ---->
    filas, columnas = len(lab), len(lab[0])
    lab_graph = np.zeros((filas, columnas))
    muros = enlistarMuros(lab) # Definir los muros (lista de tuplas con coordenadas de los muros)
    for muro in muros:
        lab_graph[muro] = -3 
    #<---- DEFINIR DIMENSIONES, OBSTACULOS Y MATRIZ DEL LABERINTO
    cursor_obj = cursor(0, character, ubicarEntrada(lab))
    salida = ubicarSalida(lab)
    #BUSCADOR DE SALIDA ---->
    while cursor_obj.posActual != salida:  # Hasta que llegue a la salida
        if not cursor_obj.avanzar(lab, muros):  # Si puede avanzar
            if not cursor_obj.retroceder():  # Intenta retroceder, si no puede, se queda atrapado
                print("¡ CAMINO SIN SALIDA !")
                return
    #<---- BUSCADOR DE SALIDA
    #DIBUJAR CAMINO CORRECTO ----->
    for paso in range(len(cursor_obj.camino)):
        display_lab(lab_graph, cursor_obj.camino[paso])
        time.sleep(0.2)  # Pausa en segundo entre movimientos
    #<----- DIBUJAR CAMINO CORRECTO
    print("¡ SALIDA ENCONTRADA !")
    return
#<----FUNCION PRINCIPAL PARA ENCONTRAR LA SALIDA

# Ejemplo de laberinto que puede ser modificado.
lab1 = [
    ["X", "X", "X", "X", "X", "X", "X"],
    ["E", " ", "X", " ", " ", " ", "X"],
    ["X", " ", "X", " ", "X", " ", "X"],
    ["X", " ", " ", " ", "X", " ", "X"],
    ["X", "X", "X", "X", "X", "S", "X"]]

lab2 = [
['X', 'X', 'E', 'X', 'X', 'X', 'X', 'X'],
[' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
[' ', 'X', ' ', 'X', 'X', 'X', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', 'X', 'X', ' '],
['X', 'X', 'X', 'X', 'X', 'X', 'X', 'S']]


lab3 = [
['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X','X', 'X', 'X', 'X', 'X', 'X', 'X','X', 'X', 'X', 'X', 'X', 'X', 'X'],
['X', ' ', 'X', 'X', 'X', ' ', ' ', ' ',' ', ' ', ' ', ' ', ' ', 'X', ' ',' ', ' ', ' ', ' ', ' ', ' ', 'X'],
['X', ' ', ' ', 'X', 'X', ' ', 'X', ' ','X', ' ', 'X', 'X', 'X', 'X', ' ','X', 'X', ' ', 'X', 'X', ' ', 'X'],
['X', 'X', ' ', ' ', ' ', ' ', 'X', ' ','X', ' ', 'X', ' ', ' ', ' ', ' ','X', 'X', ' ', 'X', 'X', 'X', 'X'],
['X', 'X', ' ', 'X', 'X', 'X', 'X', ' ','X', 'X', 'X', ' ', 'X', ' ', 'X','X', 'X', ' ', 'X', ' ', ' ', 'X'],
['X', 'X', ' ', 'X', ' ', ' ', 'X', ' ','X', 'X', 'X', ' ', 'X', ' ', 'X','X', 'X', ' ', 'X', ' ', 'X', 'X'],
['X', ' ', ' ', 'X', 'X', ' ', 'X', ' ',' ', 'X', ' ', ' ', 'X', ' ', ' ',' ', ' ', ' ', 'X', ' ', 'X', 'X'],
['X', ' ', 'X', 'X', ' ', ' ', 'X', 'X',' ', 'X', ' ', 'X', 'X', ' ', 'X',' ', 'X', ' ', ' ', ' ', 'X', 'X'],
['X', ' ', ' ', 'X', ' ', 'X', 'X', 'X',' ', 'X', ' ', ' ', 'X', ' ', 'X',' ', 'X', 'X', 'X', ' ', 'X', 'X'],
['X', 'X', ' ', 'X', ' ', 'X', ' ', ' ',' ', 'X', 'X', ' ', 'X', 'X', 'X',' ', 'X', 'X', ' ', ' ', ' ', 'X'],
['X', 'X', ' ', 'X', ' ', 'X', ' ', 'X','X', 'X', 'X', ' ', 'X', 'X', 'X',' ', 'X', ' ', ' ', 'X', ' ', 'X'],
['E', ' ', ' ', 'X', ' ', 'X', ' ', 'X','X', 'X', 'X', ' ', 'X', ' ', 'X',' ', 'X', ' ', 'X', 'X', ' ', 'X'],
['X', 'X', ' ', 'X', ' ', 'X', ' ', 'X','X', ' ', ' ', ' ', 'X', ' ', 'X',' ', 'X', ' ', 'X', ' ', ' ', 'X'],
['X', 'X', ' ', 'X', ' ', 'X', ' ', ' ','X', ' ', 'X', 'X', 'X', ' ', 'X','X', 'X', ' ', 'X', ' ', 'X', 'X'],
['X', 'X', ' ', ' ', ' ', 'X', 'X', ' ','X', ' ', 'X', 'X', 'X', ' ', 'X','X', ' ', ' ', 'X', ' ', ' ', 'X'],
['X', 'X', ' ', 'X', ' ', 'X', 'X', ' ','X', ' ', 'X', ' ', ' ', ' ', ' ',' ', ' ', 'X', 'X', 'X', ' ', 'X'],
['X', ' ', ' ', 'X', ' ', 'X', 'X', ' ',' ', ' ', 'X', ' ', 'X', ' ', 'X','X', 'X', 'X', 'X', 'X', ' ', 'X'],
['X', 'X', 'X', 'X', ' ', 'X', 'X', ' ','X', 'X', 'X', ' ', 'X', ' ', 'X',' ', 'X', 'X', ' ', ' ', ' ', 'S'],
['X', 'X', ' ', ' ', ' ', 'X', ' ', ' ','X', ' ', ' ', ' ', 'X', ' ', 'X',' ', ' ', ' ', ' ', 'X', 'X', 'X'],
['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X','X', 'X', 'X', 'X', 'X', 'X', 'X','X', 'X', 'X', 'X', 'X', 'X', 'X'],]

escape(lab3,"R")