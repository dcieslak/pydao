"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import copy

class AbstractDao:

	"""
	Base class used to specify public dao interface.

	To specify identifier attribute different that "id" specify
	class attribute "DAO_ID".

	 - DAO_ID name of primary key, default = "id"
	"""

	class MissingObjectError(Exception):
		pass

	class NotUniqueObject(Exception):
		pass

	class WrongArgumentsException(Exception):
		pass

	def __init__(self, logStream):

		self._logStream = logStream

	def list(self, exampleObject,
	firstResult = 0, maxResults = 100000):

		"""
		Retrieves list of objects the same type as exampleObject
		filtered by fields that are != None. Arguments firstResult and
		maxResults allows you to do paging.

		pre: exampleObject != None
		pre: hasattr(exampleObject, "__class__")
		"""
		return []

	def listSQL(self, sqlQuery, clazz, argList = (),
	filterModifyFunction = None):

		"""
		Retrieves list of objects of type clazz from records returned
		by sqlQuery. If database doesn't support SQL
		filterModifyFunction is used to alter result.

		Attribute sqlQuery can have %s marks to place arguments from
		argList (similar to MySQLdb).

		filterModifyFunction argument is used by SimpleDao
		implementations. It's function: fun(dao, object, argList) ->
		boolean. This function can modify object.

		pre: sqlQuery != None
		pre: clazz != None
		"""
		return []

	def listWhere(self, clazz, whereClause, argList = (),
	filterFunctioin = None):

		"""
		Retrieves list of objects of type clazz from records filtered
		by SQL whereClause. If database doesn't support SQL queries
		filterFunctioin is used to alter result.

		Attribute sqlWhere can have %s marks to place arguments from
		argList (similar to MySQLdb).

		filterFunctioin argument is used by SimpleDao implementations.
		It's function: fun(object, argList) -> boolean.

		pre: whereClause != None
		pre: clazz != None
		"""
		return []

	def count(self, exampleObject):

		"""
		Count elements that matches given template.

		pre: exampleObject != None
		pre: hasattr(exampleObject, "__class__")
		"""
		raise Exception, "unimplemented"

	def delete(self, exampleObject):

		"""
		Delets objects that match given template object
		(attributes != None).

		exampleObject must have at least one criterium filled else
		exception will be raised (safety, to prevent accidencial
		deletion).

		pre: exampleObject != None
		pre: hasattr(exampleObject, "__class__")
		"""
		raise Exception, "unimplemented"

	def deleteAll(self, clazz):

		"""
		Delets all instances of given class.

		pre: clazz != None
		"""
		raise Exception, "unimplemented"

	def save(self, obj, ignoreNone = True):

		"""
		Adds new object to database. If identifier is None it's
		generated. After this call identifier is filled.

		If ignoreNone is True None attributes will not be written into
		database.
		"""
		raise Exception, "unimplemented"

	def load(self, clazz, objectID):

		"""
		Fetches one object from database. If there's no object raises
		an exception.
		"""
		raise Exception, "unimplemented"

	def load2(self, exampleObject):

		"""
		Fetches one object from database based on passed criteria.

		An execption is raised if no object (MissingObjectError)
		or more than one object (NotUniqueObject) matches.
		"""

		objectList = self.list(exampleObject)
		if not objectList:
			raise self.MissingObjectError, exampleObject
		if len(objectList) > 1:
			raise self.NotUniqueObject, exampleObject
		return objectList[0]

	def update(self, obj, ignoreNone = True):

		"""
		Updates object attributes based on identifier
		attribute.

		If ignoreNone is True attributes that have None value
		in object will remain unchanged in database.
		"""
		raise Exception, "unimplemented"

	def commit(self):

		"""
		Commits current transaction (if choosen database backend
		supports it). For InMemoryDao this method does nothing.
		"""

	def rollback(self):

		"""
		Rollbacks current transaction (if choosen database backend
		supports it). For InMemoryDao this method does nothing.
		"""

	def generateSequence(self, objectExample, numberPropertyName):

		"""
		Generates sequence based on filled object and use
		numberAttributeName.

		pre: objectExample.__dict__.has_key(numberPropertyName)
		"""

		clazz = objectExample.__class__
		self._lockTable(clazz)

		objectList = self.list(objectExample)
		if objectList:
			obj = objectList[0]
			n = obj.__dict__[numberPropertyName]
			n += 1
			obj.__dict__[numberPropertyName] = n
			self.update(obj)
			self._unlockTable(clazz)
			return n
		else:
			obj = copy.copy(objectExample)
			obj.__dict__[numberPropertyName] = 1
			self.save(obj)
			self._unlockTable(clazz)
			return 1

	def _log(self, text, obj):

		if self._logStream:
			self._logStream.write(text\
				+ ": " + obj.__class__.__name__\
				+ " " + self._showNotNullAttributes(obj) + "\n")
			self._logStream.flush()

	def _logList(self, text, lst):

		if self._logStream:
			self._logStream.write(text\
				+ ": " + repr(lst) + "\n")
			self._logStream.flush()

	def _logClass(self, text, clazz, objectID):

		if self._logStream:
			self._logStream.write(text\
				+ ": " + clazz.__name__\
				+ "@" + repr(objectID) + "\n")
			self._logStream.flush()
	
	def _showNotNullAttributes(self, obj):

		s = "{"
		for name, value in obj.__dict__.items():
			if not name.startswith("_"):
				if value != None:
					s += name
					s += "="
					s += repr(value)
					s += " "
		s += "}"
		return s

	def _lockTable(self, clazz):

		pass

	def _unlockTable(self, clazz):

		pass


