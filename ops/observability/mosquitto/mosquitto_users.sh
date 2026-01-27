docker run --rm -it -v "$PWD:/mosquitto" eclipse-mosquitto:2.0  mosquitto_passwd -c /mosquitto/passwords telegraf
docker run --rm -it -v "$PWD:/mosquitto" eclipse-mosquitto:2.0  mosquitto_passwd -c /mosquitto/passwords grafana
docker run --rm -it -v "$PWD:/mosquitto" eclipse-mosquitto:2.0  mosquitto_passwd -c /mosquitto/passwords simulator
docker run --rm -it -v "$PWD:/mosquitto" eclipse-mosquitto:2.0  mosquitto_passwd -c /mosquitto/passwords admin