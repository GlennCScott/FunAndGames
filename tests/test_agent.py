'''
Created on Nov 28, 2016

@author: gscott
'''
import unittest

from island_of_agents import IslandOfAgents
from agent import Agent


class TestAgent(unittest.TestCase):

    def test_agent(self):
        island_of_agents = IslandOfAgents(None)
        agent = Agent(1, 1, island_of_agents)

    def test_update_coordinates(self):
        island_of_agents = IslandOfAgents(None)
        agent = Agent(1, 1, island_of_agents)

        agent._heading = 'right'
        agent._coordinates = (0, 0)
        agent._update_coordinates('moveForward')
        self.assertEquals(agent._coordinates, (1, 0))
        self.assertEquals(agent._heading, 'right')

        agent._update_coordinates('moveBackward')
        self.assertEquals(agent._coordinates, (0, 0))
        self.assertEquals(agent._heading, 'right')

        agent._update_coordinates('turnLeft')
        self.assertEquals(agent._heading, 'up')

        agent._update_coordinates('moveForward')
        self.assertEquals(agent._coordinates, (0, 1))

        agent._update_coordinates('turnLeft')
        self.assertEquals(agent._heading, 'left')
        agent._update_coordinates('moveForward')
        self.assertEquals(agent._coordinates, (-1, 1))

if __name__ == "__main__":
    unittest.main()
