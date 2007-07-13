"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import AbstractDao
import Condition
import string
import new

class SqlDao(AbstractDao.AbstractDao):

	"""
	DAO implemented in basic SQL database.

	POPO can have additional class attributes that can reflect
	database structure (uset T alias for table related to current
	class):

	 - SQL_TABLE name of a table, default = class name
	 - SQL_FROM additional from expression (LEFT JOIN ...)
	 - SQL_SELECT additional select expression (XTZ.asdf AS _asdf ...)
	 - SQL_ORDER order by expression (T.name ...)

	If unique constraints are not satisfied an IntegrityError is
	raised.
	"""

	IntegrityError = None

	def __init__(self, conn, logStream, updateSqlStream):

		"""
		logStream is user to log all queries to database. It can be
		used to track application efficiency (amount of SQL
		generated).

		updateSqlStream is used to render SQL queries that change
		state of database. Those queries can be used to replicate
		database state to another machine.
		"""

		AbstractDao.AbstractDao.__init__(self, logStream)
		self._conn = conn
		self._updateSqlStream = updateSqlStream

	def listSQL(self, sqlQuery, clazz, argList = ()):

		self._logList("listSQL()", argList)

		self._logSql(sqlQuery)
		c = self._conn.cursor()
		c.execute(sqlQuery, argList)
		result = []
		for t in c.fetchall():
			obj = new.instance(clazz)
			obj.__init__()
			self._updateObjectFromCursor(t, c, obj)
			result.append(obj)
		c.close()

		return result

	def listWhere(self, whereClause, clazz, argList = ()):

		self._logClass("listWhere()", clazz, argList)
		tableName = self._getTableName(clazz)

		obj = new.instance(clazz)
		obj.__init__()

		sqlFrom = self._getTableFrom(clazz)
		select = self._getTableSelectClause(obj)

		s = "%s FROM %s T%s WHERE %s" % (
			select,
			tableName,
			sqlFrom,
			whereClause)

		if select.lower().find("sum") >= 0\
		or select.lower().find("count") >= 0:
			groupByList = []
			for name in obj.__dict__.keys():
				if name[0] != "_":
					groupByList.append("T." + name)
			s += " GROUP BY %s" % (string.join(groupByList, ", "))
		
		orderBy = self._getTableOrderBy(clazz)
		if orderBy:
			s += " ORDER BY " + orderBy

		self._logSql(s)
		c = self._conn.cursor()
		c.execute(s, argList)
		result = []
		for t in c.fetchall():
			obj = new.instance(clazz)
			obj.__init__()
			self._updateObjectFromCursor(t, c, obj)
			result.append(obj)
		c.close()

		return result

	def list(self, exampleObject,
	firstResult = 0, maxResults = 100000):

		self._log("list()", exampleObject)
		clazz = exampleObject.__class__
		tableName = self._getTableName(clazz)

		valueList = []
		nameList = []
		for name, value in exampleObject.__dict__.items():
			if value != None and name[0] != "_":
				if isinstance(value, Condition.Condition):
					nameList.append(" AND " +
						value.generateWhereSQL("T." + name))
					valueList += value.generateArgs()
				else:
					nameList.append(" AND T." + name + " = %s")
					valueList.append(value)
		
		sqlFrom = self._getTableFrom(clazz)
		select = self._getTableSelectClause(exampleObject)

		if nameList:
			s = "%s FROM %s T%s WHERE TRUE %s" % (
				select,
				tableName,
				sqlFrom,
				string.join(nameList, ""))
		else:
			s = "%s FROM %s T%s" % (
				select,
				tableName,
				sqlFrom,
			)
		
		if select.lower().find("sum(") >= 0\
		or select.lower().find("count(") >= 0:
			groupByList = []
			for name, value in exampleObject.__dict__.items():
				if name[0] != "_":
					groupByList.append("T." + name)
			s += " GROUP BY %s" % (string.join(groupByList, ", "))
		
		orderBy = self._getTableOrderBy(clazz)
		if orderBy:
			s += " ORDER BY " + orderBy
		
		s += " LIMIT %d OFFSET %d" % (maxResults, firstResult)

		self._logSql(s)
		c = self._conn.cursor()
		c.execute(s, valueList)
		result = []
		for t in c.fetchall():
			obj = new.instance(clazz)
			obj.__init__()
			self._updateObjectFromCursor(t, c, obj)
			result.append(obj)
		c.close()

		return result

	def _updateObjectFromCursor(self, rowData, cursor, obj):

		lowerToAttributeName = {}
		for name in obj.__dict__.keys():
			lowerToAttributeName[name.lower()] = name
		
		for n in range(0, len(rowData)):
			name = cursor.description[n][0].lower()
			if name in lowerToAttributeName:
				obj.__dict__[lowerToAttributeName[name]] = rowData[n]

	def count(self, exampleObject):

		self._log("count()", exampleObject)
		clazz = exampleObject.__class__
		tableName = self._getTableName(clazz)
		idName = self._getIdName(clazz)

		valueList = []
		nameList = []
		for name, value in exampleObject.__dict__.items():
			if value != None and name[0] != "_":
				if isinstance(value, Condition.Condition):
					nameList.append(" AND " +
						value.generateWhereSQL("T." + name))
					valueList += value.generateArgs()
				else:
					nameList.append(" AND T." + name + " = %s")
					valueList.append(value)

		if nameList:
			s = "SELECT COUNT(T.%s) FROM %s T WHERE TRUE %s" % (
				idName,
				tableName,
				string.join(nameList, ","))
		else:
			s = "SELECT COUNT(%s) FROM %s" % (
				idName,
				tableName
			)

		self._logSql(s)
		c = self._conn.cursor()
		c.execute(s, valueList)
		arr = c.fetchone()
		c.close()
		return arr[0]

	def delete(self, exampleObject):

		self._log("delete()", exampleObject)
		tableName = self._getTableName(exampleObject.__class__)

		valueList = []
		nameList = []
		for name, value in exampleObject.__dict__.items():
			if value != None and name[0] != "_":
				nameList.append(name + " = %s")
				valueList.append(value)

		if nameList:
			s = "DELETE FROM %s WHERE %s" % (
				tableName, string.join(nameList, " AND "))
		else:
			raise self.WrongArgumentsException,\
				"to delete all objects use deleteAll(class)"

		self._logSql(s)
		self._logUpdateSql(s, valueList)
		c = self._conn.cursor()
		c.execute(s, valueList)
		c.close()

	def deleteAll(self, clazz):

		self._logClass("deleteAll()", clazz, None)
		tableName = self._getTableName(clazz)
		s = "DELETE FROM %s" % tableName

		self._logSql(s)
		self._logUpdateSql(s, ())
		c = self._conn.cursor()
		c.execute(s)
		c.close()

	def load(self, clazz, objectID):

		self._logClass("load()", clazz, objectID)
		tableName = self._getTableName(clazz)
		objectIDName = self._getIdName(clazz)

		obj = new.instance(clazz)
		obj.__init__()

		selectClause = self._getTableSelectClause(obj)
		s = "%s FROM %s T%s WHERE T.%s = %%s" % (
			selectClause,
			tableName,
			self._getTableFrom(clazz),
			objectIDName)

		if selectClause.lower().find("sum(") >= 0\
		or selectClause.lower().find("count(") >= 0:
			groupByList = []
			for name in obj.__dict__.keys():
				if name[0] != "_":
					groupByList.append("T." + name)
			s += " GROUP BY %s" % (string.join(groupByList, ", "))
		
		self._logSql(s)
		c = self._conn.cursor()
		c.execute(s, [objectID,])
		t = c.fetchone()
		if not t:
			raise self.MissingObjectError, "not found: " + clazz.__name__\
				+ "@" + str(objectID)
		self._updateObjectFromCursor(t, c, obj)
		c.close()

		return obj

	def update(self, objectID, ignoreNone = True):

		self._log("update()", objectID)
		tableName = self._getTableName(objectID.__class__)
		idName = self._getIdName(objectID.__class__)

		valueList = []
		nameList = []
		for name, value in objectID.__dict__.items():
			if name[0] != "_" and name != idName:
				if (not ignoreNone) or value != None:
					nameList.append(name + " = %s")
					valueList.append(value)

		s = "UPDATE %s SET %s WHERE %s = %%s" % (
			tableName,
			string.join(nameList, ","),
			idName)
		valueList.append(objectID.__dict__[idName])

		self._logSql(s)
		self._logSql(repr(valueList))
		self._logUpdateSql(s, valueList)
		c = self._conn.cursor()
		c.execute(s, valueList)
		if not objectID.__dict__[idName]:
			objectID.__dict__[idName] = self._conn.insert_id()
		c.close()

	def save(self, objectID, ignoreNone = True):

		self._log("save()", objectID)
		clazz = objectID.__class__
		tableName = self._getTableName(clazz)
		idName = self._getIdName(clazz)

		self._beforeSaveHook(objectID)

		valueList = []
		nameList = []
		percentList = []
		for name, value in objectID.__dict__.items():
			if name[0] != "_"\
			and (name != idName or value):
				if (not ignoreNone) or value != None:
					nameList.append(name)
					percentList.append("%s")
					valueList.append(value)

		s = "INSERT INTO %s(%s) VALUES(%s)" % (
			tableName,
			string.join(nameList, ","),
			string.join(percentList, ","))

		self._logSql(s)
		self._logUpdateSql(s, valueList)
		c = self._conn.cursor()
		c.execute(s, valueList)
		c.close()

		self._afterSaveHook(objectID)

	def commit(self):

		self._conn.commit()

	def rollback(self):

		self._conn.rollback()

	def _getTableName(self, clazz):

		if clazz.__dict__.has_key("SQL_TABLE"):
			return clazz.__dict__["SQL_TABLE"]
		else:
			return clazz.__name__

	def _getIdName(self, clazz):

		if clazz.__dict__.has_key("DAO_ID"):
			return clazz.__dict__["DAO_ID"]
		else:
			return "id"

	def _getTableFrom(self, clazz):

		if clazz.__dict__.has_key("SQL_FROM"):
			return " " + clazz.__dict__["SQL_FROM"]
		else:
			return ""

	def _getTableOrderBy(self, clazz):

		if clazz.__dict__.has_key("SQL_ORDERBY"):
			return " " + clazz.__dict__["SQL_ORDERBY"]
		else:
			return None

	def _getTableSelectClause(self, obj):

		clazz = obj.__class__

		names = []
		for name in obj.__dict__.keys():
			if name[0] != "_":
				names.append("T." + name)

		sql = "SELECT %s" % string.join(names, ", ")
		if clazz.__dict__.has_key("SQL_SELECT"):
			sql += ", " + clazz.__dict__["SQL_SELECT"]
		
		return sql

	def _logSql(self, text):

		if self._logStream:
			self._logStream.write("    " + text + "\n")
			self._logStream.flush()

	def _beforeSaveHook(self, anObject):

		pass

	def _afterSaveHook(self, anObject):

		pass

	def _logUpdateSql(self, sqlQuery, arguments):

		# TODO: fill implementation
		pass



