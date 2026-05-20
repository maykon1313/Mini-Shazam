import numpy as np
from scipy.ndimage import maximum_filter

def encontrar_picos(espectrograma, frequencias, tempos):
	# Destaca maximos locais em uma vizinhanca tempo-frequencia.
	maximos_locais = maximum_filter(espectrograma, size=(15, 15))

	# Marca os pontos que sao exatamente maximos locais.
	mascara_picos = espectrograma == maximos_locais

	# Define um limiar de energia para reduzir pontos fracos.
	limiar = np.percentile(espectrograma, 75) # ajustar se necessario

	# Seleciona apenas os maximos acima do limiar.
	linhas, colunas = np.where(mascara_picos & (espectrograma >= limiar))

	# Converte indices para valores fisicos: tempo (s) e frequencia (Hz).
	picos = []
	for linha, coluna in zip(linhas, colunas):
		freq_hz = frequencias[linha]
		tempo_s = tempos[coluna]
		picos.append((tempo_s, freq_hz))

	# Retorna lista de tuplas (tempo_em_segundos, frequencia_em_hz).
	return picos
