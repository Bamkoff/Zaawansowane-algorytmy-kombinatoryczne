Do generowanie losowych sieci przepływowych służy generate_graph.py

Wykonuje to funkcja generate_random_graph.
Wykonuje ona następujące kroki:
1. Tworzy losowy kod prefera dla danej liczby wierzchołków i przerabia go na graf z losowo wybranym korzeniem.
   Jeżeli drzewo nie ma przynajmniej dwóch wierzchołków, z których wychodzą co najmniej dwie krawędzie to losuje nowe.
2. Losowo wybiera jeden z liści(zawsze omijając korzeń) jako ujście i dopisuje krawędzie z reszty liści do ujścia.
3. Znajduje wszystkie ścieżki prowadzące z korzenia do ujścia.
4. Losuje ile krawedzi doda do środka grafu.
5. Wybiera dwa losowe wierzchołki z grafu nie licząc korzenia i źródła i sprawdza czy są z dwóch różnych ścierzek i 
   czy nie ma już miedzy nimi krawędzi. Jeżeli te dwa warunki są prawdziwe dodaje pomiędzy nimi krawędź
6. Powtarza punkt 5 aż osiągnie tyle dodanych krawędzi ile wcześniej wylosował
7. Jeżeli korzeń ma tylko jedną wychodzącą z niego krawędź losuje mu jeszcze jedną
8. Na koniec losuje wartości przepływów dla wszystkich krawędzi (dla problemu znajdowania ścierzek o rozłącznych 
   krawędziach wszystkie wartości przepływów w częsci main kodu są zastępowane przez 1)

W tym pliku znajdują się również dwie funkcje jedna do zapisu a druga do odczytu sieci przepływów z pliku.
W main tego programu jest wygenerowanie grafu i zapisanie go do pliku oraz odczytanie tego grafu z tego pliku.
