def enlargement_code_algorithm(n):
    if n == 1:
        return [[0], [1]]
    else:
        lower_codes = enlargement_code_algorithm(n - 1)
        codes = []
        for element in lower_codes:
            codes.append([0] + element)
        for element in lower_codes[::-1]:
            codes.append([1] + element)
        return codes


for code in enlargement_code_algorithm(int(input())):
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