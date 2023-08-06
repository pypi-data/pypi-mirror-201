#%% Warning and information about the code implemention


# Implement database that will store every  information
# This file is the central point of all the database
# Coordinates the flow of information, the type of information that comes in and out. Stores
# all of the information in the database


#ERRORS
# -1 -> Could not connect to the central database
# -2 -> Type of argument not correct
# -3 -> Entry/Table does not exist (or the object that is being search for doesn't exist)
# -4 -> Being implemented ( it is in datatypes available but it is yet to be implemented)
# -5 -> Something unexpected
# -6 -> Could not create entry on the database
# -7 -> Data is not in the correct format
# -8 ->
# -10-> Format saved but it is in wrong format
#%%
# gBaseDB imports
from .gBaseDB import Base, session
from .gBaseDB import Column,String,Integer,DateTime
from .gBaseDB import createTable
from datetime import datetime
# Other tables imports
# There are three functions for every table:
# Create new entry on the table, list things on the table and look for a specific ID on the table

from .sBessMeasurementDataDB    import newBessMeasurementData, listBessMeasurementData, listBessMeasurementDataID 
from .sBessSetPointDataDB       import newBessSetPointData, listBessSetPointData, listBessSetPointDataByID
from .sMeasureDB                import newMeasurement, listMeasurementsData, listMeasurementByID
from .sPVGeneratorData          import newPVGeneratorData, listPVGeneratorData, listPVGeneratorDataByID
from .sPVGeneratorSetPoint      import newPVGeneratorSetPoint, listPVGeneratorSetPoint, listPVGeneratorSetPointByID 
from .sServiceArbitrage         import newServiceArbitrage, listServiceArbitrage, listServiceArbitrageByID
from .sServicePeakShaving       import newServicePeakShaving, listServicePeakShaving, listServicePeakShavingByID
from .sServiceSelfConsumption   import newServiceSelfConsumption, listServiceSelfConsumption, listServiceSelfConsumptionforID
from .sInvertorData             import newInvertorData, listInvertorData, listInvertorDataByID
from .sVariableList             import newVariableList, listVariableList, listVariableListByID

#For the user, we need someone to fix bugs so it prints on the terminal a issue solver
EMERGENCY_CONTACT = "Instituto Superior Técnico"


# Tables and datatype implemented or yet to be implemented
# #
dataTypesAvailable = ["bessMeasurementData",
                   "bessSetPointDataDB",
                   "measurementData",
                   "pVGeneratorData",
                   "pVGeneratorSetPoint",
                   "serviceArbitrage",
                   "ServicePeakShaving",
                   "serviceSelfConsumption",
                   "invertorData",
                   "variableList",
                   ]




#%% # Declaration of Central Table:


# This table has all the flow of information that comes in and out
class allPayLoads(Base):
    
    __tablename__ = 'All Payloads'
    # This should be uncommented if the tables changes
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    iotDeviceID = Column(String)
    dataType = Column(String)
    createdDate = Column(DateTime)
    dump = Column(String)


    def __repr__(self):
        return "All Payloads :  \nsid : %d, \ntopic : %s, \nIoT Device ID : %s, \ndataType : %s, \ncreatedDate : %s, \nDump: %s " % (
            self.id, self.topic,
            self.iotDeviceID, self.dataType, str(self.createdDate), self.dump )


#Create a table in the database with the allPayLoads
#Functions from the gBaseDB
createTable()




#%% #List Functions: All the funtions that retrieve information from databases
 
# Retrieve all the data from the central table
def listData():
    
    
    try:
        return session.query(allPayLoads).all()
    except:
        print("Couldn't return info from database! Contact library owner!")
        return -1

# Retrieve all the data from the dataType table passed as argument  
def listDataByDataType(dataType):
    
    # Verify if the type of the arguments is correct
    if not isinstance(dataType,str): 
        return -2
        
    else: 
        #Checks the dataTypes availale array to check if the user is searching for a existing dataType
        if not checkDataType(dataType):
            return -3

        #tries to go to every table searching for the right dataType
        try:
            if dataType == "bessMeasurementData":
                return listBessMeasurementData()
            elif dataType == "bessSetPointDataDB":
                return listBessSetPointData()
            elif dataType == "measurementData":
                return listMeasurementsData()
            elif dataType == "pVGeneratorData":
                return listPVGeneratorData()
            elif dataType == "pVGeneratorSetPoint":
                return listPVGeneratorSetPoint()
            elif dataType == "serviceArbitrage":
                return listServiceArbitrage()
            elif dataType == "ServicePeakShaving":
                return listServicePeakShaving()
            elif dataType == "serviceSelfConsumption":
                return listServiceSelfConsumption()
            elif dataType == "invertorData":
                return listInvertorData()
            elif dataType == "variableList":
                return listVariableList()
        
            else:
                print("dataType not valid because function doesn't exist!!! However it is in the dataTypesAvailable")
                return -4

        except:
            print("Couldn't access data on the database")
            return -1


