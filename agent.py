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
        self._coordinates = None
        self._horizon = 1
        self._strategy = self._wander_strategy
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
            self._coordinates = (-home[0], -home[1])
            self._update_horizon(max(home[0], home[1]))

        if 'Payloads' in self.last_scan:
            self.payloads_visible = self.last_scan['Payloads']
        else:
            self.payloads_visible = None

        if 'Walls' in self.last_scan:
            self.walls = self.last_scan['Walls']
        else:
            self.walls = None

        if 'Agents' in self.last_scan:
            self.agents = self.last_scan['Agents']
        else:
            self.agents = None

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

    def _wander_strategy(self):
        """Wander around.
        """
        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result

    def _find_home_strategy(self):
        """Find a Home.
        """
        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result
        return

    def _find_payload_strategy(self):
        """Find a payload.
        """

        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result

    def _pickup_payload_strategy(self):
        """Pick up an adjacent payload
        """

        result = None

        return result

    def _get_payload_strategy(self):
        """A Payload is visible, get it.
        """

        payload = self.get_best_payload_coordinate()

        result = None

        if abs(payload[0] + payload[1]) == 1:
            # We are right next to it. so pick it up
            result = self._pickup_payload_strategy()
        else:
            if payload[0] > 0:
                result = 'moveForward'
            elif payload[0] < 0:
                result = 'moveBackward'
            elif payload[1] > 0:
                result = 'turnLeft'
            elif payload[1] < 0:
                result = 'turnRight'

        assert result is not None
        return result

    def _deposit_strategy(self):
        """Move toward Home to make a deposit
        """

        return

    def scan_and_move(self):
        """Scan the environment and compute an action to take.
        """

        self.scan()
        # Evaluate the environment and choose an action.

        if self.has_payload and self.has_home:
            self.strategy = self._deposit_strategy
        elif self.has_payload:
            self.strategy = self._find_home_strategy
        elif self.has_home:
            self.strategy = self._find_payload_strategy
        else:
            if self.payloads_visible:
                self.strategy = self._get_payload_strategy
            else:
                self.strategy = self._wander_strategy

        movement = self.strategy()

        result = self.island_of_agents.agent_action(self.simulation_id, self.identity, movement, 1)
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

    def get_best_payload_coordinate(self):
        """Compute the distances from this Agent to the given Payloads.

        Return the best Payload coordinates.
        """

        result = None
        for payload in self.payloads_visible:
                distance = abs(payload[0]) + abs(payload[1])
                if distance <= result[1]:
                    result = payload

        return result

    def __repr__(self):
        return "Agent@(%d, %d) pointing %d" % (self.x, self.y, self.orientation)
