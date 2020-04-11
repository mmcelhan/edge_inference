import paho.mqtt.client as mqtt
import sys

local_broker = "broker"  # broker is host name
local_port = 1883  # standard mqtt port
local_topic = "car"  # topic is image


# dictionary of signs
signs = {
    1: {
        "label": "stop_sign",
        "speed": 0
    },
    2: {
        "label": "5_mph",
        "speed": 5
    },
    3: {
        "label": "10_mph",
        "speed": 10
    },
    4: {
        "label": "15_mph",
        "speed": 15
    },
    5: {
        "label": "20_mph",
        "speed": 20
    },
    6: {
        "label": "25_mph",
        "speed": 25
    },
    7: {
        "label": "30_mph",
        "speed": 30
    },
    8: {
        "label": "35_mph",
        "speed": 5
    },
    9: {
        "label": "45_mph",
        "speed": 5
    },
    10: {
        "label": "50_mph",
        "speed": 50
    },
    11: {
        "label": "55_mph",
        "speed": 55
    },
    12: {
        "label": "60_mph",
        "speed": 60
    },
    13: {
        "label": "65_mph",
        "speed": 65
    },
    14: {
        "label": "70_mph",
        "speed": 70
    },
    15: {
        "label": "75_mph",
        "speed": 75
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
        car.new_status(msg)  # change car status
    except:
        print("Unexpected error:", sys.exc_info()[0])


car = Car()
local_mqttclient = mqtt.Client("camera")  # instantiate local client
local_mqttclient.on_connect = on_connect_local  # connect using function call
local_mqttclient.connect(local_broker, local_port, 60)  # connect with inputs
local_mqttclient.on_message = on_message  # execute when message is received

# go into a loop
local_mqttclient.loop_forever()
