#from Person import DepartmentOfHealth
from abc import ABC, abstractmethod
from random import randint
# from __future__ import annotations

min_i, max_i = 0, 100
min_j, max_j = 0, 100
    

class State(ABC):
    def __init__(self, person): 
        self.person = person
        
    @abstractmethod
    def day_actions(self): pass

    @abstractmethod
    def night_actions(self): pass

    @abstractmethod
    def interact(self, other): pass

    @abstractmethod
    def get_infected(self, virus): pass


class Healthy(State):
    def day_actions(self):
        # different for CommunityPerson?!
        self.person.position = (randint(min_j, max_j), randint(min_i, max_i))

    def night_actions(self):
        self.person.position = self.person.home_position

    # def interact(self, other: Person): pass
    def interact(self, other): pass

    def get_infected(self, virus):
        if virus.get_type() not in self.person.antibody_types:
            self.person.virus = virus
            self.person.set_state(AsymptomaticSick(self.person))


class AsymptomaticSick(State):
    DAYS_SICK_TO_FEEL_BAD = 2
    
    def __init__(self, person):
        super().__init__(person)
        self.days_sick = 0

    def day_actions(self):
        # different for CommunityPerson?!
        self.person.position = (randint(min_j, max_j), randint(min_i, max_i))

    def night_actions(self):
        self.person.position = self.person.home_position
        if self.days_sick == AsymptomaticSick.DAYS_SICK_TO_FEEL_BAD:
            self.person.set_state(SymptomaticSick(self.person))
        self.days_sick += 1

    # def interact(self, other: Person):
    def interact(self, other):
        other.get_infected(self.person.virus)

    def get_infected(self, virus): 
        other.get_infected(self.person.virus)
        
class DepartmentOfHealth:
    def __init__(self):
        pass
    
    def monitor_situation(self):
        pass
    
    def issue_policy(self):
        pass
    
    def hospitalize(self, person):
        pass

class SymptomaticSick(State):
    def day_actions(self):
        self.person.progress_disease()
        
        if self.person.is_life_threatening_condition():
            health_dept = DepartmentOfHealth()
            health_dept.hospitalize(self.person)

        if self.person.is_life_incompatible_condition():
            self.person.set_state(Dead(self.person))
        
    def night_actions(self):
        # try to fight the virus
        self.person.fight_virus()
        if self.person.virus.strength <= 0:
            self.person.set_state(Healthy(self.person))
            self.person.antibody_types.add(self.person.virus.get_type())
            self.person.virus = None

    # def interact(self, other: Person):
    def interact(self, other): 
        other.get_infected(self.person.virus)

    def get_infected(self, virus): pass

class Dead(State):
    def day_actions(self): pass

    def night_actions(self): pass

    def interact(self, other): pass

    def get_infected(self, virus): pass