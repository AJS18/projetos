"""
Parte II - Mini mecanismo de busca em arquivos de texto.

Já implementado:  pré-processamento, vocabulário na Trie, índice invertido,
                  busca por palavra exata, busca por prefixo, listagem de
                  documentos e estatísticas (menu do item 3.8).
"""

import time
from pathlib import Path

from trie import Trie  # Reaproveitamento OBRIGATÓRIO da Trie da Parte I
from preprocessamento import (carregar_stopwords, preprocessar, processar_pasta,
                              converter_minusculas, remover_pontuacao, tokenizar)
from indice_invertido import construir_indice, buscar_palavra

BASE = Path(__file__).parent
PASTA_DOCUMENTOS = BASE / "documentos"
ARQUIVO_STOPWORDS = BASE / "stopwords.txt"


# ---------------------------------------------------------------------------
# 3.4 - Construção do vocabulário e inserção na Trie
# ---------------------------------------------------------------------------
def construir_vocabulario(documentos):
    """Conjunto de palavras DISTINTAS de todos os documentos.
    O set descarta repetições em O(1) médio por token -> O(T) no total."""
    vocabulario = set()
    for tokens in documentos.values():
        vocabulario.update(tokens)
    return vocabulario


def construir_trie(vocabulario):
    """Insere cada termo do vocabulário na Trie.
    Complexidade: O(V * m), V = termos distintos, m = tamanho médio do termo."""
    trie = Trie()
    for palavra in vocabulario:
        trie.insert(palavra)
    return trie


