# coding: UTF-8

import json
import paho.mqtt.client as mqtt
from evdev import InputDevice, categorize, ecodes, KeyEvent
import inspect
import time
import sys
import os

def main():
    recieve_time = 0
    # パラメータをファイルから読み込み
    script_dir = os.path.abspath(os.path.dirname(__file__))
    f = open(script_dir + "/MQTT_param.json","r")
    param = json.load(f)

    host = param["MQTT_IP"]
    port = param["MQTT_PORT"]

    topic = "gamepad"

    # インスタンス作成時に protocl v3.1.1を指定
    client = mqtt.Client(protocol=mqtt.MQTTv311)

    client.connect(host, port=port, keepalive=60)
    client.publish("presence","this is gamepad2MQTT.py")

    gamepad = InputDevice('/dev/input/event0')
    #print gamepad.capabilities(verbose=True)
    key_dict = {
        "cross_x":0,
        "cross_y":0,
        "L3D_x":0,
        "L3D_y":0,
        "R3D_x":0,
        "R3D_y":0,
        "RT":0,
        "LT":0,
        "A":0,
        "B":0,
        "Y":0,
        "X":0,
        "RB":0,
        "LB":0,
        "BACK":0,
        "START":0
    }

    recieve_time = time.time()
    while True:
        now = time.time()
        event = gamepad.read_one()

        if now - recieve_time > 2.0:
            print("gamepad no input")
            client.publish("TEST", "gamepad no input")
            client.disconnect()
            print("exit!")
            sys.exit()
            return


        if event is not None:

            code = event.code
            type_ = event.type
            value = event.value

            if(code==0 and type_ ==0 and value == 0):
                continue

            print "------------------"
            print now - recieve_time

            if code == 305:
                key_dict["B"] = value
                print "B_" + str(value)
            elif code == 304:
                key_dict["A"] = value
                print "A_" + str(value)
            elif code == 307:
                key_dict["X"] = value
                print "X_" + str(value)
            elif code == 308:
                key_dict["Y"] = value
                print "Y_" + str(value)
            elif code == 311:
                key_dict["RB"] = value
                print "R_" + str(value)
            elif code == 310:
                key_dict["LB"] = value
                print "L_" + str(value)
            elif code == 5:
                key_dict["RT"] = value
                print "RT_" + str(value)
            elif code == 2:
                key_dict["LT"] = value
                print "LT_" + str(value)
            elif code == 16:
                key_dict["cross_x"] = value
                print "cross_x_" + str(value)
            elif code == 17:
                key_dict["cross_y"] = -value
                print "cross_y_" + str(-value)
            elif code == 2:
                key_dict["LT"] = value
                print "LT_" + str(value)
            elif code == 5:
                key_dict["RT"] = value
                print "RT_" + str(value)
            elif code == 3:
                key_dict["R3D_x"] = value - 128
                print "R3D_x_" + str(value - 128)
            elif code == 4:
                key_dict["R3D_y"] = -value - 129
                print "R3D_y_" + str(-value - 129)
            elif code == 1 and type_ == 3:
                key_dict["L3D_y"] = -value - 129
                print "L3D_y_" + str(-value - 129)
            elif code == 0 and type_ == 3:
                key_dict["L3D_x"] = value - 128
                print "L3D_x_" + str(value - 128)
            elif code == 314:
                key_dict["BACK"] = value
                print "BACK_" + str(value)
            elif code == 315:
                key_dict["START"] = value
                print "START_" + str(value)

            client.publish("gamepad", json.dumps(key_dict))
            recieve_time = time.time()
        usleep = lambda x: time.sleep(x/1000000.0)
        usleep(100) #sleep during 100μs
if __name__ == "__main__":
    main()
