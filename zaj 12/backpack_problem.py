import random as rand


def generate_items(_n, _size_range=(3, 12), _price_range=(1, 100)):
    _items_size_list = []
    _items_price_list = []
    for i in range(_n):
        _items_price_list.append(rand.randint(_price_range[0], _price_range[1]))
        _items_size_list.append(rand.randint(_size_range[0], _size_range[1]))
    return _items_size_list, _items_price_list


def write_items_to_file(_w, _c, path="items"):
    with open(path, 'w') as file:
        for i in range(len(_w)):
            file.write(f'{_w[i]} {_c[i]}\n')


def read_items_from_file(path="items"):
    _w, _c = [], []
    with open(path, 'r') as file:
        _line = file.readline()
        while _line != '':
            _values = _line.strip('\n').split()
            _w.append(int(_values[0]))
            _c.append(int(_values[1]))
            _line = file.readline()
    return _w, _c


def branching_bounding_backpack(_B, _w, _c):
    w, c = _w[:], _c[:]
    best_price = [0]
    chosen_items = []
    items_indexes = [i + 1 for i in range(len(w))]
    c_by_w = [c[i]/w[i] for i in range(len(w))]
    s = [0 for i in range(len(w))]
    best_series = []
    best_border = [0]
    for i in range(len(w)):
        for j in range(len(w) - (i + 1)):
            if c_by_w[j + 1] > c_by_w[j]:
                c_by_w[j + 1], c_by_w[j] = c_by_w[j], c_by_w[j + 1]
                c[j + 1], c[j] = c[j], c[j + 1]
                w[j + 1], w[j] = w[j], w[j + 1]
                items_indexes[j + 1], items_indexes[j] = items_indexes[j], items_indexes[j + 1]

    def sum_price_and_size(series):
        _p, _s = 0, 0
        for i in range(len(series)):
            if series[i] == 1:
                _p += c[i]
                _s += w[i]
        return _p, _s

    def get_k(start, _s):
        size = _s
        _k = start
        while size <= _B and _k < len(w) - 1:
            size += w[_k]
            _k += 1
        return _k

    def recursion(series, node=-1, add=False):
        if add:
            series[node] = 1
        profit, size = sum_price_and_size(series)
        k = get_k(node, size)
        whole_size = size + sum(w[node+1: k])
        border = profit + sum(c[node+1:k]) + (_B - whole_size) * c_by_w[k]
        if size <= _B and border > best_border[0]:
            if node == len(_w) - 1:
                best_price[0] = profit
                best_series.append(series[:])
                best_border[0] = border
            else:
                recursion(series[:], node=node + 1, add=True)
                recursion(series[:], node=node + 1)

    recursion(s[:])
    for i, value in enumerate(best_series[-1]):
        if value == 1:
            chosen_items.append(items_indexes[i])
    chosen_items.sort()
    return chosen_items, best_price[0]


if __name__ == "__main__":
    # Tu zmieniam rozmiar plecaka
    B = 30

    # n jest do ewentualnego wygenerowania nowych przedmiotów
    # aby wygenerować nowy graf wystarczy odkomentować trzy poniższe linijki
    # n = 5
    # weights, prices = generate_items(n)
    # write_items_to_file(weights, prices)

    weights, prices = read_items_from_file()
    print(f'items size list: {weights}\nitems price list: {prices}')
    print(f'backpack size: {B}')
    items, price = branching_bounding_backpack(B, weights, prices)
    # numerowane od 1
    print(f'chosen items: {items}')
    print(f'best price: {price}')
