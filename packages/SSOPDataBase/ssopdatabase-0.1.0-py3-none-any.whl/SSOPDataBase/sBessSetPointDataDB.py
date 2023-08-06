from datetime import datetime
from .gBaseDB import Base, Column, DateTime
from .gBaseDB import Integer, Float
from .gBaseDB import session, createTable

# Declaration of Table

class bessSetPointDataDB(Base):
    
    __tablename__ = 'Bess Set Point Data'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True)

    bESS_ID = Column(Integer)
    timestamp = Column(DateTime)
    type = Column(Integer)
    unit = Column(Integer)
    measure_1 = Column(Float)
    measure_2 = Column(Float)
    measure_3 = Column(Float)


    def __repr__(self):
        return "<Bess Set Point Data(id = %d, name = %d)>" % (self.id,
                                                self.bESS_ID)
    

createTable()

#returns the list of the data
def listBessSetPointData():
    return session.query(bessSetPointDataDB).all()

def listBessSetPointDataByID(id):
    return session.query(bessSetPointDataDB).filter(bessSetPointDataDB.id==id).first()

#Creates a new action (history) of an existent user
def newBessSetPointData(data):
    # Verify if the type of the arguments is correct
    try:

        id = int(data)['id']
        bESS_ID = int(data['bESS_ID'])
        timestamp = datetime.fromisoformat(data['timestamp'])
        type = int(data['type'])
        unit = int(data['unit'])
        measure_1 = float(data['measure_1'])
        measure_2 = float(data['measure_2'])
        measure_3 = float(data['measure_3'])

     
        meas = bessSetPointDataDB( id = id , bESS_ID = bESS_ID, 
                                  timestamp = timestamp, type = type,
                                  unit = unit,
                                  measure_1 = measure_1,
                                  measure_2 = measure_2,
                                  measure_3 = measure_3
        )

        session.add(meas)
        try:
            session.commit()
        except:
            session.rollback()
            return -4


    except:
        return -7


