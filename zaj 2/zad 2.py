def lexicographic_subset(n: int, k: int):
    first_series = []
    for i in range(k, 0, -1):
        first_series.append(i)
    result = [first_series]
    j = k - 1
    current_series = 0
    while j != -1:
        flag = True
        while flag and j != -1:
            if j == 0:
                if result[current_series][j] < n:
                    flag = False
                else:
                    j -= 1
            else:
                if result[current_series][j-1]-1 > result[current_series][j]:
                    flag = False
                else:
                    j -= 1
        if j != -1:
            result.append(result[current_series][:])
            current_series += 1
            result[current_series][j] += 1
            temp = 1
            for i in range(k-1, j, -1):
                result[current_series][i] = temp
                temp += 1
            j = k - 1
    return result


n = int(input())
k = int(input())
subsets = lexicographic_subset(n, k)
for i in range(len(subsets)):
    for j in range(k):
        print(subsets[i][j], end="")
        if j != k-1:
            print(" ", end="")
    if i != len(subsets)-1:
        print("")
