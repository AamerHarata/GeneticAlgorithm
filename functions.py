import matplotlib.pyplot as plt
import objects as o
import random


def create_chromosome(nodes_number=16):
    valid_count = nodes_number == 4 or nodes_number == 8 or nodes_number == 16
    if not valid_count:
        return []
    return [random.randint(0, 1) for _ in range(nodes_number)]


def create_vertices(chromosome):
    temp = []
    for x in range(len(chromosome)):
        temp.append(o.Vertice(x).Set_Color(chromosome[x]))
    return temp


def create_connections(nodes, version=1):
    nodes_count = len(nodes)
    connections = []
    valid_count = nodes_count == 4 or nodes_count == 8 or nodes_count == 16
    if not valid_count:
        return connections

    if nodes_count >= 4:
        connections.append(o.Connection(nodes[0], nodes[1]))
        connections.append(o.Connection(nodes[0], nodes[2]))
        connections.append(o.Connection(nodes[1], nodes[3]))
        connections.append(o.Connection(nodes[2], nodes[3]))
    if nodes_count >= 8:
        connections.append(o.Connection(nodes[0], nodes[4]))
        connections.append(o.Connection(nodes[1], nodes[5]))
        connections.append(o.Connection(nodes[2], nodes[6]))
        connections.append(o.Connection(nodes[3], nodes[7]))
    if nodes_count == 16:
        connections.append(o.Connection(nodes[4], nodes[8]))
        connections.append(o.Connection(nodes[4], nodes[10]))
        connections.append(o.Connection(nodes[8], nodes[9]))
        connections.append(o.Connection(nodes[10], nodes[12]))

        connections.append(o.Connection(nodes[5], nodes[9]))
        connections.append(o.Connection(nodes[5], nodes[11]))
        connections.append(o.Connection(nodes[11], nodes[13]))

        connections.append(o.Connection(nodes[7], nodes[13]))
        connections.append(o.Connection(nodes[7], nodes[15]))
        connections.append(o.Connection(nodes[14], nodes[15]))

        connections.append(o.Connection(nodes[6], nodes[14]))
        connections.append(o.Connection(nodes[6], nodes[12]))

        if version == 1:
            connections.append(o.Connection(nodes[0], nodes[9]))
            connections.append(o.Connection(nodes[1], nodes[8]))

            connections.append(o.Connection(nodes[1], nodes[13]))
            connections.append(o.Connection(nodes[3], nodes[11]))

            connections.append(o.Connection(nodes[2], nodes[15]))
            connections.append(o.Connection(nodes[3], nodes[14]))

            connections.append(o.Connection(nodes[0], nodes[12]))
            connections.append(o.Connection(nodes[2], nodes[10]))

    return connections


def create_N_generations(initial_population, n_generations):
    last_to_children = [x for x in initial_population]
    new_generations = []
    for i in range(n_generations):
        last_to_children = create_next_generation(last_to_children)
        new_generations.extend(last_to_children)

    return new_generations


def create_next_generation(parents):
    all_children = []
    i = 0
    while i < len(parents) - 1:
        children = two_points_cross_over(parents[i], parents[i + 1])
        all_children.append(children[0])
        all_children.append(children[1])
        i += 2
    return all_children


def eliminate_n_chromosomes(chromosomes, n=-1):
    fitness_result = []
    if n <= 0:
        n = int(len(chromosomes) / 2)

    for i in range(len(chromosomes)):
        fitness_result.append([i, o.Graph(chromosomes[i]).satisfaction])

    fitness_result.sort(key=lambda x: x[1], reverse=True)
    fitness_result = fitness_result[:n]

    new_chromosomes = [chromosomes[x[0]] for x in fitness_result]
    return new_chromosomes


def remove_duplications(generation):
    no_duplications = []
    for x in generation:
        if x not in no_duplications:
            no_duplications.append(x)

    return no_duplications


def best_n_solutions(graphs, n):
    if n > len(graphs):
        return []

    graphs.sort(key=lambda x: x.satisfaction, reverse=True)
    return graphs[:n]


