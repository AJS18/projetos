#preprocessamento dos textos

import re #função que encontra tudo que não seja letra
from pathlib import Path #função que permite manipular caminhos de arquivos e pastas

#constante que pega pontuações, números ou espaço
#[^\w\s] pega pontuação e espaço
#\d pega números
PADRAO_NAO_LETRA = re.compile(r"[^\w\s]|\d")

#lê o arquivo de stopwords, uma por linha e devolve um set
#complexidade:O(1) médio usando hash
def carregar_stopwords(caminho="stopwords.txt"):
    with open(caminho, encoding="utf-8") as arquivo:
        return {linha.strip().lower() for linha in arquivo if linha.strip()}

#converte as palavras para minúsculas
def converter_minusculas(texto):
    return texto.lower()

#remove pontuação e números do texto, substituindo por espaço
def remover_pontuacao(texto):
    return PADRAO_NAO_LETRA.sub(" ", texto)

#tokeniza o texto em palavras, separando elas
def tokenizar(texto):
    return texto.split()

#remove qualquer palavra que esta no arquivo de stopwords
#e cria um novo set de tokens sem as stopwords
#complexidade: O(1) médio
def remover_stopwords(tokens, stopwords):
    resultado = []
    for token in tokens:
        if token not in stopwords:
            resultado.append(token)
    return resultado    

#função que aplica todas as etapas de preprocessamento em um texto
#complexidade: O(n), n = tamanho do texto
def preprocessar(texto, stopwords):
    texto = converter_minusculas(texto)
    texto = remover_pontuacao(texto)
    tokens = tokenizar(texto)
    return remover_stopwords(tokens, stopwords)

#lê todos os arquivos .txt
def ler_arquivo(caminho):
    try:
        return caminho.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return caminho.read_text(encoding="latin-1")

#pré processa todos os .txt, coloca em ordem alfabética
#e guarda em um dict {nome_arquivo: palavras}
def processar_pasta(pasta, stopwords):
    pasta = Path(pasta)
    if pasta.is_dir():
        documentos = {}
        for caminho in sorted(pasta.glob("*.txt")):
            documentos[caminho.name] = preprocessar(ler_arquivo(caminho), stopwords)
        return documentos

    raise FileNotFoundError(f"Pasta '{pasta}' não encontrada.")
