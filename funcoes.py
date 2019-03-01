from geopy.distance import geodesic
import turtle
import tkinter
import datetime
import dados
import strings
import grafico
import puras
import utm
import math

flag = dados.SEM_FLAG # Indica se a pausa vai ser considerada ou não

def le_timestamps(i, list_linhas, registros):
    linha = list_linhas[i].split()
    if i == 0:
        registros[dados.TIPO_TEMPO_TOTAL] = [int(linha[0]), int(linha[1])]
        i += 1

def le_evento(i, list_linhas, registros):
    linha = list_linhas[i].split()
    if linha[0] == "e": # Evento
        linha = list_linhas[i + 1].split()
        pausas = registros[dados.TIPO_INTERVALOS_PAUSAS]
        # Verifica qual é o evento
        if linha[0] == "i":# Início
            pausas += [len(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag))]
        elif linha[0] == "p" or linha[0] == "r":# Pausa ou einício
            pausas += [len(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag)) - 1]
        elif linha[0] == "f": # Fim
            pausas += [len(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag)) - 1]
            if registros[dados.TIPO_INTERVALOS_LAPS] != []:
                registros[dados.TIPO_INTERVALOS_LAPS].append((dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag)[-1], len(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag)) - 1))
            return i + 1
        i += 2

def le_laps(i, list_linhas, registros):
    linha = list_linhas[i].split()
    if linha[0] == "l": # Laps
        laps = registros[dados.TIPO_INTERVALOS_LAPS]
        if laps == []:
            laps.append((int(linha[1]), len(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag))))
        else:
            laps.append((int(linha[1]), len(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag)) - 1))


def le_registros(i, list_linhas, registros):
    linha = list_linhas[i].split()
    char = linha[0] 
    if char == "r": # Registro
        while char != "#":  # Fim do registro
            if char not in strings.valores_floats:  # Salva o valor como int() ou float()
                registros[linha[0]].append(int(linha[1]))
            else:
                registros[linha[0]].append(float(linha[1]))
            i += 1
            linha = list_linhas[i].split()
            char = linha[0]

        if registros["r"] != []: # Mantém as listas dos registros com o mesmo tamanho
            for key, item in registros.items():
                if key != "pausas" and key != "laps" and key != "tempo_total" and len(item) < len(registros["r"]):
                    item.append(None)

def verifica(i, list_linhas, registros):
    try:
        #Lê a primeira linha do arquivo
        le_timestamps(i, list_linhas, registros)
        # Lê os eventos
        le_evento(i, list_linhas, registros)
        # Lê os laps
        le_laps(i, list_linhas, registros)
        # Lê os dados do registro
        le_registros(i, list_linhas, registros)
    except: # pula uma linha caso, ela seja inválida
        i += 1

    return i

def altitude_max_e_min(registros):
    global flag

    lista_das_altitudes = dados.getList(registros, dados.TIPO_ALTITUDE, flag)
    if not puras.notNone(lista_das_altitudes):
        altitude_max = max(lista_das_altitudes)
        altitude_min = min(lista_das_altitudes)
        altitude_inicial = lista_das_altitudes[0]
        print(strings.altitude_maxima.format(altitude_max - altitude_inicial)) # Altitude relativa máxima
        print(strings.altitude_minima.format(altitude_inicial - altitude_min)) # Altitude relativa mínima
    else:
        print(strings.sem_altitude)

def batimentos_por_minutos(registros):
    global flag
    contador = 0
    lista_dos_bpms = dados.getList(registros, dados.TIPO_BPMS, flag)
    if not puras.notNone(lista_dos_bpms):
        tempo = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag)
        bpm_max = max(lista_dos_bpms)
        bpm_min = min(lista_dos_bpms)
        print(strings.bpm_maxima.format(bpm_max))
        print(strings.bpm_minima.format(bpm_min))
        print(strings.bpm_media.format(puras.getMediaBpm(lista_dos_bpms, tempo)))  
    else:
        print(strings.sem_bpm)


def ritmo(registros):
    global flag

    tempo_total = dados.getTempoTotal(registros)
    latitudes = dados.getList(registros, dados.TIPO_LATITUDE, flag)
    longitudes = dados.getList(registros, dados.TIPO_LONGITUDE, flag)
    if not puras.notNone(latitudes) and not puras.notNone(longitudes):
        tempo_decorrido = tempo_total / 60
        dist_total = puras.dist_percorrida(latitudes, longitudes)
        print(strings.ritmo.format(tempo_decorrido / dist_total))
    else:
        print(strings.sem_ritmo)

