"""
Author: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""


class Condition:

	"""
	Interface that allow to build conditions based on one field.
	"""

	def generateWhereSQL(self, fieldName):

		"""
		Generate where SQL fragment (including column name).
		This method is used by SqlDao.
		"""
		return "TRUE"

	def generateArgs(self):

		"""
		Generate arguments passed to DB-API.
		This method is used by SqlDao.
		"""
		return []

	def validateValue(self, value):

		"""
		Validate if given value meets criteria.
		This method is used by InMemoryDao.
		"""
		return True

	def validateObject(self, obj):

		"""
		Validate if given object meets criteria.
		This method is used by InMemoryDao.
		"""
		return True


