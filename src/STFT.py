import numpy as np
from scipy.signal import stft

TAXA_AMOSTRAGEM = 44100

def calcular_espectrograma(sinal):
	# Calcula a STFT para obter o conteudo tempo-frequencia.
	frequencias, tempos, espectro_complexo = stft(sinal, fs=TAXA_AMOSTRAGEM, window="hann", nperseg=2048, noverlap=1024,)
	
	# Converte a parte complexa em magnitude (energia por bin).
	magnitude = np.abs(espectro_complexo)
	
	# Aplica escala logaritmica para comprimir a dinamica.
	espectrograma_db = 20 * np.log10(magnitude + 1e-10)

	# Retorna o espectrograma em dB e os eixos fisicos (frequencias em Hz e tempos em s).
	return espectrograma_db, frequencias, tempos


# STFT (Short-Time Fourier Transform) é uma técnica usada para analisar o conteúdo de frequência de um sinal ao longo do tempo. 
# Ela divide o sinal em pequenos segmentos (janelas) e calcula a Transformada de Fourier em cada segmento. 
# Isso permite observar como as frequências variam com o tempo.

# A função stft da biblioteca scipy.signal realiza essa transformação.
# window="hann": Define o tipo de janela usada para suavizar os segmentos.
# nperseg=2048: Tamanho de cada segmento (em amostras).
# noverlap=1024: Quantidade de sobreposição entre segmentos (50%).

# O resultado da STFT é uma matriz complexa que representa as amplitudes e fases das frequências em cada intervalo de tempo.

# Magnitude:
# A STFT retorna valores complexos (com parte real e imaginária), que representam amplitude e fase.
# A magnitude é calculada com abs para obter apenas a intensidade das frequências, ignorando a fase.
# 
# Espectrograma (escala logarítmica):
# O espectrograma é a representação visual da energia das frequências ao longo do tempo.
# A escala logarítmica é usada porque:
#   - Comprime a grande variação de intensidades (dinâmica do sinal).
#   - Torna mais fácil visualizar frequências de baixa e alta energia no mesmo gráfico.
#   - É mais próxima da percepção humana de intensidade sonora (escala logarítmica é como ouvimos sons).
