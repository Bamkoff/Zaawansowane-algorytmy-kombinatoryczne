# Napisz program, który wypisze wszystkie podzbiory zbioru liczb {1,...,n} w porządku minimalnych zmian. Użyj algorytmu następnika.


def successor_algorithm(n : int):
    if n > 0:
        codes = [[0] * n]
        current_code = codes[0][:]
        for i in range((2**n) - 2):
            if current_code.count(1) % 2 == 0:
                if current_code[-1] == 0:
                    current_code[-1] = 1
                else:
                    current_code[-1] = 0
            else:
                j = n-1
                while current_code[j] != 1:
                    j-=1
                if current_code[j-1] == 0:
                    current_code[j-1] = 1
                else:
                    current_code[j-1] = 0
            codes.append(current_code[:])
        codes.append([1] + [0] * (n-1))
        return codes
    else:
        print('n has to be bigger than 0')
        return []


for code in successor_algorithm(int(input())):
    print('{', end='')
    temp_list = []
    for i in range(len(code)):
        if code[i] == 1:
            temp_list.append(i+1)
    for i in range(len(temp_list)):
        if i != len(temp_list) - 1:
            print(str(temp_list[i]) + " ", end='')
        else:
            print(str(temp_list[i]), end='')
    print('}')
