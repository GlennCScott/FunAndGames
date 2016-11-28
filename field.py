'''
Created on Nov 27, 2016

@author: gscott
'''
from payload import Payload
from agent import Agent


class Field(object):
    @staticmethod
    def parse_json(json_text):
        home = (2, 0)
        agents = []
        payloads = []
        return home, agents, payloads

    def __init__(self, home=None, agents=None, payloads=None):

        self.agents = map(lambda coord: Agent(coord), agents)
        self.payloads = map(lambda coord: Payload(coord), payloads)
        self.home = home[0]
        return

    def solve(self):
        # For each agent, compute the distance to each payload

        strategies = self.strategise()
        for strategy in strategies:
            agent = strategy[0]
            path = agent.plot_path(strategy[1])
            print path

        pass

    def strategise(self):
        agent_strategies = []
        exclude = None
        for agent in self.agents:
            best_payload = agent.get_best_payload(self.payloads, exclude)
            agent_strategies.append((agent, best_payload))

        return agent_strategies

    def __repr__(self):
        result = ""

        for y in range(0, 10):
            result += '|'
            for x in range(0, 10):
                if len(filter(lambda agent: agent.is_at(x, y), self.agents)) > 0:
                    result += 'A'
                elif len(filter(lambda payload: payload.is_at(x, y), self.payloads)) > 0:
                    result += 'P'
                elif self.home[0] == x and self.home[1] == y:
                    result += 'H'
                else:
                    result += '.'

            result += '|\n'

        return result