def cadencia_de_passos(registros):
    global flag

    lista_dos_passos = dados.getList(registros, dados.TIPO_PASSOS, flag)
    if not puras.notNone(lista_dos_passos):
        tempo_total = dados.getTempoTotal(registros)
        cadencia_passos = puras.getCadenciaPassos(lista_dos_passos, tempo_total)
        print(strings.cadencia.format(cadencia_passos))
    else:
        print(strings.sem_cadencia)

def tempo_total(registros):
    global flag

    tempo_total = dados.getTempoTotal(registros)
    time = tempo_total / 60
    print(strings.tempo_total.format(time))

def distancia_total(registros):
    global flag

    lista_de_longitudes = dados.getList(registros, dados.TIPO_LONGITUDE, flag)
    lista_de_latitudes = dados.getList(registros, dados.TIPO_LATITUDE, flag)
    print(strings.distancia_total.format(puras.dist_percorrida(lista_de_latitudes, lista_de_longitudes)))

def dados_nao_encontrados(bpms, passos, altitudes):
    str_msg = ""
    if  puras.notNone(bpms):
        str_msg += "\n" + strings.sem_bpm + "\n"
    if  puras.notNone(passos):
        str_msg += "\n" + strings.sem_cadencia + "\n"
    if  puras.notNone(altitudes):
        str_msg += "\n" + strings.sem_altitude + "\n"

    print(str_msg, end="")

# Abaixo se encontra as funções de apresentações
def apresentaDHD(registros):  # Apresenta a data, hora e duração
    global flag

    inicial_final = dados.getList(registros, dados.TIPO_TEMPO_TOTAL, flag)
    lista_de_tempo = dados.getTempoTotal(registros)
    tempo_inicial = datetime.datetime.fromtimestamp(inicial_final[0]).strftime('%d/%m/%Y %H:%M:%S')
    tempo_final = datetime.datetime.fromtimestamp(inicial_final[1]).strftime('%d/%m/%Y %H:%M:%S')
    duracao = puras.getDuracaoString(lista_de_tempo)
    print("\n", strings.bordas,"\n")
    print(strings.inicio_fim_duracao.format(tempo_inicial, tempo_final, duracao))
    print("\n", strings.bordas,"\n")


def apresentaResumoTotal(registros):  # Chama as funções referente ao resumo total
    print("\n", strings.bordas,"\n")
    altitude_max_e_min(registros)
    batimentos_por_minutos(registros)
    ritmo(registros)
    cadencia_de_passos(registros)
    tempo_total(registros)
    distancia_total(registros)
    print("\n", strings.bordas,"\n")

def apresentaResumoPorKM(registros):  # Chama as funções referente ao resumo por KM
    global flag

    print("\n", strings.bordas)
    i1 = 0 #Índice do início do KM
    i2 = 1 #Índice do final do KM, vai ser incrementado
    km = 1 #Contador de KM
    dist = 0 #distância
    lat = dados.getList(registros, dados.TIPO_LATITUDE, flag + dados.COM_NONE)
    lon = dados.getList(registros, dados.TIPO_LONGITUDE, flag + dados.COM_NONE)
    if not puras.notNone(lat) and not puras.notNone(lon):
        tempo = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
        alt = dados.getList(registros, dados.TIPO_ALTITUDE, flag + dados.COM_NONE)
        passos = dados.getList(registros, dados.TIPO_PASSOS, flag + dados.COM_NONE)
        bpms = dados.getList(registros, dados.TIPO_BPMS, flag + dados.COM_NONE)
        while i2 < len(dados.getList(registros, dados.TIPO_LATITUDE, flag + dados.COM_NONE)):
            dist += geodesic((lat[i2-1], lon[i2 - 1]), (lat[i2], lon[i2])).kilometers
            if dist > km or i2 == len(dados.getList(registros, dados.TIPO_LATITUDE, flag + dados.COM_NONE)) - 1: # Imprimi e armazena os dados do início do próximo k
                tempo_total = tempo[i2] - tempo[i1]
                print(strings.resumoKMLAPS.format(km, # Km atual
                "km", # Km
                puras.getMinutos(tempo_total), # Minutos
                puras.getSegundos(tempo_total), # Segundos
                puras.getMinutos(tempo_total), # Ritmo
                puras.getCadenciaPassos(passos[i1:i2], tempo_total), # Cadência
                puras.getMediaBpm(bpms[i1:i2], tempo[i1:i2]), # BPM
                puras.getGanhoOuPerda(alt[i2] - alt[i1]),# String com "ganho" ou "perder"
                puras.getModulo(alt[i2] - alt[i1])), # Altitude ganho ou perda
                end="") 
                i1 = i2
                km += 1
            i2 += 1
        dados_nao_encontrados(bpms, passos, alt)
    else:
        print("\n" + strings.sem_distancia)
    print("\n", strings.bordas, "\n")

