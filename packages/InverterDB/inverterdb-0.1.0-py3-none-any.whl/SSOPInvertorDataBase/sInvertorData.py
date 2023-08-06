from .gBaseDB import Column, String, Float
from .gBaseDB import Integer, DateTime
from .gBaseDB import session 
from .gBaseDB import Base, createTable
from datetime import datetime

# Declaration of Table

class invertorDataBase(Base):
    
    __tablename__ = 'Invertor Data'
    __table_args__ = {'extend_existing': True} 
    
    id = Column(Integer, primary_key=True)
    
    Service = Column(String)
    time = Column(DateTime)
    Begin = Column(DateTime)
    PCon = Column(Float)
    PPV = Column(Float)
    PReqInv = Column(Float)
    PMeaInv = Column(Float)
    PReqBat = Column(Float)
    PMeaBat = Column(Float)
    SoC = Column(Float)
    PCMax = Column(Float)
    PDMax = Column(Float)


    def __repr__(self):
        return "<Data(id = %d, Type Of Service = %s)>" % (self.id, self.Service)
    
createTable()

#returns the list of the  data
def listInvertorData():
    
    return session.query(invertorDataBase).all()

def listInvertorDataByID(id):
    return session.query(invertorDataBase).filter(invertorDataBase.id==id).first()

#Creates a new action (history) of an existent user
def newInvertorData(data):
    # Verify if the type of the arguments is correct
    try:
        id = int(data['id'])
        Service = str(data['Service'])
        time = datetime.fromisoformat(data['time'])
        Begin = datetime.fromisoformat(data['Begin'])
        PCon = float(data['PCon'])
        PPV = float(data['PPV'])
        PReqInv = float(data['PReqInv'])
        PMeaInv = float(data['PMeaInv'])
        PReqBat = float(data['PReqBat'])
        PMeaBat = float(data['PMeaBat'])
        SoC = float(data['SoC'])
        PCMax = float(data['PCMax'])
        PDMax = float(data['PDMax'])


        serSelfC = invertorDataBase( 
                            id = id,
                            Service = Service,
                            time = time,
                            Begin = Begin,
                            PCon = PCon,
                            PPV = PPV,
                            PReqInv = PReqInv,
                            PMeaInv = PMeaInv,
                            PReqBat = PReqBat,
                            PMeaBat = PMeaBat,
                            SoC = SoC,
                            PCMax = PCMax,
                            PDMax = PDMax
        )
        
        session.add(serSelfC)
        try:
            session.commit()
        except:
            session.rollback()
            return -4

        return 0

    except Exception as e:
        print(e)
        return e

