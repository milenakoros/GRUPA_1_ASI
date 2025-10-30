ZBIÓR DANYCH: Used Car Price Prediction Dataset 🚗

---

### O zbiorze danych

**Nazwa:** Used Car Price Prediction Dataset
**Źródło:** [Kaggle – Used Car Price Prediction Dataset](https://www.kaggle.com/datasets/vrajesh0sharma7/used-car-price-prediction/data)
**Zakres początkowy:** 7 400 ogłoszeń samochodów używanych w Indiach opisanych za pomocą 29 cech technicznych i rynkowych.

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


### Kedro Quickstart
1. Utwórz środowisko conda:
   ```bash
   #utworzenie środowiska
   conda env create -f environment.yml

   #aktywacja środowiska
   conda activate asi-ml

   #aktualizacja środowiska
   conda env update -f environment.yml --prune #aktualizacja środowiska
   ```

2. Zaloguj się do **Weights & Biases (W&B)**:
   ```bash
   wandb login
   ```

4. Uruchom kedro pipeline'y:
   ```bash
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
