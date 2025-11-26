ZBIÓR DANYCH: Used Car Price Prediction Dataset 🚗

---

### O zbiorze danych

- **Nazwa:** Used Car Price Prediction Dataset
- **Źródło:** [Kaggle – Used Car Price Prediction Dataset](https://www.kaggle.com/datasets/vrajesh0sharma7/used-car-price-prediction/data)
- **Zakres początkowy:** 7 400 ogłoszeń samochodów używanych w Indiach opisanych za pomocą 29 cech technicznych i rynkowych.

---

### Opis
Zbiór danych przedstawia szczegółowe informacje o samochodach używanych oferowanych na sprzedaż na terenie Indii. Obejmuje zarówno dane techniczne pojazdów (np. marka, model, rok produkcji, przebieg), jak i czynniki rynkowe wpływające na cenę (np. miasto, liczba wyświetleń, typ nadwozia, dostępność gwarancji).

---

### Opis kolumn

| Kolumna | Opis |
|----------|------|
| car_name | Nazwa samochodu (marka + model, np. Maruti Swift, Hyundai i10). |
| yr_mfr | Rok produkcji samochodu. |
| fuel_type | Rodzaj paliwa (Benzyna, Diesel, CNG, Elektryczny itp.). |
| kms_run | Przebieg samochodu w kilometrach. |
| sale_price | Ostateczna cena sprzedaży (zmienna docelowa w regresji). |
| city | Miasto, w którym wystawiono ogłoszenie. |
| times_viewed | Liczba wyświetleń ogłoszenia online. |
| body_type | Typ nadwozia (Hatchback, Sedan, SUV itp.). |
| transmission | Rodzaj skrzyni biegów (Manualna / Automatyczna). |
| variant | Wariant pojazdu (np. LXI, VDI, Sports itp.). |
| assured_buy | Czy samochód ma opcję gwarantowanego zakupu (True/False). |
| registered_city | Miasto rejestracji pojazdu. |
| registered_state | Stan, w którym pojazd został zarejestrowany. |
| is_hot | Czy ogłoszenie jest „gorące” (duże zainteresowanie). |
| rto | Kod lokalnego urzędu komunikacji. |
| source | Źródło (platforma ogłoszeniowa). |
| make | Producent samochodu (np. Maruti, Hyundai, Honda). |
| model | Model samochodu (np. Swift, i10, City). |
| car_availability | Dostępność pojazdu (Dostępny / Sprzedany). |
| total_owners | Liczba poprzednich właścicieli (1, 2, 3 itd.). |
| broker_quote | Cena oferowana przez pośrednika. |
| original_price | Cena pojazdu jako nowego. |
| car_rating | Ocena stanu samochodu (Excellent, Good, Fair itd.). |
| ad_created_on | Data i godzina utworzenia ogłoszenia. |
| fitness_certificate | Czy pojazd ma ważne badanie techniczne (True/False). |
| emi_starts_from | Minimalna rata miesięczna przy finansowaniu. |
| booking_down_pymnt | Minimalna wpłata przy rezerwacji. |
| reserved | Czy pojazd jest zarezerwowany (True/False). |
| warranty_avail | Dostępność gwarancji (True/False). |

---

### Kluczowe informacje
- **Liczba rekordów:** 7 400
- **Liczba kolumn:** 29 (numeryczne, kategoryczne i logiczne)
- **Zmienna docelowa:** `sale_price`
- **Potencjalne zastosowania:** predykcja cen, analiza trendów, modelowanie zachowań kupujących

---

### Licencja i źródło
- **Licencja:** CC0 – Public Domain
- **Data pobrania danych:** 10.10.2025
- Dane są publicznie dostępne do celów edukacyjnych i analitycznych.

---

### Prywatność i bezpieczeństwo danych
Zbiór danych **nie zawiera danych osobowych (PII)** ani informacji wrażliwych.
Wszystkie rekordy dotyczą wyłącznie **cech technicznych pojazdów** i danych rynkowych.

---

### Kedro Quickstart
1. Utwórz środowisko conda:
   ```bash
   #utworzenie środowiska
   conda env create -f environment.yml

   #aktywacja środowiska
   conda activate asi-ml

   #aktualizacja środowiska
   conda env update -f environment.yml --prune
   ```

2. Zaloguj się do **Weights & Biases (W&B)**:
   ```bash
   wandb login
   ```

4. Uruchom kedro pipeline'y:
   ```bash
   #wywołaj wszystkie nody
   kedro run

   #wywołaj konkretny pipeline
   kedro run --pipeline {nazwa_pipeline'a}

   #wywołaj tylko konkretny node
   kedro run --nodes {nazwa_nodu}
   ```

5. Testy pytest
   ```bash
   #wykonaj wszystkie testy
   pytest -q

   #wykonaj konkretny test
   pytest -q tests/pipelines/data_science/test_pipeline.py::TestDataScienceNodes::test_basic_clean
   ```

5. Sprawdź wyniki:
   - Model zapisany w: data/06_models/model_baseline.pkl
   - Metryki zapisane w: data/09_tracking/metrics_baseline.json

---

### Autogluton - wyniki eksperymentów

#### W&B
Link do projektu: https://wandb.ai/GRUPA_1_ASI/used-car-price-prediction/

#### Wyniki

| Presets                     | Eval Metric | Time Limit (s) |     RMSE ↓    |     MAE ↓    |    R² ↑    |
| :-------------------------- | :---------- | :------------: | :-----------: | :----------: | :--------: |
| medium_quality_faster_train | rmse        |       120      |   22 011.67   |   9 086.74   |   0.9942   |
| best_quality                | mae         |       300      |   18 500.84   |   769.424    |   0.996    |
| optimize_for_deployment     | r2          |       100      |   21 940.19   |   9 185.8    |   0.9943   |
| extreme_quality             | rmse        |       500      |   52 031.33   |   7 919.12   |   0.9681   |

#### Wniosek
Do oceny jakości modeli regresyjnych wybrano trzy główne miary: **RMSE**, **MAE** oraz **R²**.

* **RMSE (Root Mean Squared Error)** pokazuje, jak duże są przeciętne odchylenia prognoz od wartości rzeczywistych – im mniejsza wartość, tym dokładniejsze przewidywania. Jest czuły na duże błędy, dlatego dobrze pokazuje stabilność modelu.
* **MAE (Mean Absolute Error)** mierzy średni błąd bezwzględny, mniej podatny na wartości odstające, przez co lepiej odzwierciedla ogólną dokładność w typowych przypadkach.
* **R² (Współczynnik determinacji)** informuje, jak dobrze model wyjaśnia zmienność danych – wartość bliska 1 oznacza bardzo dobrą jakość dopasowania niezależnie od skali danych.

Na podstawie tych metryk można zauważyć, że konfiguracja **`best_quality`** z limitem czasu 300 sekund osiągnęła najlepsze wyniki.
Model ten zapewnia najwyższą precyzję prognoz przy umiarkowanym czasie treningu, dlatego został uznany za najlepszy kompromis między dokładnością a wydajnością.

---

### FastAPI - Quickstart
1. Odpalenie lokalnego FastAPI
```
# uruchom fastapi
uvicorn src.api.main:app --reload --port 8000
```
2. Przykładowe żadania API, przy użyciu BASHa
```
# przykładowy test (GET/healthz)
curl http://127.0.0.1:8000/healthz

# przykładowy payload (POST/predict)
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "car_name": 39,
    "yr_mfr": 11,
    "fuel_type": 1,
    "kms_run": 28652,
    "city": 1,
    "times_viewed": 483,
    "body_type": 0,
    "transmission": 0,
    "variant": 171,
    "assured_buy": 1,
    "registered_city": 15,
    "registered_state": 5,
    "is_hot": 1,
    "rto": 43,
    "source": 0,
    "make": 9,
    "model": 6,
    "car_availability": 1,
    "total_owners": 2,
    "broker_quote": 386415,
    "original_price": 395599.0,
    "car_rating": 2,
    "fitness_certificate": 1,
    "emi_starts_from": 9189,
    "booking_down_pymnt": 59340,
    "reserved": 0,
    "warranty_avail": 0
  }'
```
3. Wyświetl zawartość Bazy Danych, przy użyciu BASHa
```
# wyświetl 5 górnych elementów tabeli bazy danych
sqlite3 "./data/08_reporting/api_predictions.db" "SELECT * FROM predictions LIMIT 5;"
```

---

### Docker Quickstart

Poniższy rozdział przedstawia kompletny przewodnik dotyczący budowania, uruchamiania oraz testowania aplikacji przy użyciu Docker Compose. Znajdziesz tu również instrukcje dostępu do API, panelu UI oraz bazy danych.

#### Budowanie i uruchamianie kontenerów

Aby zbudować obrazy Dockera oraz uruchomić wszystkie usługi zdefiniowane w `docker-compose.yml`, wykonaj poniższe polecenie:

```
docker compose up --build
```

Po zakończeniu procesu wszystkie komponenty aplikacji będą działać równocześnie.

#### API — testowanie endpointów

Po uruchomieniu systemu backend dostępny jest pod adresem `http://localhost:8000`.

1. Sprawdzenie stanu aplikacji (Healthcheck)

```
curl http://localhost:8000/healthz
```

2. Wysłanie żądania POST do endpointu `/predict`

```
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "car_name": 39,
    "yr_mfr": 11,
    "fuel_type": 1,
    "kms_run": 28652,
    "city": 1,
    "times_viewed": 483,
    "body_type": 0,
    "transmission": 0,
    "variant": 171,
    "assured_buy": 1,
    "registered_city": 15,
    "registered_state": 5,
    "is_hot": 1,
    "rto": 43,
    "source": 0,
    "make": 9,
    "model": 6,
    "car_availability": 1,
    "total_owners": 2,
    "broker_quote": 386415,
    "original_price": 395599.0,
    "car_rating": 2,
    "fitness_certificate": 1,
    "emi_starts_from": 9189,
    "booking_down_pymnt": 59340,
    "reserved": 0,
    "warranty_avail": 0
  }'
```

Endpoint zwróci przewidywanie wygenerowane przez model.

#### UI — Interfejs użytkownika

Aplikacja posiada graficzny interfejs działający w Streamlit. Po uruchomieniu systemu można go otworzyć, przechodząc do:

```
http://localhost:8501
```

W przeglądarce pojawi się panel do wprowadzania danych i wyświetlania wyników predykcji.

#### BD — Dostęp do bazy danych (PostgreSQL)

Kontener z bazą danych PostgreSQL pozwala na wykonywanie zapytań SQL poprzez `psql`.

Aby wejść do kontenera i wykonać przykładowe zapytanie:

```
docker exec -it <container_db> psql -U app -d appdb -c "select * from predictions limit 5;"
```

W miejsce `<container_db>` wpisz nazwę kontenera PostgreSQL, np. `db_postgres`.
