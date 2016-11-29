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

        self.has_home = False
        self.has_payload = False

        self._heading = None
        self._home_locations = []
        self._coordinates = None
        self._horizon = 1
        self._strategy = self._find_something_strategy
        return

    def get_status(self):
        return self.island_of_agents.get_agent_status(self.identity)

    # parse what the agent sees into structures for use later
    def scan(self):
        jsonStatus = self.island_of_agents.agent_status(self.simulation_id, self.identity)

        if self.island_of_agents.debugging:
            print 'agentStatus: ', self.identity,
            pprint.pprint(jsonStatus)

        agent_data = jsonStatus['agentData']
        status = agent_data['Status']
        self.lastStatus = status['LastStatus']

        self.lastAction = status['LastAction']

        if self.lastStatus == 'Success':
            self._update_navigation(self.lastAction)

        self.mode = status['Mode']
        self.last_scan = agent_data['Scan']

        if 'Home' in self.last_scan:
            home = self.last_scan['Home']
            self._heading = 'right'
            self.has_home = True
            self.home_locations = home
            self._coordinates = (-home[0], -home[1])
            self._update_horizon(max(home[0], home[1]))

        return

    def _update_horizon(self, distance):
        """If something in the scan is farther way than what is currently the known horizon,
        update the horizon.
        """

        if distance > self._horizon:
            self._horizon = distance
        return

    def _nascar_strategy(self):
        result = None

        if self.lastStatus == 'Fail':
            result = 'turnLeft'
        else:
            result = 'moveForward'

        return result

    def _find_something_strategy(self):
        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result

    def _find_home_strategy(self):
        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result
        return

    def _find_payload_strategy(self):
        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result

    def _deposit_strategy(self):
        """move toward Home to make a deposit
        """

        return

    def scan_and_move(self):
        """Scan the environment and compute an action to take.
        """

        self.scan()

        if self.has_payload and self.has_home:
            self.strategy = self._deposit_strategy
        elif self.has_payload:
            self.strategy = self._find_home_strategy
        elif self.has_home:
            self.strategy = self._find_payload_strategy
        else:
            self.strategy = self._find_something_strategy

        self.last_movement = self.strategy()

        result = self.island_of_agents.agent_action(self.simulation_id, self.identity, self.last_movement, 1)
        return result

    def _update_navigation(self, movement):
        assert movement in ('moveForward', 'moveBackward', 'turnLeft', 'turnRight', 'drop', 'pickUp', 'idle')

        if self._heading == 'right':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] + 1, self._coordinates[1] + 0)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] - 1, self._coordinates[1] + 0)
            elif movement == 'turnLeft':
                self._heading = 'up'
            elif movement == 'turnRight':
                self._heading = 'down'
            elif movement == 'drop':
                pass
            elif movement == 'pickUp':
                pass
            elif movement == 'idle':
                pass

        elif self._heading == 'left':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] - 1,  self._coordinates[1] + 0)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] + 1, self._coordinates[1] + 0)
            elif movement == 'turnLeft':
                self._heading = 'down'
            elif movement == 'turnRight':
                self._heading = 'up'
            elif movement == 'drop':
                pass
            elif movement == 'pickUp':
                pass
            elif movement == 'idle':
                pass

        elif self._heading == 'up':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] + 0, self._coordinates[1] + 1)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] + 0, self._coordinates[1] - 1)
            elif movement == 'turnLeft':
                self._heading = 'left'
            elif movement == 'turnRight':
                self._heading = 'right'
            elif movement == 'drop':
                pass
            elif movement == 'pickUp':
                pass
            elif movement == 'idle':
                pass

        elif self._heading == 'down':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] + 0,  self._coordinates[1] - 1)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] + 0, self._coordinates[1] + 1)
            elif movement == 'turnLeft':
                self._heading = 'right'
            elif movement == 'turnRight':
                self._heading = 'left'
            elif movement == 'drop':
                pass
            elif movement == 'pickUp':
                pass
            elif movement == 'idle':
                pass

        return

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
