import csv
from typing import List

class CSVReader():
    locationFile: str
    distanceFile: str
    packageFile: str

    def __init__(self) -> None:
        self.locationFile = "Locations.csv"
        self.distanceFile = "Distances.csv"
        self.packageFile = "Packages.csv"
        
    def read_locations(self) -> List:
        csvData = []
        with open(self.locationFile) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                csvData.append(row)
            return csvData
        
    def read_distances(self) -> List:
        csvData = []
        with open(self.distanceFile) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                csvData.append(row)
            return csvData
    
    def read_packages(self) -> List:
        csvData = []
        with open(self.packageFile) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                csvData.append(row)
            return csvData