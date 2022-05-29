import turtle
import time
import random

posponer = 0.1 # segundos

#creacion de ventana

wn = turtle.Screen() # objeto ventana
wn.title("Snake Game") # titulo 
wn.bgcolor("white") , # fondo 
wn.setup(width = 600, height = 600) # dimenciones en pixeles
wn.tracer(0) # algo placentero

# Cabeza de serpiente

cabeza = turtle.Turtle() # objeto Turtle
cabeza.speed(0)
cabeza.shape("square") # forma de cuadrado
cabeza.color("red")
cabeza.penup() # quitar rastro
cabeza.goto(0,0) # posicion inicial
cabeza.direction = "stop"

# Comida de serpiente

comida = turtle.Turtle() # objeto Turtle
comida.speed(0)
comida.shape("circle") # forma de cuadrado
comida.color("green")
comida.penup() # quitar rastro
comida.goto(0,100) # posicion inicial

# Cuerpo de la serpiente

segmentos=[]


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

#Teclado

wn.listen()
wn.onkeypress(arriba, "Up") # ejecuta la funcion "arriba" si se pulsa la tecla correspondiente
wn.onkeypress(abajo, "Down")
wn.onkeypress(izquierda, "Left")
wn.onkeypress(derecha, "Right")

#los juegos corren en bucles

while True:
	wn.update()

	if cabeza.distance(comida) < 20: #tamaño de los objetos 20x20p
		x = random.randint(-280,280)
		y = random.randint(-280,280)
		comida.goto(x,y)

		nuevo_segmento = turtle.Turtle() # objeto Turtle
		nuevo_segmento.speed(0)
		nuevo_segmento.shape("square") # forma de cuadrado
		nuevo_segmento.color("blue")
		nuevo_segmento.penup() # quitar rastro
		segmentos.append(nuevo_segmento)

	# Mover el cuerpo de la serpiente

	totalSeg = len(segmentos) # cantidad de segmentos
	for index in range(totalSeg -1, 0, -1): # iteracion desde totalSeg -1, hasta 0
		x = segmentos[index - 1].xcor()
		y = segmentos[index - 1].ycor()
		segmentos[index].goto(x,y)

	if totalSeg>0:
		x = cabeza.xcor()
		y = cabeza.ycor()
		segmentos[0].goto(x,y)

	mov()
	time.sleep(posponer)