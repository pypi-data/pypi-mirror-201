from .gBaseDB import Base, Column, DateTime
from .gBaseDB import Integer, Float 
from .gBaseDB import session
from datetime import datetime

# Declaration of Table

class pVGeneratorPVData(Base):
    
    __tablename__ = 'PV Generator Data'
    
    id = Column(Integer, primary_key=True)
    
    meter_ID = Column(Integer)
    measure_ID = Column(Integer)
    timestamp = Column(DateTime)
    type = Column(Integer)
    n_Phases = Column(Integer)
    chanel = Column(Integer)
    unit = Column(Integer)
    multi_Factor = Column(Integer)
    measure_1 = Column(Float)
    measure_2 = Column(Float)
    measure_3 = Column(Float)



    def __repr__(self):
        return "<PV Generator Data(id = %d, name = %d)>" % (self.id,
                                                self.measure_ID)
    



#returns the list of the data
def listPVGeneratorData():
    return session.query(pVGeneratorPVData).all()

def listPVGeneratorDataByID(id):
    return session.query(pVGeneratorPVData).filter(pVGeneratorPVData.id==id).first()

#Creates a new action (history) of an existent user
def newPVGeneratorData(data):
    # Verify if the type of the arguments is correct

    try:

        id = int(data['id'])
        meter_ID = int(data['meter_ID'])
        measure_ID = int(data['measure_ID'])
        timestamp = datetime.fromisoformat(data['timestamp'])
        type = int(data['type'])
        n_Phases = int(data['n_Phases'])
        chanel = int(data['chanel'])
        unit = int(data['unit'])
        multi_Factor = int(data['multi_Factor'])
        measure_1 = float(data['measure_1'])
        measure_2 = float(data['measure_2'])
        measure_3 = float(data['measure_3'])

 
        meas = pVGeneratorPVData( id = id,
                                meter_ID = meter_ID,
                                measure_ID = measure_ID,
                                timestamp = timestamp,
                                type = type,
                                n_Phases = n_Phases,
                                chanel = chanel,
                                unit = unit,
                                multi_Factor = multi_Factor,
                                measure_1 = measure_1,
                                measure_2 = measure_2,
                                measure_3 = measure_3
        )

        session.add(meas)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(e)
            return -4
    
    
    except:
        return -7
    
    return 0


