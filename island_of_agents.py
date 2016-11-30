import sys
import requests
import pprint
from agent import Agent


def UUID(uid):
    return uid


class IslandOfAgents(object):

    def __init__(self, server, simulation_id=None, debugging=False):
        self.server = server
        self.simulation_id = simulation_id
        self.debugging = debugging

        self.agents = []
        self.running = False
        return

    def create_sim(self, environment_name):
        assert environment_name in ("HW1", "HW2")

        if self.simulation_id is None:
            if self.server:
                response = requests.post(self.server + "/api/simulations/create",
                                         json={'env_name': environment_name},
                                         headers={'Content-Type': 'application/json'})

                result = response.json()
            else:
                result = {'msg': 'Simulation "2" created with environment "HW1"!',
                          'status': 200,
                          'simulationId': 2,
                          'simulationData': "{'SimPoints': 0, 'NumAgents': 1, 'Statistics': {'Min': 0, 'Max': 0, 'Median': 0.0, 'TotalEnergy': 0, 'SimPoints': 0, 'Avg': 0, 'Touched': 0}, 'id': UUID('6bd9f340-f229-4338-92e8-3cd3ec26038e'), 'time': 0}"
                          }

            self.simulation_id = result['simulationId']

        return

    def start_sim(self):
        result = None
        if self.server:
            response = requests.put(self.server + '/api/simulations/%s/start' % (self.simulation_id,))
            result = response.json()
        else:
            result = {'msg': 'Simulation 2 restarted!',
                      'status': 200,
                      'simulationData': "{'SimPoints': 0, 'NumAgents': 1, 'Statistics': {'Min': 0, 'Max': 0, 'Median': 0.0, 'TotalEnergy': 0, 'SimPoints': 0, 'Avg': 0, 'Touched': 0}, 'id': UUID('6bd9f340-f229-4338-92e8-3cd3ec26038e'), 'time': 0}"}

        # This is risky, as it allows the server to execute code on the client.
        self.simulation_data = eval(result['simulationData'])
        number_of_agents = self.simulation_data['NumAgents']

        self.agents = []
        for agent_id in range(number_of_agents):
            self.agents.append(Agent(agent_id, self))

        self.running = True
        return result

    def sim_status(self):
        """Get the status of the specified simulation.
        """

        result = None
        if self.server:
            response = requests.get(self.server + '/api/simulations/%s/status' % (self.simulation_id,))
            result = response.json()
        else:
            result = {}
        return result

    def agent_status(self, agent_identifier):
        """Get the status of an agent.
        """

        result = None
        if self.server:
            response = requests.get(self.server + '/api/simulations/%s/agents/%s/status'
                                    % (self.simulation_id, agent_identifier))
            result = response.json()
        else:
            result = {'msg': 'Done',
                      'status': 200,
                      'agentData': "{'Status': {'LastStatus': 'Success', 'LastAction': 'Action.born', 'Mode': 0, 'Payload': 'None'}, 'Scan': {'Home': [(-2, 0)], 'Walls': [('B', 1), ('F', 7), ('R', 3), ('L', 5)], 'Agents': [], 'Payloads': [(0, 1)]}}"
                      }

        # This is risky, as it allows the server to execute code on the client.
        agent_data = eval(result['agentData'])
        return agent_data

    def agent_action(self, agent_id, action, mode):
        assert action in ('moveForward', 'moveBackward', 'turnLeft', 'turnRight', 'pickUp', 'drop', 'idle')

        if self.server:
            return requests.post(self.server + '/api/simulations/%s/agents/%s/action' % (self.simulation_id, agent_id),
                                 json={'action': action, 'mode': mode},
                                 headers={'Content-Type': 'application/json'})
        else:
            return None

    def step(self):
        if self.server:
            return requests.put(self.server + '/api/simulations/%s/step' % (self.simulation_id,),
                                json={},  # nothing to send at the moment
                                headers={'Content-Type': 'application/json'})
        else:
            return None

    def step_sim(self):
        json_res = self.step()
        if self.debugging:
            print 'step_sim: ',
            pprint(json_res)
        return

    def get_status(self):
        status = self.sim_status()
        if self.debugging:
            print 'get_status: ',
            pprint.pprint(status)
        return status

    def run(self, iterations):
        """Run the simulation for N iterations
        """

        for iteration in xrange(0, iterations):
            for agent in self.agents:
                action = agent.scan_and_act()
                print "%5d  %12.12s -> %s" % (iteration, action, agent)

            self.step_sim()
            print "-----"

        return


def IslandOfAgents_HW1(args):
    island = IslandOfAgents(args[0])
    island.create_sim('HW1')
    island.start_sim()
    island.run(10)
    print "All done."


def IslandOfAgents_HW2(args):
    island = IslandOfAgents(args[0])
    island.create_sim('HW2')
    island.start_sim()
    island.run(100)
    print "All done."

if __name__ == "__main__":
    # IslandOfAgents_HW1(sys.argv[1:])
    IslandOfAgents_HW2(sys.argv[1:])
