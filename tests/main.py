import unittest
import random
from Person import DefaultPerson
from Infectable import Cholera, SeasonalFluVirus, SARSCoV2
from State import SymptomaticSick, AsymptomaticSick, Healthy

class TestVirusSpread(unittest.TestCase):
    
    def setUp(self):
        self._position = (0, 0)
        
        self._person_symptomatic = self._create_sick_person()
        self._person_asymptomatic = self._create_sick_person(symptomatic=False)
        
        self._default_person_1 = self._create_healthy_person()
        self._default_person_2 = self._create_healthy_person()
        self._default_person_3 = self._create_healthy_person(default_position=False)       
        
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
    	symptomatic_interact = self._check_interaction(self._person_symptomatic, self._default_person_1)
    	self.assertIsInstance(symptomatic_interact.state, AsymptomaticSick)

    	asymptomatic_interact = self._check_interaction(self._person_asymptomatic, self._default_person_2)
    	self.assertIsInstance(asymptomatic_interact.state, AsymptomaticSick)

    	non_interact = self._check_interaction(self._person_symptomatic, self._default_person_3)
    	self.assertIsInstance(non_interact.state, Healthy)

    def test_healthy_contact(self):
    	self._default_person_1.interact(self._default_person_2)

    	self.assertIsInstance(self._default_person_1.state, Healthy)
    	self.assertIsInstance(self._default_person_2.state, Healthy)

if __name__ == "__main__":
	unittest.main()