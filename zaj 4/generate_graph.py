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


def generate_random_graph(n: int):
    root, graph = generate_tree(n)
    print("root:", root)
    print("tree:", graph)

    leaves = find_all_leaves(graph)
    rest = find_rest(graph, root)
    print("leaves:", leaves)
    print("rest:", rest)

    rand_leaf_index = random.randint(0, len(leaves) - 1)
    rand_leaf = leaves[rand_leaf_index]
    print("rand_leaf:", rand_leaf)
    leaves.pop(rand_leaf_index)

    whole = rest + leaves

    for leaf in leaves:
        graph[leaf].append(rand_leaf)

    paths = get_paths(graph, root)
    for path in paths:
        path.pop(-1)
        path.pop(0)
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
    print("graph:", graph)
    return root, graph


def get_nodes_string(node, edges):
    string = str(node)
    for edge in edges:
        string = string + " " + str(edge)
    return string


def write_directed_graph_to_file(path, filename, root, graph):
    with open(path + filename, 'w') as file:
        file.write(str(root) + ";")
        for node in graph.keys():
            file.write(get_nodes_string(node, graph[node]) + ";")


if __name__ == '__main__':
    root, graph = generate_random_graph(20)
    write_directed_graph_to_file("", "graph.txt", root, graph)
