from enum import Enum
from abc import ABC, abstractmethod
from random import expovariate, uniform, randint

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