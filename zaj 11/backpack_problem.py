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


def dynamic_programing_backpack(_B, _n, _w, _c):
    _A = []
    _items_indexes = []
    # uzupełnienie obu macierzy wartościami zerowymi
    for _i in range(0, _n + 1):
        _A.append([])
        _items_indexes.append([])
        for _j in range(0, _B + 1):
            _A[_i].append(0)
            _items_indexes[_i].append([0, 0])

    # rozpoczęcie uzupełniania obu macierzy właściwymi wartościami
    for _i in range(1, _n+1):
        for _j in range(1, _B+1):
            if _w[_i-1] > _j:
                _A[_i][_j] = _A[_i-1][_j]
                _items_indexes[_i][_j] = [_i-1, _j]
            else:
                if _A[_i-1][_j] > _A[_i-1][_j-_w[_i-1]] + _c[_i-1]:
                    _A[_i][_j] = _A[_i-1][_j]
                    _items_indexes[_i][_j] = [_i-1, _j]
                else:
                    _A[_i][_j] = _A[_i-1][_j-_w[_i-1]] + _c[_i-1]
                    _items_indexes[_i][_j] = [_i - 1, _j - _w[_i-1]]
    # for i in _A:
    #     print(i)
    # wyciągnięcie, które przedmioty trafiły do plecaka
    _items = []
    _to_add = [_n, _B]
    while _to_add != [0, 0]:
        _new_to_add = _items_indexes[_to_add[0]][_to_add[1]]
        if _to_add[1] > _new_to_add[1] and _to_add[0] > 0:
            _items.append(_to_add[0])
        _to_add = _new_to_add
    return _items, _A[_n][_B]


if __name__ == "__main__":
    # Tu zmieniam rozmiar plecaka
    B = 30

    # n jest do ewentualnego wygenerowania nowych przedmiotów
    # n = 5
    # w, c = generate_items(n)
    # print(w, c)
    # write_items_to_file(w, c)

    w, c = read_items_from_file()
    print(f'items size: {w}\nitems price: {c}')
    print(f'backpack size: {B}')
    items, price = dynamic_programing_backpack(B, len(w), w, c)
    # numerowane od 1
    print(f'chosen items: {items}')
    print(f'best price: {price}')
