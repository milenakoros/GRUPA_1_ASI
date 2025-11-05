# used_car_price_prediction

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Overview

This is your new Kedro project with PySpark setup, which was generated using `kedro 1.0.0`.

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `tests/test_run.py` and `tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```

You can configure the coverage threshold in your project's `pyproject.toml` file under the `[tool.coverage.report]` section.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. Install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can use tools like [`nbstripout`](https://github.com/kynan/nbstripout). For example, you can add a hook in `.git/config` with `nbstripout --install`. This will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://docs.kedro.org/en/stable/tutorial/package_a_project.html)

## Wyniki eksperymentów AutoGluon

| Presets                     | Eval Metric | Time Limit (s) |     RMSE ↓    |     MAE ↓    |    R² ↑    |                             
| :-------------------------- | :---------- | :------------: | :-----------: | :----------: | :--------: | 
| medium_quality_faster_train | rmse        |       120      |   36 398.52   |   22 624.13  |   0.9747   | 
| best_quality                | mae         |       300      |   11 362.58   |   2 881.45   |   0.9975   |
| optimize_for_deployment     | r2          |       100      |   36 398.52   |   22 624.13  |   0.9747   | 
| extreme_quality             | rmse        |       500      |   17 795.75   |   5 247.70   |   0.9939   | 

### 🏁 Wniosek
Do oceny jakości modeli regresyjnych wybrano trzy główne miary: **RMSE**, **MAE** oraz **R²**.

* **RMSE (Root Mean Squared Error)** pokazuje, jak duże są przeciętne odchylenia prognoz od wartości rzeczywistych – im mniejsza wartość, tym dokładniejsze przewidywania. Jest czuły na duże błędy, dlatego dobrze pokazuje stabilność modelu.
* **MAE (Mean Absolute Error)** mierzy średni błąd bezwzględny, mniej podatny na wartości odstające, przez co lepiej odzwierciedla ogólną dokładność w typowych przypadkach.
* **R² (Współczynnik determinacji)** informuje, jak dobrze model wyjaśnia zmienność danych – wartość bliska 1 oznacza bardzo dobrą jakość dopasowania niezależnie od skali danych.

Na podstawie tych metryk można zauważyć, że konfiguracja **`best_quality`** z limitem czasu **300 sekund** osiągnęła najlepsze wyniki.
Model ten zapewnia najwyższą precyzję prognoz przy umiarkowanym czasie treningu, dlatego został uznany za najlepszy kompromis między dokładnością a wydajnością.
