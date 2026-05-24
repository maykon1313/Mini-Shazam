from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

def _finalizar_figura(fig, caminho_arquivo):
	Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)
	fig.tight_layout()
	fig.savefig(caminho_arquivo, dpi=150)
	plt.close(fig)

def plot_sinal_tempo(sinal, taxa_amostragem, caminho_arquivo, titulo):
	tempos = np.arange(len(sinal)) / taxa_amostragem
	fig, ax = plt.subplots(figsize=(10, 3))
	ax.plot(tempos, sinal, color="black", linewidth=0.6)
	ax.set_title(titulo)
	ax.set_xlabel("Tempo (s)")
	ax.set_ylabel("Amplitude")
	_finalizar_figura(fig, caminho_arquivo)

def plot_espectrograma(espectrograma_db, frequencias, tempos, caminho_arquivo, titulo):
	fig, ax = plt.subplots(figsize=(10, 4))
    
    # O pcolormesh é a melhor forma de desenhar a "onda" do escalograma
	
	im = ax.pcolormesh(tempos, frequencias, espectrograma_db, cmap="viridis", shading="auto")
    
	ax.set_title(titulo)
	ax.set_xlabel("Tempo (s)")
	ax.set_ylabel("Frequencia (Hz)")
	fig.colorbar(im, ax=ax, label="Energia Wavelet (dB)")
    
	_finalizar_figura(fig, caminho_arquivo)


def plot_mapa_constelacao(picos, caminho_arquivo, titulo):
	if not picos:
		return

	tempos, frequencias = zip(*picos)

	fig, ax = plt.subplots(figsize=(10, 4))
	ax.scatter(tempos, frequencias, s=6, c="black", alpha=0.85)
	ax.set_title(titulo)
	ax.set_xlabel("Tempo (s)")
	ax.set_ylabel("Frequencia (Hz)")
	_finalizar_figura(fig, caminho_arquivo)

def plot_histograma_offsets(offsets_contagem, caminho_arquivo, titulo):
	if not offsets_contagem:
		return

	offsets = np.array(sorted(offsets_contagem.keys()))
	contagens = np.array([offsets_contagem[offset] for offset in offsets])

	fig, ax = plt.subplots(figsize=(10, 3))
	ax.bar(offsets, contagens, width=0.02, color="#2a9d8f")
	ax.set_title(titulo)
	ax.set_xlabel("Offset (s)")
	ax.set_ylabel("Contagem")
	_finalizar_figura(fig, caminho_arquivo)


def plot_escalograma(escalograma_db, frequencias, tempos, caminho_arquivo, titulo):
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # O pcolormesh é a melhor forma de desenhar a "onda" do escalograma
    im = ax.pcolormesh(tempos, frequencias, escalograma_db, cmap="viridis", shading="auto")
    
    ax.set_title(titulo)
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Frequencia (Hz)")
    fig.colorbar(im, ax=ax, label="Energia Wavelet (dB)")
    
    _finalizar_figura(fig, caminho_arquivo)