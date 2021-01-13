from LocationController import LocationController
from Graph import Graph
from CSVReader import CSVReader
from typing import List
from Location import Location
from datetime import datetime, timedelta
from Package import Package, PackageStatus
from HashTable import HashTable

class PackageController:
    def __init__(self, packages, locations) -> None:
        super().__init__()
        self.packages = HashTable()
        
        self.csvData = CSVReader()

        for row in packages:
            for location in locations:
                if location.street == row[Package.addressCol]:
                    package = Package(int(row[Package.idCol]), location, row[Package.DeadlineCol], row[Package.specialNotesCol], row[Package.mass])
                    self.packages.insert(package)
    
    #gets package for a specific truck requirement
    def get_packages_for_specific_truck(self, truckId: int) -> List[Package]:
        truck_packages: List[Package] = []
        for package in self.packages:
            if package.truck == truckId:
                truck_packages.append(package)
        return truck_packages
    
    def get_packages_with_truck(self):
        truck_packages: List[Package] = []
        for package in self.packages:
            if package.truck is None:
                truck_packages.append(package)
        return truck_packages

    def get_standard_packages(self):
        packages: List[Package] = []
        for package in self.packages:
            if package.deliverWith is None and package.truck is None and package.delayedTill is None and package.deadline is None:
                packages.append(package)
        return packages
    
    #gets all the package with a deadline if deadline not specified
    #gets packages with specific deadline if deadline is specified
    def get_packages_with_deadline(self, deadline: datetime = None):
        packages_with_deadline: List[Package] = []
        if datetime is None:
            for package in self.packages:
                if package is not None:
                    if package.deadline is not None:
                        packages_with_deadline.append(package)
        else:
            for package in self.packages:
                if package is not None:
                    if package.deadline == datetime:
                        packages_with_deadline.append(package)
        return packages_with_deadline
    
    #gets all the packages that are linked together
    #for internal use
    def get_linked_packages(self):
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
    
    #gets a list of all the packages that have deadlines and that are linked
    #these have the highest priority because of space on the trucks
    #we want to make sure that all the packages with deadlines
    #and there linked packages get loaded on the first truck
    def get_linked_packages_with_deadlines(self):
        packages = []
        all_linked_packages = self.get_linked_packages()
        for package, linked_packages in all_linked_packages.items():
            if package.deadline is not None:
                packages.append(package)
            for linked_package in linked_packages:
                if linked_package not in packages:
                    if package in packages:
                        packages.append(linked_package)
                    if linked_package.deadline is not None:
                        packages.append(package)
                        packages.append(linked_package)
        return packages
    
    #gets a list of all linked packages without deadlines
    #this is this has medium to low priority and will get loaded
    #after all the linked_with_deadline and deadline packages get loaded
    def get_linked_packages_without_deadlines(self):
        packages = []
        all_linked_packages = self.get_packages_that_deliver_together()
        for package, linked_packages in all_linked_packages.items():
            if package.deadline is None:
                packages.append(package)
            for linked_package in linked_packages:
                if linked_package not in packages:
                    if package in packages:
                        packages.append(linked_package)
                    if linked_package.deadline is not None:
                        packages.append(package)
                        packages.append(linked_package)

    def get_linked_packages_list(self) -> List:
        packages = []
        linked_packages = self.get_packages_that_deliver_together()
        for package, linked_packages in linked_packages.items():
            packages.append(package)
            for linked_package in linked_packages:
                if linked_package not in packages:
                    if package in packages:
                        packages.append(linked_package)
        return packages

    def load_package_on_truck(self, package: Package, time: timedelta):
        package.status = PackageStatus.ON_TRUCK
        package.timeOnTruck = time
        self.packages.update(package)
    
    def deliver_package(self, package: Package, time: timedelta):
        package.status = PackageStatus.DELIVERED
        package.deliveryTime = time
        self.packages.update(package)
    
    def update_package_status(self, packageId: int, status: PackageStatus, time: timedelta) -> None:
        if status == PackageStatus.ON_TRUCK:
            package = self.packages.search(packageId)
            package.status = status
            package.timeOnTruck = time
            self.packages.update(package)
        if status == PackageStatus.DELIVERED:
            package = self.packages.search(packageId)
            package.status = status
            package.deliverTime = time
            self.packages.update(package)

def main():
    csv_data = CSVReader()
    location_controller = LocationController(csv_data.read_locations())
    package_controller = PackageController(csv_data.read_packages(), location_controller.locations)
    
    print(package_controller.get_linked_packages_with_deadlines())

if __name__ == "__main__":
    main()