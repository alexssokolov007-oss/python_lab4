# Лабораторная работа №4. Казино и гуси — симуляция

## Цель проекта
Учебный проект-симуляция казино с игроками и гусями, показывающий работу пользовательских коллекций, наследования, магических методов и псевдослучайных событий.

## Структура проекта
lab4-main/
├── src/
│   ├── __init__.py
│   ├── collections_ext/
│   │   ├── __init__.py
│   │   ├── casino_balance.py
│   │   ├── goose_collection.py
│   │   └── player_collection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chip.py
│   │   ├── goose.py
│   │   └── player.py
│   ├── casino.py
│   ├── constants.py
│   ├── main.py
│   └── simulation.py
├── tests/
│   ├── __init__.py
│   ├── test_casino_balance.py
│   ├── test_casino.py
│   ├── test_chip.py
│   ├── test_goose.py
│   ├── test_main.py
│   ├── test_player.py
│   └── test_simulation.py
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── README.md
├── requirements.txt
└── uv.lock

## Используемые технологии
- Python 3.12+.
- pytest, pytest-cov для тестирования и покрытия.

## Реализованное
- Есть базовый класс Goose и два наследника (WarGoose, HonkGoose) с отличающимся поведением.
- Пользовательские коллекции: списковые (PlayerCollection, GooseCollection с поддержкой срезов/индексации/итерации) и словарная (CasinoBalance с логированием изменений).
- Магические методы по предметной области: Goose.__add__ (объединение стаи), HonkGoose.__call__, Chip.__add__, а также __contains__/__repr__ в коллекциях.
- Псевдослучайная симуляция с набором событий (ставка, бонус, атака, крик, кража, слияние гусей, паника).
- Логи событий и изменения балансов выводятся в консоль.

## Принятые решения и допущения
- Балансы игроков и доходы гусей хранятся раздельно через CasinoBalance.
- При одинаковом seed симуляция воспроизводима (используется random.Random(seed)).

## Тестирование
- 24 модульных теста с покрытием 100% всей функциональности.
- tests/ проверяют коллекции, модели, события казино, симуляцию, обработку ввода в main.

## Запуск тестов и программы
Создать и активировать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```
ИЛИ
```bash
venv\Scripts\activate  # Windows
```

Установить зависимости:
```bash
pip install -r requirements.txt
```

Запуск тестов:
```bash
python3 -m pytest
```

Запуск программы:
```bash
python -m src.main
```
