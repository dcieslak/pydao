"""
Author: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition

class LikeCondition(Condition.Condition):

	def __init__(self, text):

		self.text = text

	def generateWhereSQL(self, columnName):

		return columnName + " LIKE %s"

	def generateArgs(self):

		return [self.text]

	def validateValue(self, value):

		if value != None:
			text = self.text.replace("%", "")
			return value.find(text) >= 0
		else:
			return False

	def __repr__(self):

		return "LikeCondition(" + self.text + ")"

