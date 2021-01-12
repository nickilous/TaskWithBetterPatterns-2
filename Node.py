from Identifiable import Identifiable
class Node(Identifiable):
    def __init__(self, id: int, data) -> None:
        super().__init__(id)
        self.data = data