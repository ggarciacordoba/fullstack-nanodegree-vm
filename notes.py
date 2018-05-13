####NOTES####

####ADD ROWS TO A TABLE WITH SQLALCHEMY###
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

#Bind the classes with the tables
Base.metadata.bind = engine
#Creates a sessionmake object to establish a link between the code execution and the engine
DBSession = sessionmaker(bind = engine)
#Create an instance of the DBSession
session = DBSession()

##############################################
#Add a new entry
newEntry = ClassName(property = "value",...)
session.add(newEntry)
session.commit()
##############################################

#Know if the entry was added
session.query(Restaurant).all()

#Read entries
#Get the first Row of a table
firstResult = session.query(Restaurant).first()
firstResult.name

#Get all rows of a table
session.query(Restaurant).all()

#Display a single column for all the rows (With a for loop)
items = session.query(MenuItems).all()
for item in items:
    print item.name

#Get rows from a table filter by a value
session.query(MyClass).filter_by(MyClass.name == 'some name')
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

#Get the burger from urban veggieBurger
urbanVeggieBurger = session.query(MenuItem).filter_by(id = 7).one()
urbanVeggieBurger.price = '$2.99'
session.add(urbanVeggieBurger)
session.commit()

for veggieBurger in veggieBurgers:
    if veggieBurger.price != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()

#Delete an entry from de db
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print spinach.restaurant.name
session.delete(spinach)
session.commit()
