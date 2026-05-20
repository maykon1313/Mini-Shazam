import librosa
from scipy.signal import butter, sosfilt

TAXA_AMOSTRAGEM = 44100
FREQ_MIN = 8000
FREQ_MAX = 11025
ORDEM_FILTRO = 4

def bandpass_filter(sinal, taxa_amostragem):
	# Cria um filtro passa-faixa para manter apenas a banda de interesse.
	sos = butter(ORDEM_FILTRO, [FREQ_MIN, FREQ_MAX], btype="bandpass", fs=taxa_amostragem, output="sos")

	# Aplica o filtro no sinal no dominio do tempo.
	sinal_filtrado = sosfilt(sos, sinal)

	return sinal_filtrado

def carregar_audio(caminho_arquivo):
	# Carrega o audio em mono e reamostra para 44100 Hz.
	sinal, taxa_amostragem = librosa.load(caminho_arquivo, sr=TAXA_AMOSTRAGEM, mono=True)

	# Filtra o sinal para manter apenas a banda utils (8000-11025 Hz).
	sinal = bandpass_filter(sinal, taxa_amostragem)

	return sinal

# butter:
# É uma função da biblioteca scipy.signal que cria um filtro digital do tipo Butterworth.
# O filtro Butterworth é conhecido por ter uma resposta de frequência "suave", ou seja, ele não apresenta ondulações na banda de passagem ou na banda de rejeição.
# A função butter retorna os coeficientes do filtro, que podem ser usados para aplicar o filtro em um sinal.
# O filtro é configurado como um filtro passa-faixa (bandpass) para manter apenas as frequências entre FREQ_MIN (8000 Hz) e FREQ_MAX (11025 Hz).

# sosfilt:
# Também da biblioteca scipy.signal, a função sosfilt aplica um filtro digital a um sinal no domínio do tempo.
# O filtro é representado no formato Second-Order Sections (SOS), que é uma forma numérica mais estável para implementar filtros digitais, especialmente filtros de alta ordem como o Butterworth.
# O sosfilt aplica o filtro criado pelo butter ao sinal de áudio.