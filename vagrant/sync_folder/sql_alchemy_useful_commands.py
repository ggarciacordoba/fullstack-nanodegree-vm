from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Raise up the database
engine = create_engine('$databaseString')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Add a new element to the table
#Instantiate an object of the Table Class

# myObject = TableClass(attributes)
myFirstRestaurant = Restaurant(name="Pizzeria Victor")
session.add(myFirstRestaurant)
session.commit()

# Query data from the database without filters
# > session.query($TableClass).all()

#All the elements of a query
session.query(Restaurant).all() 

#First element of a query
firstResult = session.query(Restaurant).first()
firstResult.name

#Loop through ordered results
for instance in session.query(Users).order_by(User.id):
    print instance.name,instance.fullname

#Using tuples
for name, fullname in session.query(User.name, User.fullname):
    print name, fullname

for row in session.query(User, User.name):
    print row.User, row.name

# Limit and Offset results
for u in session.query(User).order_by(User.id)[1:3]:
    print u

# Filter results from a column
for name in session.query(User.name).filter_by(fullname = 'Ed Jones'):
    print name

for name in session.query(User.name).filter_by(User.fullname == 'Ed Jones'):
    print name

# Several filters with AND
for user in session.query(User).filter(User.name=='ed').filter(User.fullname=='Ed Jones'):
    print user

# Operators
query.filter(User.name == 'Ed') #Equal
query.filter(User.name != 'Ed') #Not Equal
query.filter(User.name.like('%ed%')) #Like
query.filter(User.name.ilike('%ed%')) #Case Sensitive Like
query.filter(User.name.in_(['ed', 'wendy', 'jack'])) #IN
# works with query objects too:
query.filter(User.name.in_(
    session.query(User.name).filter(User.name.like('%ed%'))
))

query.filter(~User.name.in_(['ed', 'wendy', 'jack'])) #Not In
"""Is null"""
query.filter(User.name == None) #Is Null

# alternatively, if pep8/linters are a concern
query.filter(User.name.is_(None)) #Is Null
"""Is not null"""
query.filter(User.name != None) # Is not null

# alternatively, if pep8/linters are a concern
query.filter(User.name.isnot(None)) # Is not null
"""And"""
# use and_()
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

# or send multiple expressions to .filter()
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

# or chain multiple filter()/filter_by() calls
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')

"""OR"""
from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))
""""""

query.filter(User.name.match('wendy'))

# Delete elements
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
session.delete(spinach)
session.commit()




