# Разделение задач: Параллельный генетический алгоритм с миграцией

## Общая архитектура

```
┌─────────────────────────────────────────────────────────┐
│              IslandModel (Разработчик 1)                │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │Island 0│  │Island 1│  │Island 2│  │Island 3│        │
│  │  (GA)  │  │  (GA)  │  │  (GA)  │  │  (GA)  │        │
│  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘        │
│      │           │           │           │              │
│      └───────────┴───────────┴───────────┘              │
│                     │                                    │
│                     ▼                                    │
│      ┌──────────────────────────────────┐               │
│      │   MigrationManager (Разработчик 2)│               │
│      │  - Случайный выбор пар           │               │
│      │  - Выбор мигрантов                │               │
│      │  - Частота миграции               │               │
│      └──────────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

---

## 🟦 РАЗРАБОТЧИК 1: Island Model (Управление популяциями)

### Файл: `classes/IslandModel.py`

### Ваши задачи:

#### 1. Инициализация островов (`_initialize_islands`)
- Создать `self.num_islands` экземпляров `GeneticAlgorithm`
- Каждый остров — это независимая эволюция
- Инициализировать структуры для хранения статистики

#### 2. Методы доступа к островам
- `get_population_entities(island_id)` — получить все особи с острова
- `add_migrants(island_id, migrants)` — добавить мигрантов на остров


#### 3. Основной цикл эволюции (`start_algorithm`)
- Для каждой итерации:
  - Выполнить **один шаг** эволюции на каждом острове
  - Вызвать `_perform_migration(iteration)`
  - Обновить лучшую особь (`_update_best_entity`)
  - Собрать статистику (`_collect_statistics`)

#### 4. Интеграция миграции (`_perform_migration`)
```python
if not self.migration_strategy.should_migrate(iteration):
    return

pairs = self.migration_strategy.get_random_migration_pairs(
    self.num_islands, 
    self.migration_strategy.migration_pairs
)

for source_id, target_id in pairs:
    source_entities = self.get_population_entities(source_id)
    migrants = self.migration_strategy.select_migrants(
        source_entities, 
        self.migration_strategy.num_migrants
    )
    self.add_migrants(target_id, migrants)
```

#### 5. Статистика и визуализация
- `_update_best_entity()` — найти лучшую особь по всем островам
- `_collect_statistics()` — собрать fitness с каждого острова
- `plot_progression()` — построить график с линиями для каждого острова
- `get_statistics()` — вернуть словарь со статистикой

### Зависимости:
- ✅ `GeneticAlgorithm` — уже существует
- ✅ `Entity` — уже существует
- ✅ `Population` — уже существует
- ⏳ `MigrationManager` — создаёт Разработчик 2 (вы используете через интерфейс)

### Важно:
- Вы **НЕ** реализуете логику выбора пар и мигрантов
- Вы **ТОЛЬКО** вызываете методы `migration_strategy`
- Можете тестировать с `migration_strategy=None` (без миграции)

---

## 🟩 РАЗРАБОТЧИК 2: Migration Manager (Управление миграцией)

### Файл: `classes/MigrationManager.py`

### Ваши задачи:

#### 1. Определение частоты миграции (`should_migrate`)
```python
def should_migrate(self, iteration: int) -> bool:
    return iteration > 0 and iteration % self.migration_interval == 0
```

#### 2. Случайный выбор пар островов (`get_random_migration_pairs`)
- Выбрать `num_pairs` случайных пар островов
- Убедиться, что `source != target`
- Пример: для 4 островов → `[(0, 2), (1, 3)]`

```python
def get_random_migration_pairs(self, num_islands: int, num_pairs: int):
    pairs = []
    for _ in range(num_pairs):
        source = random.randint(0, num_islands - 1)
        target = random.randint(0, num_islands - 1)
        while target == source:
            target = random.randint(0, num_islands - 1)
        pairs.append((source, target))
    return pairs
```

#### 3. Выбор мигрантов (`select_migrants`)

Реализовать 3 стратегии:

##### a) **Elite** (Лучшие)
```python
sorted_entities = sorted(population_entities, 
                        key=lambda e: e.get_fitness(), 
                        reverse=True)
return sorted_entities[:num_migrants]
```

##### b) **Random** (Случайные)
```python
return random.sample(population_entities, num_migrants)
```

##### c) **Diverse** (Разнообразные)
- Выбрать особей, максимально отличающихся друг от друга
- Использовать жадный алгоритм:
  1. Выбрать случайную первую особь
  2. Каждую следующую выбирать так, чтобы она была максимально далека от уже выбранных

```python
selected = [random.choice(population_entities)]
remaining = [e for e in population_entities if e not in selected]

while len(selected) < num_migrants:
    best_candidate = None
    best_min_distance = -1
    
    for candidate in remaining:
        # Минимальное расстояние до уже выбранных
        min_dist = min(self._calculate_distance(candidate, s) 
                      for s in selected)
        if min_dist > best_min_distance:
            best_min_distance = min_dist
            best_candidate = candidate
    
    selected.append(best_candidate)
    remaining.remove(best_candidate)

return selected
```

### Зависимости:
- ✅ `Entity` — уже существует
- ⏳ `IslandModel` — создаёт Разработчик 1 (но вы НЕ зависите от него напрямую)

### Важно:
- Вы **НЕ** работаете с островами напрямую
- Вы **ТОЛЬКО** возвращаете данные через методы
- Можете тестировать отдельно с тестовыми данными

---

## 📋 Интерфейс взаимодействия

### Файл: `interfaces/migration_interface.py`

Это контракт между двумя разработчиками. **НЕ ИЗМЕНЯЙТЕ** его без согласования!

**Разработчик 1** использует:
- `should_migrate(iteration)`
- `get_random_migration_pairs(num_islands, num_pairs)`
- `select_migrants(population_entities, num_migrants)`

**Разработчик 2** реализует эти методы в `MigrationManager`.

---