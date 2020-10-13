import unittest
import random
from Person import DefaultPerson
from Infectable import Cholera, SeasonalFluVirus, SARSCoV2
from State import SymptomaticSick, AsymptomaticSick, Healthy, Dead

from random import randint

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

        
#Tasks 5-6 (compulsory)
class TestSymptomaticState(unittest.TestCase):
    
    def setUp(self):
        self.person = create_persons(0, 100, 0, 100, 1) #someone from our city(100x100)
        
    #test_5

    def test_healthy(self):
        
        virus_type = SARSCoV2(strength=2.0)
        self.person[0].get_infected(virus_type)
        self.person[0].set_state(SymptomaticSick(self.person[0]))
        self.person[0].virus.strength = -1
        self.person[0].night_actions()
        
        self.assertIsInstance(self.person[0].state, Healthy)
        
  
    #test_6
    
    def test_dead(self):

        self.person[0].get_infected(SARSCoV2())
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
        self.person = create_persons(0, 100, 0, 100, 1) #someone from our city(100x100)
        
    def test_antibody(self):
        
        
        virus_type = SARSCoV2(strength=2.0)
        self.person[0].get_infected(virus_type)
        self.person[0].set_state(SymptomaticSick(self.person[0]))
        virus_type_prove = self.person[0].virus.get_type()
        self.person[0].virus.strength = -1
        self.person[0].night_actions()
        antibody = self.person[0].antibody_types
        assert virus_type_prove in antibody, "Antibody from virus type {} was not added".format(virus_type_prove)            

        
if __name__ == "__main__":
	unittest.main()