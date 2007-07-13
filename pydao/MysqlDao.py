"""
Author: Dariusz Cieslak, Aplikacja.info
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

	def __init__(self, conn, logStream = None):

		SqlDao.SqlDao.__init__(self, conn, logStream)

	def _beforeSaveHook(self, anObject):

		pass

	def _afterSaveHook(self, anObject):

		idName = self._getIdName(anObject.__class__)
		if not anObject.__dict__[idName]:
			anObject.__dict__[idName] = self._conn.insert_id()


