'''
Created on Nov 27, 2016

@author: gscott
'''


class Agent(object):
    def __init__(self, agent_id, island_of_agents):
        self.island_of_agents = island_of_agents
        self.identity = agent_id

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
        agent_data = self.island_of_agents.agent_status(self.identity)

        status = agent_data['Status']
        self.lastStatus = status['LastStatus']
        self.lastAction = status['LastAction']

        if self.lastStatus == 'Success':
            self._update_navigation(self.lastAction)
            if self.lastAction == 'Action.pickUp':
                self.has_payload = True
            if self.lastAction == 'Action.drop':
                self.has_payload = False

        self.mode = status['Mode']
        self.last_scan = agent_data['Scan']

        if 'Home' in self.last_scan:
            self._home = self.last_scan['Home'][0]
            self._heading = 'right'
            self.has_home = True

            self._update_horizon(max(abs(self._home[0]), abs(self._home[1])))

        if 'Payloads' in self.last_scan and len(self.last_scan['Payloads']) > 0:
            self.visible_payloads = self.last_scan['Payloads']
        else:
            self.visible_payloads = None

        if 'Walls' in self.last_scan and len(self.last_scan['Walls']) > 0:
            self.walls = self.last_scan['Walls']
        else:
            self.walls = None

        if 'Agents' in self.last_scan and len(self.last_scan['Agents']) > 0:
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

    def _move_toward(self, coordinates):
        # coordinates[0] is the left or rightness
        # coordinates[1] is the forward or backward direction
        result = None
        if coordinates == (0, 1):  # Right in front
            result = None
        elif coordinates == (1, 0):  # To the right
            result = 'turnRight'
        elif coordinates == (-1, 0):  # To the left
            result = 'turnLeft'
        elif coordinates == (0, -1):  # Right Behind
            result = 'turnRight'
        elif coordinates[1] > 0:
            result = 'moveForward'
        elif coordinates[1] < 0:
            result = 'moveBackward'
        elif coordinates[0] > 0:
            result = 'turnRight'
        elif coordinates[0] < 0:
            result = 'turnLeft'

        return result

    def _wander_strategy(self):
        """Loop around like NASCAR.
        """

        result = 'moveForward'

        if self.lastStatus == 'Fail':
            result = 'turnLeft'

        return result

    def _find_home_strategy(self):
        """Find a Home.
        """

        result = self._wander_strategy()

        return result

    def _find_payload_strategy(self):
        """Find a payload.
        """

        result = None
        if self.visible_payloads:
            result = self._fetch_payload_strategy()
        else:
            result = self._wander_strategy()

        return result

    def _pickup_payload_strategy(self, best_payload):
        """Pick up an adjacent payload
        """
        result = None

        if best_payload == (0, 1):
            result = 'pickUp'

        return result

    def _fetch_payload_strategy(self):
        """A Payload is visible, fetch it.
        """

        best_payload = self.get_best_payload_coordinate()

        result = self._move_toward(best_payload)

        if result is None:
            # We are right next to it. so pick it up
            result = self._pickup_payload_strategy(best_payload)

        assert result is not None
        return result

    def _move_home_strategy(self):
        """Move toward Home to make a deposit
        """

        result = self._move_toward(self._home)
        if result is None:
            result = "drop"

        assert result is not None
        return result

    def scan_and_move(self):
        """Scan the environment and compute an action to take.
        """

        self.scan()
        # Evaluate the environment and choose an action.

        if self.has_payload and self.has_home:
            self.strategy = self._move_home_strategy
        elif self.has_payload:
            self.strategy = self._find_home_strategy
        elif self.has_home:
            self.strategy = self._find_payload_strategy
        else:
            if self.visible_payloads:
                self.strategy = self._fetch_payload_strategy
            else:
                self.strategy = self._wander_strategy

        action = self.strategy()

        response = self.island_of_agents.agent_action(self.identity, action, 1)
        assert response.status_code == 200

        return action

    def _update_navigation(self, movement):
        """If we've ever seen a Home, keep track of where it is, even if it moves beyond the scan horizon.
        """

        if self._heading == 'right':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] + 1, self._coordinates[1] + 0)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] - 1, self._coordinates[1] + 0)
            elif movement == 'turnLeft':
                self._heading = 'up'
            elif movement == 'turnRight':
                self._heading = 'down'

        elif self._heading == 'left':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] - 1,  self._coordinates[1] + 0)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] + 1, self._coordinates[1] + 0)
            elif movement == 'turnLeft':
                self._heading = 'down'
            elif movement == 'turnRight':
                self._heading = 'up'

        elif self._heading == 'up':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] + 0, self._coordinates[1] + 1)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] + 0, self._coordinates[1] - 1)
            elif movement == 'turnLeft':
                self._heading = 'left'
            elif movement == 'turnRight':
                self._heading = 'right'

        elif self._heading == 'down':
            if movement == 'moveForward':
                self._coordinates = (self._coordinates[0] + 0,  self._coordinates[1] - 1)
            elif movement == 'moveBackward':
                self._coordinates = (self._coordinates[0] + 0, self._coordinates[1] + 1)
            elif movement == 'turnLeft':
                self._heading = 'right'
            elif movement == 'turnRight':
                self._heading = 'left'

        return

    def _distance_to(self, coordinates):
        return abs(coordinates[0]) + abs(coordinates[1])

    def get_best_payload_coordinate(self):
        """Get the best (nearest) Payload to this Agent.

        Return the relative coordinates of the best Payload.
        """

        result = self.visible_payloads[0]
        best_distance = self._distance_to(result)

        for payload in self.visible_payloads[1:]:
                distance = self._distance_to(payload)
                if distance <= best_distance:
                    result = payload

        return result

    def _manual(self, command):
        result = self.island_of_agents.agent_action(self.identity, command, 1)
        result = self.island_of_agents.step()
        return

    def __repr__(self):
        return "Agent(%d) heading %s" % (self.identity, self._heading)
