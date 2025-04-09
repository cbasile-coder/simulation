import simpy
import random
#import matplotlib.pyplot as plt

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

def fram_simulation():
    env = simpy.Environment()

    # Definition of FRAM model functions
    function_A = Function(env, "Function A")
    function_B = Function(env, "Function B")
    function_C = Function(env, "Function C")

    # Definition of interdependencies
    env.process(function_A.run(2, [function_B, function_C], 0.45))
    env.process(function_B.run(3, [function_C], 0.3))
    env.process(function_C.run(1, [], 0.2))

    # Run simulation
    env.run()

if __name__ == "__main__":
    fram_simulation()