# First looks for the entry in the central table
# If success, looks for the entry in the right table (the dataType found).
# If success, retrieves information
def listDataByID(ID):
    
    # Verify if the type of the arguments is correct
    if not isinstance(ID,int): 
        print("Id is not a in the correct format!")
        return -2
        
    else: 

        try:
            entry = session.query(allPayLoads).get(ID)
        except:
            print("Couldn't access to that id! Error in database")
            return -1
        
        if entry == None:
            print("There is no entry with this ID!")
            return -3

        try:
            if entry.dataType == "bessMeasurementData":
                return listBessMeasurementDataID(ID)
            elif entry.dataType == "bessSetPointDataDB":
                return listBessSetPointDataByID(ID)
            elif entry.dataType == "measurementData":
                return  listMeasurementByID(ID)
            elif entry.dataType == "pVGeneratorData":
                return  listPVGeneratorDataByID(ID)
            elif entry.dataType == "pVGeneratorSetPoint":
                return listPVGeneratorSetPointByID(ID)
            elif entry.dataType == "serviceArbitrage":
                return listServiceArbitrageByID(ID)
            elif entry.dataType == "ServicePeakShaving":
                return  listServicePeakShavingByID(ID)
            elif entry.dataType == "serviceSelfConsumption":
                return listServiceSelfConsumptionforID(ID)
            elif entry.dataType == "invertorData":
                return listInvertorDataByID(ID)
            elif entry.dataType == "variableList":
                return listVariableList(ID)
                    
            else:
                print("Something happen when tried to write that ID in the correct table! Not valid!")
                return -5

        except:

            print("Couldn't access data on the database of specific table!")
            return -1












# %% Functions to manipulate data in the database ( tranform into dictionary and delete entries ) 
# #
# 
# Simple Functions: 
# -> Delete one row 
# -> Check all the rows in one dataType
# -> Tranform into dict form 
#
# #

def deleteEntryByID(id):
    
    session.query(allPayLoads).filter_by(id=id).delete()
    session.commit()

def deleteEntryByDate(  endDate, beginDate = datetime(1999,3,14)  ):

    session.query(allPayLoads).filter_by(beginDate< allPayLoads.createdDate).filter_by(endDate>allPayLoads.createdDate).delete()    

def checkDataType(dataType):

    for a in dataTypesAvailable:

        if a == dataType:
            return 1

    return 0

def checkCredentials(iotDeviceID, password):
    #To be implemented
    return 0

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def table2dict(table):

    d = { 'data' : [] }

    for line in range(100000000):
        
        try:
           d['data'].append(row2dict(table.pop(0)))

        except IndexError:
            return d
        except Exception as e:
            print(e)
            return -1

    return d


#%% New data : newPayload Function
# #
# 
# Add Rows o the right places in the database
# 

#To add a new payload, first creates an attemp of access data in the main table,
# Then, if the informatio is correct, it creates the entry in the right table with the dataType given 

def newPayload(topic, iotDeviceID, dataType, data, dumpBool = False):
    
    if dumpBool:

        if not isinstance(data,str): 
            print("Type of argument/arguments is not correct!")
            return -2

        createdData = datetime.now()

        newPayload = allPayLoads(  dump = data, createdDate = createdData )
        session.add(newPayload)

            
        try:
            session.commit()
            return -10
        except Exception as e:
            session.rollback()
            print("Could not create that entry on main database do to database error! Contact {}.".format(EMERGENCY_CONTACT))
            return -6


    # Verify if the type of the arguments is correct
    if not (isinstance(topic,str) and isinstance(iotDeviceID,str) and isinstance(dataType,str) and isinstance(data,dict)): 
        print("Type of argument/arguments is not correct!")
        return -2
        
    else:     
        if not checkDataType(dataType):
            print("dataType argument does not exist! Try an existing dataType!")
            return -2


        createdData = datetime.now()

        newPayload = allPayLoads(topic = topic, iotDeviceID = iotDeviceID, dataType = dataType,  createdDate = datetime.now() )
        session.add(newPayload)

        
        try:
            session.commit() 
        except Exception as e:
            print(e)
            session.rollback()
            print("Could not create that entry on main database do to database error! Contact {}.".format(EMERGENCY_CONTACT))
            return -6
        
        data['id'] = newPayload.id

        try:
            if dataType == "bessMeasurementData":
                result = newBessMeasurementData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "bessSetPointDataDB":
                result = newBessSetPointData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "measurementData":
                result =  newMeasurement(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "pVGeneratorData":
                result =  newPVGeneratorData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "pVGeneratorSetPoint":
                result = newPVGeneratorSetPoint(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "serviceArbitrage":
                result = newServiceArbitrage(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "ServicePeakShaving":
                result =  newServicePeakShaving(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "serviceSelfConsumption":
                result = newServiceSelfConsumption(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "invertorData":
                result = newInvertorData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            elif dataType == "variableList":
                result = newVariableList(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
                    
            else:
                print("Data type not valid because functions not implemented!!! However it is in the available dataTypes. Contact {%s}".format(EMERGENCY_CONTACT) )
                return -4

        except:
            deleteEntryByID(data['id'])
            print("Couldn't write data on the database. Database error!")
            return -1
        
    return result
