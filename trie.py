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
            if character in current_node.children:
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
        pass
    
    def has_prefix(self, word):
        pass
    
    def starts_with(self, word):
        pass
    
    def list_words(self):
        pass