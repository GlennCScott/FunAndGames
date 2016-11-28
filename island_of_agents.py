'''
Created on Nov 28, 2016

@author: Glenn Scott
'''
import requests
import pprint
from agent import Agent


class IslandOfAgents(object):

    def __init__(self, server, debugging=False):
        self.agents = []
        self.server = server
        self.simulation_id = None
        self.debugging = debugging
        return

    def create_sim(self, name):
        assert name in ("Test1", "Test2")

        response = None
        if self.server:
            response = requests.post(self.server + "/simulations/create",
                                     json={'env_name': name},
                                     headers={'Content-Type': 'application/json'})
        else:
            response = {'msg': 'Simulation "%s" created with environment "%s"!' % ("foo", name),
                        'status': 200,
                        'simulationId': 1,
                        'simulationData': {'id': 1, 'time': 0, 'NumAgents': 3, 'Statistics': 0, 'SimPoints': 0}
                        }

        self.simulation_id = response['simulationId']
        data = response['simulationData']
        numAgents = data['NumAgents']

        self.agents = []
        for agent_id in range(numAgents):
            self.agents.append(Agent(agent_id, self.simulation_id, self))

        return

    def start_sim(self, simulation_id):
        result = None
        if self.server:
            result = requests.put(self.server + '/simulations/%s/start' % simulation_id)
        else:
            result = {'msg': 'Simulation <sid> restarted!' % (self.simulation_id),
                      'status': 200,
                      'simulationData': {'id': self.simulation_id,
                                         'time': "now",
                                         'NumAgents': len(self.agents),
                                         'Statistics': "something",
                                         'SimPoints': "<status>"}}
        return result

    def sim_status(self, simulation_id):
        """Get the status of the specified simulation.
        """

        result = None
        if self.server:
            result = requests.get(self.server + '/simulations/%s/status' % (simulation_id))
        else:
            result = {}
        return result

    def agent_status(self, simulation_id, agent_identifier):
        """Get the status of an agent.
        """

        result = None
        if self.server:
            result = requests.get(self.server + '/simulations/%s/agents/%s/status' % (simulation_id, agent_identifier))
        else:
            result = {'msg': 'Done',
                      'status': 200,
                      'agentData': {
                          "Status": {
                                "LastAction": "<lastAction>",
                                "LastStatus": "<lastStatus>",
                                "Mode": "<modeInt>"},
                          "Scan": {
                              "Walls": "<WallScan>",
                              "Home": "<HomeScan>",
                              "Payloads": "<PayloadScan>",
                              "Agents": "<AgentScan>"}
                       }}
        return result

    def agent_action(self, simulation_id, agent_id, action, mode):
        assert action in ('moveForward', 'turnLeft', 'turnRight', 'pickUp', 'drop', 'idle')

        return requests.post(self.server_url + '/simulations/%s/agents/%s/action' % (simulation_id, agent_id),
                             json={'action': action, 'mode': mode},
                             headers={'Content-Type': 'application/json'})

    # all the actions are recorded, now simulate them
    def step(self, simulation_id):
        return requests.post(self.server_url + '/simulations/%s/step' % (simulation_id),
                             json={}, # nothing to send at the moment
                             headers={'Content-Type': 'application/json'})

    def step_sim(self):
        json_res = self.step(self.simulation_id)
        if self.debugging:
            print 'step: ',
            pprint(json_res)
        return

    def get_status(self):
        json_res = self.sim_status(self.simulation_id).json()
        if self.debugging:
            print 'simStatus: ',
            pprint.pprint(json_res)
        return

    def run(self):
        while self.simulating:
            for agent in self.agents:
                agent.scan_and_move()

            self.step_sim()
            self.get_status()
        return


if __name__ == "__main__":
    # tart Sim
    sim = IslandOfAgents()
    sim.init_sim('Test2')
    sim.start_sim()
    sim.run()