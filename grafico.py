import turtle
import tkinter
import puras

# globais
width = 400
height = 200
eixoX = None
eixoY = None
janela = None
tela = None
puloX = 10
puloY = 10
cores = ["blue", "yellow", 	"red"]
cores_zonas = ["red", "orange", "green", "blue", "grey"]
legenda_zonas = ["Máximo", "Intenso", "Moderado", "Leve", "Muito leve"]
legenda_grafico = ["Altitude", "BPMS", "Ritmo"]
graficos = None
idade = 1

def getPorcentagem(bpm):# Converte bpm em % de frequência cardíaca 
	return (bpm * 100) / (220 - idade)

def getBPM(porcentagem):# Converte % de frequência cardíaca em bpm
	return (porcentagem * (220 - idade)) // 100	


def getPontoX(x):# Pega o ponto x correspondente a escala
	global width, eixoX
	ponto = (x * (width * 2)) // eixoX
	ponto -= width

	return ponto

def getPontoY(y):# Pega o ponto y correspondente a escala
	global height, eixoY
	ponto = (y * (height * 2)) // eixoY
	ponto -= height

	return ponto

def barra(orientation, pontoX, pontoY): # Barras que delimita os intervalos do gráfico
	global tela
	if orientation == "horizontal":
		tela.goto(pontoX, pontoY - 8)

	tela.down()
	tela.goto(pontoX, pontoY)
	tela.up()
	tela.goto(pontoX, pontoY)

def intervalos(fazerY):# Intervalos do gráfico
	global janela, tela, width, height, pulo

	if fazerY:
		for y in range(int(eixoY), -1, -int(puloY)):
			tela.goto(-width - 5, getPontoY(y))
			tela.write(y, True, "right", ("Arial", 9, "bold"))
			barra("vertical", -width, getPontoY(y))

	tela.goto(-width, -height - 10)
	for x in range(int(puloX), int(eixoX) + 1, int(puloX)):
		tela.goto(getPontoX(x), -(height + 20))
		tela.write(x, True, "right", ("Arial", 9, "bold"))
		barra("horizontal", getPontoX(x), -height)

def planoCartesiano(): # Cria o plano
	global janela, tela, width, height

	tela.up()
	tela.goto(-width, height)
	tela.down()
	tela.goto(-width, -height)
	tela.goto(width, -height)

	tela.up()
	tela.goto(-width, height) # Move a turtle para o topo do eixo y
	 
def curva(x, y):# Desenha a curva do gráfico
	global tela
	for i in range(len(y)):
		if y[i] != None:
			tela.goto(getPontoX((x[i] - x[0]) / 60), getPontoY(y[i]))
			if i == 0:
				tela.down()

def zona_de_bpms(): # Delimita a zona do bpm no gráfico
	global tela, width, eixoX
	i = len(legenda_zonas) - 1
	for y in range(getBPM(50), eixoY, getBPM(10)):
		tela.goto(-width, getPontoY(y))
		if y < eixoY and i >= 0:
			tela.color(cores_zonas[i])
			barra("vertical", width + 10, getPontoY(y))
			tela.color("black")
			tela.write(legenda_zonas[i], True, "left", ("Arial", 12, "bold"))
			i -= 1
		else:
			break

def legenda_linha(i, y): # Desenha as cores do gráfico e os nomes, para a legenda
	global tela, width, cores

	tela.down()
	tela.color(cores[i])
	tela.goto(width + 60, y)
	tela.color("black")
	tela.write(legenda_grafico[i])


def legenda(): # Loop para desenhas as linhas da legenda (legenda_linha())
	global tela, width, height, cores
	i = 0
	for y in range(height - 60, height, 20):
		tela.goto(width + 20, y)
		if i < len(graficos):
			legenda_linha(graficos[i][2], y)
		i += 1
		tela.up()

def getTitle(info): # Pega o title quando o gráfico é da zona de bpm
	return info[0]

def getIdade(info): # Pega a idade para calcular a frequência cardíaca
	return info[1]

def criarGrafico(xys, info): # Método a ser chamado em funcoes.py
	global janela, tela, eixoX, eixoY, puloX, puloY, idade, cores, graficos

	try:
		janela = turtle.Screen()
		tela = turtle.Turtle()
		title = getTitle(info) if len(info) == 2 else info

		janela.title(title)
		janela.setup(width=.80, height=.70, startx=None, starty=None)
		tela.shape("blank")
		tela.speed(10)
		tela.pensize(3)
		graficos = xys
		for i, xy in enumerate(xys):
			x, y = xy[:2]
			eixoX = (int(puras.max(x)) - x[0]) / 60
			eixoY = int(puras.max(y))

			puloX = eixoX // 10 if eixoX >= 10 else 1
			puloY = eixoY // 10 if eixoY >= 10 else 1

			if i == 0:
				planoCartesiano()
				intervalos(len(xys) == 1)
				if "zona" in title.lower():
					idade = getIdade(info)
					zona_de_bpms()

				if "completo" in title.lower():
					legenda()

			if "completo" in title.lower():
				tela.color(cores[xy[2]])
			else:
				tela.color("blue")
			tela.pensize(2)
			curva(x, y)
			tela.up()
		janela.mainloop()

	except turtle.Terminator: # Conflito de instancia da Turtle()
		janela.clearscreen()
		criarGrafico(xys, info)
	except tkinter.TclError:# Fechar a janela antes de acabar o desenho
		pass
	