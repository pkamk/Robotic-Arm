# In order to use, connect power supply and usb to LeArm controller board. Connect Rx to Tx and Tx to Rx (see what arduino
# serial pins are in arduino program) between arduino and robot controller. Connect USB to arduino and upload arduino
# program first. In blender, press spacebar and start the animation player in the view. Then, run this script. Make sure to only 
# run the script one time. Otherwise, running it multuple times will cause COM3 to fail, as there will already be a
# connection on it.
#
# Possible Errors:
# 1. If robotic arm quickly moves back and forth without any external input, check if ground connection is good between
# the arduino and LeArm controller board. Also, check if power connection is good. Another problem could be if robot arm
# is still for too long, the servos could try to overcorrect themselves.
# 2. Use pose mode for controlling claw (bone.009) by selecting armature.001 and switching to pose mode.
# or lock empty.009 object to local axis (press G then Z while selected, not recommended) for controlling claw also.
# 3. Be calm with empty.008 object movements, so that ground wire between LeArm controller and arduino does not disconnect.
# 4. Turn off Snap During Transform for smoothest arm movements.

import bpy
import math
import time

import sys
import serial
import glob
port=''.join(glob.glob("COM3"))
ser = serial.Serial(port,115200)
print("connected to: " + ser.portstr)
    
ob = bpy.data.objects['Armature']
ob1 = bpy.data.objects['Armature.001']
bpy.context.view_layer.objects.active = ob

bpy.ops.object.mode_set(mode='POSE')

offset1=0
offset2=0



def get_local_orientation(pose_bone):
    local_orientation = pose_bone.matrix_channel.to_euler()
    if pose_bone.parent is None:
        return local_orientation
    else:
        x=local_orientation.x-pose_bone.parent.matrix_channel.to_euler().x
        y=local_orientation.y-pose_bone.parent.matrix_channel.to_euler().y
        z=local_orientation.z-pose_bone.parent.matrix_channel.to_euler().z
        return(x,y,z)

def get_local_position(pose_bone):
    local_position = pose_bone.matrix_channel.to_translation()
    if pose_bone.parent is None:
        return local_position
    else:
        x=local_position.x-pose_bone.parent.matrix_channel.to_translation().x
        y=local_position.y-pose_bone.parent.matrix_channel.to_translation().y
        z=local_position.z-pose_bone.parent.matrix_channel.to_translation().z
        return(x,y,z)

def remapAngle(angle, OldMin, OldMax, NewMin, NewMax):
    OldRange = OldMax - OldMin
    NewRange = NewMax - NewMin
    NewAngle = (((angle - OldMin) * NewRange) / OldRange) + NewMin
    return(NewAngle)
    
def sendAngles():
    
    bpy.context.view_layer.objects.active = ob1
    servo1=ob.pose.bones['Bone']
    servo2=ob.pose.bones['Bone.002']
    servo3=ob.pose.bones['Bone.003']
    servo4=ob.pose.bones['Bone.004']
    servo5=ob.pose.bones['Bone.005']
    servo6=ob1.pose.bones['Bone.009']
      
    angle1=round(math.degrees(get_local_orientation(servo1)[2])+offset1)  #[0]=x,[1]=y,[2]=z
    angle2=round(math.degrees(get_local_orientation(servo2)[1])+offset2)
    angle3=round(math.degrees(get_local_orientation(servo3)[1])+offset2)
    angle4=round(math.degrees(get_local_orientation(servo4)[1])+offset2)
    angle5=round(math.degrees(get_local_orientation(servo5)[2])+offset2)
    angle6=round((get_local_position(servo6)[2]+offset2),2) #is a postion matrix since claw is adjusted by position of bone
    
    if -90<angle1<90:
        trueAngle1 = str(round(remapAngle(angle1, -90, 90, 500, 2500)))
    trueAngle2 = str(round(remapAngle(angle2, 90, -90, 500, 2500)))
    trueAngle3 = str(round(remapAngle(angle3, -90, 90, 500, 2500)))
    trueAngle4 = str(round(remapAngle(angle4, -90, 90, 500, 2500)))
    trueAngle5 = str(round(remapAngle(angle5, -90, 90, 500, 2500)))
    trueAngle6 = str(round(remapAngle(angle6, 0, 1.2, 1500, 2500)))
    print( "%s  %s  %s  %s  %s  %s \n" %( trueAngle1, trueAngle2, trueAngle3, trueAngle4, trueAngle5, trueAngle6 ) )

    ser.write(("DUMM,"+trueAngle1+','+trueAngle2+','+trueAngle3+','+trueAngle4+','+trueAngle5+','+trueAngle6+'|').encode('UTF-8'))
    # print( " %s \n " % ser.readline())
    
def frameChange(passedScene):
    
    sendAngles()
    
bpy.app.handlers.frame_change_pre.append(frameChange)