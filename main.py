from pathlib import Path
import pickle

from src.matching import indexar_musica, buscar_musica

BASE_DIR = Path(__file__).parent

ref_dir = BASE_DIR / "audios" / "raw"
gravacao_teste = BASE_DIR / "audios" / "gravacao" / "gravacao_de_audio.mp3"
banco_arquivo = BASE_DIR / "data" / "banco_fingerprint.pkl"

def salvar_banco(banco, caminho_arquivo):
	with open(caminho_arquivo, "wb") as arquivo:
		pickle.dump(banco, arquivo)

def carregar_banco(caminho_arquivo):
	with open(caminho_arquivo, "rb") as arquivo:
		return pickle.load(arquivo)

def indexar():
	banco = {}

	for caminho in sorted(ref_dir.glob("*.mp3")):
		nome = caminho.stem
		print("Indexando:", caminho)
		indexar_musica(str(caminho), nome, banco)

	salvar_banco(banco, banco_arquivo)
	print("Banco salvo em:", banco_arquivo)

def buscar(caminho_gravacao):
	banco = carregar_banco(banco_arquivo)
	print("Buscando correspondencia para:", caminho_gravacao)
	buscar_musica(str(caminho_gravacao), banco)

def main():
	ind = True
	bus = True

	if ind:
		indexar()
		
	if bus:
		buscar(gravacao_teste)

if __name__ == "__main__":
	main()
