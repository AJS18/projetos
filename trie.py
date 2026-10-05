#trie e auto complete

class Node:
    def __init__(self):
        self.children = dict() #um dict dos caracteres das palavras. custo O(1) para acessar um nó
        self.is_end_of_word = False #indica se o nó é o final de uma palavra

class Trie:
    def __init__(self):
        self.root = Node()
        self.word_count = 0  #qtd de palavras distintas armazenadas

    #insere uma palavra na trie
    #complexidade: O(m), m = tamanho da palavra.
    def insert(self, word):
        current_node = self.root

        for character in word:
            if character not in current_node.children:
                current_node.children[character] = Node()

            current_node = current_node.children[character]

        #só conta se a palavra ainda não existia (evita contar palavras repetidas)
        if not current_node.is_end_of_word:
            current_node.is_end_of_word = True
            self.word_count += 1

    #retorna true se a palavra existe na trie, false caso contrário
    #complexidade: O(m)
    def search(self, word):
        current_node = self.root

        for character in word:
            if character not in current_node.children:
                return False

            current_node = current_node.children[character]

        return current_node.is_end_of_word

    #retorna todas as palavras que começam com o prefixo
    #complexidade: O(m) para chegar ao nó do prefixo + O(k) para
    #percorrer os k caracteres descendentes e montar as palavras. 0(m+k)
    def starts_with(self, prefix):
        words = []
        current_node = self.root

        #percorre na trie até o último caractere do prefixo
        for character in prefix:
            if character not in current_node.children:
                return words

            current_node = current_node.children[character]

        #algoritmo que percorre toda a trie
        #se o caractere atual for o final de uma palavra
        #adiciona a palavra na lista
        def _dfs(node, path):
            if node.is_end_of_word:
                words.append(''.join(path))

            for character, child_node in node.children.items():
                _dfs(child_node, path + [character])

        _dfs(current_node, list(prefix))
        return words

    #função que retorna a qtd de palavras distintas armazenadas na trie
    def __len__(self):
        return self.word_count


#palavras previamente cadastradas na trie
PALAVRAS_INICIAIS = [
    "computador", "computação", "computacional", "compilador",
    "complexidade", "programação", "processador", "processamento",
]

#ler palavra digitada, removendo os espaços e convertendo para minúsculas
def ler_palavra(mensagem):
    return input(mensagem).strip().lower()


def menu():
    trie = Trie()
    for palavra in PALAVRAS_INICIAIS:
        trie.insert(palavra)

    while True:
        print("\n====================================")
        print("       AUTOCOMPLETE COM TRIE")
        print("====================================")
        print(f"Palavras cadastradas: {len(trie)}")
        print("1 - Buscar palavra")
        print("2 - Buscar por prefixo")
        print("3 - Inserir nova palavra")
        print("4 - Sair")

        option = input("Escolha uma opção: ").strip()

        if option == "1":
            palavra = ler_palavra("Digite a palavra: ")
            if palavra and trie.search(palavra):
                print(f"A palavra '{palavra}' existe na Trie.")
            elif palavra:
                print(f"A palavra '{palavra}' não existe na Trie.")
            else:
                print("Entrada vazia.")

        elif option == "2":
            prefixo = ler_palavra("Digite o prefixo: ")
            if prefixo:
                results = sorted(trie.starts_with(prefixo))
                if results:
                    print("Palavras encontradas:")
                    for palavra in results:
                        print(palavra)
                else:
                    print("Nenhuma palavra encontrada.")
            else:
                print("Entrada vazia.")

        elif option == "3":
            palavra = ler_palavra("Digite a nova palavra: ")
            if palavra and trie.search(palavra):
                print(f"'{palavra}' já está cadastrada.")
            elif palavra:
                trie.insert(palavra)
                print(f"'{palavra}' adicionada!")
            else:
                print("Entrada vazia.")

        elif option == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()