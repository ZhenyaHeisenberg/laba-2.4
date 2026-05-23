<h1>laba-2.3</h1>

<h2>Очередь задач: итераторы и генераторы</h2>
<h2>Описание проекта</h2>

<p>Реализация ленивой очереди задач `TaskQueue` с поддержкой:</p>
<ul>
    <li>- повторного обхода</li>
    <li>- ленивых фильтров по статусу и приоритету</li>
</ul>
<h2>Архитектура</h2>
<pre>
src/
├── main.py                             # Точка входа
├── cli.py                              # Интерфейс командной строки
├── contracts/
│   ├── message.py                      # Message
│   └── message_source.py               # MessageSource
├── inbox/
│   ── core.py                          # Ядро с проверкой контракта
├── models/
│   ├── task.py # Класс Task (из лаб.2)
│   ├── task_queue.py                   # Очередь задач
│   └── generator.py                    # Генератор задач
├── sources/
│   ├── repository.py # Реестр источников
│   ├── stdin.py                        # Чтение из STDIN
│   ├── json.py                         # Чтение из JSONL файлов
│   └── api.py                          # API-заглушка
└── common/
    └── config.py                       # Логирование
</pre>

<h2>TaskQueue</h2>

Основная структура данных для ленивой обработки задач.

<h3>Принцип работы</h2>
<ul>
    <li>- Задачи не хранятся в памяти, а генерируются при итерации</li>
    <li>- Буфер сохраняет пройденные задачи для повторного обхода</li>
    <li>- Фильтры возвращают новые очереди, а не изменяют исходную</li>
</ul>

<h3>Показать доступные плагины</h3>
python -m src plugins

<h3>Генерация задач из API</h3>
python -m src read --api 10

<h3>Фильтрация по содержимому</h3>
python -m src read --api 20 --contains "5"

<h3>Чтение из JSONL файла</h3>
python -m src read --jsonl data.jsonl

<h3>Чтение из STDIN</h3>
echo "1:title:desc:author:message:created:3" | python -m src read --stdin

<h2>Покрытие тестами</h2>
`python -m pytest --cov=src --cov-report=term-missing`

<pre>
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src\models\generator.py       12      0   100%
src\models\task_queue.py      46      1    98%   23
--------------------------------------------------------
TOTAL                         58      1    98%
Required test coverage of 80.0% reached. Total coverage: 98.28%
</pre>

<h2>Отладка</h2>
<p>Код покрыт тестами на 98%, а так же лоиггирует ошибки, связанные с приёмом задач неверного формата</p>