"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import SqlDao

class PostgresqlDao(SqlDao.SqlDao):

	"""
	DAO implemented in MysqlDatabase.

	POPO can have additional class attributes that can reflect
	database structure:

	 - SQL_SEQUENCE sequence name to use for primary key

	"""

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

		clazz = anObject.__class__
		idName = self._getIdName(clazz)
		if not anObject.__dict__[idName]:
			c = self._conn.cursor()
			c.execute("SELECT NEXTVAL('%s')"
				% self._getSequenceName(clazz))
			arr = c.fetchone()
			c.close()
			anObject.__dict__[idName] = arr[0]

	def _afterSaveHook(self, anObject):

		pass

	def _getSequenceName(self, clazz):

		return clazz.__dict__["SQL_SEQUENCE"]

	def _lockTable(self, clazz):

		c = self._conn.cursor()
		tableName = self._getTableName(clazz)
		sqlQuery = "LOCK TABLE %s" % tableName
		self._logSql(sqlQuery)
		c.execute(sqlQuery)
		c.close()

	def _unlockTable(self, anObject):

		c = self._conn.cursor()
		sqlQuery = "COMMIT"
		self._logSql(sqlQuery)
		c.execute(sqlQuery)
		c.close()

