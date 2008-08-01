"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition
import string

class OrCondition(Condition.Condition):

    def __init__(self):

        self.conditions = []

    def addCondition(self, condition):

        self.conditions.append(condition)

    def generateWhereSQL(self, columnName):

        arr = []
        for cond in self.conditions:
            arr.append(cond.generateWhereSQL(columnName))

        return ("(" + string.join(arr, " OR ") + ")")

    def generateArgs(self):

        arr = []
        for cond in self.conditions:
            arr += cond.generateArgs()
        return arr

    def validateValue(self, value):

        for cond in self.conditions:
            if cond.validateValue(value):
                return True
        return False

    def __repr__(self):

        return "OrCondition(%s)" % self.conditions


