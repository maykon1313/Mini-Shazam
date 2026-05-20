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
