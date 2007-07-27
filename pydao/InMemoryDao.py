"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import SimpleDao

class InMemoryDao(SimpleDao.SimpleDao):

	"""
	DAO implemented in memory.
	
	To make this instance persistent use pickle module.
	"""

	def __init__(self, logStream = None):

		"""
		logStream: output of logging messages.
		"""

		SimpleDao.SimpleDao.__init__(self, logStream)
		self._n = 1000
		self._classNameToList = {}

	def _newId(self, className):

		result = self._n
		self._n += 1
		return result

	def _getWholeList(self, clazz):

		className = clazz.__name__
		if self._classNameToList.has_key(className):
			objectList = self._classNameToList[className]
		else:
			objectList = []
			self._classNameToList[className] = objectList
		return objectList

	def _replaceWholeList(self, clazz, lst):

		className = clazz.__name__
		self._classNameToList[className] = lst
