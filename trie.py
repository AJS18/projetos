"""
Parte I - Implementação de Trie e Sistema de Autocomplete.

Equivalência com as operações pedidas no enunciado:
    inserir(palavra)        -> Trie.insert(word)
    buscar(palavra)         -> Trie.search(word)
    buscar_prefixo(prefixo) -> Trie.starts_with(prefix)
"""


class Node:
    """Nó da Trie: cada nó guarda seus filhos (caractere -> Node)
    e uma marcação indicando se uma palavra termina nele."""

    def __init__(self):
        self.children = dict()
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = Node()
        self.word_count = 0  # quantidade de palavras distintas armazenadas

    def insert(self, word):
        """Insere uma palavra na Trie. Complexidade: O(m), m = tamanho da palavra."""
        current_node = self.root

        for character in word:
            if character not in current_node.children:
                current_node.children[character] = Node()

            current_node = current_node.children[character]

        # Só conta se a palavra ainda não existia (evita contar duplicatas)
        if not current_node.is_end_of_word:
            current_node.is_end_of_word = True
            self.word_count += 1

    def search(self, word):
        """Busca exata: retorna True se a palavra existe. Complexidade: O(m)."""
        current_node = self.root

        for character in word:
            if character not in current_node.children:
                return False

            current_node = current_node.children[character]

        return current_node.is_end_of_word

    def has_prefix(self, prefix):
        """Retorna True se existe alguma palavra com o prefixo. Complexidade: O(m)."""
        current_node = self.root

        for character in prefix:
            if character not in current_node.children:
                return False

            current_node = current_node.children[character]

        return True

    def starts_with(self, prefix):
        """Retorna todas as palavras que começam com o prefixo.
        Complexidade: O(m) para chegar ao nó do prefixo + O(k) para
        percorrer os k nós descendentes e montar as palavras."""
        words = []
        current_node = self.root

        # 1) Desce na Trie até o último caractere do prefixo
        for character in prefix:
            if character not in current_node.children:
                return words

            current_node = current_node.children[character]

        # 2) DFS a partir desse nó coletando as palavras completas
        def _dfs(node, path):
            if node.is_end_of_word:
                words.append(''.join(path))

            for character, child_node in node.children.items():
                _dfs(child_node, path + [character])

        _dfs(current_node, list(prefix))
        return words

    def list_words(self):
        """Lista todas as palavras armazenadas (prefixo vazio)."""
        return self.starts_with("")

    def delete(self, word):
        """Remove uma palavra da Trie (funcionalidade extra)."""
        if self.search(word):
            self._delete(self.root, word, 0)
            self.word_count -= 1

    def _delete(self, current_node, word, index):
        # Chegou ao fim da palavra: desmarca e indica se o nó pode ser apagado
        if index == len(word):
            if not current_node.is_end_of_word:
                return False

            current_node.is_end_of_word = False
            return len(current_node.children) == 0

        character = word[index]
        node = current_node.children.get(character)

        if node is None:
            return False

        delete_current_node = self._delete(node, word, index + 1)
        if delete_current_node:
            del current_node.children[character]
            return len(current_node.children) == 0 and not current_node.is_end_of_word

        return False

    def __len__(self):
        return self.word_count


# Palavras iniciais (exemplo do enunciado). Na Parte II serão
# substituídas pelo vocabulário extraído dos arquivos .txt.
palavras_iniciais = [
    "computador", "computação", "computacional", "compilador",
    "complexidade", "programação", "processador", "processamento",
]


def ler_palavra(mensagem):
    """Lê uma entrada do usuário normalizada (minúsculas, sem espaços)."""
    return input(mensagem).strip().lower()


def menu():
    trie = Trie()
    for palavra in palavras_iniciais:
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
            if not palavra:
                print("Entrada vazia.")
            elif trie.search(palavra):
                print(f"A palavra '{palavra}' foi encontrada.")
            else:
                print(f"A palavra '{palavra}' não existe na Trie.")

        elif option == "2":
            prefixo = ler_palavra("Digite o prefixo: ")
            if not prefixo:
                print("Entrada vazia.")
                continue

            results = sorted(trie.starts_with(prefixo))
            if results:
                if len(results) == 1:
                    print("Palavra encontrada:", results)
                else:
                    print("Palavras encontradas:", results)
            else:
                print("Nenhuma palavra encontrada.")

        elif option == "3":
            palavra = ler_palavra("Adicione uma palavra: ")
            if not palavra:
                print("Entrada vazia.")
            elif trie.search(palavra):
                print(f"'{palavra}' já está cadastrada.")
            else:
                trie.insert(palavra)
                print(f"'{palavra}' adicionada!")

        elif option == "4":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()