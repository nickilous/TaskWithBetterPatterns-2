from Package import PackageStatus
from datetime import datetime, time, timedelta
from PackageController import PackageController
from LocationController import LocationController
from Location import Location
from Graph import Graph
from Truck import Truck
from typing import List
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
            truck_is_full = truck.is_full()
            truck_has_deadline = truck.deadline in self.package_controller.deadlines
            truck_is_delayed = truck.delayed_till in self.package_controller.delay_times
            no_packages_left_to_load = self.package_controller.packages_left_to_load_on_truck()
            
            while True:
                truck = self.package_controller.load_packages_on_truck(truck)

                truck_is_full = truck.is_full()
                truck_has_deadline = truck.deadline in self.package_controller.deadlines
                no_packages_left_to_load = self.package_controller.packages_left_to_load_on_truck()
                truck_is_delayed = truck.delayed_till in self.package_controller.delay_times

                #Reason to stop trying to laod a truck
                if truck_is_full:
                    break
                if truck_has_deadline:
                    break
                if truck_is_delayed:
                    break
                if not no_packages_left_to_load:
                    break

    
    def start_day(self):
        packages_left_to_deliver = self.package_controller.packages_left_to_deliver()
        trucks_with_drivers = [truck for truck in self.trucks if truck.has_driver]
        
        while self.current_time < self.endOfDay or packages_left_to_deliver:
            self.load_trucks()
            
            delivery_results = []
            
            trucks_with_drivers = [truck for truck in self.trucks if truck.has_driver == True]
            trucks_with_packages = [truck for truck in trucks_with_drivers if len(truck.packages) > 0]
            
            for truck in trucks_with_packages:
                for package in truck.packages:
                    if package.has_wrong_address:
                        #19,Third District Juvenile Court,410 S State St
                        location = Location(19, "Third District Juvenile Court", "410 S State St")
                        self.package_controller.update_package_location(package, location, truck.current_time)
            
            packages = [package for package in self.package_controller.packages if package is not None\
                and package.status == PackageStatus.AT_HUB]

            for truck in trucks_with_packages:
                delivery_results.append(truck.deliver_packages())
                self.package_controller.deliver_package(truck)
                truck.reset()
            
            if len(delivery_results) == 0:
                self.current_time = self.current_time + timedelta(minutes=1)
                for truck in self.trucks:
                    truck.current_time = self.current_time
            else:
                truck_return_times = []
                truck_total_milage = 0
                for result in delivery_results:
                    truck_return_time = result[0]
                    truck_return_times.append(truck_return_time)
                    
                    truck_total_milage += result[1]
                self.total_distance += truck_total_milage
                if len(truck_return_times) > 1:
                    truck_return_times = sorted(truck_return_times)
                
                time_between_trucks = truck_return_times[0] - self.current_time
                self.current_time = self.current_time + time_between_trucks
            
            
            packages_left_to_deliver = self.package_controller.packages_left_to_deliver()
            
