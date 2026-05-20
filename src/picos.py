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

# ndimage é um módulo da biblioteca scipy que fornece ferramentas para processamento de imagens e dados multidimensionais.
# Ele é amplamente usado para operações como filtragem, transformações geométricas, detecção de bordas, e análise de imagens.

# maximum_filter é uma função do módulo scipy.ndimage que aplica um filtro de máximo local a uma matriz (como uma imagem ou espectrograma).
# Como funciona:
# 	- Para cada elemento da matriz, ele considera uma vizinhança definida pelo parâmetro size (15, 15).
#   - Dentro dessa vizinhança, ele encontra o maior valor (máximo local) e substitui o valor do elemento central por esse máximo.
#   - Ele é usado para identificar os máximos locais no espectrograma, destacando os pontos de maior energia em uma região tempo-frequência.

# percentile é uma função do módulo `numpy` que calcula o valor abaixo do qual uma certa porcentagem dos dados cai.
# Como funciona:
#   - percentile calcula o valor do 75º percentil do espectrograma.
#   - Isso significa que 75% dos valores no espectrograma são menores ou iguais a esse valor.
#   - Esse valor é usado como um limiar para filtrar os picos, mantendo apenas os pontos com energia maior ou igual ao 75º percentil (os mais fortes).
