from Identifiable import Identifiable
class Location(Identifiable):
    
    name: str
    street: str
    
    def __init__(self, id: int, name: str, street: str):
        super().__init__(id)
        self.name = name
        self.street = street
        
    
    def __repr__(self) -> str:
        string = "\n\tLocation ID: " + str(self.id)
        string += "\n\t\tName: " + str(self.name)
        string += "\n\t\tStree: " + str(self.street) + "\n"
        return string
    

    def __str__(self) -> str:
        return self.__repr__()
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def __eq__(self, o ) -> bool:
        if isinstance(o, self.__class__):
            return self.street == o.street
        return NotImplemented
