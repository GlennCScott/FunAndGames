'''
Created on Nov 28, 2016

@author: gscott
'''
import unittest
from island_of_agents import IslandOfAgents


class Test(unittest.TestCase):

    def test_create_sim(self):
        island = IslandOfAgents(None)
        island.create_sim("Test1")

if __name__ == "__main__":
    unittest.main()
