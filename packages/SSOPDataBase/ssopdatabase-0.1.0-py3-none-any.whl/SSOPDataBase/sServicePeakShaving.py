from .gBaseDB import Base, Column,String, DateTime, Integer
from .gBaseDB import session, createTable
from datetime import datetime

# Declaration of Table

class ServicePeakShaving(Base):
    
    __tablename__ = 'Service Peak Shaving'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True)
    
    Type_Of_Service = Column(String)
    Type_Of_Activation = Column(DateTime)
    Min_SOC = Column(DateTime)

    def __repr__(self):
        return "<Service Peak Shaving(id = %d, name = %s)>" % (self.id,
                                                self.Type_Of_Service)
    

createTable

#returns the list of the data
def listServicePeakShaving():
    return session.query(ServicePeakShaving).all()

def listServicePeakShavingByID(id):
    return session.query(ServicePeakShaving).filter(ServicePeakShaving.id==id).first()

#Creates a new action (history) of an existent user
def newServicePeakShaving(data):
    # Verify if the type of the arguments is correct
    
    try: 
        id = int(data['id'])
        Type_Of_Service = str(data['Type_Of_Service'])
        Type_Of_Activation = datetime.fromisoformat(data['Type_Of_Activation'])
        Min_SOC = datetime.fromisoformat(data['Min_SOC'])
       
        serv = ServicePeakShaving( 
                                id = id, 
                                Type_Of_Service = Type_Of_Service, 
                                Type_Of_Activation = Type_Of_Activation,
                                Min_SOC = Min_SOC
        )
        session.add(serv)
        
        try:
            session.commit()
        except:
            session.rollback()
            return -4
    
    except:
        return -7
    
    return 0