def apresentarResumoPorLaps(registros):
    print("\n", strings.bordas)
    laps = dados.getList(registros, dados.TIPO_INTERVALOS_LAPS, dados.SEM_FLAG)
    if laps != []:
        lat = dados.getList(registros, dados.TIPO_LATITUDE, dados.COM_NONE)
        lon = dados.getList(registros, dados.TIPO_LONGITUDE, dados.COM_NONE)
        tempo = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, dados.COM_NONE)
        alt = dados.getList(registros, dados.TIPO_ALTITUDE, dados.COM_NONE)
        passos = dados.getList(registros, dados.TIPO_PASSOS, dados.COM_NONE)
        bpms = dados.getList(registros, dados.TIPO_BPMS, dados.COM_NONE)
        lap = 1

        for i in range(1, len(laps)):
            j = dados.getInicioLaps(i - 1, laps) # Início do lap
            k = dados.getInicioLaps(i, laps) # Final do lap e início do próximo, na maioria dos casos

            tempo_total = laps[i][0] - laps[i - 1][0]
            print(strings.resumoKMLAPS.format(lap, # Km atual
            "laps", # Km
            puras.getMinutos(tempo_total), # Minutos
            puras.getSegundos(tempo_total), # Segundos
            puras.getMinutos(tempo_total), # Ritmo
            puras.getCadenciaPassos(passos[j:k + 1], tempo_total), # Cadência
            puras.getMediaBpm(bpms[j:k + 1], tempo[j:k + 1]), # BPM
            puras.getGanhoOuPerda(alt[k] - alt[j]), # String com "ganho" ou "perder"
            puras.getModulo(alt[k] - alt[j])), # Altitude ganho ou perda
            end="") 
            lap += 1
        dados_nao_encontrados(bpms, passos, alt)
    else:
        print(strings.sem_laps)
    print("\n", strings.bordas,"\n")

def escalaa(x, inc):
    x = ((x * 1000000) % 10000) / inc
    return x

def grafico_do_percurso(registros):
    global flag

    try:
        window = turtle.Screen()
        tartaruga = turtle.Turtle()

        window.title("Gráfico de Percurso")
    
        tartaruga.pensize(3)
        tartaruga.shape("blank")

        lista_de_lat = dados.getList(registros, dados.TIPO_LATITUDE, flag + dados.COM_NONE)
        lista_de_lon = dados.getList(registros, dados.TIPO_LONGITUDE, flag + dados.COM_NONE)

        max_lat = ((max(lista_de_lat) * 1000000) % 10000)
        max_lon = ((max(lista_de_lon) * 1000000) % 10000)
        div = (6 * max_lat) / 3864 
        inc = 3

        tartaruga.up()
        tartaruga.goto(escalaa(lista_de_lon[0], div) - ((275 * inc) * max_lon) / 6458, escalaa(lista_de_lat[0], div) - ((125 * inc) * max_lat) / 3864)
        tartaruga.down()
        tartaruga.write("   Início", align= "left", font= ("Arial", 16, "normal"))
        tartaruga.dot("red")
        tartaruga.pencolor("blue")

        dist = 0
        km = 1
        for i in range(1, len(lista_de_lat)):
            dist += geodesic((lista_de_lat[i-1], lista_de_lon[i - 1]), (lista_de_lat[i], lista_de_lon[i])).kilometers
            x = escalaa(lista_de_lon[i], div) -  ((275 * inc) * max_lon) / 6458
            y = escalaa(lista_de_lat[i], div) -  ((125 * inc) * max_lat) / 3864
            tartaruga.goto(x, y)
            if dist > km:
                tartaruga.dot("grey")
                tartaruga.pencolor("black")
                tartaruga.write("{}º km    ".format(km), align= "right", font= ("Arial", 12, "normal"))
                tartaruga.pencolor("blue")
                km += 1
        tartaruga.dot("red")
        tartaruga.pencolor("black")
        tartaruga.write("   Fim", align= "right", font= ("Arial", 16, "normal"))

        window.mainloop()
    except turtle.Terminator: # Conflito de instancia da Turtle()
        window.clearscreen()
        grafico_do_percurso(registros)
    except tkinter.TclError: # Fechar a janela antes de acabar o desenho
        pass

