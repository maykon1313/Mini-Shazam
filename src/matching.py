from collections import defaultdict

from src.padronizacao import carregar_audio
from src.STFT import calcular_espectrograma
from src.picos import encontrar_picos
from src.hashes import gerar_hashes

def indexar_musica(caminho_arquivo, nome_musica, banco_dados):
	# Carrega o sinal no dominio do tempo.
	sinal, taxa_amostragem = carregar_audio(caminho_arquivo)

	# Converte o sinal para o dominio tempo-frequencia e obtém eixos.
	espectrograma, frequencias, tempos = calcular_espectrograma(sinal)

	# Extrai os picos de maior energia (em segundos e Hz).
	picos = encontrar_picos(espectrograma, frequencias, tempos)

	# Gera os hashes com base nas distancias entre picos.
	hashes = gerar_hashes(picos)

	for chave, tempo_ancora in hashes:
		if chave not in banco_dados:
			banco_dados[chave] = []
		banco_dados[chave].append((nome_musica, tempo_ancora))

def buscar_musica(caminho_gravacao, banco_dados):
	# Carrega o trecho gravado.
	sinal, taxa_amostragem = carregar_audio(caminho_gravacao)

	# Calcula o espectrograma do trecho e obtém eixos.
	espectrograma, frequencias, tempos = calcular_espectrograma(sinal)

	# Extrai os picos do trecho (tempo em s, freq em Hz).
	picos = encontrar_picos(espectrograma, frequencias, tempos)

	# Gera os hashes do trecho.
	hashes = gerar_hashes(picos)

	contagem = defaultdict(lambda: defaultdict(int))

	for chave, tempo_gravacao in hashes:
		if chave in banco_dados:
			for nome_musica, tempo_banco in banco_dados[chave]:
				# Calcula o offset temporal entre banco e gravacao.
				offset = tempo_banco - tempo_gravacao
				# Conta quantas vezes o mesmo offset aparece.
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
