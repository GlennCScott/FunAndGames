import sys
import unittest
from island_of_agents import IslandOfAgents


class Test(unittest.TestCase):
    server = None

    def test_create_sim(self):
        island = IslandOfAgents(None)
        island.create_sim("HW1")

    def test_runner(self):
        sim = IslandOfAgents(None)
        sim.create_sim('HW1')
        sim.start_sim()
        sim.run(10)

    def test_runner_server(self):
        sim = IslandOfAgents(Test.server)
        sim.create_sim('HW1')
        sim.start_sim()
        sim.run(10)

if __name__ == "__main__":
    Test.server = sys.argv[1]
    unittest.main()
