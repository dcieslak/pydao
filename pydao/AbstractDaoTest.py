"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import unittest
import LikeCondition
import IsNullCondition
import NotNullCondition
import InRangeCondition
import InSequenceCondition
import ArbitraryCondition

def suite(dao):

	s = unittest.TestSuite()
	for methodName in dir(AbstractDaoTest):
		if methodName.startswith("test"):
			s.addTest(AbstractDaoTest(dao, methodName))
	return s

class AbstractDaoTest(unittest.TestCase):

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
		self.dao.deleteAll(BigCompany)

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
		self.u1.salary = 5000
		self.dao.save(self.u1)

		self.u2 = User()
		# two characters in iso-8859-2 used for encoding tests
		self.u2.login = "u2 login \xa3\xb1"
		self.u2.salary = 7000
		self.dao.save(self.u2)

	def test_list(self):

		"""
		list(): load array of objects from database based on example
		object.
		"""

		userExample = User()
		userExample.login = "u2 login \xa3\xb1"
		self.assertEquals(len(self.dao.list(userExample)), 1,
			"one object in database matching query")
		self.assertEquals(self.dao.list(userExample)[0].id, self.u2.id,
			"object u2 listed")
		userExample.login = None
		self.assertEquals(len(self.dao.list(userExample)), 2,
			"two objects in database matching query")

	def test_list_paging(self):

		"""
		list(): check pagination of results
		"""

		userExample = User()
		self.assertEquals(len(self.dao.list(userExample, firstResult=1)), 1,
			"omitted 0th object")
		self.assertEquals(
		len(self.dao.list(userExample, firstResult=2)), 0,
			"omitted first two objects, none remains")
		self.assertEquals(len(self.dao.list(userExample,
		firstResult=0, maxResults=1)), 1,
			"only first")

	def test_list_like(self):

		"""
		list(): load array of objects from database based on example
		object.
		"""

		userExample = User()

		userExample.login = "%\xa3\xb1"
		uList = self.dao.list(userExample)
		self.assertEquals(len(uList), 0,
			"like not enabled")

		userExample.login = LikeCondition.LikeCondition("%\xa3\xb1")
		uList = self.dao.list(userExample)
		self.assertEquals(len(uList), 1,
			"one object in database matching query")
		self.assertEquals(uList[0].login, "u2 login \xa3\xb1",
			"one object in database matching query")

		userExample.login = LikeCondition.LikeCondition("u%")
		uList = self.dao.list(userExample)
		self.assertEquals(len(uList), 2,
			"two objects in database matching query")

	def test_count_like(self):

		"""
		list(): load array of objects from database based on example
		object.
		"""

		userExample = User()

		userExample.login = "%\xa3\xb1"
		self.assertEquals(
		self.dao.count(userExample), 0,
			"like not enabled")

		userExample.login = LikeCondition.LikeCondition("%\xa3\xb1")
		self.assertEquals(
		self.dao.count(userExample), 1,
			"one object in database matching query: %s" %
			self.dao.count(userExample))

		userExample.login = LikeCondition.LikeCondition("u%")
		self.assertEquals(
		self.dao.count(userExample), 2,
			"two objects in database matching query")

	def test_list_from_empty_table(self):

		"""
		list(): load data from empty table.
		"""

		self.dao.deleteAll(BigCompany)

		self.assertEquals(self.dao.count(BigCompany()), 0,
			"no records found: " + `self.dao.count(BigCompany())`)
		self.assertEquals(self.dao.list(BigCompany()), [],
			"no records found: " + `self.dao.list(BigCompany())`)

	def test_IsNullCondition(self):

		"""
		list(): check for NULL fields.
		"""

		u = User()
		u.companyID = IsNullCondition.IsNullCondition()
		self.assertEquals(self.dao.count(u), 1,
			"one object matches")
		self.assertEquals(self.dao.list(u)[0].login, "u2 login \xa3\xb1",
			"u2.companyID IS NULL")

	def test_NotNullCondition(self):

		"""
		list(): check for NOT NULL fields.
		"""

		u = User()
		u.companyID = NotNullCondition.NotNullCondition()
		self.assertEquals(self.dao.count(u), 1,
			"one object matches")
		self.assertEquals(self.dao.list(u)[0].login, "u1",
			"u2.companyID IS NOT NULL")

	def test_InRange(self):

		"""
		list(): check for value in range (BETWEEN operator)
		"""

		u = User()
		u.salary = InRangeCondition.InRangeCondition(5000, 6900)
		self.assertEquals(self.dao.count(u), 1,
			"one object matches: %s" % self.dao.count(u))
		self.assertEquals(self.dao.list(u)[0].login, "u1",
			"u1.salary is in range")

		u.salary = InRangeCondition.InRangeCondition(5000, 7000)
		self.assertEquals(self.dao.count(u), 2,
			"two objects matches")

		u.salary = InRangeCondition.InRangeCondition(5001, 7000)
		self.assertEquals(self.dao.count(u), 1,
			"one object matches")
		login = self.dao.list(u)[0].login
		self.assertEquals(login, "u2 login \xa3\xb1",
			"u2.salary is in range: %s" % `login`)

	def test_InSequenceCondition(self):

		"""
		list(): check for value in given sequence
		"""

		isc = InSequenceCondition.InSequenceCondition()
		isc.addValue(5000)
		u = User()
		u.salary = isc
		self.assertEquals(self.dao.count(u), 1,
			"one object matches: %s" % self.dao.count(u))
		self.assertEquals(self.dao.list(u)[0].login, "u1",
			"u1.salary is in range")

		isc.addValue(10000)
		self.assertEquals(self.dao.count(u), 1,
			"still only one object matches")

		isc.addValue(7000)
		self.assertEquals(self.dao.count(u), 2,
			"two objects match")

	def test_multi_field_filtering(self):

		"""
		list(): load array of objects from database based on example
		object.
		"""

		userExample = User()
		userExample.login = "u1"
		userExample.companyID = self.c2.id
		self.assertEquals(len(self.dao.list(userExample)), 1,
			"one object in database matching query")

	def test_count(self):

		"""
		count(): count objects in database based on example object.
		"""

		userExample = User()
		userExample.login = "u2 login \xa3\xb1"
		self.assertEquals(self.dao.count(userExample), 1,
			"one object in database matching query")
		userExample.login = None
		self.assertEquals(self.dao.count(userExample), 2,
			"two objects in database matching query")

	def test_delete_empty_filter(self):

		"""
		delete(): delete objects from database based on example object.
		"""

		userExample = User()
		try:
			self.dao.delete(userExample)
			raise Exception, "shouldn't be here"
		except self.dao.WrongArgumentsException:
			return

	def test_delete(self):

		"""
		delete(): delete objects from database based on example object.
		"""

		userExample = User()
		userExample.login = "u1"
		self.dao.delete(userExample)
		self.assertEquals(len(self.dao.list(User())), 1,
			"one object remaining in DB")
		self.assertEquals(self.dao.list(User())[0].id, self.u2.id,
			"object u2 not deleted")

	def test_load(self):

		"""
		load(): load one object from database based on primary key.
		"""

		obj = self.dao.load(Company, self.c1.id)
		self.assertEquals(obj.id, self.c1.id,
			"check id if correct")
		self.assertEquals(obj.name, "c1",
			"check id if correct")

	def test_load_missingObject(self):

		"""
		load(): load one object from database based on primary key.
		"""

		try:
			self.dao.load(Company, 1000000001)
			self.assert_(False)
		except self.dao.MissingObjectError:
			return

	def test_update_nonexistent(self):

		"""
		update(): udpate not existing entity
		"""

		try:
			c = BigCompany()
			c.id = 100000001
			c.name = "ASDF"
			self.dao.update(c)
		except self.dao.MissingObjectError:
			return

	def test_load2_one_attribute(self):

		"""
		load2(): loading objects by example object.
		"""

		c = Company()
		c.name = self.c1.name
		obj = self.dao.load2(c)
		self.assertEquals(obj.id, self.c1.id,
			"check id if correct")
		self.assertEquals(obj.name, "c1",
			"check if data loaded")

	def test_load2_many_attributes(self):

		c = Company()
		c.id = self.c1.id
		c.name = self.c1.name
		obj = self.dao.load2(c)
		self.assertEquals(obj.id, self.c1.id,
			"check id if correct")

	def test_update(self):

		"""
		update(): update database state based on current object state.
		"""

		obj = self.dao.load(Company, self.c1.id)
		obj.name = "ASDF"
		self.dao.update(obj)

		obj = self.dao.load(Company, self.c1.id)
		self.assertEquals(obj.name, "ASDF",
			"data updated")
		
		# code coverage
		self.dao.commit()
		self.dao.rollback()

	def test_joined_data(self):

		"""
		load(), list(): check if joined data is visible aflter
		loading/listing.
		"""

		obj = self.dao.load(User, self.u1.id)
		self.assertEquals(obj._companyName, "c2",
			"data from joined class: %s" % obj._companyName)
		
		obj2 = User()
		obj2.id = obj.id
		objList = self.dao.list(obj2)
		self.assertEquals(objList[0]._companyName, "c2",
			"data from joined class")

	def test_save(self):

		"""
		save(): checks if object attributes are saved.
		"""

		self.dao.deleteAll(User)

		u = User()
		u.login = "u1"
		self.dao.save(u)
		self.assert_(u.id,
			"dentifier filled")
		userExample = User()
		self.assertEquals(len(self.dao.list(userExample)), 1,
			"one object in database")

		u = User()
		u.login = "u2 login \xa3\xb1"
		self.dao.save(u)
		self.assertEquals(len(self.dao.list(userExample)), 2,
			"two objects in database")

	def test_ArbitraryCondition(self):

		"""
		ArbitraryCondition.
		"""

		ac = ArbitraryCondition.ArbitraryCondition()
		u = User()
		u.salary = ac
		self.assertEquals(self.dao.count(u), 2,
			"two object matches: %s" % self.dao.count(u))
		
		ac.addCriteria(
			"T.salary <= %s",
			lambda obj, args: obj.salary <= args[0],
			[5000.0])
		self.assertEquals(self.dao.count(u), 1,
			"one object matches: %s" % self.dao.count(u))

def _userLoad(dao, user):

	if user.companyID:
		c = dao.load(Company, user.companyID)
		user._companyName = c.name

class User:

	DAO_ID = "id"
	SQL_SEQUENCE = "TEST_USER_ID"
	SQL_TABLE = "TEST_USER"
	SQL_FROM = "LEFT JOIN TEST_COMPANY TC"\
		" ON T.COMPANYID = TC.ID"
	SQL_SELECT = "TC.NAME AS _companyName"
	INMEMORY_LOAD = _userLoad

	def __init__(self):
		self.id = None
		self.login = None
		self.salary = None
		self.password = None
		self.companyID = None
		# virtual attribute: not present in database
		self._companyName = None
		self._anotherAttribute = 123

class Company:

	DAO_ID = "id"
	SQL_SEQUENCE = "TEST_COMPANY_ID"
	SQL_TABLE = "TEST_COMPANY"

	def __init__(self):
		self.id = None
		self.name = None
		self._anotherAttribute = "XYZ"

class BigCompany:

	SQL_SEQUENCE = "TEST_COMPANY_ID"
	SQL_TABLE = "TEST_COMPANY"

	def __init__(self):
		self.id = None
		self.name = None

