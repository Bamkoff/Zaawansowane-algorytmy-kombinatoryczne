Funkcja my_heuristic_solution działa bardzo podobnie do First fit'a tyle, że na początku każdy obiekt, który jest
równy lub większy niż 0.5 jest wkładany do osobnego pojemnika. A dla reszty obiektów wykonywane są te same operacje co
przy First fit. 

Wprowadziłem też przez przypadek chyba nieheurystyczny algorytm wykonujący to samo zadanie, zaczyna z pustą
paczką i próbuje do niej dopasować największy możliwy obiekt. Za każdym razem gdy dobierze taki obiekt dodaje go do 
paczki i usuwa z listy obiektów. Następnie próbuje do tej samej paczki dopasować następny największy możliwy element i 
jeżeli taki znajdzie postępuje w ten sam sposób. Jeżeli nie znajdzie żadnego elementu, który zmieści się w obecnej paczce
, a istnieją jeszcze elemnty na liście to stworzy nową paczkę i dla niej zacznie wykonywać ten sam proces do czasu aż
skończą się obiekty na liście