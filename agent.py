'''
Created on Nov 27, 2016

@author: gscott
'''


class Agent(object):
    def __init__(self, agent_identity, island_of_agents):
        self.island_of_agents = island_of_agents
        self.identity = agent_identity

        self.has_home = False
        self.has_payload = False
        self._home = None

        self.experimental_home = None

        self.strategy = None

        self._horizon = 1
        self._strategy = self._wander_strategy
        return

    def _update_home_information(self, homes):
        """Given a list of Homes, pick the best one and remember where it is.

        Currently the first one is considered the best one.
        """

        if homes is not None and len(homes) > 0:
            self._home = homes[0]
            self.has_home = True
            self._update_horizon(max(abs(self._home[0]), abs(self._home[1])))
            if self.experimental_home is None:
                self.experimental_home = self._home
            else:
                if self.experimental_home not in self.last_scan['Home']:
                    print self, self.experimental_home, "is not in", self.last_scan['Home']
                    self.experimental_home = self._home
        else:
            self._home = self.experimental_home  # Try some reckoning

        return

    def _update_payload_information(self, payloads):
        if payloads is not None and len(payloads) > 0:
            self.visible_payloads = payloads
        else:
            self.visible_payloads = None
        return

    def _update_wall_information(self, walls):
        if walls is not None and len(walls) > 0:
            self.walls = walls
        else:
            self.walls = None
        return

    def _update_agent_information(self, agents):
        if agents is not None and len(agents) > 0:
            self.agents = agents
        else:
            self.agents = None
        return

    # parse what the agent sees into structures for use later
    def scan(self):
        agent_data = self.island_of_agents.agent_status(self.identity)

        status = agent_data['Status']
        self.last_status = status['LastStatus']
        self.last_action = status['LastAction']

        if self.last_status == 'Success':
            self._update_navigation(self.last_action)
            if self.last_action == 'Action.pickUp':
                self.has_payload = True
            if self.last_action == 'Action.drop':
                self.has_payload = False

        self.mode = status['Mode']
        self.last_scan = agent_data['Scan']

        if 'Home' in self.last_scan:
            self._update_home_information(self.last_scan['Home'])

        if 'Payloads' in self.last_scan:
            self._update_payload_information(self.last_scan['Payloads'])

        if 'Walls' in self.last_scan and len(self.last_scan['Walls']) > 0:
            self._update_wall_information(self.last_scan['Walls'])

        if 'Agents' in self.last_scan and len(self.last_scan['Agents']) > 0:
            self._update_agent_information(self.last_scan['Agents'])

        return

    def _update_horizon(self, distance):
        """If something in the scan is farther way than what is currently the known horizon,
        update the horizon.
        """

        if distance > self._horizon:
            self._horizon = distance
        return

    def move_toward(self, coordinates):
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

        if self.last_status == 'Fail' or self.last_action == 'Action.drop':
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

        result = self.move_toward(best_payload)

        if result is None:
            # We are right next to it. so pick it up
            result = self._pickup_payload_strategy(best_payload)

        assert result is not None
        return result

    def _move_home_strategy(self):
        """Move toward Home to make a deposit
        """

        if self.last_status == "Fail":
            result = "turnRight"
        else:
            result = self.move_toward(self._home)
            if result is None:
                result = "drop"

        assert result is not None
        return result

    def scan_and_act(self):
        """Scan the environment and compute an action to take.
        """

        self.scan()

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
        if self.experimental_home is not None:
            if movement == 'Action.moveForward':
                self.experimental_home = (self.experimental_home[0], self.experimental_home[1] - 1)
            elif movement == 'Action.moveBackward':
                self.experimental_home = (self.experimental_home[0], self.experimental_home[1] + 1)
            elif movement == 'Action.turnLeft':  # (0, -3) -> (-3, 0)
                self.experimental_home = (self.experimental_home[1], -self.experimental_home[0])
            elif movement == 'Action.turnRight':  # (0, -3) -> (3, 0)
                self.experimental_home = (-self.experimental_home[1], self.experimental_home[0])

        return self.experimental_home

    def _distance_to(self, coordinates):
        """Compute the distance, in the number of moves, to the given coordinates.
        """

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
                    best_distance = distance

        return result

    def _manual(self, command):
        result = self.island_of_agents.agent_action(self.identity, command, 1)
        result = self.island_of_agents.step()
        return

    def __repr__(self):
        return "Agent(%d) home=%s payloads=%s %s:%s" % (
            self.identity, self._home, self.visible_payloads, self.last_action, self.last_status)
