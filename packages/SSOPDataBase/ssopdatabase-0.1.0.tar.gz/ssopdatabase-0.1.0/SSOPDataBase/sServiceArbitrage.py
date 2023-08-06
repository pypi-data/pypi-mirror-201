#%%
from .gBaseDB import Base, Column, String, DateTime, Integer
from .gBaseDB import session, createTable 
from datetime import datetime


# Declaration of Table

class serviceArbitrage(Base):
    
    __tablename__ = 'Service Arbitrage'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    
    Type_Of_Service = Column(String)
    Type_Of_Activation = Column(DateTime)
    Price = Column(DateTime)
    Price_Min = Column(DateTime)
    Price_Max = Column(DateTime)

    def __repr__(self):
        return "<Service(id = %d, Type of Service = %s)>" % (self.id,
                                                self.Type_Of_Service)
    

createTable

#%%
#returns the list of the data
def listServiceArbitrage():
    return session.query(serviceArbitrage).all()

def listServiceArbitrageByID(id):
    return session.query(serviceArbitrage).filter(serviceArbitrage.id==id).first()

#Creates a new action (history) of Service
def newServiceArbitrage(data):
    
    # Verify if the type of the arguments is correct
    try:
     
        id = int(data['id'])
        Type_Of_Service = str(data['Type_Of_Service'])
        Type_Of_Activation = datetime.fromisoformat(data['Type_Of_Activation'])
        Price = datetime.fromisoformat(data['Price'])
        Price_Min = datetime.fromisoformat(data['Price_Min'])
        Price_Max = datetime.fromisoformat(data['Price_Max'])
        
    except:
        return -7

    try:    
        serv = serviceArbitrage(id = id , 
                                Type_Of_Service = Type_Of_Service, 
                                Type_Of_Activation = Type_Of_Activation, 
                                Price = Price, Price_Min = Price_Min, 
                                Price_Max = Price_Max
        )

    except:
        return -5

    
    try:
        session.add(serv)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return -4
    return 0
