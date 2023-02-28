import random
import functions

# Initiate the colors.. Or we can take Black=0, White=1 so we have binary array
colors = ['BLACK', 'ORANGE']


# This object a node that has number, name, color, and position
class Vertice:
    def __init__(self, number):
        self.number = number
        self.name = f"V_{number}"
        self.position = None
        self.binary_color = random.randint(0, 1)  # Color is black if 0, otherwise it is blue
        self.color = colors[self.binary_color]

    def Print(self):
        print(f"Node: {self.name}, Color: {self.color}, Position {self.position}")

    def Set_Color(self, binary_color):
        if binary_color != 0 and binary_color != 1:
            return self
        self.binary_color = binary_color
        self.color = colors[binary_color]
        return self


# This object represent a connection (line) between two nodes
class Connection:
    def __init__(self, node_1, node_2):
        self.node_1 = node_1
        self.node_2 = node_2
        self.satisfaction = node_1.color != node_2.color

    def Print(self):
        print(
            f"Node: {self.node_1.name} ({self.node_1.color}) Connected to Node: {self.node_2.name} ({self.node_2.color}). Value: {self.satisfaction}")


# This object includes a solution (set of vertices) with their connections, and used to simulate the solution
class Graph:
    def __init__(self, chromosome):

        self.vertices = functions.create_vertices(chromosome)
        self.connections = functions.create_connections(self.vertices)
        self.satisfaction = functions.fitness(self.connections)
        self.Set_Positions()
        self.binary_solution = [x.binary_color for x in self.vertices]

    def Print(self):
        print(
            f"Vertices are {len(self.vertices)}, With satisfaction = {self.satisfaction} of total {len(self.connections)}")

    def Set_Positions(self):
        self.vertices = functions.set_positions(self.vertices)
        return self

    def Create_Connections(self):
        self.connections = functions.create_connections(self.vertices)
        return self


# class Chromosome:
#     def __init__(self, label, number_of_nodes):
#         self.label = label
#         self.genes = [random.randint(0, 1) for _ in range(number_of_nodes)]
