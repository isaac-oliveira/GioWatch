from geopy.distance import geodesic

#tipos de listas
TIPO_TEMPO_TOTAL = "tempo_total"
TIPO_INTERVALOS_PAUSAS = "pausas"
TIPO_INTERVALOS_LAPS = "laps"
TIPO_TEMPO_REGISTROS = "r"
TIPO_LATITUDE = "l"
TIPO_LONGITUDE = "n"
TIPO_ALTITUDE = "a"
TIPO_PASSOS = "p"
TIPO_BPMS = "b"

#flags
SEM_FLAG = "sem_flag"
COM_PAUSAS = "com_pausa"
COM_PAUSAS_COM_NONE = "com_pausacom_none"
SEM_PAUSAS = "sem_pausa"
SEM_PAUSAS_COM_NONE = "sem_pausacom_none"
SEM_NONE = "sem_none"
COM_NONE = "com_none" # Para os gráficos

def removePausas(registros, lista):
	intervalos_pausas = getList(registros, TIPO_INTERVALOS_PAUSAS, SEM_FLAG)
	nova_lista = []
	for i in range(1, len(intervalos_pausas), 2):
		nova_lista += lista[intervalos_pausas[i - 1]:intervalos_pausas[i] + 1]
		
	return nova_lista

def removeNone(lista): # Retirar os valores nulos
	nova_lista = []
	for x in lista:
		if x != None:
			nova_lista += [x]
	return nova_lista

def getList(registros, tipo, flag):
	lista = registros[tipo]
	if flag == COM_PAUSAS or flag == SEM_NONE:
		return removeNone(lista)
	elif flag == SEM_PAUSAS:
		return removeNone(removePausas(registros, lista))
	elif flag == SEM_PAUSAS_COM_NONE:
		return removePausas(registros, lista)
	return lista

def getInicioLaps(index, laps):
	return laps[index][1]

def getDistancia(registros, flag):
	lista_distancia = []
	lat = getList(registros, TIPO_LATITUDE, flag + COM_NONE)
	lon = getList(registros, TIPO_LONGITUDE, flag + COM_NONE)

	for i in range(len(lat)):
		lista_distancia += [(geodesic((lat[0], lon[0]), (lat[i], lon[i])).kilometers)]
	return lista_distancia

def getTempoTotal(registros): #tempo total em segundos
	lista_de_tempo = getList(registros, TIPO_TEMPO_TOTAL, SEM_FLAG)
	return lista_de_tempo[-1] - lista_de_tempo[0]