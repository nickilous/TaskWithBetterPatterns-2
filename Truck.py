from Graph import Graph
import sys
from typing import List
from datetime import datetime, timedelta
from Package import Package
from Location import Location
from Identifiable import Identifiable
class Truck(Identifiable):
    
    def __init__(self, id: int, hub: Location, has_driver: bool,city_map: Graph) -> None:
        super().__init__(id)
        
        #packages to deliver
        self.packages = []
        
        #startup data for truck
        self.city_map = city_map
        self.mph = 18
        self.capacity = 16
        self.hub_location = hub
        
        #total distance from start of day to end of day
        self.total_distance = 0
        
        #route for after packages arranged by shortest distance
        self.route = []
        
        now = datetime.now()
        #running truck clock
        self.current_time = datetime(now.year, now.month, now.day, 8)

        #total travel time for truck
        self.travel_time = timedelta
        
        #each departure time of the truck
        self.departure_time = datetime
        
        #driver constraint
        self.has_driver = has_driver
        
        now = datetime.now()
        #if truck has a delayed package it is set to start of day since truck can't leave
        #till start of day
        self.delayed_till = datetime(now.year, now.month, now.day, 8)
        
        #truck deadline set to earliest deadline of package in truck
        #set to end of day because a truck with no deadline packages has to be back by end of day
        self.deadline = datetime(now.year, now.month, now.day, 17)

    
    def is_full(self) -> bool:
        return len(self.packages) >= self.capacity
    
    def is_empyt(self) -> bool:
        return len(self.packages) == 0
    
    def reset(self):
        self.packages = []
        self.route = []
        self.total_distance = 0
        self.travel_time = datetime

        now = datetime.now()
        self.delayed_till = datetime(now.year, now.month, now.day, 8)
        self.deadline = datetime(now.year, now.month, now.day, 17)
    
    def set_departure_time(self, departure_time):
        self.departure_time = departure_time

    def can_load(self, n: int) -> bool:
        return len(self.packages) + n <= self.capacity

    def load_package(self, package: Package) -> None:
        print("Loading truck: {truck}, with package: {package}".format(truck=self.id, package=package))
        self.packages.append(package)
        if package.delayed_on_plane is not None and package.delayed_on_plane > self.delayed_till:
            self.delayed_till = package.delayed_on_plane
        
        if package.will_be_address_updated_at is not None and package.will_be_address_updated_at > self.delayed_till:
            self.delayed_till = package.will_be_address_updated_at
        
        if package.deadline is not None and self.deadline > package.deadline:
            self.deadline = package.deadline
    
    def __plan_route(self) -> List:
        use_traveling_sales_man = True
        
        if use_traveling_sales_man:
            self.__plan_route_traveling_sales_man()
        else:
            self.__plan_route_nearest_neighbor()
    
    def __get_destinations(self):
        destinations = []
        for package in self.packages:
            destinations.append(package.destination)
        return destinations
    
    def __plan_route_traveling_sales_man(self):
        destinations = self.__get_destinations()
        destinations = self.city_map.travellingSalesmanProblem(self.hub_location, destinations)[1]
        for destination in destinations:
            for package in self.packages:
                if destination == package.destination:
                    self.route.append(package)
    
    def __plan_route_nearest_neighbor(self):
        current_location = self.hub_location
        
        destinations = 0
        closest_package = None
        packages = [package for package in self.packages if package is not None]
        while destinations < len(packages):
            max_miles = sys.maxsize
            for package in packages:
                if package not in self.route:
                    miles = self.city_map.dijkstra(current_location, package.destination)
                    if miles < max_miles:
                        max_miles = miles
                        closest_package = package
            if closest_package is None:
                break
            
            current_location = closest_package.destination
            
            if closest_package not in self.route:
                self.route.append(closest_package)
            destinations += 1
    def deliver_packages(self):
        self.departure_time = self.current_time
        self.delivery_time = self.current_time
        
        self.__plan_route()
        
        current_location = self.hub_location
        distance = 0
        while self.current_time < self.delayed_till:
            self.current_time = self.current_time + timedelta(minutes=1)
        
        for package in self.route:
            distance = self.city_map.dijkstra(current_location, package.destination)
            self.total_distance += distance
            
            travel_minutes = self.get_travel_time(self.total_distance)
            self.delivery_time = self.current_time + timedelta(minutes=travel_minutes)
            
            
            package.deliveryTime = self.delivery_time
            package.delivered_with_truck = self.id
            
            current_location = package.destination
        
        #return to hub after delivering packages
        distance = self.city_map.dijkstra(current_location, self.hub_location)
        
        self.total_distance += distance

        travel_minutes = self.get_travel_time(self.total_distance)
        self.travel_time = self.departure_time + timedelta(minutes=travel_minutes)
        
        self.current_time = self.travel_time
        return self.current_time, self.total_distance
    
    def get_travel_time(self, miles: int) -> int:
        return (miles / self.mph * 60)
    
    def __repr__(self) -> str:
        string = "\nID: " + str(self.id)
        #string += "\n\tRoute: " + str(self.route)
        string += "\n\tPackages: " + str(self.packages)
        return string
    
    def __str__(self) -> str:
        return self.__repr__()