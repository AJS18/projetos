#mini meacnismo de busca em arquivos de texto

import time #serve para medir o tempo das execuções
from pathlib import Path

from trie import Trie  #reaproveitamento da trie
from preprocessamento import (carregar_stopwords, preprocessar, processar_pasta,
                              converter_minusculas, remover_pontuacao, tokenizar)
from indice_invertido import construir_indice, buscar_palavra

#constantes que permitem que o main encontre os arquivos .txt
BASE = Path(__file__).parent
PASTA_DOCUMENTOS = BASE / "documentos"
ARQUIVO_STOPWORDS = BASE / "stopwords.txt"

#constrói o vocabulário
#junta as palavras distintas de todos os documentos em um set
#complexidade: O(T), T = total de tokens em todos os documentos
def construir_vocabulario(documentos):
    vocabulario = set()
    for tokens in documentos.values():
        vocabulario.update(tokens)
    return vocabulario

#constrói a trie a partir do vocabulário
#insere cada termo do vocabulário na trie
#complexidade: O(V * m), V = vocabulário(palavras distintas), m = tamanho médio do termo
def construir_trie(vocabulario):
    trie = Trie()
    for palavra in vocabulario:
        trie.insert(palavra)
    return trie

#classe que junta todas as estruturas do mecanismo de busca
class MecanismoBusca:
    
    #carrega as stopwords, processa os documentos e conta o total de palavras
    def __init__(self, pasta, arquivo_stopwords):
        self.stopwords = carregar_stopwords(arquivo_stopwords)
        self.documentos = processar_pasta(pasta, self.stopwords)
        self.total_palavras = sum(len(t) for t in self.documentos.values())

        #vocabulário e trie com medição de tempo
        self.vocabulario = construir_vocabulario(self.documentos)
        inicio = time.perf_counter()
        self.trie = construir_trie(self.vocabulario)
        self.tempo_trie = time.perf_counter() - inicio

        #índice invertido com medição de tempo
        inicio = time.perf_counter()
        self.indice = construir_indice(self.documentos)
        self.tempo_indice = time.perf_counter() - inicio

        #histórico das consultas
        self.historico = []
    
    #registra cada consulta no histórico e mostra o tempo de execução
    def registrar(self, tipo, termo, resultados, duracao):
        self.historico.append((tipo, termo, resultados, duracao))
        print(f"Tempo da consulta: {duracao * 1000:.4f} ms")

    #consulta por palavra exata
    def consultar_palavra(self):
        entrada = input("Digite a palavra: ")
        termos = preprocessar(entrada, self.stopwords)

        if termos:
            if len(termos) > 1:
                print(f"Digite apenas uma palavra. Buscando somente '{termos[0]}'.")
            palavra = termos[0]

            #medição de tempo da consulta da palavra
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
        else:
            print("Entrada vazia ou composta só por stopwords (essas palavras não são indexadas).")

    #consulta por prefixo sem remover as stopwords
    def buscar_prefixo(self):
        entrada = input("Digite o prefixo: ")
        termos = tokenizar(remover_pontuacao(converter_minusculas(entrada)))

        if termos:
            prefixo = termos[0]
            
            #medindo o tempo da consulta do prefixo
            inicio = time.perf_counter()
            palavras = sorted(self.trie.starts_with(prefixo))                          # Trie
            resultados = [(p, buscar_palavra(self.indice, p)) for p in palavras]       # Hash
            duracao = time.perf_counter() - inicio

            #mostra as palavras encontradas e os arquivos onde elas aparecem
            if resultados:
                print(f"Palavras encontradas ({len(resultados)}):")
                for palavra, arquivos in resultados:
                    print(f"{palavra} -> {', '.join(arquivos)}")
            else:
                print(f"Nenhuma palavra começa com '{prefixo}'.")
            self.registrar("Prefixo", prefixo, len(resultados), duracao)
        else:
            print("Entrada vazia.")

    #lista todos os documentos processados
    #mostrando o total de palavras e o total de palavras distintas
    def listar_documentos(self):
        print(f"\n{len(self.documentos)} documento(s) em '{PASTA_DOCUMENTOS.name}':")
        print(f"{'Arquivo':<32}{'Palavras':>10}{'Distintas':>11}")
        for nome, tokens in self.documentos.items():
            print(f"{nome:<32}{len(tokens):>10}{len(set(tokens)):>11}")

    #mostra as estatísticas do mecanismo de busca e do histórico de consultas
    def exibir_estatisticas(self):
        print("\n------------- ESTATÍSTICAS -------------")
        print(f"Documentos processados:         {len(self.documentos)}")
        print(f"Total de palavras (tokens):     {self.total_palavras}")
        print(f"Termos distintos:               {len(self.vocabulario)}")
        print(f"Palavras armazenadas na Trie:   {len(self.trie)}")
        print(f"Tempo de construção da Trie:    {self.tempo_trie * 1000:.4f} ms")
        print(f"Tempo de construção do índice:  {self.tempo_indice * 1000:.4f} ms")

        print("\nConsultas realizadas:")
        if self.historico:
            print(f"{'#':<4}{'Tipo':<10}{'Termo':<20}{'Resultados':>11}{'Tempo (ms)':>13}")
            
            #percorre o histórico enumerando as consultas
            for i, (tipo, termo, qtd, duracao) in enumerate(self.historico, start=1):
                print(f"{i:<4}{tipo:<10}{termo:<20}{qtd:>11}{duracao * 1000:>13.4f}")
        else:
            print("(nenhuma consulta ainda)")


#menu mecanismo de busca
def main():
    motor = MecanismoBusca(PASTA_DOCUMENTOS, ARQUIVO_STOPWORDS)

    #constrói um disct de opções
    opcoes = {
        "1": motor.consultar_palavra,
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
            opcoes[opcao]()  #o próprio dict de opções também é uma tabela hash
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()