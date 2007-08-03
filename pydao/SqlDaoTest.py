"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import unittest

def suite(dao):

	s = unittest.TestSuite()
	for methodName in dir(SqlDaoTest):
		if methodName.startswith("test"):
			s.addTest(SqlDaoTest(dao, methodName))
	return s

class SqlDaoTest(unittest.TestCase):

	def __init__(self, dao, testName):

		unittest.TestCase.__init__(self, testName)
		self.dao = dao

		self.c1 = None
		self.c2 = None
		self.u1 = None
		self.u2 = None
		
	def setUp(self):

		"""
		Build small graph of objecys to test.
		"""

		self.dao.deleteAll(User)
		self.dao.deleteAll(Company)

		self.c1 = Company()
		self.c1.id = 111590
		self.c1.name = "c1"
		self.dao.save(self.c1)
		assert self.c1.id

		self.c2 = Company()
		self.c2.name = "c2"
		self.dao.save(self.c2)

		self.u1 = User()
		self.u1.login = "u1"
		self.u1.companyID = self.c2.id
		self.dao.save(self.u1)

		self.u2 = User()
		self.u2.login = "u2"
		self.dao.save(self.u2)

	def test_missing_SQL_TABLE(self):

		"""
		If SQL_TABLE field is missing use class name.
		(Improve coverage).
		"""

		self.assertEquals(len(self.dao.list(TEST_COMPANY())), 2,
			"read from TEST_COMPANY table")

	def test_listSQL(self):

		"""
		listSQL(): load array of objects from database based on
		SQL query.
		"""

		uList = self.dao.listSQL("""
		SELECT *
		FROM TEST_USER
		""", User)
		self.assertEquals(len(uList), 2,
			"all objects")

	def test_listSQL_arguments(self):

		"""
		listSQL(): load array of objects from database based on
		SQL query with arguments.
		"""

		uList = self.dao.listSQL("""
		SELECT *
		FROM TEST_USER
		WHERE login = %s
		""", User, ["u1"])
		self.assertEquals(len(uList), 1,
			"filtered by login")

	def test_listWhere_group_by(self):

		"""
		listWhere(): load array of objects from database based on
		SQL where clause.
		"""

		cList = self.dao.listWhere("""
		T.name = %s
		""", Company, ["c1"])
		self.assertEquals(len(cList), 1,
			"one object")
		self.assertEquals(cList[0].id, self.c1.id,
			"u1 selected")

	def test_list_aggregation(self):

		"""
		list(): virtual attributes (computed from database queries)
		"""

		c = Company()
		c.id = self.c1.id
		cList = self.dao.list(c)
		self.assertEquals(len(cList), 1,
			"one object")
		self.assertEquals(cList[0]._numberOfUsers, 0,
			"no users in company 1: %s" % cList[0]._numberOfUsers)

		c = Company()
		c.id = self.c2.id
		cList = self.dao.list(c)
		self.assertEquals(len(cList), 1,
			"one object")
		self.assertEquals(cList[0].id, self.c2.id,
			"c2 object selected")
		self.assertEquals(cList[0]._numberOfUsers, 1,
			"number of users in company 2: %s" % cList[0]._numberOfUsers)

	def test_load_aggregation(self):

		"""
		load(): load object with virtual attributes got from
		aggregation functions.
		"""

		c = self.dao.load(Company, self.c2.id)
		self.assertEquals(c._numberOfUsers, 1,
			"value from aggregate function")


class User:

	DAO_ID = "id"
	SQL_SEQUENCE = "TEST_USER_ID"
	SQL_TABLE = "TEST_USER"
	SQL_ORDERBY = "T.id"
	SQL_FROM = "LEFT JOIN TEST_COMPANY TC"\
	    " ON T.COMPANYID = TC.ID"
	SQL_SELECT = "TC.NAME AS _companyName"

	def __init__(self):
		self.id = None
		self.login = None
		self.password = None
		self.companyID = None
		# virtual attribute: not present in database
		self._companyName = None
		self._anotherAttribute = 123

class Company:

	DAO_ID = "id"
	SQL_SEQUENCE = "TEST_COMPANY_ID"
	SQL_TABLE = "TEST_COMPANY"
	SQL_FROM = "LEFT JOIN TEST_USER U ON U.companyID = T.id"
	SQL_SELECT = "COUNT(U.id) AS _numberOfUsers"
	SQL_ORDERBY = "_numberOfUsers"

	def __init__(self):
		self.id = None
		self.name = None
		self._anotherAttribute = None
		self._numberOfUsers = None

class TEST_COMPANY:

	DAO_ID = "id"
	SQL_SEQUENCE = "TEST_COMPANY_ID"
	SQL_FROM = "LEFT JOIN TEST_USER U ON U.companyID = T.id"
	SQL_SELECT = "COUNT(U.id) AS _numberOfUsers"
	SQL_ORDERBY = "_numberOfUsers"

	def __init__(self):
		self.id = None
		self.name = None
		self._anotherAttribute = None
		self._numberOfUsers = None


