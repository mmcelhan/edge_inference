import paho.mqtt.client as mqtt
import sys

local_broker = "broker"  # broker is host name
local_port = 1883  # standard mqtt port
local_topic = "signs"  # topic is image

with open("keys.json") as json_file:
    data = json.load(json_file)
    keys = {}
    for i in range(len(data)):
        keys[i] = data[str(i)]

# dictionary of signs
signs = {
    "30": {
        "label": "30_kph",
        "speed":30
    },
    "50": {
        "label": "50_kph",
        "speed":50
    },
    "60": {
        "label": "60_kph",
        "speed": 60
    },
    "70": {
        "label": "70_kph",
        "speed": 70
    },
    "80": {
        "label": "80_kph",
        "speed": 80
    },
    "100": {
        "label": "100_kph",
        "speed": 100
    },
    "120": {
        "label": "120_kph",
        "speed": 120
    },
    "Deer": {
        "label": "Deer",
        "speed": 0
    },
    "Stop": {
        "label": "Stop",
        "speed": 0
    },
    "Yield": {
        "label": "Yield",
        "speed": 0
    }
}


car_status = {
    1: "staying the same speed",
    2: "speeding up",
    3: "slowing down"
}


class Car:
    """
    class the simulates are self driving car
    """

    def __init__(self):
        """
        initiation class for self driving car
        sets speed to 0 mph and status as staying the same speed
        """

        self.speed = 0
        self.status = 1
        return None

    def new_status(self, input):
        """
        setter that allows for the self driving car to change state based on inputs
        :param input: integer from mqtt
        :return: None
        """

        print("The sign seen is ", signs[input]["label"])

        new_speed = signs[input]["speed"]
        if new_speed < self.speed:
            print("slowing down")
            self.status = 3
        elif new_speed == self.speed:
            print("staying the same speed")
            self.status = 1
        else:
            print("speeding up")
            self.status = 2

        self.speed = new_speed

        return None  # end new status


def on_connect_local(client, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(local_topic)  # subscribe to local topic
        return None  # end function


def on_message(msg):
    try:
        print("message received!")	
        msg = msg.payload  # create message
        print(msg)  # confirm message receipt, turn off for production
        car.new_status(keys[msg])  # change car status
    except:
        print("Unexpected error:", sys.exc_info()[0])

 
        
car = Car()
local_mqttclient = mqtt.Client()  # instantiate local client
local_mqttclient.on_connect = on_connect_local  # connect using function call
local_mqttclient.connect(local_broker, local_port, 60)  # connect with inputs
local_mqttclient.on_message = on_message  # execute when message is received

# go into a loop
local_mqttclient.loop_forever()
