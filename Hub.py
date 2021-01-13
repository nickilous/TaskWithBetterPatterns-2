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
        self.city_map = city_map
        self.total_distance = 0
        
        now = datetime.now()
        
        self.startOfDay = datetime(now.year, now.month, now.day, 8)
        self.endOfDay = datetime(now.year, now.month, now.day, 17)

        self.current_time = self.startOfDay
        
        self.package_controller = package_controller
        self.highest_priority_packages = package_controller.get_linked_packages_with_deadlines()
        self.hight_priority_packages = package_controller.get_packages_with_deadline()
        self.priority_packages = package_controller.get_linked_packages_without_deadlines()
        self.packages_with_truck_specified = package_controller.get_packages_with_truck()
        self.regular_packages = package_controller.get_standard_packages()
        
        self.num_of_trucks = num_of_trucks
        self.trucks: List[Truck] = []
        for index in range(num_of_trucks):
            #used positional agrumenst for better readability on the truck id argument
            truck = Truck(id=index+1, city_map=self.city_map)
    
    def load_trucks(self):
        for truck in self.trucks:
            for package in self.highest_priority_packages:
                if not truck.is_full() and package.truck != truck.id:
                    self.highest_priority_packages.remove(package)
                    self.load_truck(truck, package)


    def load_truck(self, truck: Truck, package: Package, load) -> List:
        truck.load_package(package)
        self.package_controller.load_package_on_truck(package, self.current_time)
    
    def start_deliveries(self):
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

def main():
    hub = Hub()
    #print(hub.packages)
    print(hub.trucks)
    #print(hub.graph)

if __name__ == "__main__":
    main()