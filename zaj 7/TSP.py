import random as rand
import time


# funkcja generująca losowy pełny graf o losowych wagach
def generate_complete_graph_with_weight(nodes: int, weight_scope=(1, 10)):
    weight_matrix = []
    for i in range(nodes):
        weight_matrix.append([])
        for j in range(nodes):
            if j == i:
                weight_matrix[i].append(0)
            else:
                weight_matrix[i].append(rand.randint(weight_scope[0], weight_scope[1]))
    return weight_matrix


# procedura zapisująca do pliku macierz wag grafu
def write_weights_to_file(weight_matrix, path="", filename="weights.tsp"):
    with open(path + filename, "w") as file:
        for i in range(len(weight_matrix)):
            for j in range(len(weight_matrix)):
                file.write(str(weight_matrix[i][j]) + "\t")
            file.write("\n")


# funkcja zwracająca macierz wag grafu pobraną z podanego pliku
def read_weights_from_file(path="", filename="weights.tsp", tab_on_line_end=True):
    weight_matrix = [[]]
    with open(path + filename, "r") as file:
        first_row = file.readline().split("\t")
        if tab_on_line_end:
            first_row.pop(-1)
        for weight in first_row:
            weight_matrix[0].append(int(weight))
        for line in range(len(first_row) - 1):
            next_row = file.readline().split("\t")
            weight_matrix.append([])
            if tab_on_line_end:
                next_row.pop(-1)
            for weight in next_row:
                weight_matrix[line + 1].append(int(weight))
    return weight_matrix


# tworzy losową permutacje przedstawiającą ścieżkę po unikalnych wierzchołkach od etykietach od 2 do [podana wartość]
def generate_permutation(nodes):
    permutation = list(range(2, nodes + 1))
    rand.shuffle(permutation)
    return tuple(permutation)


# funkcja generująca listę sąsiadów podanej permutacji
# można podać do niej również jaka definicja sąsiada ma być wykorzystana do generowania
def get_neighbors(permutation, definition='swap'):
    neighbors = set()
    if definition == 'swap':
        for i in range(len(permutation)):
            for j in range(len(permutation)):
                if i == j:
                    continue
                else:
                    temp_list = list(permutation)
                    temp_list[i], temp_list[j] = temp_list[j], temp_list[i]
                    neighbors.add(tuple(temp_list))
    elif definition == 'move':
        for i in range(len(permutation)):
            for j in range(len(permutation)):
                temp_list = list(permutation)
                if i < j:
                    for k in range(i, j):
                        temp_list[k], temp_list[k+1] = temp_list[k+1], temp_list[k]
                elif i > j:
                    for k in range(i, j, -1):
                        temp_list[k], temp_list[k - 1] = temp_list[k - 1], temp_list[k]
                else:
                    continue
                neighbors.add(tuple(temp_list))
    elif definition == 'inverse':
        for i in range(len(permutation) - 1):
            for j in range(i+1, len(permutation)):
                temp_list = list(permutation)
                cut = temp_list[i:j+1]
                left = temp_list[:i+1]
                right = temp_list[j:]
                left.pop(-1)
                right.pop(0)
                cut.reverse()
                neighbors.add(tuple(left + cut + right))
    else:
        print('definition takes one of three values:\n\t - "swap"\n\t - "move"\n\t - "inverse"')
    return neighbors


# funkcja obliczająca wagę ścieżki w grafie, którą reprezentuje podana permutacja
def get_permutation_weight(permutation, weight_matrix):
    weight = weight_matrix[0][permutation[0]-1]
    weight += weight_matrix[permutation[-1]-1][0]
    for i in range(len(permutation)-1):
        weight += weight_matrix[permutation[i]-1][permutation[i+1]-1]
    return weight


# funkcja znajdująca w liście sąsiada z najmniejszą wagą ścieżki jaką reprezentuje
# zwraca go oraz jego wagę
def get_best_neighbor(neighbors, weight_matrix):
    best_weight = 0
    first_neighbor = True
    neighbor_list = []
    for i in neighbors:
        neighbor_list.append(i)
    best_neighbor = neighbor_list[0]
    for neighbor in neighbor_list:
        if first_neighbor:
            first_neighbor = False
            best_weight = get_permutation_weight(neighbor, weight_matrix)
        else:
            neighbor_weight = get_permutation_weight(neighbor, weight_matrix)
            if best_weight > neighbor_weight:
                best_weight = neighbor_weight
                best_neighbor = neighbor
    return best_neighbor, best_weight


