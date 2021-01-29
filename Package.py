from Location import Location
from typing import List
import re
from datetime import datetime, timedelta
from Identifiable import Identifiable
from enum import Enum, auto

class PackageStatus(Enum):
    STAGED_AT_HUB = auto()
    AT_HUB = auto()
    ON_TRUCK = auto()
    DELIVERED = auto()

class Package(Identifiable):
    
    idCol = 0
    addressCol = 1
    DeadlineCol = 5
    mass = 6
    specialNotesCol = 7

    def __init__(self, id: int, location: Location, deadline: str, specialNotes: str, mass: int) -> None:
        super().__init__(id)
        self.now = datetime.now()
        self.destination = location
        
        #package status
        self.status = PackageStatus.AT_HUB
        
        #package data
        self.time_at_hub = None
        self.time_on_truck = None
        self.delivery_time = None
        self.package_destination_updated_at = None
        self.delivered_with_truck = -1

        self.time_at_hub = datetime(self.now.year, self.now.month, self.now.day, 8,0)
        
        #truck constraints
        self.required_truck = -1
        
        #bool values to search by
        self.is_delayed_on_plane = False
        self.has_other_packages = False
        self.has_wrong_address = False
        self.has_deadline = False

        #time constraints
        self.delayed_on_plane = None
        self.deliver_with = []
        self.will_be_address_updated_at = None
        self.deadline = None
        
        #package update constraints
        self.has_wrong_address = False

        delayedOnFlight = "Delayed on flight"
        requiredTruck = "Can only be on truck"
        mustBeDeliveredWith = "Must be delivered with"
        wrongAddressDelivered = "Wrong address listed"
        eod= "EOD"
        
        if requiredTruck in specialNotes:
            for char in specialNotes.split():
                if char.isdigit():
                    self.required_truck = int(char)
        
        if delayedOnFlight in specialNotes:
            timepart = specialNotes[-7:]
            timeparts = timepart.split(":")
            timeHour = int(timeparts[0])
            timeMinutes = int(re.findall('[0-9]+', timeparts[1])[0])
            
            self.delayed_on_plane = datetime(self.now.year, self.now.month, self.now.day, timeHour, timeMinutes)
            self.time_at_hub = self.delayed_on_plane
            self.is_delayed_on_plane = True

        if mustBeDeliveredWith in specialNotes:
            intString = re.findall('[0-9]+', specialNotes)
            self.must_be_delivered_wtih: List[int] = []
            for num in intString:
                self.deliver_with.append(int(num))
            self.has_other_packages = True

        if wrongAddressDelivered in specialNotes:
            self.will_be_address_updated_at = datetime(self.now.year, self.now.month, self.now.day, 10, 20)
            self.has_wrong_address = True
            """410 S State St., Salt Lake City, UT 84111""" #corrected address
        
        if eod not in deadline:
            timeparts = deadline.split(":")
            timeHour = int(timeparts[0])
            timeMinutes = int(re.findall('[0-9]+', timeparts[1])[0])
            
            self.deadline = datetime(self.now.year, self.now.month, self.now.day, timeHour, timeMinutes)
            self.has_deadline = True

    def on_truck(self):
        self.status = PackageStatus.ON_TRUCK
    
    def delivered(self):
        self.status = PackageStatus.DELIVERED


    def __repr__(self) -> str:
        string = "\n\tPackage Id: " + str(self.id)
        string += "\n\t\t Destination: " + str(self.destination)
        string += "\n\t\t Status: " + str(self.status)
        string += "\n\t\t Truck: " + str(self.required_truck)
        string += "\n\t\t Time on truck: " + str(self.time_on_truck)
        string += "\n\t\t Deliverd with truck: " + str(self.delivered_with_truck)
        string += "\n\t\t Delayed Till: " + str(self.delayed_on_plane)
        string += "\n\t\t Wrong Address update at: " + str(self.package_destination_updated_at)
        string += "\n\t\t Deadline: " + str(self.deadline)
        string += "\n\t\t Deliver With: " + str(self.deliver_with)
        string += "\n\t\t Delivery Time: " + str(self.delivery_time)
        return string
    
    def __eq__(self, o) -> bool:
        if isinstance(o, Package):
            return super().__eq__(o)
        return NotImplemented
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def __str__(self) -> str:
        return self.__repr__()