from generate_graph import read_directed_graph_from_file
from max_capacity import get_shortest_path
from max_capacity import get_max_capacity
from max_capacity import get_paths


def get_edge_separable_paths(root: int, graph: dict, graphs_capacity: dict, print_log=False):
    f_c = {}
    edge_separabable_paths = []
    for i in graph.keys():
        for j in graph.keys():
            f_c[(i, j)] = 0
    if print_log:
        print("capacity_function", f_c)
    max_capacity = get_max_capacity(graphs_capacity)
    paths = get_paths(graph, root, graphs_capacity, f_c)
    if print_log:
        print("paths[0]:", paths)
    while paths:
        path = paths[get_shortest_path(paths[:])]
        edge_separabable_paths.append(path[:])
        f_c_min = max_capacity
        current_node = root
        for i in range(1, len(path)):
            value = graphs_capacity[current_node][graph[current_node].index(path[i])] - f_c[(current_node, path[i])]
            if value < f_c_min:
                f_c_min = value
            current_node = path[i]
        current_node = root
        for i in range(1, len(path)):
            f_c[(current_node, path[i])] = f_c[(current_node, path[i])] + f_c_min
            f_c[(path[i], current_node)] = -f_c[(current_node, path[i])]
            current_node = path[i]
        paths = get_paths(graph, root, graphs_capacity, f_c)
        if print_log:
            print("paths[0]:", paths)
    return edge_separabable_paths


if __name__ == "__main__":
    r, g, gc = read_directed_graph_from_file("", "graph.txt")
    print("root:", r)
    print("graph:", g)
    for key in gc.keys():
        for i in range(len(gc[key])):
            gc[key][i] = 1
    print("graphs capacity:", gc)
    p = get_edge_separable_paths(r, g, gc)
    print("edge separable paths:", p)