# algorytm przeszukiwania lokalnego
def local_search(weight_matrix, start_permutation=None, logs=False):
    result = start_permutation
    if start_permutation is None:
        result = generate_permutation(len(weight_matrix))
    result_weight = get_permutation_weight(result, weight_matrix)
    neighbors = get_neighbors(result)
    best_neighbor, neighbor_weight = get_best_neighbor(neighbors, weight_matrix)
    counter = 1
    while result_weight > neighbor_weight:
        result = best_neighbor
        result_weight = neighbor_weight
        neighbors = get_neighbors(result)
        best_neighbor, neighbor_weight = get_best_neighbor(neighbors, weight_matrix)
        counter += 1
    if logs:
        print("Number of iterations in local search", counter)
    return result, result_weight


# perturbacja podanej permutacji
def perturbate_permutation(permutation, permutation_var):
    permutation_list = list(permutation)
    number_of_changes = rand.randint(permutation_var[0], permutation_var[1])
    for i in range(number_of_changes):
        first_index = rand.randint(0, len(permutation)-1)
        second_index = rand.randint(0, len(permutation)-1)
        while first_index == second_index and len(permutation) > 1:
            second_index = rand.randint(0, len(permutation) - 1)
        permutation_list[first_index], permutation_list[second_index] = permutation_list[second_index], permutation_list[first_index]
    return tuple(permutation_list)


# algorytm iteracyjnego przeszukiwania lokalnego
def iterative_local_search(weight_matrix, iterations=1000, permutation_var=(2, 4), logs=False):
    permutation = generate_permutation(len(weight_matrix))
    best_result, best_weight = local_search(weight_matrix, logs=logs)
    for i in range(iterations - 1):
        current_result, current_weight = local_search(weight_matrix, permutation, logs=logs)
        if current_weight < best_weight:
            best_result = current_result
            best_weight = current_weight
        perturbation = perturbate_permutation(current_result, permutation_var)
        current_result, current_weight = local_search(weight_matrix, perturbation, logs=logs)
        if current_weight < best_weight:
            best_result = current_result
            best_weight = current_weight
        permutation = current_result
    return best_result, best_weight


# tworzenie ciągu N na podstawie podanej permutacji
def get_n_neighbors(permutation):
    n_list = [get_neighbors(permutation),
              get_neighbors(permutation, definition='move'),
              get_neighbors(permutation, definition='inverse')]
    return n_list


# algorytm przeszukiwania zmiennego sasiedztwa
def changing_neighborhood_search(weight_matrix, start_permutation=None):
    best_result = start_permutation
    if start_permutation is None:
        best_result = generate_permutation(len(weight_matrix))
    best_weight = get_permutation_weight(best_result, weight_matrix)
    k = 0
    N = get_n_neighbors(best_result)
    while k < 3:
        best_neighbor, best_neighbor_weight = get_best_neighbor(N[k], weight_matrix)
        if best_neighbor_weight < best_weight:
            best_result, best_weight = best_neighbor, best_neighbor_weight
            k = 0
            N = get_n_neighbors(best_result)
        else:
            k += 1
    return best_result, best_weight


# wyznaczenie wartości granicznej
def get_top_boundary(weight_matrix):
    max_weight = 0
    for row in weight_matrix:
        max_in_row = row[0]
        for element in row:
            if element > max_in_row:
                max_in_row = element
        max_weight += max_in_row
    return max_weight


# ocenienie podanego osobnika
def rate_individual(individual, top_boundary, weight_matrix):
    return top_boundary - get_permutation_weight(individual, weight_matrix)


# wyznaczenie dystrybuanty dla populacji
def get_populations_distributor(population, top_boundary, weight_matrix):
    distributor = []
    individual_ratings = []
    for individual in population:
        individual_ratings.append(rate_individual(individual, top_boundary, weight_matrix))
    F = sum(individual_ratings)
    first_element = True
    for rating in individual_ratings:
        if first_element:
            distributor.append(rating/F)
            first_element = False
        else:
            distributor.append(distributor[-1] + rating/F)
    return distributor


# wybieranie nowej populacji na podstawie podanej populacji oraz podanej dystrybuanty
def get_new_population(old_population, distributor):
    new_population = []
    for i in range(len(old_population)):
        r = rand.random()
        chosen_index = -1
        for j, value in enumerate(distributor):
            if r <= value:
                chosen_index = j
                break
        new_population.append(old_population[chosen_index])
    return new_population


