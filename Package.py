from Location import Location
from typing import List
import re
from datetime import datetime, timedelta
from Identifiable import Identifiable
from enum import Enum, auto

class PackageStatus(Enum):
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
        self.status = PackageStatus.AT_HUB
        self.timeOnTruck = timedelta
        self.deliveryTime = timedelta
        self.truck = None
        self.delayedTill = None
        self.deliveredWith = None
        self.deadline = None
        
        delayedOnFlight = "Delayed on flight"
        requiredTruck = "Can only be on truck"
        mustBeDeliveredWith = "Must be delivered with"
        eod= "EOD"
        
        if requiredTruck in specialNotes:
            for char in specialNotes.split():
                if char.isdigit():
                    self.truck = int(char)
        if delayedOnFlight in specialNotes:
            timepart = specialNotes[-7:]
            timeparts = timepart.split(":")
            timeHour = int(timeparts[0])
            timeMinutes = int(re.findall('[0-9]+', timeparts[1])[0])
            
            self.delayedTill = datetime(self.now.year, self.now.month, self.now.day, timeHour, timeMinutes)

        if mustBeDeliveredWith in specialNotes:
            intString = re.findall('[0-9]+', specialNotes)
            self.deliveredWith: List[int] = []
            for num in intString:
                self.deliveredWith.append(int(num))
            

        if eod not in deadline:
            timeparts = deadline.split(":")
            timeHour = int(timeparts[0])
            timeMinutes = int(re.findall('[0-9]+', timeparts[1])[0])
            
            self.deadline = datetime(self.now.year, self.now.month, self.now.day, timeHour, timeMinutes)
    
    def on_truck(self):
        self.status = PackageStatus.ON_TRUCK
    
    def delivered(self):
        self.status = PackageStatus.DELIVERED
    
    def __repr__(self) -> str:
        string = "\n\tPackage Id: " + str(self.id)
        string += "\n\t\t Destination: " + str(self.destination)
        string += "\n\t\t Delivered: " + str(self.status)
        string += "\n\t\t Truck: " + str(self.truck)
        string += "\n\t\t Delayed Till: " + str(self.delayedTill)
        string += "\n\t\t Deadline: " + str(self.deadline)
        string += "\n\t\t Deliver With: " + str(self.deliveredWith)
        string += "\n\t\t Delivery Time: " + str(self.deliveryTime)
        return string
    
    def __eq__(self, o) -> bool:
        if isinstance(o, Package):
            return super().__eq__(o)
        return NotImplemented
    
    def __hash__(self) -> int:
        return super().__hash__()
    
    def __str__(self) -> str:
        return self.__repr__()