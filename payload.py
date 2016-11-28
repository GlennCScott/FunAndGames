'''
Created on Nov 27, 2016

@author: gscott
'''


class Payload(object):
    '''
    classdocs
    '''

    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        return

    def is_at(self, x, y):
        return self.x == x and self.y == y

    def __repr__(self):
        return "Payload@(%d, %d)" % (self.x, self.y)
