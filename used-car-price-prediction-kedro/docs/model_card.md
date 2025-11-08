# Model Card — AutoGluon Used Car Price Prediction

## Problem & Use-case
Celem projektu jest stworzenie modelu uczenia maszynowego do przewidywania ceny samochodu używanego na podstawie jego cech technicznych, historii i danych ogłoszeniowych.
Model ma wspomagać użytkowników (np. dealerów lub platformy sprzedażowe) w szybkim oszacowaniu realnej wartości pojazdu — co może przyspieszyć proces wyceny i pomóc w wykrywaniu ofert odstających od rynkowych trendów.

Model oparty jest o bibliotekę **AutoGluon Tabular**, która automatycznie testuje i łączy różne algorytmy regresyjne (ensemble), aby osiągnąć jak najlepsze wyniki bez konieczności ręcznego strojenia hiperparametrów.

---

## Data
Dane wejściowe pochodzą z publicznie dostępnych lub przykładowych zbiorów dotyczących ogłoszeń sprzedaży samochodów używanych.
Zbiór zawiera m.in. kolumny:
- dane techniczne pojazdu (rok produkcji, przebieg, moc, typ nadwozia, skrzynia biegów),
- dane rynkowe (cena wywoławcza, liczba wyświetleń, liczba właścicieli),
- dane opisowe (lokalizacja, stan, ocena pojazdu).

Charakterystyka:
- rozmiar: ok. 25 000 rekordów, po czyszczeniu ok. 20 000 rekordów,
- brak danych osobowych (PII = **no**),
- źródło danych: publiczne ogłoszenia / dane przykładowe,
- dane przetworzone i zakodowane numerycznie w etapie `basic_clean`,
- zmienna docelowa (`label`): **sale_price**.

---

## Metrics
**Główną metryką** oceny jest **RMSE** (Root Mean Squared Error) — pierwiastek z średniego błędu kwadratowego. Metryka ta szczególnie penalizuje duże odchylenia prognoz od wartości rzeczywistych, dzięki czemu dobrze odzwierciedla ogólną dokładność modelu regresyjnego.

**Metrykami pomocniczymi** są:
- **MAE** (Mean Absolute Error) — średni błąd bezwzględny, który informuje o przeciętnej różnicy między wartościami przewidywanymi a rzeczywistymi.

- **R²** (Współczynnik determinacji) — miara dopasowania modelu, pokazująca, jaka część zmienności danych jest wyjaśniana przez model (wartość bliska 1 oznacza dobre dopasowanie).

Zbiór danych został podzielony na część **treningową** stanowiącą 80% danych oraz część **testową** obejmującą 20% danych.

---

## Limitations
- **Zakres danych** – model został nauczony wyłącznie na danych z jednego regionu (rynek lokalny), przez co może gorzej generalizować na inne kraje lub rynki.
- **Czasowe ograniczenie** – dane dotyczą określonego okresu, bez uwzględnienia trendów sezonowych lub zmian rynkowych.
- **Cecha black-box** – AutoGluon generuje model zespołowy (ensemble), co utrudnia pełną interpretowalność wyników.
- **Wartości odstające** – model może mieć trudność z poprawnym przewidzeniem skrajnych wartości (np. bardzo luksusowych lub bardzo tanich aut).
- **Dane wejściowe** – poprawność prognoz zależy od jakości danych (np. błędy w przebiegu lub roku produkcji mogą mocno zniekształcić wynik).

---

## Ethics & Risk
- **Etyka i przejrzystość** – model nie powinien być wykorzystywany jako ostateczny wyznacznik ceny, a raczej jako narzędzie pomocnicze.
- **Ryzyko błędnej interpretacji** – użytkownik może przecenić dokładność predykcji, jeśli nie ma świadomości ograniczeń modelu.
- **Potencjalne nadużycia** – przewidywania mogą być użyte do manipulowania cenami w ogłoszeniach, jeśli model zostanie wykorzystany niezgodnie z przeznaczeniem.
- **Zarządzanie ryzykiem** – rekomendowane jest okresowe retraining modelu i porównywanie z aktualnymi danymi rynkowymi, aby unikać dryfu modelu.

---

## Versioning
- W&B run: https://wandb.ai/GRUPA_1_ASI/used-car-price-prediction/runs/060oghd1
- Model artifact: model_autogluon:v3
- Data: cleaned_used_cars
- Env: Python 3.11, AutoGluon 1.4.0
