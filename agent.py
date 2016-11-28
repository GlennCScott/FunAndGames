'''
Created on Nov 27, 2016

@author: gscott
'''
import pprint

"""
moveForward = 1
moveBackward = 2
turnLeft = 3
turnRight = 4
drop = 5
pickUp = 6
idle = 7
"""


class Agent(object):
    def __init__(self, agent_id, simulation_id, island_of_agents):
        self.island_of_agents = island_of_agents
        self.identity = agent_id
        self.simulation_id = simulation_id
        self.orientation = 0
        return

    def get_status(self):
        return self.island_of_agents.get_agent_status(self.identity)

    # parse what the agent sees into structures for use later
    def scan(self):
        jsonStatus = self.island_of_agents.agent_status(self.simulation_id, self.identity).json()

        if self.island_of_agents.debugging:
            print 'agentStatus: ', self.identity,
            pprint.pprint(jsonStatus)

        data = eval(jsonStatus['agentData'])
        status = data['Status']
        self.lastStatus = status['LastStatus']
        self.lastAction = status['LastAction']
        self.mode = status['Mode']
        self.lastScan = data['Scan']
        if data['Scan'].haskey(''):
            pass

        return

    # this is where the action happens.  Each agent looks around it by getting status, and based on that selects an action to do.
    def scan_and_move(self):
        self.scan()
        # >>>>>>your logic goes here!<<<<<<<
        # this simple example just blindly moves forward until it hits something. then it turns left
        if self.lastStatus == 'Fail':
            self.rc.agentAction(self.sid, self.aid, 'turnLeft', 1)
            return
        self.rc.agentAction(self.sid, self.aid, 'moveForward', 1)

    def get_best_payload(self, payloads, excluded_payloads=None):
        """Compute the distances from this Agent to the given Payloads.

        Return the best Payload and distance to it.
        """
        result = (0, 100000000)
        for payload in payloads:
            if payload not in excluded_payloads:
                distance = abs(self.x - payload.x) + abs(self.y - payload.y)
                if distance <= result[1]:
                    result = (payload, distance)

        return result

    def plot_path(self, x, y, direction='righterly'):
        """Return a list of directions necessary to reach the x,y goal.
        """
        result = []
        result.append(self.steer(x, y))

        x_delta = x - self.x
        y_delta = y = self.y


        return result

    def is_at(self, x, y):
        return self.x == x and self.y == y

    def __repr__(self):
        return "Agent@(%d, %d) pointing %d" % (self.x, self.y, self.orientation)
