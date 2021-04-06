def Prufers_code(edges_dict):
    e = edges_dict.copy()
    code = []
    nodes = list(e.keys())
    nodes.sort()
    while len(nodes) > 2:
        current_node = 1
        while len(e[current_node]) != 1:
            current_node += 1
        node = e[current_node][0]
        code.append(node)
        e[current_node] = []
        e[node].remove(current_node)
        nodes.remove(current_node)
    return code


number_of_nods = int(input())
edges = {}

for i in range(1, number_of_nods):
    edge = input().split()
    if int(edge[0]) not in edges:
        edges[int(edge[0])] = []
    edges[int(edge[0])].append(int(edge[1]))
    if int(edge[1]) not in edges:
        edges[int(edge[1])] = []
    edges[int(edge[1])].append(int(edge[0]))
prufer_code = Prufers_code(edges)

for i in range(len(prufer_code)):
    if i == len(prufer_code)-1:
        print(prufer_code[i], end="")
    else:
        print(prufer_code[i], end=" ")
