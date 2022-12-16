# Итоговый проект курса "Машинное обучение в бизнесе"
Автор: Юлия Полушина

Стек:
- ML: sklearn, catboost pandas, numpy
- API: flask
- Данные: UCI Dataset - Contraceptive Method Choice Data Set: https://archive.ics.uci.edu/ml/datasets/Contraceptive+Method+Choice

Задача: предсказать вероятность того, что женщина не использует контрацептивы. Бинарная классификация

Используемые признаки:
 1. Wife's age                     (numerical)
 2. Wife's education               (categorical)      1=low, 2, 3, 4=high
 3. Husband's education            (categorical)      1=low, 2, 3, 4=high
 4. Number of children ever born   (numerical)
 5. Wife's religion                (binary)           0=Non-Islam, 1=Islam
 6. Wife's now working?            (binary)           0=Yes, 1=No
 7. Husband's occupation           (categorical)      1, 2, 3, 4
 8. Standard-of-living index       (categorical)      1=low, 2, 3, 4=high
 9. Media exposure                 (binary)           0=Good, 1=Not good


Преобразования признаков: StandardScaler, CatBoostEncoder

Модель: CatBoost

### Клонируем репозиторий и создаем образ

```
$ git clone https://github.com/JuliPolu/Geekbrains_ML_business_project.git

$ cd Geekbrains_ML_business_project

$ docker build -t my_flask_app:v0.1 ./
```

### Запускаем контейнер

```
Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)

$ docker run -d -p 8181:8181 -v <your_local_path_to_pretrained_model>:/app/models/ my_flask_app:v0.1
```


### Переходим на localhost:8181
