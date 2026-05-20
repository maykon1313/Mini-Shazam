def gerar_hashes(lista_picos):
	hashes = []

	for i, (tempo_ancora, freq_ancora) in enumerate(lista_picos):
		for j in range(1, 11):
			if i + j >= len(lista_picos):
				break

			tempo_futuro, freq_futuro = lista_picos[i + j]

			# Mede a distancia temporal entre os picos.
			delta_tempo = tempo_futuro - tempo_ancora

			# Quantiza frequencias e delta de tempo para estabilidade do hash.
			f1 = int(round(freq_ancora))
			f2 = int(round(freq_futuro))
			# delta em milissegundos inteiro
			dt_ms = int(round(delta_tempo * 1000))
			chave = f"{f1}|{f2}|{dt_ms}"

			hashes.append((chave, tempo_ancora))
			
	return hashes

# A função recebe uma lista de picos, onde cada pico é uma tupla (tempo, frequência).

# Processo:
# 	- Para cada pico âncora (tempo_ancora, freq_ancora) na lista:
#      - São considerados até 10 picos futuros na lista.
#      - Para cada par de picos (âncora e futuro):
#        - Calcula-se o delta de tempo entre os dois picos: delta_tempo = tempo_futuro - tempo_ancora.
#        - As frequências e o delta de tempo são quantizados (convertidos para inteiros) para garantir estabilidade no hash:
#          - f1: Frequência do pico âncora.
#          - f2: Frequência do pico futuro.
#          - dt_ms: Delta de tempo em milissegundos.
#        - Um hash é gerado no formato: f"{f1}|{f2}|{dt_ms}".
#      - O hash é armazenado junto com o tempo_ancora.

# Saída:
# 	- Retorna uma lista de tuplas no formato:
#   	- (chave, tempo_ancora), onde:
#       	- chave: O hash gerado.
#       	- tempo_ancora: O tempo do pico âncora.

# Entrada:
# python
# lista_picos = [
#     (0.5, 1000),  # Pico 1: tempo 0.5s, frequência 1000 Hz
#     (0.7, 1020),  # Pico 2: tempo 0.7s, frequência 1020 Hz
#     (1.0, 1050),  # Pico 3: tempo 1.0s, frequência 1050 Hz
# ]

# Processo:
# 1. Para o Pico 1 (0.5, 1000):
#    - Compara com o Pico 2 (0.7, 1020):
#      - delta_tempo = 0.7 - 0.5 = 0.2 segundos → dt_ms = 200 ms.
#      - Hash: "1000|1020|200".
#    - Compara com o Pico 3 (1.0, 1050):
#      - delta_tempo = 1.0 - 0.5 = 0.5 segundos → dt_ms = 500 ms.
#      - Hash: "1000|1050|500".
# 
# 2. Para o Pico 2 (0.7, 1020):
#    - Compara com o Pico 3 (1.0, 1050):
#      - delta_tempo = 1.0 - 0.7 = 0.3 segundos → dt_ms = 300 ms.
#      - Hash: "1020|1050|300".

# Saída:
# python
# [
#     ("1000|1020|200", 0.5),
#     ("1000|1050|500", 0.5),
#     ("1020|1050|300", 0.7),
# ]
