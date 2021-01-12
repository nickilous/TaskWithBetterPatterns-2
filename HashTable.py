from enum import Enum, auto
from Identifiable import Identifiable
from typing import List

class HashTable():
    table: List
    def __init__(self, capacity = 20) -> None:
        super().__init__()
        self.capacity = capacity
        self.num_of_items = 0
        self.table = [None] * self.capacity
  
    # Hashing Function to return  
    # key for every value. 
    def hashing(self, keyvalue: Identifiable): 
        return hash(keyvalue)  % len(self.table)
  
    # Insert Function to add 
    # values to the hash table 
    def insert(self, value: Identifiable):
        if self.should_resize():
            self.resize()
        hash_key = self.hashing(value) 
        self.table[hash_key] = value
        self.num_of_items += 1

    # Update function to just update
    # an already filled location on
    # the Hashtable
    def update(self, value: Identifiable):
        hash_key = self.hashing(value) 
        self.table[hash_key] = value
    
    def should_resize(self) -> bool:
        if self.capacity - 1 == self.num_of_items: return True
    
    def resize(self):
        temp_table = self.table[:]
        self.capacity *= 2
        self.table = [None] * self.capacity
        for item in temp_table:
            if item is not None:
                self.insert(item)

    # Search function to return
    # values associated with Key
    def search(self, keyValue: int) -> Identifiable:
        hash_key = self.hashing(keyValue)
        return self.table[hash_key]
    
    def get_list(self):
        result = []
        for item in self.table:
            if item is not None:
                result.append(item)
        return result

    def __repr__(self) -> str:
        string = "Edges: "

        for index in range(len(self.table)):
            string += "\n\nHash: " + str(index)
            string += "\n----------------------"
            string += "\nValue: " + str(self.table[index]) 
        return string
    
    def __getitem__(self, key) -> Identifiable:
        return self.search(key)

    def __str__(self) -> str:
        return self.__repr__() 
    
    def __len__(self):
        return len(self.table)
    
    def __iter__(self):
        return iter(self.table)
