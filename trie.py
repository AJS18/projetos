from sys import prefix


class Node:
    def __init__(self):
        self.children = dict()
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = Node()        
        
    def insert(self, word):
        current_node = self.root
        
        for character in word:
            if character not in current_node.children:
                current_node.children[character] = Node()
                
            current_node = current_node.children[character]
            
        current_node.is_end_of_word = True
    
    def search(self, word):
        current_node = self.root 
        
        for character in word:
            if character not in current_node.children:
                return False
            
            current_node = current_node.children[character]
            
        return current_node.is_end_of_word
    
    def delete(self, word):
        self._delete(self.root, word, 0)
    
    def has_prefix(self, word):
        current_node = self.root 
        
        for character in prefix:
            if character not in current_node.children:
                return False
            
            current_node = current_node.children[character]
            
        return True
    
    def starts_with(self, word):
        words = []
        current_node = self.root
        
        for character in word:
            if character not in current_node.children:
                return words
            
            current_node = current_node.children[character]
            
        def _dfs(current_node, path):
            if current_node.is_end_of_word:
                words.append(''.join(path))
                
            for character, child_node in current_node.children.items():
                _dfs(child_node, path + [character])

        _dfs(current_node, list(word))
        return words
                
    def list_words(self):
        words = []
        
        def _dfs(current_node, path):
                    if current_node.is_end_of_word:
                        words.append(''.join(path))
                        
                    for character, child_node in current_node.children.items():
                        _dfs(child_node, path + [character])
                        
        _dfs(self.root, [])
            
        return words

    def _delete(self, current_node, word, index):
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
        
if __name__ == "__main__":
    trie = Trie()
        
    while True:
        print("\n1 - Inserir palavra")
        print("2 - Buscar palavra")
        print("3 - Listar todas as palavras")
        print("4 - Sair")
        
        option = input("Escolha uma opção: ").strip()
        
        if option == "1":
            palavra = input("Digite a palavra: ").strip()
            trie.insert(palavra)
            print(f"'{palavra}' adicionada!")
        
        elif option == "2":
            palavra = input("Digite a palavra: ").strip()
            results = trie.starts_with(palavra)
            
            if results:
                if len(results) == 1:
                    print("Palavra encontrada:", results)
                else:
                    print("Palavras encontradas:", results)
            else:
                print("Nenhuma palavra encontrada.")
      
        elif option == "3":
            
            if trie.list_words() == []:
                print("Nenhuma palavra cadastrada.")
            else:
                print("Palavras:", trie.list_words())
            
        
        elif option == "4":
            break
        
        else:
            print("Opção inválida.")