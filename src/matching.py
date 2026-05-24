from pathlib import Path

from src.padronizacao import carregar_audio, TAXA_AMOSTRAGEM
from src.STFT import calcular_espectrograma # Importa a função de espectrograma baseada em STFT
from src.wavelet import calcular_escalograma 
from src.picos import encontrar_picos # Importa a função de encontrar picos, que pode ser usada tanto para espectrograma quanto para escalograma
from src.hashes import gerar_hashes # Importa a função de gerar hashes, que pode ser usada para ambos os tipos de representação
from src.imagens import plot_espectrograma, plot_histograma_offsets, plot_mapa_constelacao, plot_sinal_tempo # Importa as funções de plotagem, que podem ser usadas para ambos os tipos de representação
from src.imagens import plot_espectrograma, plot_mapa_constelacao, plot_sinal_tempo, plot_escalograma
def _base_dir():
	return Path(__file__).resolve().parents[1]

def _caminho_imagem(base_dir, subpasta, categoria, nome_base, sufixo):
	return base_dir / "images" / subpasta / categoria / f"{nome_base}_{sufixo}.png"

def shazam(caminho_arquivo, categoria, base_dir=None):
	base_dir = base_dir or _base_dir()
	nome_base = Path(caminho_arquivo).stem

    # Carrega o sinal no dominio do tempo.
	sinal = carregar_audio(caminho_arquivo)

    # 1. PROCESSAMENTO STFT (O Original)
	espectrograma, freq_stft, tempos_stft = calcular_espectrograma(sinal)
	picos_stft = encontrar_picos(espectrograma, freq_stft, tempos_stft)
	hashes_stft = gerar_hashes(picos_stft)

    # 2. PROCESSAMENTO WAVELET (O Novo)
	escalograma, freq_cwt, tempos_cwt = calcular_escalograma(sinal)
	picos_cwt = encontrar_picos(escalograma, freq_cwt, tempos_cwt)
	hashes_cwt = gerar_hashes(picos_cwt)



    # (Opcional) Aqui você pode chamar os plots para a STFT e CWT separadamente se quiser salvar as imagens das duas!
    # plot_espectrograma(espectrograma, freq_stft, tempos_stft, ...)
    # plot_mapa_constelacao(picos_stft + picos_cwt, ...) # Pode até plotar os picos juntos!
	plot_sinal_tempo(
		sinal,
		TAXA_AMOSTRAGEM,
		_caminho_imagem(base_dir, "raw", categoria, nome_base, "sinal"),
		f"Sinal no tempo - {nome_base}",
	)
	plot_espectrograma(
		espectrograma,
		freq_stft,
		tempos_stft,
		_caminho_imagem(base_dir, "espectograma", categoria, nome_base, "espectrograma"),
		f"Espectrograma - {nome_base}",
	)
	plot_mapa_constelacao(
		picos_stft,
		_caminho_imagem(base_dir, "mapa_de_constelacao", categoria, nome_base, "constelacao"),
		f"Mapa de constelacao - {nome_base}",
	)

	# SALVANDO A IMAGEM DA WAVELET:
	plot_escalograma(
        escalograma,
        freq_cwt,
        tempos_cwt,
        _caminho_imagem(base_dir, "escalograma", categoria, nome_base, "escalograma"),
        f"Escalograma Wavelet - {nome_base}",
    )

    # ... (combinação dos hashes e return) ...

    # 3. COMBINAÇÃO
    # Junta as duas listas de hashes. O banco de dados não se importa de onde
    # eles vieram, ele só quer chaves únicas para comparar depois!
	hashes_totais = hashes_stft + hashes_cwt

	return hashes_totais



def indexar_musica(caminho_arquivo, nome_musica, banco_dados):
	hashes = shazam(caminho_arquivo, "musicas")

	for chave, tempo_ancora in hashes:
		if chave not in banco_dados:
			banco_dados[chave] = []
		banco_dados[chave].append((nome_musica, tempo_ancora))

def buscar_musica(caminho_gravacao, banco_dados):
	base_dir = _base_dir()
	nome_base = Path(caminho_gravacao).stem

	hashes = shazam(caminho_gravacao, "gravacao", base_dir=base_dir)

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
		plot_histograma_offsets(
			contagem.get(melhor_musica, {}),
			_caminho_imagem(base_dir, "histograma", "gravacao", nome_base, "offsets"),
			f"Histograma de offsets - {melhor_musica}",
		)

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
