#índice invertido

#o índice usa um dict, que é uma tabela hash
#complexidade 0(1) médio
#se duas palavras caírem na mesma posição da tabela, ocorre uma colisão
#no pior caso com muitas colisões, a busca pode piorar para O(n)

#construir o índice invertido a partir de 
#{nome_arquivo: [palavras]} para {palavra: {arquivos}}
def construir_indice(documentos):
    indice = {}
    for nome_arquivo, tokens in documentos.items():
        for token in tokens:
            if token not in indice:
                indice[token] = set()
            indice[token].add(nome_arquivo)
    return indice
 
 
#consulta exata no índice invertido
#retorna a lista ordenada de arquivos onde a palavra aparece
def buscar_palavra(indice, palavra):
    return sorted(indice.get(palavra, set()))