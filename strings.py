#strings do programa
opcoes = "1 2 3 4 5 6 7 8 9 10 11 0" # String para verificar se a opção é válida
valores_floats = "l n a" # String para verifcar se a linha contém um valor float() ou int()

''' --- main.py --- '''
menu = "Escolha uma opção: \n 1 - Apresentar a data, horário e duração da corrida. \n 2 - Apresentar um resumo da atividade. \n 3 - Apresentar um resumo de cada quilômetro da atividade.\n 4 - Apresentar resumo por laps. \n 5 - Apresentar gráfico de percurso.\n 6 - Apresentar gráfico de ritmo. \n 7 - Apresentar gráfico de altitude. \n 8 - Apresentar gráfico de bpms.\n 9 - Apresentar gráfico das zonas de bpm.\n 10 - Apresentar gráfico completo. \n 11 - Escolher outro arquivo. \n 0 - Sair"
opcoes_pausa = "Pausas encontradas, deseja exibir-lás?\nS - Sim\nN - Não\n "
arquivo_invalido = " Arquivo inválido!"
arquivo_nao_encontrado = " Arquivo não encontrado!"
opcao_invalida = " Opção inválida!"
bye = " Obrigado por usar nosso programa!"

''' --- funcoes.py --- '''

#Inicio, fim e duração
inicio_fim_duracao = " - Início: {}\n - Final: {}\n - Duração: {}"

# Altitudes
altitude_maxima = " - A altitude máxima em relação a inicial é de: {:.2f}m"
altitude_minima = " - A altitude mínima em relação a inicial é de: {:.2f}m"
sem_altitude = " Sem dados sobre a altitude no arquivo de entrada!"

# BPMs
bpm_maxima = " - O nível de BPM máximo foi de: {}"
bpm_minima = " - O nível de BPM mínimo foi de: {}"
bpm_media = " - A média de BPM durante a corrida foi de: {:.2f}"
sem_bpm = " Sem BPMs no arquivo de entrada!"

# Ritmo
ritmo = " - O ritmo da corrida foi de {:.2f} min/Km"
sem_ritmo = " Sem dados sobre a latitude ou longitude no arquivo de entrada!"

# Cadência 
cadencia = " - Cadência média de passos: {:.2f} passos/min"
sem_cadencia = " Sem dados referentes ao número de passos no arquivo de entrada!"

# Tempo Total
tempo_total = " - O tempo total foi de {:.2f} minutos"

# Distância total
distancia_total = " - A distância total foi de: {:.2f} km"
sem_distancia = " Sem dados para calcular a distância no arquivo de entrada!"

# Resumo por laps e km
resumoKMLAPS = "\n{}º {}:\n - Tempo total: {} min {} s\n - Ritmo médio: {:.2f} min/km\n - Cadência média: {:.2f} passos/min\n - Média de Bpm: {:.2f}\n - Altitude: {}{:.2f} m\n"

# Laps
sem_laps = "\n Desculpe, o arquivo não possui laps!"

# Bordas
bordas = "-" * 33

# Gráficos
sem_dados_para_grafico = " \n Sem dados o suficiente para montar esse gráfico!\n"