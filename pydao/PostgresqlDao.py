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

	def __init__(self, conn, logStream = None, updateSqlStream = None):

		"""
		logStream is user to log all queries to database. It can be
		used to track application efficiency (amount of SQL
		generated).

		updateSqlStream is used to render SQL queries that change
		state of database. Those queries can be used to replicate
		database state to another machine.
		"""

		SqlDao.SqlDao.__init__(self, conn, logStream, updateSqlStream)

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

