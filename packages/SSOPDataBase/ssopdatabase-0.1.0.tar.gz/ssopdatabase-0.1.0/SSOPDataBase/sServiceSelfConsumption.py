from .gBaseDB import Column,String
from .gBaseDB import Integer, DateTime
from .gBaseDB import session 
from .gBaseDB import Base, createTable
from datetime import datetime

# Declaration of Table

class serviceSelfConsumption(Base):
    
    __tablename__ = 'Service Self Consumption'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True)
    
    Type_Of_Service = Column(String)
    Type_Of_Activation = Column(DateTime)
    SOC_Goal = Column(DateTime)
    Min_SOC = Column(DateTime)


    def __repr__(self):
        return "<Service Self Consumption(id = %d, Type Of Service = %s)>" % (self.id, self.Type_Of_Service)
    
createTable

#returns the list of the  data
def listServiceSelfConsumption():
    
    return session.query(serviceSelfConsumption).all()

def listServiceSelfConsumptionforID(id):
    return session.query(serviceSelfConsumption).filter(serviceSelfConsumption.id==id).first()

#Creates a new action (history) of an existent user
def newServiceSelfConsumption(data):
    # Verify if the type of the arguments is correct
    try:
        id = int(data['id'])
        Type_Of_Service = str(data['Type_Of_Service'])
        Type_Of_Activation = datetime.fromisoformat(data['Type_Of_Activation'])
        SOC_Goal = datetime.fromisoformat(data['SOC_Goal'])
        Min_SOC = datetime.fromisoformat(data['Min_SOC'])

        serSelfC = serviceSelfConsumption( 
                            id = id,                    
                            Type_Of_Service = Type_Of_Service,
                            Type_Of_Activation = Type_Of_Activation,
                            SOC_Goal = SOC_Goal,
                            Min_SOC = Min_SOC 
        )
        
        session.add(serSelfC)
        try:
            session.commit()
        except:
            session.rollback()
            return -4

        return 0

    except:
        return -7

