"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import copy
import AbstractDao
import Condition

class SimpleDao(AbstractDao.AbstractDao):

	"""
	DAO implemented without SQL backend.

	Class attributes:

	 - INMEMORY_LOAD: procedure wth args dao, object to update
	   object before return from list() and load() methods
	"""

	def __init__(self, logStream = None):

		"""
		logStream: output of logging messages.
		"""
		AbstractDao.AbstractDao.__init__(self, logStream)

	def list(self, exampleObject,
	firstResult = 0, maxResults = 100000):

		self._log("list()", exampleObject)

		clazz = exampleObject.__class__
		objectList = self._getWholeList(clazz)
		result = []

		hint = self._getLoadHint(clazz)

		for obj in objectList:
			hint(self, obj)
			if self._objectsMatches(obj, exampleObject):
				result.append(copy.copy(obj))

		return result[firstResult:firstResult+maxResults]

	def count(self, exampleObject):

		self._log("count()", exampleObject)

		clazz = exampleObject.__class__
		objectList = self._getWholeList(clazz)
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

		clazz = exampleObject.__class__
		objectList = self._getWholeList(clazz)
		tmpList = []
		for obj in objectList:
			if not self._objectsMatches(obj, exampleObject):
				tmpList.append(obj)
		self._replaceWholeList(clazz, tmpList)
		return objectList

	def deleteAll(self, clazz):

		self._logClass("deleteAll()", clazz, None)

		self._replaceWholeList(clazz, [])

	def save(self, anObject, ignoreNone = True):

		self._log("save()", anObject)

		assert anObject
		idName = self._getIdName(anObject.__class__)
		if not anObject.__dict__[idName]:
			anObject.__dict__[idName] = self._newId(
				anObject.__class__.__name__)
		clazz = anObject.__class__
		anObjectList = self._getWholeList(clazz)
		anObjectList.append(anObject)

		self._replaceWholeList(clazz, anObjectList)

	def load(self, clazz, objectID):

		self._logClass("load()", clazz, objectID)

		hint = self._getLoadHint(clazz)
		idName = self._getIdName(clazz)
		objectList = self._getWholeList(clazz)
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

		clazz = anObject.__class__
		anObjectList = self._getWholeList(clazz)
		idName = self._getIdName(anObject.__class__)
		for t in anObjectList:
			if str(t.__dict__[idName]) == str(anObject.__dict__[idName]):
				for name, value in anObject.__dict__.items():
					if not ignoreNone or value:
						t.__dict__[name] = value
				self._replaceWholeList(clazz, anObjectList)
				return
		raise self.MissingObjectError,\
			"not found: %s@%s" % (clazz.__name__, anObject.id)

	def _newId(self, className):
		
		"""
		Returns generated identifier.
		"""
		return 0

	def _getWholeList(self, clazz):

		"""
		Returns list of objects based on clazz.
		"""
		return []

	def _replaceWholeList(self, clazz, lst):

		"""
		Replaces list of objects with new one.
		"""


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


