import turtle
import time
import random

import os
from util import Nodo, PathFinder

# ---------- # PREPARATIVOS PARA EL CÓDIGO # -------------- #


# -- # Funciones, objetos y herramientas # -- #

# Función que limpia la consola
ClearConsole = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear")

posponer = 0.1 # segundos
score = 0
high_score = 0


# -- # Preparación de la API gráfica # -- #

#creacion de ventana
wn = turtle.Screen() # objeto ventana
wn.title("Snake Game") # titulo 
wn.bgcolor("black") , # fondo 
wn.setup(width = 600, height = 600) # dimenciones en pixeles
wn.tracer(0) # algo placentero

# Cabeza de serpiente
cabeza = turtle.Turtle() # objeto Turtle
cabeza.speed(0)
cabeza.shape("square") # forma de cuadrado
cabeza.color("green")
cabeza.penup() # quitar rastro
cabeza.goto(0,0) # posicion inicial
cabeza.direction = "stop"

# Comida de serpiente
comida = turtle.Turtle() # objeto Turtle
comida.speed(0)
comida.shape("circle") # forma de cuadrado
comida.color("red")
comida.penup() # quitar rastro
comida.goto(0,100) # posicion inicial

# Cuerpo de la serpiente
segmentos=[]

# Texto
texto = turtle.Turtle()
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0,260)
texto.write("Score:  0     High Score: 0", align = "center", font = ("Courier", 24, "normal"))


# -- # Funciones del juego # -- #

#Direcciones variables 
def arriba():
	cabeza.direction = "up"
def abajo():
	cabeza.direction = "down"
def izquierda():
	cabeza.direction = "left"
def derecha():
	cabeza.direction = "right"


#Funciones de movimiento
def mov():
	if cabeza.direction == "up":
		y = cabeza.ycor()
		cabeza.sety(y + 20)

	if cabeza.direction == "down":
		y = cabeza.ycor()
		cabeza.sety(y - 20)

	if cabeza.direction == "left":
		x = cabeza.xcor()
		cabeza.setx(x - 20)

	if cabeza.direction == "right":
		x = cabeza.xcor()
		cabeza.setx(x + 20)

# Teclado
wn.listen()
wn.onkeypress(arriba, "Up") # ejecuta la funcion "arriba" si se pulsa la tecla correspondiente
wn.onkeypress(abajo, "Down")
wn.onkeypress(izquierda, "Left")
wn.onkeypress(derecha, "Right")

# -- # Funciones de discretización # -- #

# SÍMBOLOS PARA LOS ELEMENTOS DEL JUEGO

CAB = "0"  # cabeza de la serpiente
CUE = "="  # cuerpo de la serpiente
COM = "%"  # comida
EMP = "-"

# Función que devuelve una matriz del tamaño del tablero de juego
def inicializar_matriz(n):

	# matriz estado de juego
	game_state = list()

	# por cada fila (total de n) creo una columna con n espacios
	for i in range(n):

		row = list()

		for j in range(n):

			row.append(EMP)
		
		game_state.append(row)
	
	return game_state


# Función que me devuelve el índice de la matriz dependiendo las coordenadas
def in_matriz(obj):
	return (int((obj.ycor() + 280) / 20), int((obj.xcor() + 280) / 20))

# Función que crea la matriz que representa el estado del juego,
# Devuelve la matriz estado de juego y las coordenadas de la cabeza y la comida
def discretizar_mundo(cabeza, snake, comida):

	game_state = inicializar_matriz(30)

	cabeza_x, cabeza_y = in_matriz(cabeza)
	comida_x, comida_y = in_matriz(comida)

	game_state[cabeza_x][cabeza_y] = CAB
	game_state[comida_x][comida_y] = COM

	# hago lo mismo para cada segmento del cuerpo 
	for segmento in snake:

		segmento_x, segmento_y = in_matriz(segmento)

		game_state[segmento_x][segmento_y] = CUE

	return (game_state[::-1], (cabeza_x, cabeza_y), (comida_x, comida_y))

# Función que imprime a consola el estado del juego
def print_game_state(GameState):

	for row in GameState:
		
		for element in row:

			print(element, end = " ")
		
		print("")


# -------------- # IMPLEMENTACIÓN IA # ----------------------- #

# Función que me devuelve los posibles movimientos dada una celda como cabeza
def cell_neighbors(GameState, node, explored):

	neighbors = list()

	node = node[::-1]

	instant_cells = [(node[0] - 1, node[1]), (node[0] + 1, node[1]), (node[0], node[1] + 1), (node[0], node[1] - 1)]

	for cell in instant_cells:

		if (GameState[cell[0]][cell[1]] == EMP) and (cell not in explored):
			neighbors.append(cell)
	
	return neighbors

