from Graph import Graph
from typing import List
from datetime import datetime
from Package import Package
from Identifiable import Identifiable
class Truck(Identifiable):
    
    def __init__(self, id: int) -> None:
        super().__init__(id)
        self.packages = []

        self.mph = 18
        self.capacity = 16

        self.departure_time = datetime
        self.current_time = datetime
    
    def is_full(self) -> bool:
        return len(self.packages) >= self.capacity

    def depart_at(self, time: datetime) -> None:
        self.departure_time = time
        self.current_time = self.departure_time if self.departure_time > self.current_time else self.current_time

    def destinations(self) -> List[str]:
        return [package.destination for package in self.packages]

    def can_load(self, n: int) -> bool:
        return len(self.packages) + n <= self.capacity

    def load_package(self, package: Package) -> None:
        self.packages.append(package)

    def load_packages(self, packages: List[Package]) -> None:
        for package in packages:
            self.load_package(package)

    def unload_package(self, package: Package) -> None:
        if package in self.packages:
            self.packages.remove(package)

    def unload_packages(self, packages: List[Package]) -> None:
        for package in packages:
            if package in self.packages:
                self.packages.remove(package)

    def has_package(self, package: Package) -> bool:
        return package in self.packages

    def can_deliver(self, package: Package) -> bool:
        return self.id in package.deliverable_by and self.departure_time >= package.arrival_time

    def travel_time(self, miles: int) -> int:
        return round((miles / self.mph) * 60)
    
    def __repr__(self) -> str:
        string = "\nID: " + str(self.id)
        #string += "\n\tRoute: " + str(self.route)
        string += "\n\tPackages: " + str(self.packages)
        return string
    
    def __str__(self) -> str:
        return self.__repr__()