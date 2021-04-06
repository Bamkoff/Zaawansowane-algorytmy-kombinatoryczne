# def newton(n:int, k:int):
#     nominator = 1
#     for i in range(1, n+1):
#         nominator *= i
#     denominator_1 = 1
#     denominator_2 = 1
#     for i in range(1, k+1):
#         denominator_1 *= i
#     for i in range(1, n-k+1):
#         denominator_1 *= i
#     denominator = denominator_1 * denominator_2
#     return nominator/denominator


# def rank(n:int, k:int):
#     result = 0
#     for i in range(1, k+1):
#         for j in range(i):
#             result += newton(n-j, k-i)
#     return result

# def algorithm(n:int, k:int):
#     x = 1
#     r = rank(n, k)
#     for i in range(1, k+1):
#         while newton(n-x, k-i) <= r:
#             r = r - newton(n-x, k-i)
#             x += 1
#         print(x)
#         x = x+1


def lexicographic_subset(n: int, k: int):
    first_series = []
    for i in range(1, k+1):
        first_series.append(i)
    result = [first_series]
    j = k - 1
    current_series = 0
    while j != -1:
        flag = True
        while flag and j != -1:
            if j == k-1:
                if result[current_series][j] < n:
                    flag = False
                else:
                    j -= 1
            else:
                if result[current_series][j] < result[current_series][j+1]-1:
                    flag = False
                else:
                    j -= 1
        if j != -1:
            result.append(result[current_series][:])
            current_series += 1
            result[current_series][j] += 1
            for i in range(j+1, k):
                result[current_series][i] = result[current_series][i-1] + 1
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
