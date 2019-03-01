import funcoes
import dados 
import strings

def e_valido_arquivo(registros):
	resultado = False
	for k, x in registros.items():
		if x != []:
			resultado = True
			break

	return resultado

def e_valida(opcao, opces_validas):# Verifica se a opção esta em "opcoes_validas"
	return opcao.lower().strip(" ") in opces_validas and opcao != "" and opcao != " "

def temPausa(opcao, registros): # Retorna uma string "s" ou "n"
	pausas = dados.getList(registros, dados.TIPO_INTERVALOS_PAUSAS, dados.SEM_FLAG)
	sem_pausas = "default"
	while e_valida(opcao, "2 3") and not e_valida(sem_pausas, "n s") and len(pausas) > 2:
		sem_pausas = input(strings.opcoes_pausa).lower().strip(" ")

	return sem_pausas

def validar_opcao(opcao): # Impedi que o usuário escolha uma opção inválida
	while not e_valida(opcao, strings.opcoes): 
		print(strings.opcao_invalida)
		opcao = input("Digite uma opção válida: ")

	return opcao

def validar_arquivo(registros):
	resultado = e_valido_arquivo(registros)
	if not resultado:
		print(strings.arquivo_invalido)

	return resultado

def getFlag(sem_pausas): # Retorna uma flag indicando se as pausas serão consideradas ou não
	if sem_pausas == "s":
		return dados.COM_PAUSAS
	elif sem_pausas == "n":
		return dados.SEM_PAUSAS

	return dados.SEM_NONE

def ler_arquivo(file, list_linhas, registros):
	list_linhas  += [x for x in file]
	i = 0
	while i < len(list_linhas):# Lê os dados
		i = funcoes.verifica(i, list_linhas, registros)
		i += 1

def abrir_menu(registros):
	opcao = ""
	while opcao != "11" and opcao != "0":
		print(strings.menu)
		opcao = validar_opcao(input("Digite o valor da opção desejada: "))
		sem_pausas = temPausa(opcao, registros)

		if opcao != "0" and opcao != "11":# Evita erro, já que a opcao 0 e 10, são para controlar os loops
			flag = getFlag(sem_pausas)
			funcoes.opcao_selecionada(opcao, registros, flag)
			opcao = "-" + input("Pressione Enter para rever o menu") # "-" impedi que o usuário digite alguma opção válida, e a mesma seja executada
	return opcao
						
opcao = ""
while opcao != "0": # Mantém o programa "aberto"
	list_linhas = []
	registros = {"r": [], "l" : [], "n" : [], "a" : [], "p" : [], "b" : [], "pausas": [], "laps": [], "tempo_total":[]}
	path = input("Digite o caminho do arquivo: ") 

	try: # Se o arquivo existir, caso não, veja o "except"
		with open(path, "r") as file:
			ler_arquivo(file, list_linhas, registros)
			file.close() # Fecha o arquivo após a leitura
			valido = validar_arquivo(registros)
		if valido:
			opcao = abrir_menu(registros)
	except FileNotFoundError: # Caso a parte de cima de erro, quando o arquivo não existir
		print(strings.arquivo_nao_encontrado)
	except UnicodeDecodeError: # Caso seja inserido um arquivo com outro formato, sem ser um .txt
		print(strings.arquivo_invalido)
else:
	print("\n", strings.bordas,"\n")
	print(strings.bye)
	print("\n", strings.bordas,"\n")
		