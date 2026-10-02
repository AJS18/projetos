"""
Parte II - Etapa 1: leitura dos documentos e pré-processamento textual.

Etapas aplicadas a cada texto:
    1. Conversão para minúsculas
    2. Remoção de pontuação (e de números)
    3. Tokenização em palavras
    4. Remoção de stopwords

Decisão de implementação: os acentos são MANTIDOS ("computação" continua
"computação"), para ficar consistente com as palavras da Parte I.
"""

import re
from pathlib import Path

# Tudo que NÃO for letra (inclusive acentuadas) ou espaço vira espaço.
# [^\w\s] pega pontuação; \d pega dígitos; _ é tratado à parte porque \w o inclui.
PADRAO_NAO_LETRA = re.compile(r"[^\w\s]|\d|_")


def carregar_stopwords(caminho="stopwords.txt"):
    """Lê o arquivo de stopwords (uma por linha) e devolve um set.
    Usar set deixa a verificação 'palavra in stopwords' O(1) em média (hash)."""
    with open(caminho, encoding="utf-8") as arquivo:
        return {linha.strip().lower() for linha in arquivo if linha.strip()}


def converter_minusculas(texto):
    return texto.lower()


def remover_pontuacao(texto):
    return PADRAO_NAO_LETRA.sub(" ", texto)


def tokenizar(texto):
    # split() sem argumento separa por qualquer espaço em branco e ignora vazios
    return texto.split()


def remover_stopwords(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]


def preprocessar(texto, stopwords):
    """Aplica as 4 etapas em sequência. Complexidade: O(n), n = tamanho do texto."""
    texto = converter_minusculas(texto)
    texto = remover_pontuacao(texto)
    tokens = tokenizar(texto)
    return remover_stopwords(tokens, stopwords)


def ler_arquivo(caminho):
    """Lê um .txt em UTF-8; se falhar (arquivo salvo no Bloco de Notas
    antigo, por exemplo), tenta latin-1."""
    try:
        return caminho.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return caminho.read_text(encoding="latin-1")


def processar_pasta(pasta, stopwords):
    """Processa automaticamente TODOS os .txt da pasta (nenhum nome fixo no código).
    Retorna um dict: nome_do_arquivo -> lista de tokens."""
    pasta = Path(pasta)
    if not pasta.is_dir():
        raise FileNotFoundError(f"Pasta '{pasta}' não encontrada.")

    documentos = {}
    for caminho in sorted(pasta.glob("*.txt")):
        documentos[caminho.name] = preprocessar(ler_arquivo(caminho), stopwords)
    return documentos


# Teste isolado desta etapa: python preprocessamento.py
if __name__ == "__main__":
    # Caminhos relativos à pasta deste arquivo, para rodar de qualquer lugar
    base = Path(__file__).parent
    stopwords = carregar_stopwords(base / "stopwords.txt")

    exemplo = "Os Algoritmos de Busca são muito importantes."
    print("Entrada:", exemplo)
    print("Saída:  ", " | ".join(preprocessar(exemplo, stopwords)))

    documentos = processar_pasta(base / "documentos", stopwords)
    print(f"\nDocumentos processados: {len(documentos)}")
    for nome, tokens in documentos.items():
        print(f"- {nome}: {len(tokens)} tokens -> {tokens[:8]} ...")

    total = sum(len(t) for t in documentos.values())
    distintos = {token for tokens in documentos.values() for token in tokens}
    print(f"\nTotal de palavras após tokenização: {total}")
    print(f"Termos distintos: {len(distintos)}")
