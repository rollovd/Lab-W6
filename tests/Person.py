from abc import ABC, abstractmethod
from State import Healthy

class Person(ABC):
    MAX_TEMPERATURE_TO_SURVIVE = 44.0
    LOWEST_WATER_PCT_TO_SURVIVE = 0.4
    
    LIFE_THREATENING_TEMPERATURE = 40.0
    LIFE_THREATENING_WATER_PCT = 0.5
    
    def __init__(self, home_position=(0, 0), age=30, weight=70, virus=None, name=None):
        self.name = name
        self.age = age
        self.weight = weight
        self.temperature = 36.6
        self.water = 0.6 * self.weight
        self.virus = virus
        self.antibody_types = set()
        self.home_position = home_position
        self.position = home_position
        self.state = Healthy(self)
    
    @abstractmethod
    def day_actions(self): pass

    @abstractmethod
    def night_actions(self): pass

    @abstractmethod
    def interact(self, other): pass

    @abstractmethod
    def get_infected(self, virus): pass
    
    def is_contacting(self, other):
        return self.position == other.position
    
    @abstractmethod
    def fight_virus(self): pass

    @abstractmethod
    def progress_disease(self): pass

    @abstractmethod
    def set_state(self, state): pass
    
    def is_life_threatening_condition(self):
        return self.temperature >= Person.LIFE_THREATENING_TEMPERATURE or \
           self.water / self.weight <= Person.LIFE_THREATENING_WATER_PCT
    
    def is_life_incompatible_condition(self):        
        return self.temperature >= Person.MAX_TEMPERATURE_TO_SURVIVE or \
            self.water / self.weight <= Person.LOWEST_WATER_PCT_TO_SURVIVE


class DefaultPerson(Person):
    
    def day_actions(self):
        self.state.day_actions()

    def night_actions(self):
        self.state.night_actions()

    def interact(self, other):
        self.state.interact(other)

    def get_infected(self, virus):
        self.state.get_infected(virus)
    
    def is_contacting(self, other):
        return self.position == other.position
    
    def fight_virus(self):
        if self.virus:
            self.virus.strength -= (3.0 / self.age)
        
    def progress_disease(self):
        if self.virus:
            self.virus.cause_symptoms(self)

    def set_state(self, state):
        self.state = state

class CommunityPerson(Person):

    def __init__(self, community_position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.community_position = community_position
    
    def day_actions(self):
        self.state.day_actions()

    def night_actions(self):
        self.state.night_actions()

    def interact(self, other):
        self.state.interact(other)

    def get_infected(self, virus):
        self.state.get_infected(virus)
    
    def is_contacting(self, other):
        return self.position == other.position
    
    def fight_virus(self):
        if self.virus:
            self.virus.strength -= (3.0 / self.age)
        
    def progress_disease(self):
        if self.virus:
            self.virus.cause_symptoms(self)

    def set_state(self, state):
        self.state = state