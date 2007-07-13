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

import contract

if __name__ == "__main__":

	logStream = cStringIO.StringIO()
	#logStream = sys.stderr
	verbosity = 1

	contract.checkmod(pydao.AbstractDao)
	contract.checkmod(pydao.InMemoryDao)
	contract.checkmod(pydao.SqlDao)
	contract.checkmod(pydao.MysqlDao)
	contract.checkmod(pydao.PostgresqlDao)

	testSuite = unittest.TestSuite()

	dao = pydao.InMemoryDao.InMemoryDao(logStream)
	testSuite.addTest(pydao.AbstractDaoTest.suite(
		dao))

	conn = MySQLdb.connect(
		host = "localhost",
		user = "pydao",
		passwd = "pydao",
		db = "pydao")
	dao = pydao.MysqlDao.MysqlDao(conn, logStream)
	testSuite.addTest(pydao.AbstractDaoTest.suite(dao))
	testSuite.addTest(pydao.SqlDaoTest.suite(dao))

	conn = psycopg.connect("dbname=template1 user=postgres")
	dao = pydao.PostgresqlDao.PostgresqlDao(conn, logStream)
	testSuite.addTest(pydao.AbstractDaoTest.suite(dao))
	testSuite.addTest(pydao.SqlDaoTest.suite(dao))

	# ---------------------------------
	if 0:
		testSuite = unittest.TestSuite()
		testSuite.addTest(
			pydao.AbstractDaoTest.AbstractDaoTest(dao,
			"test_ArbitraryCondition"))

	unittest.TextTestRunner(verbosity=verbosity).run(testSuite)

