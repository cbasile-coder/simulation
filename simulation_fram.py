import simpy
import matplotlib.pyplot as plt

class Function:
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.output_ready = env.event()

    def run(self, duration, dependent_functions):
        yield self.env.timeout(duration)
        print(f"{self.name} completed at time: {self.env.now}s")
        
        # Attivare le funzioni dipendenti
        for func in dependent_functions:
            func.output_ready.succeed()
            func.output_ready = self.env.event()

def fram_simulation():
    env = simpy.Environment()

    # Definition of FRAM model functions
    function_A = Function(env, "Funzione A")
    function_B = Function(env, "Funzione B")
    function_C = Function(env, "Funzione C")

    # Definition of interdependencies
    env.process(function_A.run(2, [function_B, function_C]))
    env.process(function_B.run(3, [function_C]))
    env.process(function_C.run(1, []))

    # Run simulation
    env.run()

if __name__ == "__main__":
    fram_simulation()