def fitness(connections):
    # Note that this function will count the True values regardless how many connections is there.
    # Consider that nodes can be 4, 8, or 16; This function however does not take care of that number.

    true_count = sum(x.satisfaction for x in connections)
    false_count = len(connections) - true_count  # how many false If needed
    return true_count  # the true count is how many Satisfactions, what means how many vertices been colored correctly


def mutation(chromosome):
    new_chromosome = [x for x in chromosome]

    rand_index = random.randint(0, len(chromosome) - 1)
    rand_val = random.randint(0, 1)
    new_chromosome[rand_index] = rand_val

    # If there is no mutation return value will be empty
    if new_chromosome == chromosome:
        return [False, []]

    # Otherwise, it will return the chromosome with new mutation
    return [True, new_chromosome]


def create_mutations(chromosomes):
    mutations = []
    for x in chromosomes:
        new_mutation = mutation(x)
        if new_mutation[0]:
            mutations.append(new_mutation[1])
    return mutations


def set_positions(nodes):
    nodes_count = len(nodes)
    new_nodes = []
    valid_count = nodes_count == 4 or nodes_count == 8 or nodes_count == 16
    if not valid_count:
        return nodes

    if nodes_count >= 4:
        nodes[0].position = (7, 10)
        nodes[1].position = (10, 10)
        nodes[2].position = (7, 7)
        nodes[3].position = (10, 7)

    if nodes_count >= 8:
        nodes[4].position = (3, 14)
        nodes[5].position = (14, 14)
        nodes[6].position = (3, 3)
        nodes[7].position = (14, 3)

    if nodes_count == 16:
        nodes[8].position = (7, 16)
        nodes[9].position = (10, 16)
        nodes[10].position = (1, 10)
        nodes[11].position = (16, 10)
        nodes[12].position = (1, 7)
        nodes[13].position = (16, 7)
        nodes[14].position = (7, 1)
        nodes[15].position = (10, 1)
    return nodes


def plot_solution(graph):
    nodes_circles = graph.vertices
    nodes_connections = graph.connections

    ax = plt.axes()
    ax.set_xlim((0, 18))
    ax.set_ylim((0, 18))
    ax.set_aspect('equal')
    for node in nodes_circles:
        circle = plt.Circle(node.position, 1, color=node.color)
        ax.add_patch(circle)
        plt.text(node.position[0] - 0.50, node.position[1] - 0.25, node.name, color="White", size=8)

    for con in nodes_connections:
        color = "Green" if con.satisfaction else "Red"
        plt.plot([con.node_1.position[0], con.node_2.position[0]], [con.node_1.position[1], con.node_2.position[1]],
                 color=color)
    plt.show()


def two_points_cross_over(chromosome_1, chromosome_2):
    if len(chromosome_1) != len(chromosome_2):
        return []

    # Choose random two points between first and last indexes. Excluding the first and last values
    lower_boundary = random.randint(1, len(chromosome_1) - 1)
    upper_boundary = random.randint(1, len(chromosome_1) - 1)

    # Prevent the same value in the two boundaries
    while upper_boundary == lower_boundary:
        upper_boundary = random.randint(1, len(chromosome_1) - 1)

    # Be sure the upper_boundary is higher than lower_boundary
    if lower_boundary > upper_boundary:
        temp = lower_boundary
        lower_boundary = upper_boundary
        upper_boundary = temp

    child_1 = []
    child_2 = []

    for i in range(len(chromosome_1)):
        if i < lower_boundary:
            child_1.append(chromosome_1[i])
            child_2.append(chromosome_2[i])

        elif lower_boundary <= i < upper_boundary:
            child_1.append(chromosome_2[i])
            child_2.append(chromosome_1[i])

        else:
            child_1.append(chromosome_1[i])
            child_2.append(chromosome_2[i])

    # print(f"Two points cross-over function launched, with lower_boundary: {lower_boundary} "
    #       f"and upper_boundary: {upper_boundary}. New children are:")
    # print(child_1)
    # print(child_2)
    # print("-----------------")
    return [child_1, child_2]


def random_reducing(chromosome):
    if len(chromosome) < 1:
        return []
    random.shuffle(chromosome)
    return chromosome[0: int(len(chromosome) / 2)]
