"""
Copyright: Dariusz Cieslak, Aplikacja.info
http://aplikacja.info
"""

import unittest
import XmlStorageDao

def suite():

    s = unittest.TestSuite()
    for methodName in dir(XmlStorageDaoTest):
        if methodName.startswith("test"):
            s.addTest(XmlStorageDaoTest(methodName))
    return s

class XmlStorageDaoTest(unittest.TestCase):

    def __init__(self, testName):

        unittest.TestCase.__init__(self, testName)
        self.dao = None

    def setUp(self):

        self.dao = XmlStorageDao.XmlStorageDao("test", "iso-8859-2")

    def testRead(self):

        self.dao.deleteAll(User)
        u = User()
        # two iso-8859-2 characters
        u.name = "Jack \xa3\xb1"
        u.age = 32
        self.dao.save(u)
        self.dao.sync()

        dao2 = XmlStorageDao.XmlStorageDao("test", "iso-8859-2")
        u2 = User()
        lista = dao2.list(u2)
        self.assertEquals(len(lista), 1,
            "one object read from XML")
        self.assertEquals(lista[0].name, "Jack \xa3\xb1",
            "object attribute (string)")
        self.assertEquals(lista[0].age, 32,
            "object attribute (int)")

class User:

    def __init__(self):

        self.id = None
        self.name = None
        self.age = None


