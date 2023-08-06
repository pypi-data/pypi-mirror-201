from .gBaseDB import Column
from datetime import datetime
from .gBaseDB import Integer, DateTime, Float
from .gBaseDB import session
from .gBaseDB import Base, createTable

# Declaration of Table

class pVGeneratorSetPoint(Base):
    
    __tablename__ = 'PV Generator Set Point'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True)
    
    pV_ID = Column(Integer)
    timestamp = Column(DateTime)
    type = Column(Integer)
    unit = Column(Integer)
    measure_1 = Column(Float)
    measure_2 = Column(Float)
    measure_3 = Column(Float)


    def __repr__(self):
        return "<PV Generator SetPoint(id = %d, Type Of Service = %d)>" % (self.id, self.pV_ID)
    
createTable

#returns the list of the data
def listPVGeneratorSetPoint():
    return session.query(pVGeneratorSetPoint).all()

def listPVGeneratorSetPointByID(id):
    return session.query(pVGeneratorSetPoint).filter(pVGeneratorSetPoint.id==id).first()

#Creates a new action (history) of an existent user
def newPVGeneratorSetPoint(data):
    # Verify if the type of the arguments is correct
    try:
        id = int(data['id'])
        pV_ID = int(data['PV_ID'])
        timestamp = datetime.fromisoformat(data['timestamp'])
        type = int(data['type'])
        unit = int(data['unit'])
        measure_1 = float(data['measure1'])
        measure_2 = float(data['measure2'])
        measure_3 = float(data['measure3'])


        serSelfC = pVGeneratorSetPoint( id = id, pV_ID = pV_ID, timestamp = timestamp, 
                                      type = type, unit = unit,
                                      measure_1 = measure_1, 
                                      measure_2 = measure_2, measure_3 = measure_3
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

