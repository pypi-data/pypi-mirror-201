"""
In this code, is developed the library in order to have a communication channel 
between the broker and the publisher
"""







"""
How to publish?

The only function needed to publish to a topic is the "publish" function. In this function, it is going to be sent a message
to a broker in order to be forward to the subscribers.

The function return 1 if the message was sent
Else returns 0


######

PARAMETERS:

topic: is the topic that the client wants to subscribe. This topic has to be separated by slashes ( "/" ) and has to be
between 2 and 10 arguments ("toAsset/deviceID/something/something_else")

information: the information is the message or the body that is going to be sent. It has to be a string.

clientID: Client ID is only a way to diferenciate the people that are accessing the information

username: Yet to be implemented

password: Yet to be implemented



WARNING AND ADVICES:

Make sure the information is in double quotes "" and not in single quotes ''

EXAEMPLES:

from mqtt_SSOP import clientPublisher

if __name__ == '__main__':

    clientPublisher.publish("toAsset/123","Ola tudo bem","IDClient")

######

    

"""










"""
Errors:
1-> To much arguments
2-> Couldn't split arguments correctly
3-> The input in the main funciton is not a string
4-> Couldn't read the input
5-> To few arguments in the topic
6-> Error! Could not send the message to the cloud
7-> Error! Could not send the message to the topic
8-> Topic is not in the correct format ("ssop/#")
"""

from paho.mqtt import client as mqtt_client


#Messges must be shoreter than 10000 carachters
MAX_LEN_MESSAGE = 10000
#The topic given cannot be longer than x arguments
MAX_N_OF_ARGUMENTS = 10
#The topic given cannot be shorter than x arguments
MINIMUM_TOPIC_LENGHT = 1

#Password and username to be implemanted later 
USERNAME = 'selssopcloud2'
PASSWORD = 'jp4dg'

CLOUD_TOPIC = 'ssop/SSOPCloud'


#Online broker information
broker = 'mqtt-broker.smartenergylab.pt'
port = 1883

#Connection to the online broker made available by spider
    
#First it is needed to connect to the broker
def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def sendMessage(client,message,topic):

    try:
        message = str(message)

    except:
        print("Couldn't convert Dict to String")
        return -1

    status = client.publish( CLOUD_TOPIC ,message)[0]
    
    if status != 0:
        print(f"Could not send: \n\n`{message}`\n to the cloud")
        return -6
    else:
        
        status = client.publish(topic, message)[0]
        
        if status != 0:
            print(f"Could not send: \n\n`{message}`\n to topic `{topic}`")
            return -7
        
        return 0


#Main function used to publish topics

def publish(topic,message,client_id, username=USERNAME, password=PASSWORD):
    
    if len(message) > MAX_LEN_MESSAGE:
        exit(-2)

    try:
        splitTopic = topic.split('/', MAX_N_OF_ARGUMENTS)
    except:
        exit(-3)

    if len(splitTopic) < MINIMUM_TOPIC_LENGHT:
        print("To few arguments in the topic")
        exit(-5)

    #if splitTopic[0] != 'ssop':
    #    print("The topic must be in the ssop/# format!")
    #    exit(-8)


    if type(message) is not dict:
        print("Input is not in the correct format: Must be a dictionary")
        exit(-3)
    
    client = connect_mqtt(client_id)
    return sendMessage(client,message,topic)



    #return 1