# krzyżowanie dwóch podanych osobników
def order_hybridization(first_indv, second_indv):
    temp_1 = list(first_indv)
    temp_2 = list(second_indv)
    s = rand.randint(0, len(first_indv)-1)
    t = rand.randint(0, len(first_indv)-1)
    while t == s:
        t = rand.randint(0, len(first_indv)-1)
    if t < s:
        t, s = s, t
    alfa, beta = [], []
    for i in range(s):
        alfa.append(-1)
        beta.append(-1)
    alfa += temp_1[s:t+1]
    beta += temp_2[s:t+1]
    for i in range(t+1, len(first_indv)):
        alfa.append(-1)
        beta.append(-1)
    for i in range(t + 1, len(first_indv)):
        found_value_alpha = False
        found_value_beta = False
        for j in range(t + 1, len(first_indv)):
            if not found_value_alpha:
                if second_indv[j] not in alfa and alfa[i] == -1:
                    alfa[i] = second_indv[j]
                    found_value_alpha = True
            if not found_value_beta:
                if first_indv[j] not in beta and beta[i] == -1:
                    beta[i] = first_indv[j]
                    found_value_beta = True
        if not found_value_alpha or not found_value_beta:
            for j in range(len(first_indv)):
                if not found_value_alpha:
                    if second_indv[j] not in alfa and alfa[i] == -1:
                        alfa[i] = second_indv[j]
                        found_value_alpha = True
                if not found_value_beta:
                    if first_indv[j] not in beta and beta[i] == -1:
                        beta[i] = first_indv[j]
                        found_value_beta = True
    for i in range(0, s):
        found_value_alpha = False
        found_value_beta = False
        for j in range(t + 1, len(first_indv)):
            if not found_value_alpha:
                if second_indv[j] not in alfa and alfa[i] == -1:
                    alfa[i] = second_indv[j]
                    found_value_alpha = True
            if not found_value_beta:
                if first_indv[j] not in beta and beta[i] == -1:
                    beta[i] = first_indv[j]
                    found_value_beta = True
        if not found_value_alpha or not found_value_beta:
            for j in range(len(first_indv)):
                if not found_value_alpha:
                    if second_indv[j] not in alfa and alfa[i] == -1:
                        alfa[i] = second_indv[j]
                        found_value_alpha = True
                if not found_value_beta:
                    if first_indv[j] not in beta and beta[i] == -1:
                        beta[i] = first_indv[j]
                        found_value_beta = True
    return tuple(alfa), tuple(beta)


# mutacja osobnika
def mutation_substring_inversion(individual):
    s = rand.randint(0, len(individual)-1)
    t = rand.randint(0, len(individual)-1)
    while t == s:
        t = rand.randint(0, len(individual)-1)
    if t < s:
        t, s = s, t
    temp_list = list(individual)
    cut = temp_list[s:t + 1]
    left = temp_list[:s + 1]
    right = temp_list[t:]
    left.pop(-1)
    right.pop(0)
    cut.reverse()
    return tuple(left + cut + right)


# wykonanie krzyżowania i mutacji na podanej populacji
def change_population(population):
    chosen_individuals = []
    for i in range(len(population)):
        r = rand.randint(0, 100)
        if r <= 50:
            chosen_individuals.append(i)
    rand.shuffle(chosen_individuals)
    for i in range(0, len(chosen_individuals)-1, 2):
        population[chosen_individuals[i]], population[chosen_individuals[i+1]] =\
            order_hybridization(population[chosen_individuals[i]], population[chosen_individuals[i+1]])
    chosen_individuals = []
    for i in range(len(population)):
        r = rand.randint(0, 100)
        if r <= 5:
            chosen_individuals.append(i)
    for i in chosen_individuals:
        population[i] = mutation_substring_inversion(population[i])


# algorytm genetyczny
def genetic_algorithm(weight_matrix, N: int = 500, max_iterations: int = 1000, top_boundary: int = None):
    population = []
    if top_boundary is None:
        top_boundary = get_top_boundary(weight_matrix)
    for i in range(N):
        population.append(generate_permutation(len(weight_matrix)))
    populations_distributor = get_populations_distributor(population, top_boundary, weight_matrix)
    best_result, best_weight = get_best_neighbor(population, weight_matrix)
    iteration = 0
    while iteration < max_iterations:
        population = get_new_population(population, populations_distributor)
        change_population(population)
        populations_distributor = get_populations_distributor(population, top_boundary, weight_matrix)
        current_result, current_weight = get_best_neighbor(population, weight_matrix)
        if current_weight < best_weight:
            best_result, best_weight = current_result, current_weight
        iteration += 1
    return best_result, best_weight


