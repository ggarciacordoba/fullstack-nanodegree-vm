from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name="Pizzeria Victor")
session.add(myFirstRestaurant)
session.commit()

mySecRestaurant = Restaurant(name="Mc Donalds")
session.add(mySecRestaurant)
session.commit()

session.query(Restaurant).all()

cheesePizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingredients and fresh Mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(cheesePizza)
session.commit()
session.quert(MenuItem).all()

pepperoniPizza = MenuItem(name = "Pepperoni Pizza", description = "Made with all natural ingredients, salami and fresh Mozzarella", course = "Entree", price = "$8.99", restaurant = myFirstRestaurant)
session.add(pepperoniPizza)
session.commit()
session.quert(MenuItem).all()

muzzaPizza = MenuItem(name = "Muzzarella Pizza", description = "The most basic pizza", course = "Desert", price = "$5.00", restaurant = myFirstRestaurant)
session.add(muzzaPizza)
session.commit()
session.quert(MenuItem).all()

bigMac = MenuItem(name = "Big Mac", description = "Most popular hamburger", course = "Desert", price = "$3.00", restaurant = mySecRestaurant)
session.add(bigMac)
session.commit()
session.quert(MenuItem).all()

angus = MenuItem(name = "Angus", description = "Most tasty hamburger", course = "Desert", price = "$10.00", restaurant = mySecRestaurant)
session.add(angus)
session.commit()

frenchFrites = MenuItem(name = "French Frites", description = "The best company for the hamburger", course = "Entree", price = "$1.75", restaurant = mySecRestaurant)
session.add(frenchFrites)
session.commit()
