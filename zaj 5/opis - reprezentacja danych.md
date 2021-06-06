Graf w programie zapisany jest w słowniku pythonowym gdzie dla każdego wierchołka
zapisana jest lista wierzchołków, do których prowadzi z niego krawędź skierowana.

Więc zapis {1: [2], 2: [3, 4], 3: [4], 4:[]} oznacza, że z 1 jest poprowadzona 
krawędź skierowana do 2, z 2 do 3 i 4, z 3 do 4, a z 4 nie wychodzi żadna krawędź.

Przyjmuje, że ten graf jest siecią przepływową, na którą się umówiliśmy więc ujściem
jest wierzchołek, z którego nie wychodzą żadne krawędzie

Oprócz tego przechowuje również, który wierzchołek jest korzeniem oraz słownik
odpowiadający słownikowi z krawędziami zawierający wartości przepływów dla danej krawędzi

Przykładowe dane są zapisane w graph.txt i można je nadpisać świerzo wygenerowanymi
wykonując program generate_graph.py

Program max_capacity.py rozwiązuje problem maksymalnego przepływu, a edge_separable_paths.py
problem znajdowania ścierzek o rozłącznych krawędziach. Oprócz tego do generowania danych potrzebny 
jest prufers_code_to_tree.py, który zawiera funkcję przekształcającą kod prufera na drzewo oraz do odczytu
danych z pliku (co robią max_capacity.py oraz edge_separable_paths.py) potrzebne jest generate_graph.py.
Powinny działać na pythonie 3.* jak są w tym samym folderze.

Program max_capacity.py wyświetla: 
    Maximal capacity: {znaleziona funckja maksymalnego przepływu dla sieci z pliku}

Program edge_separable_paths.py wyświetla:
    edge separable paths: [znalezione ścieżki o rozłącznych krawędziach dla sieci z pliku]

