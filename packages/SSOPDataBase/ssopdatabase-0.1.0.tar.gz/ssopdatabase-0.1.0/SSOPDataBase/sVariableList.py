from .gBaseDB import Column
from .gBaseDB import Integer, Float
from .gBaseDB import session 
from .gBaseDB import Base, createTable

# Declaration of Table

class variableList(Base):
    
    __tablename__ = 'Service Self Consumption'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True)

    voltage_pv1 = Column(Float)
    current_pv1 = Column(Float)
    voltage_pv2 = Column(Float)
    current_pv2 = Column(Float)
    power_active_grid = Column(Float)
    voltage_grid = Column(Float)
    current_grid = Column(Float)
    frquency_grid = Column(Float)
    energy_from_grid = Column(Float)
    energy_to_grid = Column(Float)
    soc = Column(Float)
    capacity = Column(Float)
    voltage_bat = Column(Float)
    current_bat = Column(Float)
    temp_bat = Column(Float)
    soc_target = Column(Float)

    def __repr__(self):
        return "< Variable List : (id = %d)>" % (self.id)
    
createTable

#returns the list of the  data
def listVariableList():
    
    return session.query(variableList).all()

def listVariableListByID(id):
    return session.query(variableList).filter(variableList.id==id).first()

#Creates a new action (history) of an existent user
def newVariableList(data):
    # Verify if the type of the arguments is correct
    try:
        id = int(data['id'])
        voltage_pv1 =               float(data['voltage_pv1'])
        current_pv1 =               float(data['current_pv1'])
        voltage_pv2 =               float(data['voltage_pv2'])
        current_pv2 =               float(data['current_pv2'])
        power_active_grid =         float(data['power_active_grid'])
        voltage_grid =              float(data['voltage_grid'])
        current_grid =              float(data['current_grid'])
        frquency_grid =             float(data['frquency_grid'])
        energy_from_grid =          float(data['energy_from_grid'])
        energy_to_grid =            float(data['energy_to_grid'])
        soc =                       float(data['soc'])
        capacity =                  float(data['capacity'])
        voltage_bat =               float(data['voltage_bat'])
        current_bat =               float(data['current_bat'])
        temp_bat =                  float(data['temp_bat'])
        soc_target =                float(data['soc_target'])


        serSelfC = variableList( 
                            id = id,
                            voltage_pv1 = voltage_pv1,
                            current_pv1 = current_pv1,
                            voltage_pv2 = voltage_pv2,
                            current_pv2 = current_pv2,
                            power_active_grid = power_active_grid,
                            voltage_grid = voltage_grid,
                            current_grid = current_grid,
                            frquency_grid = frquency_grid,
                            energy_from_grid = energy_from_grid,
                            energy_to_grid = energy_to_grid,
                            soc = soc,
                            capacity = capacity,
                            voltage_bat = voltage_bat,
                            current_bat = current_bat,
                            temp_bat = temp_bat,
                            soc_target = soc_target,
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

