DJI Tello Edu to dron zaprojektowany specjalnie dla edukacji i nauki programowania. Ten mały i lekki dron wyposażony jest w kamery, czujniki i narzędzia, które umożliwiają naukę i zabawę w programowanie.

Dron Tello Edu został opracowany we współpracy z firmą Ryze Tech i posiada funkcje, które ułatwiają naukę programowania. Dron ten jest kompatybilny z językiem programowania Scratch, co pozwala na łatwe tworzenie programów przez dzieci i młodzież. Ponadto, dron Tello Edu obsługuje również języki Python i Swift, umożliwiając bardziej zaawansowanym użytkownikom tworzenie bardziej skomplikowanych programów.

Dron Tello Edu jest wyposażony w kamerę HD, która umożliwia nagrywanie wideo w rozdzielczości 720p. Można nim również wykonywać zdjęcia o rozdzielczości 5 megapikseli. Dron posiada również wiele czujników, w tym czujniki wysokości, czujniki odległości oraz czujniki optyczne, które pozwalają na stabilne loty w pomieszczeniach.

Jednym z największych atutów drona Tello Edu jest jego łatwość obsługi. Dron ten jest bardzo prosty w użyciu i ma intuicyjny interfejs, co sprawia, że jest on idealny dla początkujących. Można nim również kontrolować za pomocą specjalnej aplikacji mobilnej, co dodatkowo ułatwia użytkowanie.

DJI Tello Edu to świetny wybór dla nauczycieli i uczniów, którzy chcą poznać podstawy programowania i uczyć się nowych umiejętności w interaktywny i zabawny sposób. Dron ten oferuje wiele możliwości i narzędzi, które pomagają w nauce, co czyni go idealnym narzędziem dla nauki w szkole, na kursach lub w domu.

----
*Mamy do dyspozycji dwa modele dronów:*

* czarny **Tello EDU** bez wyświetlacza LCD, dla niego jest przeznaczona klasa `TelloEDU()`
* czerwony **Ryzen TT** z wyświetlaczem LCD, dla niego jest przeznaczona klasa `RyzenTT()`

Naszym zadaniem jest użyć odpowiednie klasy - wówczas mamy dostęp do pewnych metod zarezerwowanych dla danego typu drona.

----
Minimalny kod, który pozwala na sprawdzenie **TelloEDU**:

```python
from tello_solectric_pl import TelloEDU
from time import sleep

dron = TelloEDU()

if dron.connect():
    print("Połączenie OK - start..")
    dron.takeoff()
    sleep(2)
    dron.land()
else:
    print("Połączenie nieudane")

print("KONIEC")

```

---
Zmiany w stosunku do oryginalnych metod biblioteki `djitellopy`:

* metoda `connect()` zwraca wartość `True` lub `False` - i w ten sposób kontrolujemy, czy połączenie się powiodło oraz czy używamy odpowiedniego drona.
