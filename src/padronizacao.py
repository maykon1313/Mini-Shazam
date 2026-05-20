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

	return sinal, taxa_amostragem
