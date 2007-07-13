
	    PyDAO - Python ORM (Object Relational Mapper)

			   Dariusz Cieslak
		    cieslakd@users.sourceforge.net

PyDAO is very thin object-relational mapper similar to Hibernate (but
much simpler). It's created to speed-up application development. It's
very simple, but powerful, based on POPO (Plain Old Python Objects).

Main features:

 - can use any database that has DB-API interface (MySQLdb, psycopg
   tested)
 - can work without database at all (useful for early phases of
   development)
 - speeds up unit testing (dedicated in memory database)

What is not handled:

 - automatic scheme generation
 - separate query language
 - automated handling of associations (replaced by filtering by
   foreign keys)

Here's an example how to use PyDAO:

    class User:
        def __init__(self):
            self.id = None
            self.login = None
            self.password = None

    dao = pydao.InMemoryDao()

    # filling database
    user = User()
    user.login = "user1"
    user.password = "roh8OoPh"
    dao.save(user)

    # filtering based on example
    userSearch = User()
    userSearch.login = "user1"
    userList = dao.list(userSearch)

    # updating
    user.password = "eew8Me8g"
    dao.update(user)

Enjoy!
