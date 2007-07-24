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
import OrCondition

def suite(dao):

	s = unittest.TestSuite()
	for methodName in dir(GuideTest):
		if methodName.startswith("test"):
			s.addTest(GuideTest(dao, methodName))
	return s

class GuideTest(unittest.TestCase):

	def __init__(self, dao, testName):

		unittest.TestCase.__init__(self, testName)
		self.dao = dao

	def test_case(self):

		# BEGIN test_simple_insert
		user1 = TEST_USER()
		user1.login = "user1"
		user1.salary = 5000.0
		self.dao.save(user1)

		user2 = TEST_USER()
		user2.login = "user2"
		user2.salary = 7000.0
		self.dao.save(user2)
		# END test_simple_insert

		# BEGIN test_simple_list
		userExample = TEST_USER()
		userExample.login = "user1"
		self.dao.list(userExample)
		# END test_simple_list

		# BEGIN test_simple_update
		userExample = TEST_USER()
		userExample.id = user1.id
		userExample.salary = 6000.0
		self.dao.update(userExample)
		# END test_simple_update

		# BEGIN test_simple_delete
		userExample = TEST_USER()
		userExample.salary = InRangeCondition.InRangeCondition(0, 6500)
		self.dao.delete(userExample)
		# END test_simple_delete


def _userLoad(dao, user):

	if user.companyID:
		c = dao.load(Company, user.companyID)
		user._companyName = c.name

# BEGIN TEST_USER
class TEST_USER:

	def __init__(self):
		self.id = None
		self.login = None
		self.salary = None
		self.password = None
		self.companyID = None
# END TEST_USER

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
		self._anotherAttribute = None

class Company:

	DAO_ID = "id"
	SQL_SEQUENCE = "TEST_COMPANY_ID"
	SQL_TABLE = "TEST_COMPANY"

	def __init__(self):

		self.id = None
		self.name = None
		self._anotherAttribute = None

