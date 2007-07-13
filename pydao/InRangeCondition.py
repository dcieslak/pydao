"""
Author: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition

class InRangeCondition(Condition.Condition):

	def __init__(self, minValue, maxValue):

		self.minValue = minValue
		self.maxValue = maxValue

	def generateWhereSQL(self, columnName):

		return columnName + " BETWEEN %s AND %s"

	def generateArgs(self):

		return [self.minValue, self.maxValue]

	def validateValue(self, value):

		if value != None:
			return value >= self.minValue and value <= self.maxValue
		else:
			return False

	def __repr__(self):

		return "InRangeCondition(%s,%s)" % (self.minValue, self.maxValue)


