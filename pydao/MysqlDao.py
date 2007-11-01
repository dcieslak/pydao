"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import SqlDao
import _mysql_exceptions

class MysqlDao(SqlDao.SqlDao):

	"""
	DAO implemented in MysqlDatabase.

	POPO can have additional class attributes that can reflect
	database structure:

	 - SQL_TABLE name of a table, default = class name
	 - DAO_ID name of primary key, default = "id"

	"""

	IntegrityError = _mysql_exceptions.IntegrityError

	def __init__(self, conn, logStream = None, updateSqlStream = None,
	encoding = None):

		"""
		logStream is user to log all queries to database. It can be
		used to track application efficiency (amount of SQL
		generated).

		updateSqlStream is used to render SQL queries that change
		state of database. Those queries can be used to replicate
		database state to another machine.

		If encoding is set PyDAO assumes that all data sent directly
		to SQL backend and received from SQL backend shoud be Unicode.
		PyDAO accepts and returns in this case strings with selected
		encoding.

		"""

		SqlDao.SqlDao.__init__(self, conn, logStream, updateSqlStream,
			encoding)

	def _beforeSaveHook(self, anObject):

		pass

	def _afterSaveHook(self, anObject):

		idName = self._getIdName(anObject)
		if idName and not anObject.__dict__[idName]:
			anObject.__dict__[idName] = self._conn.insert_id()

	def _lockTable(self, clazz):

		c = self._conn.cursor()
		tableName = self._getTableName(clazz)
		sqlQuery = "LOCK TABLE %s WRITE, %s AS T WRITE" % (
			tableName, tableName)
		self._logSql(sqlQuery)
		c.execute(sqlQuery)
		c.close()

	def _unlockTable(self, anObject):

		c = self._conn.cursor()
		sqlQuery = "UNLOCK TABLES"
		self._logSql(sqlQuery)
		c.execute(sqlQuery)
		c.close()


