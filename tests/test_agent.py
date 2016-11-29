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
        agent = Agent(1, island_of_agents)

    def test_update_navigation(self):
        island_of_agents = IslandOfAgents(None)
        agent = Agent(1, island_of_agents)

        agent._heading = 'right'
        agent._coordinates = (0, 0)
        agent._update_navigation('moveForward')
        self.assertEquals(agent._coordinates, (1, 0))
        self.assertEquals(agent._heading, 'right')

        agent._update_navigation('moveBackward')
        self.assertEquals(agent._coordinates, (0, 0))
        self.assertEquals(agent._heading, 'right')

        agent._update_navigation('turnLeft')
        self.assertEquals(agent._heading, 'up')

        agent._update_navigation('moveForward')
        self.assertEquals(agent._coordinates, (0, 1))

        agent._update_navigation('turnLeft')
        self.assertEquals(agent._heading, 'left')
        agent._update_navigation('moveForward')
        self.assertEquals(agent._coordinates, (-1, 1))
        pass

    def test__move_towards(self):
        island_of_agents = IslandOfAgents(None)
        agent = Agent(1, island_of_agents)

        m = agent._move_toward((2, 2))
        print m
        m = agent._move_toward((2, 1))
        print m
        m = agent._move_toward((2, 0))
        print m
        m = agent._move_toward((0, 2))
        print m
        m = agent._move_toward((0, 1))
        print m

        pass

#     def test_scan_and_move__visible_payloads(self):
#         island_of_agents = IslandOfAgents(None)
#         agent = Agent(1, island_of_agents)
#         agent.scan_and_move()

#     def test_scan_and_move__has_payload(self):
#         island_of_agents = IslandOfAgents(None)
#         agent = Agent(1, island_of_agents)
#         agent.has_payload = True
#         agent.scan_and_move()

        pass

if __name__ == "__main__":
    unittest.main()
