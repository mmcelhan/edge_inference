sudo docker create --name forwarder --network hw3 -t -i ab69d63b347d
sudo docker network connect bridge forwarder 
sudo docker exec exit
sudo docker start forwarder
sudo docker exec forwarder apk update
sudo docker exec forwarder apk add python3
sudo docker exec forwarder apk add mosquitto
sudo docker exec forwarder apk add py3-paho-mqtt
sudo docker cp alpine_docker_mqtt/mqtt_subscribe.py forwarder:/home
sudo docker exec -t -d forwarder python3 /home/mqtt_subscribe.py
