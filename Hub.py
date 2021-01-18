from Package import Package, PackageStatus
from datetime import datetime, timedelta
from LocationController import LocationController
from PackageController import PackageController
from ReturningThread import ReturningThread
import queue

from Graph import Graph
from typing import List
from Truck import Truck
from CSVReader import CSVReader


class Hub():
    def __init__(self, package_controller: PackageController, location_controller: LocationController, city_map: Graph, num_of_trucks: int = 3, number_of_drivers: int = 2) -> None:
        super().__init__()
        self.hub_location = location_controller.locations[0]
        self.city_map = city_map
        self.total_distance = 0
        
        now = datetime.now()
        
        self.startOfDay = datetime(now.year, now.month, now.day, 8)
        self.endOfDay = datetime(now.year, now.month, now.day, 17)
    

        self.current_time = self.startOfDay

        self.package_controller = package_controller
                
        self.num_of_trucks = num_of_trucks
        self.num_of_drivers = number_of_drivers
        
        self.trucks: List[Truck] = []
        drivers = self.num_of_drivers
        for index in range(num_of_trucks):
            has_driver = False
            #used positional agruments for better readability on the truck id argument
            if drivers > 0:
                has_driver = True
                drivers -= 1
            truck = Truck(id=index+1,hub=self.hub_location, has_driver=has_driver, city_map=self.city_map)
            self.trucks.append(truck)
    
    def load_trucks(self):
        trucks = [truck for truck in self.trucks if truck.has_driver == True]
        for truck in trucks:
            while not truck.is_full() and self.package_controller.packages_left_to_load_on_truck():
                truck = self.package_controller.load_packages_on_truck(truck, self.current_time)
                self.current_time = self.current_time + timedelta(minutes=1)
                print(self.current_time)
            print(truck.packages)
                
    def load_truck(self, truck: Truck, package: Package) -> List:
        truck.load_package(package, self.current_time)
        self.package_controller.load_packages_on_truck(package, self.current_time)
    
    def start_day(self):
        deliver = self.package_controller.packages_left_to_deliver()
        while deliver:
            results = []
            threads_list = []
            self.load_trucks()
            for truck in self.trucks:
                if truck.has_driver:
                    results.append(truck.deliver_packages(self.current_time))
                    """ t = ReturningThread(target=truck.deliver_packages, args=(self.current_time,))
                    t.start()
                    threads_list.append(t) """

            """ #Join all the threads
            for t in threads_list:
                result = t.join()
                results.append(result) """
            
            
            if len(results) > 0:
                times = sorted(results, reverse=True)
                self.current_time = self.current_time + times[0][0]
                for result in results:
                    self.total_distance += result[1]
            else:
                self.current_time = self.current_time + timedelta(minutes=1)
            
            for truck in self.trucks:
                self.package_controller.deliver_package(truck)
            
            deliver = self.package_controller.packages_left_to_deliver()
        print("----------------------------------------")
        print(self.package_controller.packages)
        print("Total Distance: " + str(self.total_distance))
            
    def _load_distances(self):
        csvData = CSVReader()
        distances = []
        for row in csvData.read_distances():
            distances.append(row)
        return distances
    
def main():
    hub = Hub()
    hub.start_day()
    print(hub.trucks)
    #print(hub.graph)

if __name__ == "__main__":
    main()