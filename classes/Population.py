from typing import List
from classes.Entity import Entity


class Population:

    def __init__(self, entities: List[Entity]):
        self.entities = entities
    def get_entities(self):
        return self.entities
    def get_entity(self, index: int):
        return self.entities[index]
    def get_popultion_fitness(self):
        return max(entity.get_fitness() for entity in self.entities)
    def get_distant_entity(self, entity: Entity):
        pass