# procedura wyświetlająca wyniki 3 zaimplementowanych algorytmów dla podanego pliku
def print_outcome(file="weights.tsp", tab_on_line_end=True, best_weight=None, print_path_and_weight=True):
    weights = read_weights_from_file(filename=file, tab_on_line_end=tab_on_line_end)
    print(file + ":")
    if print_path_and_weight:
        print(f"\twaga najlepszej ścieżki: {best_weight}")
    start_time = time.time()
    r1, w1 = iterative_local_search(weights, permutation_var=(3, 7))
    print("\titeracyjne przeszukiwanie lokalne:")
    error1 = ((w1 - best_weight) / best_weight) * 100
    print(f"\t\tBłąd względny: {error1}")
    if print_path_and_weight:
        print(f"\t\tznaleziona ścieżka: {r1},\n\t\twaga znalezionej ścieżki: {w1}")
    time1 = (time.time() - start_time)
    print("\t\tskończone w czasie: %s \n" % time1)
    start_time = time.time()
    r2, w2 = changing_neighborhood_search(weights)
    print("\tprzeszukiwanie zmiennego sasiedztwa:")
    error2 = ((w2 - best_weight) / best_weight) * 100
    print(f"\t\tBłąd względny: {error2}")
    if print_path_and_weight:
        print(f"\t\tznaleziona ścieżka: {r2},\n\t\twaga znalezionej ścieżki: {w2}")
    time2 = (time.time() - start_time)
    print("\t\tskończone w czasie: %s \n" % time2)
    start_time = time.time()
    r3, w3 = genetic_algorithm(weights)
    print("\talgorytm genetyczny:")
    error3 = ((w3 - best_weight) / best_weight) * 100
    print(f"\t\tBłąd względny: {error3}")
    if print_path_and_weight:
        print(f"\t\tznaleziona ścieżka: {r3},\n\t\twaga znalezionej ścieżki: {w3}")
    time3 = (time.time() - start_time)
    print("\t\tskończone w czasie: %s " % time3)


# funkcja zwraca tabele zawierające wyniki testów zaimplementowanych algorytmów zapisaną w latex'u
def create_test_table(file, algorithm, best_weight, iterations=10):
    weights = read_weights_from_file(filename=file, tab_on_line_end=False)
    table = "\\begin{tabular}{|c|c|c|c|}\n" \
            "\\hline\n" \
            "\\multicolumn{4}{|c|}{" + algorithm + "} \\\\\n" \
            "\\hline\n" \
            "iteracja & znaleziona waga & błąd względny (\\%) & czas zakończenia \\\\\n" \
            "\\hline\n"
    error_list = []
    time_list = []
    weight_list = []
    for i in range(iterations):
        start_time = time.time()
        if algorithm == "iteracyjne przeszukiwanie lokalne":
            r, w = iterative_local_search(weights, permutation_var=(3, 7))
        elif algorithm == "przeszukiwanie zmiennego sąsiedztwa":
            r, w = changing_neighborhood_search(weights)
        else:
            r, w = genetic_algorithm(weights)
        stop_time = (time.time() - start_time)
        error = ((w - best_weight) / best_weight) * 100
        error_list.append(error)
        time_list.append(stop_time)
        weight_list.append(w)
        table += f"{i+1} & {w} & {error} & {stop_time} \\\\\n"
    error_sum = sum(error_list)
    time_sum = sum(time_list)
    weight_sum = sum(weight_list)
    mean_error = error_sum / iterations
    mean_time = time_sum / iterations
    mean_weight = weight_sum / iterations
    table += "\\hline\n" \
             f"uśrednione: & {mean_weight} & {mean_error} & {mean_time} \\\\" \
             "\\hline\n" \
             "\\end{tabular}\n"
    return table


if __name__ == "__main__":
    # https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html

    file_list = ["5cities.tsp", "15cities.tsp", "17cities.tsp", "26cities.tsp", "42cities.tsp", "48cities.tsp"]
    best_weigh_list = [19, 291, 2085, 937, 699, 33523]

    for i, file_name in enumerate(file_list):
        print_outcome(file_name, tab_on_line_end=False, best_weight=best_weigh_list[i], print_path_and_weight=True)
        print("")


    # zapisanie w pliku tabel.txt danych testów do przeklejenia do latex'a
    # with open("tables.txt", "w", encoding="utf-8") as table_file:
    #     table_file.write("\\begin{itemize} \n")
    #     for index, file_name in enumerate(file_list):
    #         table_file.write(f"\\item Nazwa pliku: {file_name}. Najlepsza możliwa waga: {best_weigh_list[index]}\\\\\n")
    #         table_file.write(create_test_table(file_name, "iteracyjne przeszukiwanie lokalne",
    #                                            best_weight=best_weigh_list[index]))
    #         table_file.write("\n")
    #         table_file.write(create_test_table(file_name, "przeszukiwanie zmiennego sąsiedztwa",
    #                                            best_weight=best_weigh_list[index]))
    #         table_file.write("\n")
    #         table_file.write(create_test_table(file_name, "algorytm genetyczny", best_weight=best_weigh_list[index]))
    #         table_file.write("\\newpage\n")
    #         print(f"zakończone tworzenie tabeli dla pliku {file_name}")
    #     table_file.write("\\end{itemize}\n")
