"""
Parte II - Etapa 2: índice invertido (palavra -> documentos).
 
O índice usa um dict do Python, que é uma tabela HASH:
    - a função hash transforma a palavra (chave) em uma posição da tabela;
    - por isso a busca de um termo custa O(1) em média;
    - quando duas chaves caem na mesma posição ocorre uma COLISÃO, que o
      Python resolve internamente (endereçamento aberto). No pior caso,
      com muitas colisões, a busca pode degradar para O(n).
 
Chama-se "invertido" porque inverte a relação natural documento -> palavras
(cada arquivo contém uma lista de palavras) para palavra -> documentos.
"""
 
 
def construir_indice(documentos):
    """Recebe {nome_arquivo: [tokens]} e devolve {palavra: {arquivos}}.
    Complexidade: O(T), T = total de tokens de todos os documentos
    (cada token faz uma inserção O(1) média no dict e no set)."""
    indice = {}
    for nome_arquivo, tokens in documentos.items():
        for token in tokens:
            if token not in indice:
                indice[token] = set()
            indice[token].add(nome_arquivo)
    return indice
 
 
def buscar_palavra(indice, palavra):
    """Consulta exata no índice: O(1) em média (acesso ao dict por hash).
    Retorna a lista ordenada de arquivos onde a palavra aparece."""
    return sorted(indice.get(palavra, set()))