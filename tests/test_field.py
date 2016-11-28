'''
Created on Nov 27, 2016

@author: gscott
'''
import unittest
from field import Field


class TestField(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

#     def testField(self):
#         d = {'Status': {'LastStatus': 'Success', 'LastAction': 'Action.born', 'Mode': 0},
#              'Scan': {
#                  'Home': [(2, 0)],
#                  'Walls': [('B', 3), ('F', 3), ('R', 3), ('L', 3)],
#                  'Agents': [],
#                  'Payloads': [(-1, 1)]}}
# 
#         f = Field(d)
#         pass

    def testField(self):
        d = {'Status': {'LastStatus': 'Success', 'LastAction': 'Action.born', 'Mode': 0},
             'Scan': {
                 'Home': [(2, 0)],
                 'Walls': [('B', 3), ('F', 3), ('R', 3), ('L', 3)],
                 'Agents': [],
                 'Payloads': [(-1, 1)]}}

        f = Field(home=[(2, 0)], agents=[(2, 2), (6, 3)], payloads=[(1, 1), (5, 5)])
        pass

    def testField_strategise(self):
        f = Field(home=[(2, 0)], agents=[(2, 2), (6, 3)], payloads=[(1, 1), (5, 5)])
        strategies = f.strategise()
        print strategies
        pass

if __name__ == "__main__":
    unittest.main()
