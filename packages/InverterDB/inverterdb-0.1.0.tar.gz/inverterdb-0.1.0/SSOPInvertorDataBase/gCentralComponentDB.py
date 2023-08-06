#%%
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
# -7 ->
# -8 ->

# gBaseDB imports
from .gBaseDB import Base, session
from .gBaseDB import Column,String,Integer, createTable
# Other tables imports
# There are three functions for every table:
# Create new entry on the table, list things on the table and look for a specific ID on the table

from .sInvertorData    import listInvertorData, listInvertorDataByID, newInvertorData 

#For the user, we need someone to fix bugs so it prints on the terminal a issue solver
EMERGENCY_CONTACT = "Instituto Superior Técnico"


# Tables and datatype implemented or yet to be implemented
# #
dataTypesAvailable = ["invertorData"]




# Declaration of Central Table:
# This table has all the flow of information that comes in and out
#%%

class allPayLoads(Base):
    
    __tablename__ = 'All Payloads'
    # This should be uncommented if the tables changes
    __table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    topic = Column(String)
    iotDeviceID = Column(String)
    dataType = Column(String)


    def __repr__(self):
        return "All Payloads : {{ sid : %d, topic : %s, IoT Device ID : %s, dataType : %s)}}" % (
            self.id, self.topic,
            self.iotDeviceID, self.dataType)


#Create a table in the database with the allPayLoads
#Functions from the gBaseDB
createTable()



#
#List Functions: All the funtions that retrieve information from databases
#

#%% 
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

            if dataType == "invertorData":
                return listInvertorData()
        
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
            if entry.dataType == "invertorData":
                return listInvertorDataByID(ID)
                    
            else:
                print("Something happen when tried to write that ID in the correct table! Not valid!")
                return -5

        except:

            print("Couldn't access data on the database of specific table!")
            return -1











# %% 
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

def checkDataType(dataType):

    for a in dataTypesAvailable:

        if a == dataType:
            return 1

    return 0

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def table2dict(table):

    d = { 'data' : [] }

    for i in range(100000000):
        
        try:
           d['data'].append(row2dict(table.pop(0)))

        except IndexError:
            return d
        except Exception as e:
            print(e)
            return -1

    return d


#%% New data
# #
# 
# Add Rows o the right places in the database
# 
# 


#To add a new payload, first creates an attemp of access data in the main table,
# Then, if the informatio is correct, it creates the entry in the right table with the dataType given 



def newPayload(topic, iotDeviceID, dataType, data):
    
    # Verify if the type of the arguments is correct
    if not (isinstance(topic,str) and isinstance(iotDeviceID,str) and isinstance(dataType,str) and isinstance(data,dict)): 
        print("Type of argument/arguments is not correct!")
        return -2
        
    else:     
        if not checkDataType(dataType):
            print("dataType argument does not exist! Try an existing dataType!")
            return -2

        newPayload = allPayLoads(topic = topic, iotDeviceID = iotDeviceID, dataType = dataType )
        session.add(newPayload)

        try:
            session.commit()
        except:
            session.rollback()
            print("Could not create that entry on main database do to database error! Contact {}.".format(EMERGENCY_CONTACT))
            return -6
        
        data['id'] = newPayload.id

        try:
            if dataType == "invertorData":
                result = newInvertorData(data)
                if 0 >  result:
                    deleteEntryByID(data['id'])
            
                    
            else:
                print("Data type not valid because functions not implemented!!! However it is in the available dataTypes. Contact {%s}".format(EMERGENCY_CONTACT) )
                return -4

        except Exception as e:
            deleteEntryByID(data['id'])
            print("Couldn't write data on the database. Database error!")
            return -1
        
    
    return result




