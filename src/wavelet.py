import numpy as np
import pywt

TAXA_AMOSTRAGEM = 44100

def calcular_escalograma(sinal):
    wavelet = 'cmor1.5-1.0'
    frequencias_alvo = np.linspace(8000, 11025, num=30)
    
    freq_central = pywt.central_frequency(wavelet)
    escalas = (freq_central * TAXA_AMOSTRAGEM) / frequencias_alvo
    
    # --- A MÁGICA DA MEMÓRIA: CORTAR EM PEDAÇOS ---
    tamanho_chunk = 10 * TAXA_AMOSTRAGEM  # Pedaços de 10 segundos
    fator_reducao = 1024
    
    escalograma_reduzido_total = []
    tempos_reduzidos_total = []
    
    # Eixo de tempo original de toda a música
    tempos_total = np.arange(len(sinal)) / TAXA_AMOSTRAGEM

    # Processa a música de 10 em 10 segundos
    for i in range(0, len(sinal), tamanho_chunk):
        # Pega a fatia atual do sinal e do tempo
        sinal_chunk = sinal[i : i + tamanho_chunk]
        tempo_chunk = tempos_total[i : i + tamanho_chunk]
        
        # 1. Calcula a CWT apenas para esses 10 segundos (Usa pouca RAM!)
        coeficientes, frequencias = pywt.cwt(sinal_chunk, escalas, wavelet, sampling_period=1.0/TAXA_AMOSTRAGEM)
        
        # 2. Converte para magnitude e decibéis
        magnitude = np.abs(coeficientes)
        escalograma_db = 20 * np.log10(magnitude + 1e-10)
        
        # 3. Faz a redução temporal (diminui a matriz)
        escalograma_reduzido = escalograma_db[:, ::fator_reducao]
        tempos_reduzidos = tempo_chunk[::fator_reducao]
        
        # 4. Guarda a fatia reduzida na lista
        escalograma_reduzido_total.append(escalograma_reduzido)
        tempos_reduzidos_total.append(tempos_reduzidos)
        
    # Quando terminar, cola todas as fatias reduzidas de volta em uma matriz só
    matriz_final = np.hstack(escalograma_reduzido_total)
    tempos_finais = np.concatenate(tempos_reduzidos_total)
    
    return matriz_final, frequencias, tempos_finais