# ---------------------------------------------------------------------------
# Classe que agrupa todas as estruturas do mecanismo de busca
# ---------------------------------------------------------------------------
class MecanismoBusca:
    def __init__(self, pasta, arquivo_stopwords):
        self.stopwords = carregar_stopwords(arquivo_stopwords)
        self.documentos = processar_pasta(pasta, self.stopwords)
        self.total_palavras = sum(len(t) for t in self.documentos.values())

        # Vocabulário + Trie (com medição de tempo)
        self.vocabulario = construir_vocabulario(self.documentos)
        inicio = time.perf_counter()
        self.trie = construir_trie(self.vocabulario)
        self.tempo_trie = time.perf_counter() - inicio

        # Índice invertido (com medição de tempo)
        inicio = time.perf_counter()
        self.indice = construir_indice(self.documentos)
        self.tempo_indice = time.perf_counter() - inicio

        # Histórico das consultas: (tipo, termo, nº de resultados, tempo em s)
        self.historico = []

    def registrar(self, tipo, termo, resultados, duracao):
        self.historico.append((tipo, termo, resultados, duracao))
        print(f"Tempo da consulta: {duracao * 1000:.4f} ms")

    # -----------------------------------------------------------------------
    # 3.7.1 - Consulta por palavra exata (índice invertido / hash)
    # -----------------------------------------------------------------------
    def buscar_palavra(self):
        entrada = input("Digite a palavra: ")

        # A consulta passa pelo MESMO pré-processamento dos documentos,
        # senão "Algoritmos" ou "busca," nunca seriam encontrados.
        termos = preprocessar(entrada, self.stopwords)
        if not termos:
            print("Entrada vazia ou composta só por stopwords (essas palavras não são indexadas).")
            return
        if len(termos) > 1:
            print(f"Digite apenas uma palavra. Buscando somente '{termos[0]}'.")
        palavra = termos[0]

        inicio = time.perf_counter()
        arquivos = buscar_palavra(self.indice, palavra)
        duracao = time.perf_counter() - inicio

        if arquivos:
            print(f"Encontrada em {len(arquivos)} arquivo(s):")
            for nome in arquivos:
                print(f"- {nome}")
        else:
            print(f"A palavra '{palavra}' não foi encontrada em nenhum documento.")
        self.registrar("Palavra", palavra, len(arquivos), duracao)

    # -----------------------------------------------------------------------
    # 3.7.2 - Consulta por prefixo: Trie -> termos; índice -> documentos
    # -----------------------------------------------------------------------
    def buscar_prefixo(self):
        entrada = input("Digite o prefixo: ")

        # Aqui NÃO removemos stopwords: um prefixo como "de" é válido
        # (encontra "dados", "definidos"...). Só normalizamos o texto.
        termos = tokenizar(remover_pontuacao(converter_minusculas(entrada)))
        if not termos:
            print("Entrada vazia.")
            return
        prefixo = termos[0]

        inicio = time.perf_counter()
        palavras = sorted(self.trie.starts_with(prefixo))                          # Trie
        resultados = [(p, buscar_palavra(self.indice, p)) for p in palavras]       # Hash
        duracao = time.perf_counter() - inicio

        if resultados:
            print(f"Palavras encontradas ({len(resultados)}):")
            for palavra, arquivos in resultados:
                print(f"{palavra} -> {', '.join(arquivos)}")
        else:
            print(f"Nenhuma palavra começa com '{prefixo}'.")
        self.registrar("Prefixo", prefixo, len(resultados), duracao)

    # -----------------------------------------------------------------------
    # Listar documentos
    # -----------------------------------------------------------------------
    def listar_documentos(self):
        print(f"\n{len(self.documentos)} documento(s) em '{PASTA_DOCUMENTOS.name}/':")
        print(f"{'Arquivo':<32}{'Palavras':>10}{'Distintas':>11}")
        for nome, tokens in self.documentos.items():
            print(f"{nome:<32}{len(tokens):>10}{len(set(tokens)):>11}")

    # -----------------------------------------------------------------------
    # 3.9 - Estatísticas obrigatórias
    # -----------------------------------------------------------------------
    def exibir_estatisticas(self):
        print("\n------------- ESTATÍSTICAS -------------")
        print(f"Documentos processados:         {len(self.documentos)}")
        print(f"Total de palavras (tokens):     {self.total_palavras}")
        print(f"Termos distintos:               {len(self.vocabulario)}")
        print(f"Palavras armazenadas na Trie:   {len(self.trie)}")
        print(f"Tempo de construção da Trie:    {self.tempo_trie * 1000:.4f} ms")
        print(f"Tempo de construção do índice:  {self.tempo_indice * 1000:.4f} ms")

        print("\nConsultas realizadas:")
        if not self.historico:
            print("(nenhuma consulta ainda)")
            return
        print(f"{'#':<4}{'Tipo':<10}{'Termo':<20}{'Resultados':>11}{'Tempo (ms)':>13}")
        for i, (tipo, termo, qtd, duracao) in enumerate(self.historico, start=1):
            print(f"{i:<4}{tipo:<10}{termo:<20}{qtd:>11}{duracao * 1000:>13.4f}")


# ---------------------------------------------------------------------------
# 3.8 - Menu
# ---------------------------------------------------------------------------
def main():
    motor = MecanismoBusca(PASTA_DOCUMENTOS, ARQUIVO_STOPWORDS)

    opcoes = {
        "1": motor.buscar_palavra,
        "2": motor.buscar_prefixo,
        "3": motor.listar_documentos,
        "4": motor.exibir_estatisticas,
    }

    while True:
        print("\n================================================")
        print("          SISTEMA DE BUSCA EM DOCUMENTOS")
        print("================================================")
        print(f"Documentos processados: {len(motor.documentos)}")
        print(f"Total de palavras: {motor.total_palavras}")
        print(f"Termos distintos: {len(motor.vocabulario)}")
        print("1 - Buscar palavra")
        print("2 - Buscar por prefixo")
        print("3 - Listar documentos")
        print("4 - Exibir estatísticas")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "5":
            print("Encerrando...")
            break
        elif opcao in opcoes:
            opcoes[opcao]()  # o próprio dict de opções também é uma tabela hash
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()