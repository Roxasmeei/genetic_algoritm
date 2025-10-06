# 🚀 Быстрый старт: Island Model

## 📝 Для разработчиков

### 🟦 Разработчик 1: Ты работаешь с `classes/IslandModel.py`

**Твоя задача:** Управлять несколькими островами (популяциями)

**Что нужно сделать:**

1. **Инициализация** (`_initialize_islands`):
```python
def _initialize_islands(self):
    for _ in range(self.num_islands):
        island = GeneticAlgorithm(self.genetic_characteristics)
        self.islands.append(island)
    self.island_fitness_history = [[] for _ in range(self.num_islands)]
```

2. **Доступ к островам**:
```python
def get_population_entities(self, island_id: int):
    return self.islands[island_id].population.entities

def add_migrants(self, island_id: int, migrants: List[Entity]):
    self.islands[island_id].population.entities.extend(migrants)
```

3. **Основной цикл** (`start_algorithm`):
```python
for iteration in range(self.genetic_characteristics.max_iterations):
    # Шаг эволюции на каждом острове
    for island in self.islands:
        # Скопируй логику из GeneticAlgorithm.start_algorithm (один шаг)
        # Создание потомков, мутация, селекция
        pass
    
    # Миграция
    self._perform_migration(iteration)
    
    # Статистика
    self._update_best_entity()
    self._collect_statistics()
```

**Тестируй так:**
```python
island_model = IslandModel(num_islands=4, ..., migration_strategy=None)
island_model.start_algorithm()
```

---

### 🟩 Разработчик 2: Ты работаешь с `classes/MigrationManager.py`

**Твоя задача:** Управлять миграцией между островами

**Что нужно сделать:**

1. **Частота миграции**:
```python
def should_migrate(self, iteration: int) -> bool:
    return iteration > 0 and iteration % self.migration_interval == 0
```

2. **Случайные пары**:
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

3. **Выбор мигрантов** (3 стратегии):

**Elite:**
```python
sorted_entities = sorted(population_entities, 
                        key=lambda e: e.get_fitness(), 
                        reverse=True)
return sorted_entities[:num_migrants]
```

**Random:**
```python
return random.sample(population_entities, num_migrants)
```


---

## 🔗 Интеграция (когда оба готовы)

```python
# Шаг 1: Создай MigrationManager (Dev 2)
migration_manager = MigrationManager(
    migration_interval=100,
    num_migrants=3,
    migration_pairs=2,
    selection_strategy='elite'
)

# Шаг 2: Передай в IslandModel (Dev 1)
island_model = IslandModel(
    num_islands=4,
    genetic_characteristics=...,
    migration_strategy=migration_manager
)

# Шаг 3: Запусти
best_fitness, best_entity = island_model.start_algorithm(show_progression_type='plot')

print(f"Лучший результат: {best_fitness}")
```

---

## 📂 Структура проекта

```
genetic_algoritm/
├── classes/
│   ├── IslandModel.py          ← Dev 1
│   ├── MigrationManager.py     ← Dev 2
│   ├── GeneticA.py             ✓ готов
│   ├── Entity.py               ✓ готов
│   └── Population.py           ✓ готов
├── interfaces/
│   └── migration_interface.py  ✓ контракт
├── TASK_DIVISION.md            📖 детали
├── example_island_usage.py     💡 примеры
└── QUICKSTART.md               👈 ты здесь
```

---

