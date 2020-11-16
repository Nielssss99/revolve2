from typing import List

from nca.core.abstract.configurations import PopulationConfiguration
from nca.core.actor.actors import Actors
from nca.core.ecology.population import Population


class PopulationManagement:

    def __init__(self, configuration: PopulationConfiguration = PopulationConfiguration()):
        super().__init__()
        self.configuration: PopulationConfiguration = configuration
        self.population: Population = None

    def populations(self) -> List[Population]:
        if self.population is None:
            raise Exception("PopulationManagement: Not existing population")
        return [self.population]

    def initialize(self, agents: Actors):
        assert(len(agents) > 0)
        self.population = Population(agents)

    def speciate(self):
        pass

    def to_json(self):
        return {
            'id': 1,
            'species': [
                self.population.to_json()
            ]
        }