"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition

class NotNullCondition(Condition.Condition):

    def generateWhereSQL(self, columnName):

        return columnName + " IS NOT NULL"

    def generateArgs(self):

        return []

    def validateValue(self, value):

        return value != None


