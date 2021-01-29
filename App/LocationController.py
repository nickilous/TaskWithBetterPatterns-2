from CSVReader import CSVReader
from Location import Location
#test sync grom working copy
class LocationController():
    
    def __init__(self, locations) -> None:
        super().__init__()
        self.locations = []
        for row in locations:
            location = Location(int(row[0]), row[1], row[2])
            self.locations.append(location)
    
        
