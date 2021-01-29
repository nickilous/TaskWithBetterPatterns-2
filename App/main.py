from Package import Package, PackageStatus
from Hub import Hub
from datetime import datetime
from LocationController import LocationController
from PackageController import PackageController
from Graph import Graph
from CSVReader import CSVReader
from Hub import Hub

"""C950 Task
Nicholas Hartman
01/22/21
Package Delivery with hash table, graph, and greedy algorithms"""

def main():

    now = datetime.now()

    csv_data = CSVReader()
   
    
    location_controller = LocationController(csv_data.read_locations())
    package_controller = PackageController(csv_data.read_packages(), location_controller.locations)

    city_map = Graph.from_raw_data(location_controller.locations, csv_data.read_distances())
    hub = Hub(package_controller, location_controller, city_map)
    hub.start_day()
    
    print("Total distance traveled by trucks: " + str(hub.total_distance))
    run = True
    while run:
        check_one_package = input("If you would like to check the status of one package please enter (y/n) - if no checks all packages: ")
        if check_one_package == "y":
            check_one_package = True
        else:
            check_one_package = False
        
        if check_one_package:
            package_id = input("Please input Package ID (1 - 40): ")
        
            try:
                package_id = int(package_id)
                if package_id > 40:
                    print("Package ID must be less than 40")
                    continue
                elif package_id < 1:
                    print("Package ID must be greater than or equal to 1")
                    continue
            except ValueError:
                print("Package ID must be a number")
        
            time_to_check = input("Please input time in HH:MM format: ")
            hour = time_to_check.split(':')[0]
            try:
                hour = int(hour)
                if hour > 24:
                    print("HH must be less than 24")
                    continue
                elif hour < 0:
                    print("HH must be greater than or equal to 00")
                    continue
            except ValueError:
                print("HH must be a number")
                continue
        
            minute = time_to_check.split(':')[1]
            try:
                minute = int(minute)
                if minute > 60:
                    print("MM must be less than 60")
                    continue
                elif minute < 0:
                    print("MM must be greater than or equal to 00")
                    continue
            except ValueError:
                print("MM must be a number")
            time_to_check = datetime(now.year, now.month, now.day, hour, minute)
            
            package = package_controller.get_package_from_id(package_id)
            if package.delivery_time <= time_to_check:
                package.status = PackageStatus.DELIVERED
                print("Package {id} is {package_status} at {time_on_truck}".format(id=package.id, package_status=package.status, time_on_truck=package.delivery_time))
            elif package.time_on_truck <= time_to_check:
                package.status = PackageStatus.ON_TRUCK
                print("Package {id} is {package_status} at {time_on_truck}".format(id=package.id, package_status=package.status, time_on_truck=package.time_on_truck))
            
            check_one_package = input("If you would like to check the status of another package please enter (y/n): ")
            if check_one_package == "y":
                check_one_package = True
                continue
            else:
                check_one_package = False
                continue
    
        time_to_check = input("Please input time in HH:MM format: ")
        hour = time_to_check.split(':')[0]
        try:
            hour = int(hour)
            if hour > 24:
                print("HH must be less than 24")
                continue
            elif hour < 0:
                print("HH must be greater than or equal to 00")
                continue
        except ValueError:
            print("HH must be a number")
            continue
        
        minute = time_to_check.split(':')[1]
        try:
            minute = int(minute)
            if minute > 60:
                print("MM must be less than 60")
                continue
            elif minute < 0:
                print("MM must be greater than or equal to 00")
                continue
        except ValueError:
            print("MM must be a number")
        time_to_check = datetime(now.year, now.month, now.day, hour, minute)
        packages = package_controller.get_list_of_packages()
        for package in packages:
            if package.delivery_time <= time_to_check:
                package.status = PackageStatus.DELIVERED
                print("Package {id} is {package_status} at {time_on_truck}".format(id=package.id, package_status=package.status, time_on_truck=package.delivery_time))
            if package.time_on_truck <= time_to_check and time_to_check < package.delivery_time:
                package.status = PackageStatus.ON_TRUCK
                print("Package {id} is {package_status} at {time_on_truck}".format(id=package.id, package_status=package.status, time_on_truck=package.time_on_truck))
            if time_to_check < package.time_on_truck:
                package.status = PackageStatus.AT_HUB
                print("Package {id} is {package_status} at {time_on_truck}".format(id=package.id, package_status=package.status, time_on_truck=package.time_at_hub))
        
        run = input("If you would like to run this app again enter (y/n): ")
        if run == "y":
            run = True
            continue
        else:
            run = False
            continue
if __name__ == "__main__":
    main()