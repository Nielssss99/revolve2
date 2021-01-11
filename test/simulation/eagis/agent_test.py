import unittest

import numpy as np
import matplotlib.pyplot as plt

from nca.core.abstract.configurations import InitializationConfiguration
from nca.core.actor.individual_factory import ActorFactory
from nca.core.ecology.population import Population
from nca.core.genome.genotype import Genotype
from nca.core.genome.operators.initialization import UniformInitialization
from nca.core.genome.representations.valued_representation import ValuedRepresentation
from simulation.AEGIS.animal import Animal
from simulation.AEGIS.decision_model import decide_all
from simulation.AEGIS.scape_environment import ScapeEnvironment

import imageio


class AgentAEGIS(unittest.TestCase):

    def test_agent(self):
        n_individuals = 60

        genotype: Genotype = Genotype(
            ValuedRepresentation(UniformInitialization(InitializationConfiguration(0.0, 1.0))))
        individual_factory = ActorFactory(genotype, Animal)

        individuals = individual_factory.create(n_individuals)

        scape_env = ScapeEnvironment(20, 20, 200, Population(individuals))

        done_n = [False for _ in range(len(scape_env.population.individuals))]
        ep_reward = 0

        filenames = []
        obs_n = scape_env.reset()

        print("start loop")
        for step in range(100):  # while not all(done_n):
            scape_env.step(decide_all(scape_env.population))
            if step % 3 == 0:
                filenames.append(scape_env.render())

        scape_env.close()

        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))

        imageio.mimsave("../../../log/aegis/animation.gif", images)

        plt.close()

        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('generations')
        ax1.set_ylabel('count', color=color)
        ax1.plot(scape_env.history['flora_count'], 'red')
        ax1.plot(scape_env.history['animal_count'], 'blue')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.legend(labels=["Flora count", 'Animalia count'])

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        color = 'tab:blue'
        ax2.set_ylabel('energy', color=color)  # we already handled the x-label with ax1
        plt.plot(scape_env.history['flora_energy'], 'orange')
        plt.plot(scape_env.history['animal_energy'], 'lightblue')
        ax2.tick_params(axis='y', labelcolor=color)
        plt.legend(labels=['Flora energy', 'Animalia energy'])
        fig.tight_layout()  # otherwise the right y-label is slightly clipped

        plt.show()
