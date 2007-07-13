"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import copy
import AbstractDao
import Condition

class InMemoryDao(AbstractDao.AbstractDao):

	"""
	DAO implemented in memory.
	
	To make this instance persistent use pickle module.

	Class attributes:

	 - INMEMORY_LOAD: procedure wth args dao, object to update
	   object before return from list() and load() methods
	"""

	def __init__(self, logStream = None):

		"""
		logStream: output of logging messages.
		"""

		AbstractDao.AbstractDao.__init__(self, logStream)

		self._n = 1000

		self._classNameToList = {}
		self._logStream = None

	def list(self, exampleObject,
	firstResult = 0, maxResults = 100000):

		self._log("list()", exampleObject)

		clazz = exampleObject.__class__
		className = clazz.__name__
		objectList = self._getWholeList(className)
		result = []

		hint = self._getLoadHint(clazz)

		for obj in objectList:
			hint(self, obj)
			if self._objectsMatches(obj, exampleObject):
				result.append(copy.copy(obj))

		return result[firstResult:firstResult+maxResults]

	def count(self, exampleObject):

		self._log("count()", exampleObject)

		className = exampleObject.__class__.__name__
		objectList = self._getWholeList(className)
		n = 0
		for obj in objectList:
			if self._objectsMatches(obj, exampleObject):
				n += 1
		return n

	def delete(self, exampleObject):

		self._log("delete()", exampleObject)

		filled = False
		for name, value in exampleObject.__dict__.items():
			if not name.startswith("_") and value != None:
				filled = True
				break
		if not filled:
			raise self.WrongArgumentsException,\
				"delete() argument must have at least one criteria "\
				"(safety protection)"

		className = exampleObject.__class__.__name__
		objectList = self._getWholeList(className)
		tmpList = []
		for obj in objectList:
			if not self._objectsMatches(obj, exampleObject):
				tmpList.append(obj)
		self._classNameToList[className] = tmpList
		return objectList

	def deleteAll(self, clazz):

		self._logClass("deleteAll()", clazz, None)

		className = clazz.__name__
		self._classNameToList[className] = []

	def save(self, anObject, ignoreNone = True):

		self._log("save()", anObject)

		assert anObject
		idName = self._getIdName(anObject.__class__)
		if not anObject.__dict__[idName]:
			anObject.__dict__[idName] = self._newId()
		className = anObject.__class__.__name__
		anObjectList = self._getWholeList(className)
		anObjectList.append(anObject)

	def load(self, clazz, objectID):

		self._logClass("load()", clazz, objectID)

		hint = self._getLoadHint(clazz)
		idName = self._getIdName(clazz)
		className = clazz.__name__
		objectList = self._getWholeList(className)
		for t in objectList:
			if str(t.__dict__[idName]) == str(objectID):
				hint(self, t)
				return t
		raise self.MissingObjectError,\
			"not found: " + clazz.__name__\
			+ "@" + str(objectID)

	def update(self, anObject, ignoreNone = True):

		self._log("update()", anObject)

		idName = self._getIdName(anObject.__class__)
		assert anObject.__dict__[idName],\
			"for update anObject id has to be set"

		className = anObject.__class__.__name__
		anObjectList = self._getWholeList(className)
		idName = self._getIdName(anObject.__class__)
		for t in anObjectList:
			if str(t.__dict__[idName]) == str(anObject.__dict__[idName]):
				for name, value in anObject.__dict__.items():
					if not ignoreNone or value:
						t.__dict__[name] = value
				return
		raise self.MissingObjectError,\
			"not found: %s@%s" % (className, anObject.id)

	def _newId(self):

		result = self._n
		self._n += 1
		return result

	def _getWholeList(self, className):

		if self._classNameToList.has_key(className):
			objectList = self._classNameToList[className]
		else:
			objectList = []
			self._classNameToList[className] = objectList
		return objectList

	def _objectsMatches(self, databaseObject, exampleObject):

		for name, value in exampleObject.__dict__.items():
			if not name.startswith("_") and value != None:
				if not self._valueMatches(value,
				databaseObject.__dict__[name],
				databaseObject):
					return 0
		return 1

	def _valueMatches(self, searchValue, dbValue, databaseObject):

		if isinstance(searchValue, Condition.Condition):
			return searchValue.validateValue(dbValue)\
				and searchValue.validateObject(databaseObject)
		else:
			return str(searchValue) == str(dbValue)

	def _getLoadHint(self, clazz):

		if clazz.__dict__.has_key("INMEMORY_LOAD"):
			return clazz.__dict__["INMEMORY_LOAD"]
		else:
			return lambda x,y: None

	def _getIdName(self, clazz):

		if clazz.__dict__.has_key("DAO_ID"):
			return clazz.__dict__["DAO_ID"]
		else:
			return "id"

