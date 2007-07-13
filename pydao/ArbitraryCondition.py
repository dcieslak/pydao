"""
Author: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import Condition
import string

class ArbitraryCondition(Condition.Condition):
	
	"""
	Allows to add arbitrary conditions to query.
	"""

	def __init__(self):

		self._sqlQueryList = []
		self._args = []
		self._functions = []
   
	def addCriteria(self, sqlQuery, function, arguments):

		"""
		Add sqlQuery criterium (function for InMemoryDao) with
		arguments. Arguments are used in sqlQuery by %s syntax and
		are passed to function as second parameter (first one is
		object being checked).

		Example call:

		  c.addCriteria("T.salary > %s",
		    lambda obj, args: obj.salary > args[0],
		    [120.0])
		"""

		self._sqlQueryList.append(sqlQuery)
		self._args.append(arguments)
		self._functions.append(function)

	def generateWhereSQL(self, fieldName):

		if self._sqlQueryList:
			return string.join(self._sqlQueryList, " AND ")
		else:
			return "TRUE"

	def generateArgs(self):

		tmp = []
		for a in self._args:
			tmp += a
		return tmp

	def validateValue(self, value):

		return True

	def validateObject(self, obj):

		for n in range(0, len(self._functions)):
			fn = self._functions[n]
			args = self._args[n]
			if not fn(obj, args):
				return False
		
		return True

	def __repr__(self):

		return "ArbitraryCondition(%s, %s)" % (
			self._sqlQueryList,
			self._args,
		)

