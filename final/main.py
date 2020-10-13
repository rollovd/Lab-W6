import unittest
import random

from random import expovariate, uniform, randint

from abc import ABC, abstractmethod

from enum import Enum

class Infectable(ABC):
    def __init__(self, strength=1.0, contag=1.0):
        # contag is for contagiousness so we have less typos
        self.strength = strength
        self.contag = contag

    @abstractmethod
    def cause_symptoms(self, person):
        pass
    
    
class SeasonalFluVirus(Infectable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name= 'SeasonalFluVirus'

    def cause_symptoms(self, person):
        person.temperature += 0.25

    def get_type(self):
        return InfectableType.SeasonalFlu

   
    
class SARSCoV2(Infectable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name= 'SARSCoV2'

    def cause_symptoms(self, person):
        person.temperature += 0.5

    def get_type(self):
        return InfectableType.SARSCoV2


class Cholera(Infectable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name= 'Cholera'

    def cause_symptoms(self, person):
        person.water -= 1.0

    def get_type(self):
        return InfectableType.Cholera
    

class InfectableType(Enum):
    SeasonalFlu = 1
    SARSCoV2 = 2
    Cholera = 3

    
def get_infectable(infectable_type: InfectableType):
    if InfectableType.SeasonalFlu == infectable_type:
        return SeasonalFluVirus(strength=expovariate(10.0), contag=expovariate(10.0))
    
    elif InfectableType.SARSCoV2 == infectable_type:
        return SARSCoV2(strength=expovariate(2.0), contag=expovariate(2.0))
    
    elif InfectableType.Cholera == infectable_type:
        return Cholera(strength=expovariate(2.0), contag=expovariate(2.0))
    
    else:
        raise ValueError()

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

    def get_infected(self, other): pass

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


def create_persons(min_j, max_j, min_i, max_i, n_persons):
    min_age, max_age = 1, 90
    min_weight, max_weight = 30, 120
    persons = [
        DefaultPerson(
            home_position=(randint(min_j, max_j), randint(min_i, max_i)),
            age=randint(min_age, max_age),
            weight=randint(min_weight, max_weight),
        )
        for i in range(n_persons)
    ]
    return persons

#Tasks 1-2 (compulsory)
class TestVirusSpread(unittest.TestCase):
    
    def setUp(self):
        self._position = (0, 0)
        
        self._person_symptomatic = self._create_sick_person()
        self._person_asymptomatic = self._create_sick_person(symptomatic=False)
        
        self._default_person_1 = self._create_healthy_person()
        self._default_person_2 = self._create_healthy_person()
        self._default_person_3 = self._create_healthy_person(default_position=False)   

    def tearDown(self):
    	self._default_person_1.set_state(Healthy(self._default_person_1))
    	self._default_person_2.set_state(Healthy(self._default_person_2))
        
    def _get_infection(self):
        infection = random.choice([Cholera(), SeasonalFluVirus(), SARSCoV2()])
        return infection
    
    def _create_sick_person(self, symptomatic=True):
        person = DefaultPerson(
            home_position=self._position, 
            virus=self._get_infection()
        )
        
        _ = person.set_state(SymptomaticSick(person)) if symptomatic \
                            else person.set_state(AsymptomaticSick(person))
        return person
    
    def _create_healthy_person(self, default_position=True):
        return DefaultPerson(home_position=self._position) if default_position \
                                else DefaultPerson(home_position=(0, 1))
    
    @staticmethod
    def _check_interaction(sick_person: DefaultPerson, healthy_person: DefaultPerson):
        if sick_person is not healthy_person and sick_person.is_contacting(healthy_person):
            sick_person.interact(healthy_person)
            
        return healthy_person
    
    def test_get_infected(self): 
    	symptomatic_interact_person_1 = self._check_interaction(self._person_symptomatic, self._default_person_1)
    	self.assertIsInstance(symptomatic_interact_person_1.state, AsymptomaticSick)

    	asymptomatic_interact_person_2 = self._check_interaction(self._person_asymptomatic, self._default_person_2)
    	self.assertIsInstance(asymptomatic_interact_person_2.state, AsymptomaticSick)

    	non_interact = self._check_interaction(self._person_symptomatic, self._default_person_3)
    	self.assertIsInstance(non_interact.state, Healthy)

    def test_healthy_contact(self):
    	self._default_person_1.interact(self._default_person_2)

    	self.assertIsInstance(self._default_person_1.state, Healthy)
    	self.assertIsInstance(self._default_person_2.state, Healthy)



#Tasks 3-4 (compulsory)
class TestInfectedAntibodies(unittest.TestCase):
    
    def setUp(self):
        self._position = (0, 0)
        
        self._person_with_cholera_antibodies = self._create_person_with_antibodies(Cholera)
        self._person_with_covid_antibodies = self._create_person_with_antibodies(SARSCoV2)
        self._person_with_flu_antibodies = self._create_person_with_antibodies(SeasonalFluVirus)

        self._sick_person = self._create_sick_person(random.choice([True, False]))
        
        self._infected_person = self._create_sick_person(False)


    def tearDown(self):
        self._infected_person = self._create_sick_person(False)

    def _get_infection(self):
        infection = random.choice([Cholera(), SeasonalFluVirus(), SARSCoV2()])
        return infection

    def _create_sick_person(self, symptomatic=True):
        person = DefaultPerson(
            home_position=self._position, 
            virus=self._get_infection()
        )
        
        _ = person.set_state(SymptomaticSick(person)) if symptomatic \
                            else person.set_state(AsymptomaticSick(person))
        return person

    def _create_person_with_antibodies(self, antibodies_type):
        person = DefaultPerson(
            home_position=self._position, 
        )
        
        person.antibody_types.add(antibodies_type)

        return person
    
    def test_infected_person_and_antibodies(self):
        self.assertIsInstance(self._person_with_cholera_antibodies.state, Healthy)
        if isinstance(self._sick_person.virus, Cholera):
            self._person_with_cholera_antibodies.interact(self._sick_person)
            self.assertIsInstance(self._person_with_cholera_antibodies.state, Healthy)
        if isinstance(self._sick_person.virus, SARSCoV2):
            self._person_with_covid_antibodies.interact(self._sick_person)
            self.assertIsInstance(self._person_with_covid_antibodies.state, Healthy)
        if isinstance(self._sick_person.virus, SeasonalFluVirus):
            self._person_with_flu_antibodies.interact(self._sick_person)
            self.assertIsInstance(self._person_with_flu_antibodies.state, Healthy)

    def test_infected_person_change_state(self):
        for day in range(3):
            self.assertIsInstance(self._infected_person.state, AsymptomaticSick)
            self._infected_person.state.day_actions()
            self._infected_person.state.night_actions()
        self.assertIsInstance(self._infected_person.state, SymptomaticSick)

        

    

#Tasks 5-6 (compulsory)
class TestSymptomaticState(unittest.TestCase):
    
    def setUp(self):
        self.person = create_persons(0, 100, 0, 100, 1)

    def _get_infection(self):
        infection = random.choice([Cholera(), SeasonalFluVirus(), SARSCoV2()])
        return infection
        
    #test_5
    def test_healthy(self):
        virus_type = self._get_infection()
        self.person[0].get_infected(virus_type)
        self.person[0].set_state(SymptomaticSick(self.person[0]))
        self.person[0].virus.strength = -1
        self.person[0].night_actions()
        
        self.assertIsInstance(self.person[0].state, Healthy)
        
  
    #test_6
    def test_dead(self):
        self.person[0].get_infected(self._get_infection())
        self.person[0].set_state(SymptomaticSick(self.person[0]))
        self.person[0].temperature = self.person[0].MAX_TEMPERATURE_TO_SURVIVE + 1
        self.person[0].day_actions()
        self.assertIsInstance(self.person[0].state, Dead)
        self.person[0].set_state(Healthy(self.person[0]))
        self.person[0].get_infected(Cholera())
        self.person[0].set_state(SymptomaticSick(self.person[0]))
        self.person[0].water  = self.person[0].LOWEST_WATER_PCT_TO_SURVIVE * self.person[0].weight - 1
        self.person[0].day_actions()
        self.assertIsInstance(self.person[0].state, Dead)
        
#Task 1 (optional)
class TestSymptoms(unittest.TestCase):
    
    def setUp(self):
        age = 40
        weight=80
         
        self._sick_person_flu = DefaultPerson(
            age=age, 
            weight=weight,
            virus=SeasonalFluVirus(strength=1.0)
        )

        self._sick_person_cholera = DefaultPerson(
            age=age,
            weight=weight,
            virus=Cholera(strength=1.0)
        )
        
    @staticmethod
    def simulation_person(person: DefaultPerson, days: int = 10, flu=True):
        
        characteristics = []
        
        for day in range(days):
            person.day_actions()
            person.night_actions()

            day_num = day
            temperature = person.temperature
            water = person.water
            
            current_value = temperature if flu else water
            characteristics.append(current_value)
            
        return characteristics
    
    def test_temperature_increased(self):
        temperature = self.simulation_person(self._sick_person_flu)
        for i in range(len(temperature) - 1):
            current_day = temperature[i]
            future_day = temperature[i+1]
            
            self.assertGreaterEqual(future_day, current_day)
            
    def test_water_decreased(self):
        water = self.simulation_person(self._sick_person_cholera)
        for i in range(len(water) - 1):
            current_day = water[i]
            future_day = water[i+1]
            
            self.assertLessEqual(future_day, current_day)


#Task 3 (optional)
class TestAntibodyState(unittest.TestCase):
    
    def setUp(self):
        self.person = create_persons(0, 100, 0, 100, 1)
        
    def _get_infection(self):
        infection = random.choice([Cholera(), SeasonalFluVirus(), SARSCoV2()])
        return infection
    
    def test_antibody(self):
        virus_type = self._get_infection()
        self.person[0].get_infected(virus_type)
        self.person[0].set_state(SymptomaticSick(self.person[0]))
        virus_type_prove = self.person[0].virus.get_type()
        self.person[0].virus.strength = -1
        self.person[0].night_actions()
        antibody = self.person[0].antibody_types
        assert virus_type_prove in antibody, "No antibody to virus type {}".format(virus_type_prove)            

        
if __name__ == "__main__":
	unittest.main()
