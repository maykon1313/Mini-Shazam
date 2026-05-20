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
