import sys
sys.path.append("lib")

import ConfigParser
import MySQLdb
import psycopg
import cStringIO
import pydao.InMemoryDao
import pydao.MysqlDao
import pydao.PostgresqlDao
import pydao.SqlDao
import pydao.AbstractDaoTest
import pydao.SqlDaoTest
import unittest
import warnings

import contract

warnings.resetwarnings()
warnings.filterwarnings("error")

if __name__ == "__main__":

	logStream = cStringIO.StringIO()
	#logStream = sys.stderr
	verbosity = 1

	updateSqlStream = cStringIO.StringIO()

	contract.checkmod(pydao.AbstractDao)
	contract.checkmod(pydao.InMemoryDao)
	contract.checkmod(pydao.SqlDao)
	contract.checkmod(pydao.MysqlDao)
	contract.checkmod(pydao.PostgresqlDao)

	testSuite = unittest.TestSuite()

	if 1:
		dao = pydao.InMemoryDao.InMemoryDao(logStream)
		testSuite.addTest(pydao.AbstractDaoTest.suite(
			dao))

	TEST_ENCODING = 1
	if TEST_ENCODING:
		connUnicode = MySQLdb.connect(
			host = "localhost",
			user = "pydao",
			passwd = "pydao",
			db = "pydao",
			use_unicode = True,
			charset = "latin2")
		dao = pydao.MysqlDao.MysqlDao(connUnicode,
			logStream = logStream,
			updateSqlStream = updateSqlStream,
			encoding = "iso-8859-2")
		testSuite.addTest(pydao.AbstractDaoTest.suite(dao))
		testSuite.addTest(pydao.SqlDaoTest.suite(dao))
	else:
		connRaw = MySQLdb.connect(
			host = "localhost",
			user = "pydao",
			passwd = "pydao",
			db = "pydao",
			use_unicode = False,
			charset = "latin2")
		dao = pydao.MysqlDao.MysqlDao(connRaw,
			logStream = logStream,
			updateSqlStream = updateSqlStream)
		testSuite.addTest(pydao.AbstractDaoTest.suite(dao))
		testSuite.addTest(pydao.SqlDaoTest.suite(dao))

	if 1:
		conn = psycopg.connect("dbname=template1 user=postgres")
		dao = pydao.PostgresqlDao.PostgresqlDao(conn,
			logStream = logStream,
			updateSqlStream = updateSqlStream)
		testSuite.addTest(pydao.AbstractDaoTest.suite(dao))
		testSuite.addTest(pydao.SqlDaoTest.suite(dao))

	# ---------------------------------
	if 0:
		testSuite = unittest.TestSuite()
		testSuite.addTest(
			pydao.AbstractDaoTest.AbstractDaoTest(dao,
			"test_ArbitraryCondition"))

	unittest.TextTestRunner(verbosity=verbosity).run(testSuite)

