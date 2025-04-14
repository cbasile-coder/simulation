import simpy
import random
#import matplotlib.pyplot as plt
import framalytics

class Function:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.output_ready = env.event()

    def run(self, duration, dependent_functions, probDelay=0):
        if random.random() < probDelay:  # Delay probability
            yield self.env.timeout(random.uniform(1, 5))
            print(f"{self.name} has been delayed!")
        yield self.env.timeout(duration)
        print(f"{self.name} completed at time: {self.env.now}s")
        
        # Activate dependent functions
        for func in dependent_functions:
            func.output_ready.succeed()
            func.output_ready = self.env.event()

def id_to_function(funcs, idList):
    functions = []
    for id in idList:
        if id in funcs:
            functions += funcs[id].keys()
    return functions

def fram_simulation():
    env = simpy.Environment()
    fram = framalytics.FRAM('FRAM_tesi.xfmv')
    functions = {}

    # Definition of FRAM model functions
    for id, function_name in fram.get_functions().items():
        dependencies = list(fram.get_function_inputs(function_name).keys())
        dependencies += list(fram.get_function_preconditions(function_name).keys())
        dependencies += list(fram.get_function_times(function_name).keys())
        dependencies += list(fram.get_function_controls(function_name).keys())
        dependencies += list(fram.get_function_resources(function_name).keys())
        functions[id] = {Function(env, function_name): dependencies}

    # Definition of interdependencies
    for id, values in functions.items():
        for func, value in values.items():
            env.process(func.run(random.randint(1, 5), id_to_function(functions, value),random.uniform(0.01, 0.99)))

    # Run simulation
    env.run()

if __name__ == "__main__":
    fram_simulation()