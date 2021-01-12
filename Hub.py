from Package import Package, PackageStatus
from os import close
from Location import Location
from datetime import datetime, timedelta
from LocationController import LocationController
from PackageController import PackageController
import sys

from Graph import Graph
from typing import List
from Truck import Truck
from CSVReader import CSVReader


class Hub():
    def __init__(self, package_controller: PackageController, location_controller: LocationController, city_map: Graph, num_of_trucks: int = 3) -> None:
        super().__init__()
        self.hub_location = location_controller.locations[0]
        self.total_distance = 0
        now = datetime.now()
        self.startOfDay = datetime(now.year, now.month, now.day, 8)
        self.endOfDay = datetime(now.year, now.month, now.day, 17)
        self.package_controller = package_controller

        self.num_of_trucks = num_of_trucks
        self.truck = Truck(0)

        for package in package_controller.packages:
            if package is not None:
                self.truck.load_package(package)
        
        
        
        # self.route = []
        # for source in location_controller.locations:
        #     max_miles = sys.maxsize
        #     if source is not None:
        #         closest_package: Location = None
        #         for package in self.truck.packages:
                    
        #             if source != package:
        #                 miles = city_map.dijkstra(source, package.destination)
        #                 if miles < max_miles:
        #                     closest_package = package
        #                     max_miles = miles
        #         if closest_package is not None:
        #             print(max_miles)
        #             self.route.append(closest_package)
        # self.total_distance = 0
        """ self.route = []
        current_location = self.hub_location
        
        destinations = 0
        closest_package = None
        packages = package_controller.packages
        before_len_packages = len(packages)
        while destinations < len(packages) - 1:
            len_packages = len(packages)
            max_miles = sys.maxsize
            for package in packages:
                if package is not None:
                    if package not in self.route:
                        miles = city_map.dijkstra(current_location, package.destination)
                        if miles < max_miles:
                            max_miles = miles
                            closest_package = package
            #print(max_miles)
            current_location = closest_package.destination
            destinations += 1
            if closest_package not in self.route:
                self.route.append(closest_package)
            #package.status = PackageStatus.ON_TRUCK
            #package_controller.load_package_on_truck(closest_package, timedelta(minutes=3))

        current_location = self.hub_location
        
        for package in self.route:
            self.total_distance += city_map.dijkstra(current_location, package.destination)
            travel_minutes = self.truck.travel_time(self.total_distance)
            delivery_time = self.startOfDay + timedelta(minutes=travel_minutes)
            package_controller.deliver_package(package, delivery_time)
            current_location = package.destination
        print(self.total_distance) """
    
    def load_truck(self) -> List:
        pass
            



    def _load_distances(self):
        csvData = CSVReader()
        distances = []
        for row in csvData.read_distances():
            distances.append(row)
        return distances
    

    def _load_trucks(self):
        trucks = []
        for i in range(self.num_of_trucks):
            truck = Truck(i + 1)
            trucks.append(truck)
           
        
        
        # for truck in trucks:
        #     for package in self.packages:
        #         if not truck.is_full():
        #             if package is not None:
        #                 if package.deadline is not None and package.status is PackageStatus.AWAITING_DELIVERY:
        #                     truck.load_package(package)
        #                     package.on_truck()
        #                 elif package.status is PackageStatus.AWAITING_DELIVERY:
        #                     truck.load_package(package)
        #                     package.on_truck()
        
        for truck in trucks:
            for package in self.packages:
                if not truck.is_full():
                    if package is not None and package.status is PackageStatus.AWAITING_DELIVERY:
                        if truck.id == package.truck:
                            truck.load_package(package)
                            if package.deliveredWith is not None:
                                for id in package.deliveredWith:
                                    truck.load_package(self.packages[id])
                                    se
                            continue
                        if package.deadline is not None and package.delayedTill is None:
                            truck.load_package(package)
                            if package.deliveredWith is not None:
                                for id in package.deliveredWith:
                                    truck.load_package(self.packages[id])
                            package.status = PackageStatus.ON_TRUCK
                            continue
                        if package.delayedTill is not None:
                            truck.load_package(package)
                            if package.deliveredWith is not None:
                                for id in package.deliveredWith:
                                    truck.load_package(self.packages[id])
                            package.status = PackageStatus.ON_TRUCK

        # for package in self.packages:
        #     if package is not None:
        #         for truck in trucks:
        #             if not truck.is_full():
        #                 if package.truck == truck.id:
        #                     if truck.load_package(package):
        #                         package.on_truck()
        #                 if package.deadline is not None and package.status is PackageStatus.AWAITING_DELIVERY:
        #                     if truck.load_package(package):
        #                         package.on_truck()
        #                     break
        #                 if package.deadline is None and package.status is PackageStatus.AWAITING_DELIVERY:
        #                     if truck.load_package(package):
        #                         package.on_truck()
        return trucks
    
    def deliver_packages(self, distance_table: Graph, return_to_depot: bool) -> None:
        current_location = distance_table.depot_address
        destinations = self.destinations()
        total_time = self.departure_time
        total_distance = 0

        while self.packages:
            destinations = sorted(destinations,
                                  key=lambda x: distance_table.distance(current_location, x))
            closest = destinations.pop(0)

            distance = distance_table.distance(current_location, closest)
            travel_time = self.travel_time(distance)
            total_time.add_minutes(travel_time)

            deliveries = [package for package in self.packages
                          if package.street == closest]

            for package in deliveries:
                self.packages.remove(package)
                package.deliver(total_time.clone())

            current_location = closest
            total_distance += distance

        if return_to_depot:
            distance = distance_table.to_depot(current_location)
            travel_time = self.travel_time(distance)

            total_distance += distance
            total_time.add_minutes(travel_time)

        self.current_time = Clock(self.current_time.hours + total_time.hours,
                                  self.current_time.minutes + total_time.minutes)
        return total_distance
def main():
    hub = Hub()
    #print(hub.packages)
    print(hub.trucks)
    #print(hub.graph)

if __name__ == "__main__":
    main()