import heapq
import random
import time
import argparse
import matplotlib.pyplot as plt
from enum import Enum
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.circuit import QuantumCircuit

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

def GenExponentialTime(rate, simTypes):
    if simTypes == SimulationType.CLASSIC:
        return random.expovariate(rate)
    elif simTypes == SimulationType.QUANTUM:
        backend = Aer.get_backend('qasm_simulator')
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        
        new_circuit = transpile(qc, backend)
        job = backend.run(new_circuit)

        result = job.result()
        counts = result.get_counts(qc)
        measurement = int(list(counts.keys())[0])
        
        if measurement == 0:
            return random.expovariate(rate)
        else:
            return random.expovariate(rate) * 2

def StartSimulation(arrivalRate, serviceRate, eventCounter, simType=SimulationType.CLASSIC):
    startTime = time.time()
    events = []
    heapq.heappush(events, Event(GenExponentialTime(arrivalRate, simType), EventType.ARRIVAL))

    currentTime = 0
    simulatedEvents = 0
    serviceTimes = []
    
    while simulatedEvents < eventCounter:
        currentEvent = heapq.heappop(events)
        currentTime = currentEvent.time
        
        if currentEvent.type == EventType.ARRIVAL:
            heapq.heappush(events, Event(currentTime + GenExponentialTime(serviceRate, simType), EventType.SERVICE))
            heapq.heappush(events, Event(currentTime + GenExponentialTime(arrivalRate, simType), EventType.ARRIVAL))
        elif currentEvent.type == EventType.SERVICE:
            simulatedEvents += 1
            serviceTimes.append(currentTime)
            print(f"Service event executed: {currentTime:.2f}")

    print(f"Simulation completed with {simulatedEvents} service events")
    endTime = time.time()
    return (endTime - startTime), serviceTimes

def main():
    # Input arguments
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--type', type=str, default='classic')
    parser.add_argument('--arrivalRate', type=float, default=1.0)
    parser.add_argument('--serviceRate', type=float, default=0.5)
    parser.add_argument('--eventCounter', type=int, default=10)
    args = parser.parse_args()

    arrivalRate = args.arrivalRate      # Event arrival rate
    serviceRate = args.serviceRate      # Event service rate
    eventCounter = args.eventCounter    # Number of events to simulate

    simType = SimulationType.CLASSIC if args.type == 'classic' else SimulationType.QUANTUM
    
    # Simulation start
    timeToExecution, listOfServices = StartSimulation(arrivalRate, serviceRate, eventCounter, simType)
    print(f"Time to execution: {timeToExecution:.5f}s")

    plt.plot(listOfServices, range(len(listOfServices)), marker='o')
    plt.xlabel('Service time (s)')
    plt.ylabel('Number of service events')
    plt.title('Simulation results')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()