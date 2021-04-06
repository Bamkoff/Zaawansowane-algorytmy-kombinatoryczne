def sort_edges(edges, edge):
    if edge[0] > edge[1]:
        temp = edge[0]
        edge[0] = edge[1]
        edge[1] = temp
    index = 0
    for i in edges:
        if edge[0] < i[0]:
            break
        elif edge[0] == i[0] and edge[1] < i[1]:
            break
        else:
            index += 1
    edges.insert(index, edge)


def generate_tree_from_prufer_code(code):
    L1 = code[:]
    L2 = []
    edges = []
    nodes = set()
    for i in range(len(code)+2):
        L2.append(i+1)
        nodes.add(i+1)
    for k in range(len(L1)):
        current_node = L2[0]
        counter = 1
        while L1.count(current_node) > 0:
            current_node = L2[counter]
            counter += 1
        sort_edges(edges, [code[k], current_node])
        L1.remove(code[k])
        L2.remove(current_node)
    sort_edges(edges, [L2[0], L2[1]])
    return edges


if __name__ == '__main__':
    number_of_nods = int(input())
    string_list = input().split()
    prufer_code = []
    for i in string_list:
        prufer_code.append(int(i))

    tree = generate_tree_from_prufer_code(prufer_code)

    for i in tree:
        print(str(i[0]), str(i[1]))

