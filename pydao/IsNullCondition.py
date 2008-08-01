"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition

class IsNullCondition(Condition.Condition):

    def generateWhereSQL(self, columnName):

        return columnName + " IS NULL"

    def generateArgs(self):

        return []

    def validateValue(self, value):

        return value == None


