import funcoes
import dados
from geopy.distance import geodesic

def notNone(lista):
	nova = []
	for x in lista:
		if x != None:
			nova += [x]
	return nova == []

def getMinutos(s):
    return s // 60

def getSegundos(s):
    return s % 60

def getGanhoOuPerda(a):
    if a > 0:
        return "Ganho de "
    elif a < 0:
        return "Perda de "
    return ""

def getModulo(n):
    return abs(n)

def getDuracaoString(s):  # converte milissegundos para string formatada
    h = s // 3600
    min = s // 60
    s %= 60
    if h <= 0:
        return "{}min {}s".format(min, s)
    return "{}h {}min {}s".format(h, min, s) 

def getCadenciaPassos(passos, tempo_total):
	if not notNone(passos):
		passos_total = passos[-1] - passos[0]
		return passos_total / (tempo_total / 60) 
	return 0

def getMediaBpm(bpms, tempo):
	if not notNone(bpms):
		tempo_total = tempo[-1] - tempo[0]
		media = bpms[0] / tempo_total if tempo_total != 0 else bpms[0]
		pulo = 1
		for i in range(1, len(bpms)):
			if bpms[i] != None and len(tempo) > 1:
				media += bpms[i] * (tempo[i] - tempo[i - pulo]) / tempo_total
				pulo = 1
			else:
				pulo += 1

		return media
		
	return 0

def dist_percorrida(lat, lon): # Para o ritmo
    resultado = 0
    for i in range(1, len(lat)):
        resultado += geodesic((lat[i-1], lon[i-1]), (lat[i], lon[i])).kilometers
    return resultado

def tempo_registros(tempo):
	resultado = [0]
	for i in range(1, len(tempo)):
		resultado += [(tempo[i] - tempo[i-1])]
	return resultado

def dist_percorrida_por_registro(lat, lon):
	dists = [0]
	for i in range(1, len(lat)):
		dists += [geodesic((lat[i-1], lon[i-1]), (lat[i], lon[i])).kilometers]
	return dists

def getRitmo_Por_Registro(tempo, dist):
	resultado = []
	for i in range(len(tempo)):
		if dist[i] != 0:
			resultado += [(tempo[i] / 60) / dist[i]]
		else:
			resultado += [0]

	return resultado

def max(lista): # Pega o maior item da lista desconsiderandos os Nones 
	max = 0
	for x in lista:
		if x != None and max < x:
			max = x
	return max
