"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition

class LikeCondition(Condition.Condition):

	def __init__(self, text, columnName = None):

		"""
		If tested column name is different (for example from joined
		table) you can specifu columnName to use in condition. Used
		only by SqlDao, ignored for InMemoryDao.
		"""

		self.text = text
		self.columnName = columnName

	def generateWhereSQL(self, columnName):

		if self.columnName:
			columnName = self.columnName

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

