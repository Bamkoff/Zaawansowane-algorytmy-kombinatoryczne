from generate_graph import read_directed_graph_from_file


def get_shortest_path(paths):
    min_path = 0
    for i in range(len(paths)):
        if len(paths[min_path]) > len(paths[i]):
            min_path = i
    return min_path


def get_max_capacity(graphs_capacity: dict):
    max_capacity = 0
    for node in graphs_capacity.keys():
        for i in graphs_capacity[node]:
            if i > max_capacity:
                max_capacity = i
    return max_capacity


def get_paths(graph: dict, root: int, graphs_capacity: dict, capacity_function: dict):
    paths = []

    def bfs(g: dict, path, current, closed):
        queue = [current]
        path.append(current)
        while queue:
            current_node = queue.pop(0)
            closed.append(current_node)
            flag = True
            if len(g[current_node]) == 0:
                paths.append(path)
                return
            if len(g[current_node]) > 1:
                for i in g[current_node]:
                    if flag:
                        flag = False
                    else:
                        if i not in closed and capacity_function[(current_node, i)] \
                                < graphs_capacity[current_node][graph[current_node].index(i)]:
                            bfs(g, path[:], i, closed[:])
            if g[current_node][0] not in closed and capacity_function[(current_node, g[current_node][0])]\
                    < graphs_capacity[current_node][graph[current_node].index(g[current_node][0])]:
                path.append(g[current_node][0])
                queue.append(g[current_node][0])
    bfs(graph, [], root, [])
    return paths


def edmonds_karps_algorithm(root: int, graph: dict, graphs_capacity: dict, print_log=False):
    f_c = {}
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
    return f_c


if __name__ == "__main__":
    r, gr, g_c = read_directed_graph_from_file("", "graph.txt")
    print("root:", r)
    print("directed graph", gr)
    print("edges capacities:", g_c)
    print("Maximal capacity:", edmonds_karps_algorithm(r, gr, g_c, False))