def apresentaGraficoRitmo(registros):  # Chama as funções referente ao gráfico ritmo
    global flag

    lat, lon = dados.getList(registros, dados.TIPO_LATITUDE, flag + flag + dados.COM_NONE), dados.getList(registros, dados.TIPO_LONGITUDE, flag + dados.COM_NONE)
    tempo = puras.tempo_registros(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + flag + dados.COM_NONE))
    if not puras.notNone(lat) and not puras.notNone(lon) and len(tempo) > 1:
        x = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
        y = puras.getRitmo_Por_Registro(tempo, puras.dist_percorrida_por_registro(lat, lon))
        grafico.criarGrafico([(x, y)], ("Gráfico de Ritmo"))
    else:
        print(strings.sem_dados_para_grafico)

def apresentaGraficoAltitude(registros):  # Chama as funções referente ao gráfico altitude
    global flag

    x = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + flag + dados.COM_NONE)
    y = dados.getList(registros, dados.TIPO_ALTITUDE, flag + flag + dados.COM_NONE)
    if not puras.notNone(y) and len(x) > 1:
        grafico.criarGrafico([(x, y)], ("Gráfico Altitude"))
    else:
        print(strings.sem_dados_para_grafico)

def apresentaGraficoBPMs(registros):  # Chama as funções referente ao gráfico BPMs
    global flag

    x = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
    y = dados.getList(registros, dados.TIPO_BPMS, flag + dados.COM_NONE)
    if not puras.notNone(y) and len(x) > 1:
        grafico.criarGrafico([(x, y)], ("Gráfico BPM"))
    else:
        print(strings.sem_dados_para_grafico)

def apresentaGraficoBPMsZonas(registros):  # Chama as funções referente ao gráfico de Zonas do BPM
    global flag

    x = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
    y = dados.getList(registros, dados.TIPO_BPMS, flag + dados.COM_NONE)
    if not puras.notNone(y) and len(x) > 1:
        idade = int(input("Digite sua idade: "))
        grafico.criarGrafico([(x, y)], ("Gráfico Zonas de BPM", idade))
    else:
        print(strings.sem_dados_para_grafico)

def apresentaGraficoCompleto(registros):  # Chama as funções referente ao gráfico completo
    global flag

    xys = []
    xa = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
    ya = dados.getList(registros, dados.TIPO_ALTITUDE, flag + dados.COM_NONE)
    if not puras.notNone(ya) and len(xa) > 1:
        xys += [(xa, ya, 0)]

    xb = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
    yb = dados.getList(registros, dados.TIPO_BPMS, flag + dados.COM_NONE)
    if not puras.notNone(yb) and len(xb) > 1:
        xys += [(xb, yb, 1)]

    lat, lon = dados.getList(registros, dados.TIPO_LATITUDE, flag + dados.COM_NONE), dados.getList(registros, dados.TIPO_LONGITUDE, flag + dados.COM_NONE)
    tempo = puras.tempo_registros(dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE))
    if not puras.notNone(lat) and not puras.notNone(lon) and len(tempo) > 1:
        xc = dados.getList(registros, dados.TIPO_TEMPO_REGISTROS, flag + dados.COM_NONE)
        yc = puras.getRitmo_Por_Registro(tempo, puras.dist_percorrida_por_registro(lat, lon))
        xys += [(xc, yc, 2)]

    if xys != []:
        grafico.criarGrafico(xys, "Gráfico Completo")
    else:
        print(strings.sem_dados_para_grafico)

def opcao_selecionada(op, registros, flag_arg):  #'Switch' caseiro para python
    global flag
    flag = flag_arg

    return {
        "1": apresentaDHD,
        "2": apresentaResumoTotal,
        "3": apresentaResumoPorKM,
        "4": apresentarResumoPorLaps,
        "5": grafico_do_percurso,
        "6": apresentaGraficoRitmo,
        "7": apresentaGraficoAltitude,
        "8": apresentaGraficoBPMs,
        "9": apresentaGraficoBPMsZonas,
        "10": apresentaGraficoCompleto
    }[op](registros)