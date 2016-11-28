'''
Created on Nov 27, 2016

@author: gscott
'''
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
    def __init__(self, coords):
        '''
        Constructor
        '''
        self.x = coords[0]
        self.y = coords[1]
        self.orientation = 0
        return

    def get_best_payload(self, payloads):
        """Compute the distances from this Agent to the given Payloads.

        Return the best Payload and distance to it.
        """
        result = (0, 100000000)
        for payload in payloads:
            distance = abs(self.x - payload.x) + abs(self.y - payload.y)
            if distance <= result[1]:
                result = (payload, distance)
        return result

    def is_at(self, x, y):
        return self.x == x and self.y == y

    def __repr__(self):
        return "Agent@(%d, %d) pointing %d" % (self.x, self.y, self.orientation)
