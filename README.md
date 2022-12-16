# Итоговый проект курса "Машинное обучение в бизнесе"
Автор: Юлия Полушина

Стек:
- ML: sklearn, pandas, numpy
- API: flask
- Данные: UCI Dataset - Contraceptive Method Choice Data Set: https://archive.ics.uci.edu/ml/datasets/Contraceptive+Method+Choice

Задача: предсказать вероятность того, что женщина не использует контрацептивы. Бинарная классификация

Используемые признаки:
Wife_age
Wife_education
Husband_education
Children
Religion
Working
Husband_Work
Standard-of-living
Media_exposure

Преобразования признаков: StandardScaler, CatBoostEncoder

Модель: CatBoost

### Клонируем репозиторий
```
$ git clone https://github.com/shatandv/GB-ML-Business-Project.git ml_api_project
$ cd ml_api_project
```

### Запускаем контейнер

```
$ docker-compose up -d
```

### Можно отправить POST-запрос на 127.0.0.1:8180/predict c полями, указанными в "Признаках"
