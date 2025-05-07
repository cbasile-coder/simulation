import simpy
import random
import networkx as nx
import matplotlib.pyplot as plt
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

def create_dependency_graph(fram):
    G = nx.DiGraph()

    function_id_to_name = fram.get_functions()

    for func_name in function_id_to_name.values():
        G.add_node(func_name)

    # Interdependencies
    for func_id, func_name in function_id_to_name.items():
        dependencies = list(fram.get_function_inputs(func_id).keys()) + \
                       list(fram.get_function_preconditions(func_id).keys()) + \
                       list(fram.get_function_times(func_id).keys()) + \
                       list(fram.get_function_controls(func_id).keys()) + \
                       list(fram.get_function_resources(func_id).keys())

        for dep_id in dependencies:
            if dep_id in function_id_to_name:
                dep_name = function_id_to_name[dep_id]
                G.add_edge(dep_name, func_name)

    return G

def plot_dependency_graph(G):
    plt.figure(figsize=(16, 10))
    pos = nx.spring_layout(G, seed=42)  # Layout
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray",
            node_size=3000, font_size=10, font_weight="bold", arrows=True)
    plt.title("Diagram of dependencies between FRAM functions")

    # Save graph as PNG file
    plt.savefig("dep_graph", dpi=600, bbox_inches='tight')
    plt.show()

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

    # Plot dependency graph
    plot_dependency_graph(create_dependency_graph(fram))

    # Run simulation
    env.run()

if __name__ == "__main__":
    fram_simulation()