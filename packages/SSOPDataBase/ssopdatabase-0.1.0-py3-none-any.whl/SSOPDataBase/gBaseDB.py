# This file has the initialization of the database.
# It declares the database and then creates it. In addition, 
# has the function that link the tables created into one data base
#
#
# Os imports
import os.path
# sqlalchemy imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



#%%
#SQL access layer initialization
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(BASE_DIR, "database.sqlite")

#Checks if database exists, i.e., if there is a path to the database viable
if os.path.exists(DATABASE_FILE):

    print("################\nInitiating\n################")

# # 
# Initialization protocol where we build a path to the tables and data
# echo:
# if True, the Engine will log all statements as well as a repr() of their parameter lists to the default log handler, 
# which defaults to sys.stdout for output. If set to the string "debug", result rows will be printed to the standard output as well. 
# The echo attribute of Engine can be modified at any time to turn logging on and off; 
# direct control of logging is also available using the standard Python logging module.
# It is kept as false because we wanted a costume data storage and deletion
# Connecr arg is just a parameter than we can pass into the function and access it anytime
# #
engine = create_engine('sqlite:///%s'%(DATABASE_FILE), 
                       echo=False, 
                       connect_args={"check_same_thread": False}
                       ) 
                        

#Standard intializaion, mandatory in order to use the SQLAlchemy database
Session = sessionmaker(bind=engine)
session = Session() 

#Creates the tables that is in the file where we apply the this function
def createTable():
    Base.metadata.create_all(engine)