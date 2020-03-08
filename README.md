# MQTT Mini Project

**MQTT Mini Project** for CPE314 COMPUTER NETWORK. Implement MQTT by socket library in python

## Spec Required
- python 3.7+

## How to run
### Run Broker
```
$ python broker.py {ip-broker}:{port-broker}?
```
NOTE: `port-broker` is optional, default 5000

### Run Client
```
$ python client.py
$ {type-connection} {ip-broker}:{port-broker}? {room-topic} {message}?
```
NOTE: `type-connection`: *publish* or *subscribe*, alias name is *pub* and *sub*

NOTE: `port-broker` is optional, default 500

NOTE: `message` allow only publish type


## Syntax

Client --> Broker
```
{pub/sub} {room} {message}?only publish
```

Broker --> Client
```
{port}:{message}
```

