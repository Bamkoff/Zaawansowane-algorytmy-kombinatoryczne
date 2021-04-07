from prufers_code_to_tree import generate_tree_from_prufer_code
import random


def generate_prufers_code(n: int):
    code = []
    for i in range(n-2):
        code.append(random.randint(1, n))
    return code


def find_all_leaves(tree: dict):
    leaves = []
    for i in tree.keys():
        if len(tree[i]) == 0:
            leaves.append(i)
    return leaves


def find_rest(tree: dict, root: int):
    rest = []
    for i in tree.keys():
        if len(tree[i]) != 0 and i != root:
            rest.append(i)
    return rest


def get_paths(graph: dict, root: int):
    paths = []

    def bfs(g: dict, path, current):
        queue = [current]
        path.append(current)
        while queue:
            current_node = queue.pop(0)
            flag = True
            if len(g[current_node]) == 0:
                paths.append(path)
                return
            if len(g[current_node]) > 1:
                for i in g[current_node]:
                    if flag:
                        flag = False
                    else:
                        bfs(g, path[:], i)
            path.append(g[current_node][0])
            queue.append(g[current_node][0])

    bfs(graph, [], root)
    return paths


def generate_tree(n: int):
    code = generate_prufers_code(n)
    edges = generate_tree_from_prufer_code(code)
    root = random.randint(1, n)
    edges_map = {i: [] for i in range(1, n+1)}
    queue = [root]
    while queue:
        current_node = queue.pop(0)
        for i in range(len(edges)-1, -1, -1):
            if edges[i][0] == current_node:
                edges_map[current_node].append(edges[i][1])
                queue.append(edges[i][1])
                edges.pop(i)
            elif edges[i][1] == current_node:
                edges_map[current_node].append(edges[i][0])
                queue.append(edges[i][0])
                edges.pop(i)
    return root, edges_map


def generate_random_graph(n: int, log=False):
    root, graph = generate_tree(n)
    if log:
        print("root:", root)
        print("tree:", graph)

    leaves = find_all_leaves(graph)
    rest = find_rest(graph, root)
    if log:
        print("leaves:", leaves)
        print("rest:", rest)

    rand_leaf_index = random.randint(0, len(leaves) - 1)
    rand_leaf = leaves[rand_leaf_index]
    if log:
        print("rand_leaf:", rand_leaf)
    leaves.pop(rand_leaf_index)

    whole = rest + leaves

    for leaf in leaves:
        graph[leaf].append(rand_leaf)

    paths = get_paths(graph, root)
    for path in paths:
        path.pop(-1)
        path.pop(0)
    if log:
        print("paths:", paths)

    added_edges_number = random.randint(1, len(paths)) - 1
    counter = 0
    while counter < added_edges_number:
        x, y = random.randint(0, len(whole)-1), random.randint(0, len(whole)-1)
        flag = True
        for path in paths:
            if whole[x] in path and whole[y] in path:
                flag = False
        if flag:
            if whole[y] not in graph[whole[x]]:
                graph[whole[x]].append(whole[y])
                counter += 1

    while len(graph[root]) < 2:
        rand_edge_index = random.randint(0, len(rest) - 1)
        if rest[rand_edge_index] not in graph[root]:
            graph[root].append(rest[rand_edge_index])
    if log:
        print("graph:", graph)
    graphs_capacity = {}
    for key in graph.keys():
        graphs_capacity[key] = []
        for edge in graph[key]:
            graphs_capacity[key].append(random.randint(1, 10))
    if log:
        print("graphs_capacity:", graphs_capacity)
    return root, graph, graphs_capacity


def get_nodes_string(node, edges):
    string = str(node)
    for edge in edges:
        string = string + " " + str(edge)
    return string


def write_directed_graph_to_file(path, filename, root, graph, graphs_capacity):
    with open(path + filename, 'w') as file:
        file.write(str(root) + ";")
        for node in graph.keys():
            file.write(get_nodes_string(node, graph[node]) + ";")
        file.write("\n")
        for node in graphs_capacity.keys():
            file.write(get_nodes_string(node, graphs_capacity[node]) + ";")



def read_directed_graph_from_file(path, filename):
    with open(path + filename, 'r') as file:
        graph = {}
        root = -1
        graphs_capacity = {}
        str = file.readline()
        if str != "" and str is not None:
            graph_str = str.split(";")
            graph_str.pop(-1)
            root = int(graph_str[0])
            for i in range(1, len(graph_str)):
                edges_of_node = graph_str[i].split(" ")
                graph[int(edges_of_node[0])] = []
                if len(edges_of_node) > 1:
                    for j in range(1, len(edges_of_node)):
                        graph[int(edges_of_node[0])].append(int(edges_of_node[j]))
        if str != "" and str is not None:
            str = file.readline()
            graph_str = str.split(";")
            graph_str.pop(-1)
            for i in graph_str:
                capacities_of_node = i.split(" ")
                key = int(capacities_of_node[0])
                graphs_capacity[key] = []
                if len(capacities_of_node) > 1:
                    for j in range(1, len(capacities_of_node)):
                        graphs_capacity[key].append(int(capacities_of_node[j]))
        return root, graph, graphs_capacity


if __name__ == '__main__':
    root, graph, graphs_capacity = generate_random_graph(20)
    print(root, graph)
    print(graphs_capacity)
    print()
    write_directed_graph_to_file("", "graph.txt", root, graph, graphs_capacity)
    root, graph, graphs_capacity = read_directed_graph_from_file("", "graph.txt")
    print(root, graph)
    print(graphs_capacity)
