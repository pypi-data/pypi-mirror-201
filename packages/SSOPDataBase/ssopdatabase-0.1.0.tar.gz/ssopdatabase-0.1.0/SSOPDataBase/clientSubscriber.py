"""
Errors:
1-> To much arguments
2-> Message to big
3-> Couldn't decode the topic
4-> Couldn't read the info corretly
5-> Couldn't decode the data from the payload
6-> Couldn't write on the database because the whole message was not well structured
7-> Didn't recieve the correct data structure
8-> Credentials are not correct
"""
import json
from time import sleep
from paho.mqtt import client as mqtt_client
from .gCentralComponentDB import newPayload, checkCredentials, listData, listDataByID, listDataByDataType
from .gCentralComponentDB import table2dict, row2dict

#Messges must be shoreter than 10000 carachters
MAX_LEN_MESSAGE = 10000
#The topic given cannot be longer than 10 arguments
MAX_N_OF_ARGUMENTS = 10

#Password and username to be implemanted later 
USERNAME = 'selssopcloud2'    
PASSWORD = 'jp4dg'     
CLOUD_TOPIC = 'ssop/SSOPCloud'

#Online broker information
broker = 'mqtt-broker.smartenergylab.pt'
port = 1883

#Connection to the online broker made available by spider


#First the client needs to connect to the broker
def connect_mqtt(clientID) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(clientID)
    client.username_pw_set(USERNAME,PASSWORD)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

#After the client set up, it can send messages freely
def recieveMessage(client: mqtt_client, topic):
    
    def on_message(client, userdata, msg):

        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print(f"Received message from `{msg.topic}` topic")
        
        try: 
            payload = msg.payload.decode()
            payload = json.loads(payload.replace("\'", "\""))
            
            credentials = dict(payload['credentials'])
            iotDeviceID = str(credentials['ID'])
            secret = str(credentials['password'])
            
            dataType = str(payload['dataType'])
            data = dict(payload['data'])

        except:
            try:
                print("Message format not correct!")
                return newPayload(topic = "NN", 
                       iotDeviceID="NN",
                       dataType="NN", 
                       data = str(msg.payload.decode()), 
                       dumpBool= True
                       )
            except:
                print("Couldn't write the information in the database!")
                return -6
            


        try:

            if checkCredentials(iotDeviceID,secret) != 0:
                return -11

            id = newPayload( topic, iotDeviceID ,dataType, data)
            if id < 1:
                try:
                    
                    print("Message data not correct!")
                    return newPayload("NN","NN","NN", str(msg.payload.decode()), True)
                except:
                    print("Couldn't write the information in the database!")
                    return -6
            else:
                print(f"Data with ID '{id}' correctly created!")
                

        except:
            #print("Something went wrong when mainupulating the database!")
            return -5
        
    client.subscribe(topic)
    client.on_message = on_message



#Function of subscription by function 
def subscribe( topic = CLOUD_TOPIC, username=USERNAME, password=PASSWORD):
    

    try:
        splitTopic = topic.split('/', MAX_N_OF_ARGUMENTS)
    except:
        exit(-3)

    direction = splitTopic[0]
    

    
    # generate client ID with pub prefix randomly

    client = connect_mqtt(clientID = "SSOPCloud")
    #print(recieveMessage(client, topic))
    recieveMessage(client, topic)
    
    client.loop_start()

    sleep(2)
    
    print("Commmands:")
    print("a : List All data from database")
    print("t : List data from database by Data Type")
    print("id: List data from database by ID")
    print("h : Show commands")

    while 1:

        cycle = True

        try:
            command = input()
            
            if command =='a':
                print(table2dict(listData()))

            elif command =='t':
                
                while cycle == True:
                    
                    print("Which type of data? ('e' to exit)\t")
                    command = input()

                    if command == 'e':
                        cycle = False
                    else:
                        try:
                            print(table2dict(listDataByDataType(str(command))))
                        except:
                            print("Invalid input")                        

            elif command =='id':
                
                while cycle == True:
                
                    print("Which ID? ('e' to exit)\t")
                    command = input()
                    
                    if command == 'e':
                        cycle = False
                    else:
                        try:
                            print(row2dict(listDataByID(int(command))))
                        except:
                            print("Invalid input")
                    
            elif command =='h':
                print("Commmands:")
                print("a : List All data from database")
                print("t : List data from database by Data Type")
                print("id: List data from database by ID")
                print("h : Show commands")

            else:
                print("Invalid input")

        except KeyboardInterrupt:
            client.loop_stop()
            return 0
        except:
            print("something went wrong!")
            return -1000

    
