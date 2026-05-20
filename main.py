from pathlib import Path
import pickle

from src.matching import indexar_musica, buscar_musica

BASE_DIR = Path(__file__).parent

MUSICAS = BASE_DIR / "audios" / "raw"
GRAVACOES = BASE_DIR / "audios" / "gravacao"
BANCO = BASE_DIR / "data" / "banco_fingerprint.pkl"

def salvar_banco(banco, caminho_arquivo):
	with open(caminho_arquivo, "wb") as arquivo:
		pickle.dump(banco, arquivo)

def carregar_banco(caminho_arquivo):
	with open(caminho_arquivo, "rb") as arquivo:
		return pickle.load(arquivo)

def indexar():
	banco = {}

	print("\nIndexando músicas para o banco de dados.")
	
	for caminho in sorted(MUSICAS.glob("*.mp3")):
		nome = caminho.stem
		print("Indexando:", caminho)
		indexar_musica(str(caminho), nome, banco)

	salvar_banco(banco, BANCO)
	print("Banco salvo em:", BANCO)

def buscar():
	banco = carregar_banco(BANCO)

	print("\nBuscando correspondencia para os áudios.")

	for caminho in sorted(GRAVACOES.glob("*.mp3")):
		nome = caminho.stem
		print("\nBuscando:", nome)
		buscar_musica(str(caminho), banco)

def main():
	ind = False
	bus = True

	if ind:
		indexar()
		
	if bus:
		buscar()

if __name__ == "__main__":
	main()

# O pickle é um módulo da biblioteca padrão do Python usado para serializar e desserializar objetos Python. 
# 	- Serialização: Processo de converter um objeto Python (como listas, dicionários, classes, etc.) em um formato binário que pode ser armazenado em um arquivo ou transmitido pela rede.
# 	- Desserialização: Processo inverso, onde o formato binário é convertido de volta para o objeto Python original.

# Serializar (salvar um objeto): Usa-se a função dump para gravar o objeto em um arquivo binário.
# Aqui, o dicionário banco é salvo no arquivo banco_fingerprint.pkl.

# Desserializar (carregar um objeto):Usa-se a função load para ler o arquivo binário e reconstruir o objeto Python.
# Aqui, o arquivo banco_fingerprint.pkl é carregado e convertido de volta para o dicionário banco.

# Ele é usado para armazenar o banco de dados de fingerprints gerado durante a indexação das músicas.
