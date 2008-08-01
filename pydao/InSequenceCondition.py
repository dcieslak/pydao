"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import string
import Condition

class InSequenceCondition(Condition.Condition):

    def __init__(self, values = None):

        if not values:
            self.values = []
        else:
            self.values = values

    def addValue(self, value):

        self.values.append(value)

    def generateWhereSQL(self, columnName):

        return columnName + " IN (%s)" \
            % string.join(["%s"] * len(self.values), ",")

    def generateArgs(self):

        return self.values

    def validateValue(self, value):

        if value != None:
            return value in self.values
        else:
            return False

    def __repr__(self):

        return "InSequenceCondition(%s)" % `self.values`

