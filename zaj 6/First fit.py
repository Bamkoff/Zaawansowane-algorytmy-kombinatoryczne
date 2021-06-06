import random as rand
import math


# funkcja znajdująca rozłorzenie obiektów w pojemnikach algorytmem First fit
def first_fit(object_list, rel_tol: float = 1e-6):
    package_list = []
    for obj in object_list:
        added = False
        for package in package_list:
            if 1.0 - sum(package) >= obj or math.isclose(1.0 - sum(package), obj, rel_tol=rel_tol):
                package.append(obj)
                added = True
                break
        if not added:
            package_list.append([obj])
    return package_list


# funkcja znajdująca rozłorzenie obiektów w pojemnikach algorytmem jaki przyszedł mi do głowy ale nie jest heurystyczny
def my_solution(obj_list, rel_tol: float = 1e-6):
    def find_max_fitting(package, object_list):
        max_object = 0.0
        max_index = -1
        package_sum = 1.0 - sum(package)
        for index, element in enumerate(object_list):
            if (package_sum >= element or math.isclose(package_sum, element, rel_tol=rel_tol)) and element > max_object:
                max_object = element
                max_index = index
        if max_index > -1:
            object_list.pop(max_index)
        return max_object, max_index
    package_list = [[]]
    while obj_list:
        max_fitting, fitting_index = find_max_fitting(package_list[-1], obj_list)
        if fitting_index == -1 and obj_list:
            package_list.append([])
        else:
            package_list[-1].append(max_fitting)
    return package_list


# funkcja znajdująca rozłorzenie obiektów w pojemnikach zmodyfikowanym algorytmem First fit
def my_heuristic_solution(obj_list, rel_tol: float = 1e-6):
    package_list = []
    for index, element in enumerate(obj_list):
        if element >= 0.5:
            package_list.append([element])
            obj_list.pop(index)
    for obj in obj_list:
        added = False
        for package in package_list:
            if 1.0 - sum(package) >= obj or math.isclose(1.0 - sum(package), obj, rel_tol=rel_tol):
                package.append(obj)
                added = True
                break
        if not added:
            package_list.append([obj])
    return package_list


# funkcja do generowania listy o n obiektach
def generate_object_list(object_number: int, denominator: float = 10.0):
    new_list = []
    if denominator > 2:
        for i in range(object_number):
            new_list.append(float(rand.randint(1, int(denominator)-1))/denominator)
    return new_list


# funkcja zapisująca liste obiektów do pliku
def write_object_set_to_file(object_list, path: str = "", filename: str = "Object_list.txt"):
    with open(path + filename, "w") as file:
        for index, obj in enumerate(object_list):
            if index < len(object_list) - 1:
                file.write(str(obj) + " ")
            else:
                file.write(str(obj))


# funkcja odczytująca liste obiektów z pliku
def read_object_set_from_file(path: str = "", filename: str = "Object_list.txt"):
    new_list = []
    with open(path + filename, "r") as file:
        line = file.readline()
        for i in line.split(" "):
            new_list.append(float(i))
    return new_list


# część main kodu
if __name__ == "__main__":
    # zmienna generate_new_object_list ustawiona na:
    # True - generuje nową liste obiektów i wpisuje ją do pliku
    # False - odczytuje listę obiektów z pliku
    generate_new_object_list = False
    objects = []
    if generate_new_object_list:
        objects = generate_object_list(10)
        write_object_set_to_file(objects)
    else:
        objects = read_object_set_from_file()

    first_fit_sol = first_fit(objects)
    my_sol = my_solution(objects[:])
    my_heu_sol = my_heuristic_solution(objects[:])

    print("lista obiektów:", objects)
    print("paczki z obiektami:")
    print(" - first_fit:", first_fit_sol, "paczki:", len(first_fit_sol))
    print(" - moje rozwiązanie:", my_sol, "paczki:", len(my_sol))
    print(" - moje rozwiązanie heurystyczne:", my_heu_sol, "paczki:", len(my_heu_sol))
