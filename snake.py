import turtle
import time
import random

posponer = 0.1 # segundos
score = 0
high_score = 0

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

#Texto
texto = turtle.Turtle()
texto.speed(0)
texto.color("black")
texto.penup()
texto.hideturtle()
texto.goto(0,260)
texto.write("Score:  0     High Score: 0", align = "center", font = ("Courier", 24, "normal"))


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
		x = random.randint(-280,280)
		y = random.randint(-280,280)
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

	mov()
	time.sleep(posponer)