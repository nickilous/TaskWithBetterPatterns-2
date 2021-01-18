from Truck import Truck
from LocationController import LocationController
from Graph import Graph
from CSVReader import CSVReader
from typing import List
import threading
from Location import Location
from datetime import date, datetime, timedelta
from Package import Package, PackageStatus
from HashTable import HashTable

class PackageController:
    def __init__(self, packages, locations) -> None:
        super().__init__()
        self.packages = HashTable()
        
        self.csvData = CSVReader()

        now = datetime.now()
        self.end_of_day = datetime(now.year, now.month, now.day, 17)

        for row in packages:
            for location in locations:
                if location.street == row[Package.addressCol]:
                    package = Package(int(row[Package.idCol]), location, row[Package.DeadlineCol], row[Package.specialNotesCol], row[Package.mass])
                    self.packages.insert(package)
        
        self.linked_package_graph = Graph(len(self.packages) + 1, len(self.packages) + 1, self.packages)
        self.__link_packages()
        
        self.packages_with_wrong_address = [package for package in self.packages\
            if package is not None\
            and package.has_wrong_address == True]
        
        self.wrong_address_update_times = [package.will_be_address_updated_at for package in self.packages_with_wrong_address]
        self.wrong_address_update_times = self.__remove_duplicates(self.wrong_address_update_times)
        
        self.deadlines = self.__get_deadlines()
        self.deadlines = self.__remove_duplicates(self.deadlines)
        self.deadlines = sorted(self.deadlines)

        self.delay_times = self.__get_delay_times()
        self.delay_times = self.__remove_duplicates(self.delay_times)
        self.delay_times = sorted(self.delay_times)

    
    def __link_packages(self):
        for package in self.__get_linked_packages_list():
            if package.must_be_delivered_with is not None:
                for package_id in package.deliverWith:
                    package_to_link = self.packages.search(package_id)
                    self.linked_package_graph.connect(package, package_to_link)

    def __get_deadlines(self):
        deadlines = []
        for package in self.packages:
            if package is not None:
                if package.deadline is not None:
                    deadlines.append(package.deadline)
        return deadlines
    
    def __remove_duplicates(self, collection: List) -> List:
        results = []
        for item in collection:
            if item not in results:
                results.append(item)
        return results
    
    def __get_delay_times(self):
        delay_times = []
        for package in self.packages:
            if package is not None:
                if package.delayed_on_plane is not None:
                    delay_times.append(package.delayed_on_plane)
        return delay_times
    
    def get_list_of_packages(self):
        all_packages = []
        for package in self.packages:
            if package is not None:
                all_packages.append(package)
        return all_packages

    #gets all the packages that are linked together
    #for internal use
    def __get_linked_packages(self):
        package_dict = {}
        for package in self.packages:
            if package is not None:
                if package.deliveredWith is not None:
                    packages_to_link = []   
                    for linked_package in package.deliveredWith:
                        package_to_connect = self.packages.search(linked_package)
                        packages_to_link.append(package_to_connect)
                        package_dict[package_to_connect] = []
                    package_dict[package] = packages_to_link
        return package_dict
    
    def __link_packages(self):
        for package in self.packages:
            if package is not None:
                if package.deliver_with is not None:
                    for linked_package in package.deliver_with:
                        package_to_connect = self.packages.search(linked_package)
                        self.linked_package_graph.connect(package, package_to_connect)

    def __get_linked_packages_list(self) -> List:
        packages = []
        linked_packages = self.__get_linked_packages()
        for package, linked_packages in linked_packages.items():
            packages.append(package)
            for linked_package in linked_packages:
                if linked_package not in packages:
                    if package in packages:
                        packages.append(linked_package)
        return packages
    
   
    def load_truck_with_packages(self, truck: Truck, packages: List[Package], time: datetime) -> Truck:
        if truck.can_load(len(packages)):
                for package in packages:
                    self.update_package_status(package, PackageStatus.ON_TRUCK, time)
                    truck.load_package(package)
        return truck
    
    def load_truck_with_package(self, truck: Truck, package: Package, time: datetime) -> Truck:
        if truck.can_load(1):
            truck.load_package(package)
            self.update_package_status(package, PackageStatus.ON_TRUCK, time)
    
    def __get_all_connected_packages(self, package: Package, packages: List[Package]) -> List:
        if package not in packages:
            packages.append(package)
        for package_id in self.linked_package_graph.connections_to(package):
            package_to_add = self.packages.search(package_id)
            if package_to_add not in packages:
                packages.append(package_to_add)
                self.__get_all_connected_packages(package_to_add, packages)
    
    
    def load_packages_on_truck(self, truck: Truck) -> Truck:
        # gets packages with deadlines and no delay times that are still at the hub
        packages = [package for package in self.packages\
             if package is not None\
                and package.status == PackageStatus.AT_HUB\
                and package.has_deadline\
                and not package.is_delayed_on_plane\
                and not package.has_wrong_address]
        
        # loads the previously grab packages on the truck that have requirments that they are delivered
        # with other packages
        packages_to_deliver = []
        for package in packages:
            if self.linked_package_graph.node_has_conn(package):
                if package not in packages_to_deliver:
                    self.__get_all_connected_packages(package, packages_to_deliver)
                    self.load_truck_with_packages(truck, packages_to_deliver, truck.current_time)

        
        # gets packages with deadlines and no delay times that are still at the hub
        packages = [package for package in self.packages\
             if package is not None\
                and package.status == PackageStatus.AT_HUB\
                and package.has_deadline\
                and not package.is_delayed_on_plane\
                and not package.has_wrong_address]
        # loads the previously grab packages
        self.load_truck_with_packages(truck, packages, truck.current_time)
        
        #----------------- Packages with deadlines and now delays and no wrong address or delay times ABOVE -----
        
        # get packages with a delay time less than the truck deadline and that have a deadline
        packages = [package for package in self.packages if package is not None\
            and package.status == PackageStatus.AT_HUB\
            and package.is_delayed_on_plane\
            and package.has_deadline\
            and truck.current_time >= package.delayed_on_plane\
            and not truck.deadline < package.delayed_on_plane]
        self.load_truck_with_packages(truck, packages, truck.current_time)
        
        package = [package for package in self.packages if package is not None\
            and package.status == PackageStatus.AT_HUB\
            and package.has_deadline\
            and package.is_delayed_on_plane\
            and truck.current_time > package.delayed_on_plane]
        
        self.load_truck_with_packages(truck, packages, truck.current_time)
        package = [package for package in self.packages if package is not None\
            and package.status == PackageStatus.AT_HUB\
            and package.has_deadline\
            and package.is_delayed_on_plane
            and truck.current_time > package.delayed_on_plane\
            and truck.deadline < package.deadline]
        self.load_truck_with_packages(truck, packages, truck.current_time)

        if truck.deadline == self.end_of_day:
            packages = [package for package in self.packages if package is not None\
                and package.status == PackageStatus.AT_HUB\
                and package.has_wrong_address
                and truck.current_time > package.will_be_address_updated_at]
            self.load_truck_with_packages(truck, packages, truck.current_time)
        
        if truck.deadline == self.end_of_day:
            packages = [package for package in self.packages if package is not None\
                and package.status == PackageStatus.AT_HUB\
                and package.required_truck == truck.id]
            self.load_truck_with_packages(truck, packages, truck.current_time)
        
        if truck.deadline == self.end_of_day:
            packages = [package for package in self.packages\
                if package is not None\
                    and package.status == PackageStatus.AT_HUB\
                    and package.is_delayed_on_plane\
                    and not package.has_deadline\
                    and not package.has_wrong_address\
                    and truck.current_time > package.delayed_on_plane\
                    and truck.deadline == self.end_of_day]
            self.load_truck_with_packages(truck, packages, truck.current_time)
        
        # gets all the packages that have no special requirements and are still at the hub
        if truck.deadline == self.end_of_day:
            packages = [package for package in self.packages\
                if package is not None\
                    and package.status == PackageStatus.AT_HUB\
                    and not package.is_delayed_on_plane\
                    and not package.has_deadline\
                    and not package.has_wrong_address\
                    and truck.deadline == self.end_of_day]
            for package in packages:
                self.load_truck_with_package(truck, package, truck.current_time)
        return truck
        
    def packages_left_to_load_on_truck(self) -> bool:
        result = False
        packages = [package for package in self.packages if package is not None and package.status == PackageStatus.AT_HUB]
        for package in packages:
            result = True
        return result
    
    def packages_left_to_deliver(self) -> bool:
        result = False
        packages = [package for package in self.packages if package is not None and package.status != PackageStatus.DELIVERED]
        for package in packages:
                result = True
        return result
    
    def deliver_package(self, truck: Truck):
        for package in truck.packages:
            if package is not None:
                self.update_package_status(package, PackageStatus.DELIVERED, package.deliveryTime)

    def update_package_location(self, package: Package, destination: Location, time: datetime):
        package.destination = destination
        package.package_destination_updated_at = time
        
        with threading.Lock():
            self.packages.update(package)

    def update_package_status(self, package: Package, status: PackageStatus, time: datetime) -> None:
        if status == PackageStatus.ON_TRUCK:
            package = self.packages.search(package)
            package.status = status
            package.time_on_truck = time
            with threading.Lock():
                self.packages.update(package)
        if status == PackageStatus.DELIVERED:
            package = self.packages.search(package)
            package.status = status
            package.deliver_time = time
            with threading.Lock():
                self.packages.update(package)

def main():
    csv_data = CSVReader()
    location_controller = LocationController(csv_data.read_locations())
    package_controller = PackageController(csv_data.read_packages(), location_controller.locations)
    
    print(package_controller.deadlines)
    print(package_controller.delay_times)
    print(package_controller.linked_package_graph)

if __name__ == "__main__":
    main()