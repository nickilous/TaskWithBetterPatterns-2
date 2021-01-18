from Hub2 import Hub2
from LocationController import LocationController
from PackageController import PackageController
from Graph import Graph
from CSVReader import CSVReader
from Hub import Hub

def main():
    csv_data = CSVReader()
   
    
    location_controller = LocationController(csv_data.read_locations())
    package_controller = PackageController(csv_data.read_packages(), location_controller.locations)

    city_map = Graph.from_raw_data(location_controller.locations, csv_data.read_distances())

    hub = Hub2(package_controller, location_controller, city_map)
    hub.start_day()
    print(hub.package_controller.packages)
    print(hub.total_distance)
    
    #print(hub.truck)
    #print(hub.route)
    #print(hub.route)
    #print(len(hub.route))
    #print(hub.load_truck())
    #print(hub.total_distance)
    

if __name__ == "__main__":
    main()