# Función que implementa la el algoritmo de Djistkra (no sé cómo se escribe xD)
def path(GameState, cab_coords, com_coords):

	start = Nodo(cab_coords, None)	# EL nodo inicial es la cabeza del snake
	goal = com_coords               # La meta es la celda que contiene la comida

	pf = PathFinder()	# pf abreviación de PathFinder
	pf.add(start)		# Agregamos el nodo inicial al PathFinder


	# Se empieza la búsqueda del path
	while (True):
		explored = set()    # Set en donde guardaremos las celdas ya explorados
							# para optimizar la búsqueda

		# Si no hay nada en el path finder devolvemos None
		if (pf.empty()):
			return None

		# Tomamos un nodo de la fila
		node = pf.remove()

		# Si el nodo el la meta, devolvemos el path que llegó a él
		if (node.coords == goal):
			
			path = list()

			# Construimos el path
			while (node.parent != None):

				path.append(node.coords)
				node = node.parent

			print("Find path")
			print(f"head: {cab_coords}")
			return path[::-1]
		
		# Si no hemos llegado a la meta, expandimos los path
		else:
			
			explored.add(node.coords)

			# Exploramos cada una de los posibles caminos por turno
			for cell in cell_neighbors(GameState, node.coords, explored):
				
				# Agregamos al PathFinder ese nodo para que sea explorado
				# En siguientes iteraciones
				pf.add(Nodo(cell, node))

# Función que devuelve el movimiento a seguir por el snaje
def IA_mov(cab_coords, cell_to_move):

	x_mov = cell_to_move[0] - cab_coords[0]
	y_mov = cell_to_move[1] - cab_coords[1]

	print(f"x move: {x_mov}")
	print(f"y move: {y_mov}")

	direction = None

	if (x_mov == 1):
		direction = "right"
	if (x_mov == -1): 
		direction = "left"
	if (y_mov == -1):
		direction = "down"
	if (y_mov == 1):
		direction = "up"

	return direction

# -------------- # MAIN DEL JUEGO # ------------------------- #

#los juegos corren en bucles
while True:

	# Borramos la consola para dibujar el mapa
	ClearConsole()

	wn.update()

	# Pedimos la matriz estado de juego junto con las coordenadas de la cabeza 
	game_state, cab_coors, com_coors = discretizar_mundo(cabeza, segmentos, comida)
	print_game_state(game_state)


	# Colisiones bordes
	if cabeza.xcor() > 280:
		cabeza.setx(-280)
	if cabeza.xcor() < -280:
		cabeza.setx(280) 
	if cabeza.ycor() > 280:
		cabeza.sety(-280)
	if cabeza.ycor() < -280:
		cabeza.sety(280)

	# Colisiones comida

	if cabeza.distance(comida) < 20: #tamaño de los objetos 20x20p

		posible_starts = range(-280, 280, 20)

		x = random.choice(posible_starts)
		y = random.choice(posible_starts)
		comida.goto(x,y)

		nuevo_segmento = turtle.Turtle() # objeto Turtle
		nuevo_segmento.speed(0)
		nuevo_segmento.shape("square") # forma de cuadrado
		nuevo_segmento.color("blue")
		nuevo_segmento.penup() # quitar rastro
		segmentos.append(nuevo_segmento) # en una lista puedo guardar objetos, que putas

		# aumenta marcador

		score+=10

		if score > high_score:
			high_score=score

		texto.clear()
		texto.write("Score:  {}     High Score: {}".format(score,high_score)
										, align = "center", font = ("Courier", 24, "normal"))
	# colision con el cuerpo
	for segmento in segmentos:
		if segmento.distance(cabeza) < 20:
			time.sleep(1)
			cabeza.goto(0,0)
			cabeza.direction = "stop"

			#esconder los segmentos
			for segmento in segmentos:
				segmento.goto(1000,1000)

			segmentos.clear()

			score = 0
			texto.clear()
			texto.write("Score:  {}     High Score: {}".format(score,high_score)
										, align = "center", font = ("Courier", 24, "normal"))

	# Mover el cuerpo de la serpiente

	totalSeg = len(segmentos) # cantidad de segmentos
	for index in range(totalSeg -1, 0, -1): # iteracion en el intervalo [totalSeg -1, 0) reduciendo de 1 en 1
		x = segmentos[index - 1].xcor() # posicion del segmento superior
		y = segmentos[index - 1].ycor() 
		segmentos[index].goto(x,y) # el segmento posterior toma la posicion del superior

	if totalSeg>0:
		x = cabeza.xcor() # la cabeza es el eje fundamental
		y = cabeza.ycor()
		segmentos[0].goto(x,y)


	path_to_take = path(game_state, cab_coors, com_coors)

	print(f"path found: {path_to_take}")
	movToMake = IA_mov(cab_coors, path_to_take[0])
	cabeza.direction = movToMake

	print(f"Move to make: {movToMake}")
	input()
	mov()

	time.sleep(posponer)