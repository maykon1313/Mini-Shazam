from src.padronizacao import carregar_audio
from src.STFT import calcular_espectrograma
from src.picos import encontrar_picos
from src.hashes import gerar_hashes

def shazam(caminho_arquivo):
	# Carrega o sinal no dominio do tempo.
	sinal = carregar_audio(caminho_arquivo)

	# Converte o sinal para o dominio tempo-frequencia e obtém eixos.
	espectrograma, frequencias, tempos = calcular_espectrograma(sinal)

	# Extrai os picos de maior energia (em segundos e Hz).
	picos = encontrar_picos(espectrograma, frequencias, tempos)

	# Gera os hashes com base nas distancias entre picos.
	hashes = gerar_hashes(picos)

	return hashes

def indexar_musica(caminho_arquivo, nome_musica, banco_dados):
	hashes = shazam(caminho_arquivo)

	for chave, tempo_ancora in hashes:
		if chave not in banco_dados:
			banco_dados[chave] = []
		banco_dados[chave].append((nome_musica, tempo_ancora))

def buscar_musica(caminho_gravacao, banco_dados):
	hashes = shazam(caminho_gravacao)

	contagem = {}

	for chave, tempo_gravacao in hashes:
		if chave in banco_dados:
			for nome_musica, tempo_banco in banco_dados[chave]:
				# Calcula o offset temporal entre banco e gravacao.
				offset = tempo_banco - tempo_gravacao

				# Verifica se a música já está no dicionário.
				if nome_musica not in contagem:
					contagem[nome_musica] = {}

				# Verifica se o offset já está no dicionário interno.
				if offset not in contagem[nome_musica]:
					contagem[nome_musica][offset] = 0

				# Incrementa a contagem do offset.
				contagem[nome_musica][offset] += 1

	melhor_musica = None
	melhor_contagem = 0

	for nome_musica, offsets in contagem.items():
		# Encontra o pico do histograma de offsets.
		pico = max(offsets.values())
		if pico > melhor_contagem:
			melhor_contagem = pico
			melhor_musica = nome_musica

	if melhor_musica is None:
		print("Nao encontrada")
	else:
		print("Resultado:", melhor_musica)

# shazam(caminho_arquivo)
# 	- Objetivo: Extrair os hashes únicos de um arquivo de áudio.
#   - Passos:
#   	1. Carrega o áudio no domínio do tempo usando carregar_audio.
#       2. Converte o áudio para o domínio tempo-frequência (espectrograma) com calcular_espectrograma.
#       3. Identifica os picos de maior energia no espectrograma com encontrar_picos.
#       4. Gera os hashes baseados nas relações entre os picos com gerar_hashes.
#   - Retorno: Lista de hashes no formato (chave, tempo_ancora).

# indexar_musica(caminho_arquivo, nome_musica, banco_dados)
# 	- Objetivo: Adicionar os hashes de uma música ao banco de dados.
#   - Passos:
#   	1. Gera os hashes da música usando a função shazam.
#       2. Para cada hash gerado:
#       	- Verifica se a chave já existe no banco de dados.
#         	- Se não existir, inicializa uma lista vazia.
#         	- Adiciona o par (nome_musica, tempo_ancora) à lista correspondente à chave.
#   - Retorno: Atualiza o banco de dados com os hashes da música.

# buscar_musica(caminho_gravacao, banco_dados)
#   - Objetivo: Encontrar a música correspondente a uma gravação no banco de dados.
#   - Passos:
#   	1. Gera os hashes da gravação usando a função shazam.
#       2. Para cada hash da gravação:
#       	- Verifica se ele existe no banco de dados.
#         	- Para cada correspondência encontrada:
#           	- Calcula o offset temporal entre o banco e a gravação.
#           	- Atualiza a contagem de offsets para a música correspondente.
#       3. Analisa os offsets:
#         	- Encontra a música com o maior pico no histograma de offsets.
#       4. Retorna o nome da música correspondente ou informa que não foi encontrada.
#   - Retorno: Nome da música correspondente ou mensagem de "não encontrada".
