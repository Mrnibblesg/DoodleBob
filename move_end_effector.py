#!/usr/bin/python3

import sys
import time
import numpy as np
from scipy.spatial.transform import Rotation as R
from interpreter.interpreter import InterpreterHelper

ip = "192.168.56.101"


def genPose(x,y,z,rx,ry,rz):
    pose = [x,y,z,rx,ry,rz]
    return pose

def moveToPose(pose):
    print("moving...")
    interpreter.execute_command("movej("+str(pose)+",a=1,v=1.05,t=0,r=0)")
    time.sleep(1.0)

if __name__ == "__main__":

    
    diff = 0.01

    print("Connecting....")
    interpreter = InterpreterHelper(ip)
    interpreter.connect()
    print("Connected!")
    time.sleep(1.)
    
    for i in range(3):
        pose = genPose(x=-0.3+diff*i,y=-.12,z=-0.25,rx=1.8,ry=2.5,rz=0.)
        moveToPose(pose)

    interpreter.end_interpreter()
