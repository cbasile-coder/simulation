import heapq
import random
import time
from enum import Enum

class SimulationType(Enum):
    CLASSIC = 0
    QUANTUM = 1

class EventType(Enum):
    ARRIVAL = 0
    SERVICE = 1

class Event:
    def __init__(self, time, type):
        self.time = time
        self.type = type
    
    def __lt__(self, other):
        return self.time < other.time

def GenExponentialTime(rate):
    return random.expovariate(rate)

def StartSimulation(arrivalRate, serviceRate, eventCounter, simulationType=SimulationType.CLASSIC):
    startTime = time.time()
    events = []
    heapq.heappush(events, Event(GenExponentialTime(arrivalRate), EventType.ARRIVAL))
    
    currentTime = 0
    simulatedEvents = 0
    
    while simulatedEvents < eventCounter:
        currentEvent = heapq.heappop(events)
        currentTime = currentEvent.time
        
        if currentEvent.type == EventType.ARRIVAL:
            heapq.heappush(events, Event(currentTime + GenExponentialTime(serviceRate), EventType.SERVICE))
            heapq.heappush(events, Event(currentTime + GenExponentialTime(arrivalRate), EventType.ARRIVAL))
        elif currentEvent.type == EventType.SERVICE:
            simulatedEvents += 1
            print(f"Service event executed: {currentTime:.2f}")

    print(f"Simulation completed with {simulatedEvents} service events")
    endTime = time.time()
    return endTime - startTime

def main():
    # Input arguments (they will be replaced by an external input arguments mechanism)
    arrivalRate = 1.0    # Event arrival rate
    serviceRate = 0.5    # Event service rate
    eventCounter = 10    # Number of events to simulate
    
    # Simulation start
    timeToExecution = StartSimulation(arrivalRate, serviceRate, eventCounter)
    print(f"Time to execution: {timeToExecution}s")


if __name__ == "__main__":
    main()