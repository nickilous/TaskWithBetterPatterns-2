from Graph import Graph
import sys
from typing import List
from datetime import datetime, timedelta
from Package import Package
from Identifiable import Identifiable
class Truck(Identifiable):
    
    def __init__(self, id: int, city_map: Graph) -> None:
        super().__init__(id)
        self.packages = []
        self.city_map = city_map
        self.mph = 18
        self.capacity = 16
        
        self.total_miles = 0

        self.departure_time = datetime
        self.current_time = datetime
    
    def is_full(self) -> bool:
        return len(self.packages) >= self.capacity
    
    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    def can_load(self, n: int) -> bool:
        return len(self.packages) + n <= self.capacity

    def load_package(self, package: Package, loa) -> None:
        self.packages.append(package)
    
    def plan_route(self) -> List:
        route = []
        current_location = self.hub_location
        
        destinations = 0
        closest_package = None
        packages = self.packages
        while destinations < len(packages) - 1:
            max_miles = sys.maxsize
            for package in packages:
                if package is not None:
                    if package not in self.route:
                        miles = self.city_map.dijkstra(current_location, package.destination)
                        if miles < max_miles:
                            max_miles = miles
                            closest_package = package
            current_location = closest_package.destination
            destinations += 1
            if closest_package not in self.route:
                route.append(closest_package)
        return route

    def deliver_packages(self, route: List):
        current_location = self.hub_location
        for package in self.route:
            self.total_distance += self.city_map.dijkstra(current_location, package.destination)
            travel_minutes = self.travel_time(self.total_distance)
            delivery_time = self.startOfDay + timedelta(minutes=travel_minutes)
            current_location = package.destination
        return self.total_distance
    
    def travel_time(self, miles: int) -> int:
        return round((miles / self.mph) * 60)
    
    def __repr__(self) -> str:
        string = "\nID: " + str(self.id)
        #string += "\n\tRoute: " + str(self.route)
        string += "\n\tPackages: " + str(self.packages)
        return string
    
    def __str__(self) -> str:
        return self.__repr__()