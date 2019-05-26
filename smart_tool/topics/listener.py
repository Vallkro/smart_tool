

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import smbus2
import time
import struct
import os

##import Jetson.GPIO as GPIO


bus = smbus2.SMBus(0)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

#Slave Address 2
address_2 = 0x05
dataSize=4

previousCommand=""
previousButton=2
ROSMode=0

   

def writeNumber(value):
        #bus.write_byte(address, value)
        bus.write_byte(address_2, value)
        # bus.write_byte_data(address, 0, value)
        return -1

def readNumber():
    # number = bus.read_byte(address)
    number = bus.read_byte_data(address_2,dataSize)
    return number
    
def get_data():
    return bus.read_i2c_block_data(address_2,0,16);
  
def get_float(data, index):
    bytes = data[4*index:(index+1)*4]
    return struct.unpack('f', "".join(map(chr, bytes)))[0]

class Listener(Node):
    

    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(String, 'toolListener', self.chatter_callback)
        self.pub = self.create_publisher(String, 'toolState')
        self.i=0
        timer_period = .1
        self.tmr = self.create_timer(timer_period, self.timer_callback)
    def chatter_callback(self, msg):
        global previousCommand
        global ROSMode
        self.get_logger().info('I heard: [%s]' % msg.data)
         
        if msg.data !=previousCommand and ROSMode==1:
            
            previousCommand=msg.data            
            writeNumber(int(ord(msg.data)))
            time.sleep(.01)
            writeNumber(int(0x0A))
            time.sleep(.01)
            
    def timer_callback(self):
        global previousButton
        global ROSMode
        




        #reads GPIO 7 and 8 
        startA='A'
        resetSeq='R'
        f = os.popen('cat /sys/class/gpio/gpio388/value')
        ROSMode=int(f.read())
        f2 = os.popen('cat /sys/class/gpio/gpio298/value')
        buttonHandle=int(f2.read())
        #Buttonhandler
        if ROSMode==0 and buttonHandle==0 and previousButton!=0:
            previousButton=buttonHandle
            writeNumber(int(ord(startA)))
            time.sleep(.01)
            writeNumber(int(0x0A))
            
        
        if ROSMode==0 and buttonHandle==1 :
            previousButton=buttonHandle
            writeNumber(int(ord(resetSeq)))
            time.sleep(.01)
            writeNumber(int(0x0A))
            
        
        # Gather data from Arduino using i2c
        dataList=[]
        for i in range(0,34):
            dataList.append(readNumber())
            time.sleep(0.001)
        #Pick out the numbers 
        #converts bytes to chars and ints           
        state=chr(dataList[0])
        stage=int(dataList[1])
        #unpacks shorts to an array
        shorts=struct.unpack('<HH',bytearray(dataList[2:6]))
        angle=shorts[0]
        omega=shorts[1]
        #unpacks floats to an array 
        floats=struct.unpack('<fffffff',bytearray(dataList[6:34]))
        accX=floats[0]
        accY=floats[1]
        accZ=floats[2]
        gyroX=floats[3]
        gyroY=floats[4]
        gyroZ=floats[5]
        torque=floats[6]

        #Publish the data
        msg = String()
        msg.data = 'Mode : {} State : {} Stage : {} Angle : {} deg Omega : {} rad/s Torque : {:.3} Nm \n Acceleration X : {:.3} m/s^2 Acceleration Y : {:.3} m/s^2 Acceleration Z : {:.3}  m/s^2 \n Gyro X : {:.3} dps Gyro Y : {:.3} dps Gyro Z : {:.3} dps  Pubnum[{}]'.format(ROSMode,state,stage,angle,omega,torque,accX,accY,accZ,gyroX,gyroY,gyroZ,self.i)
        self.i += 1
        self.get_logger().info('Publishing: "{0}"'.format(msg.data))
        self.pub.publish(msg)

            
    
    
                


def main(args=None):
    print(0)
    rclpy.init(args=args)
    print (1)

    node = Listener()
    print (2)
    rclpy.spin(node)
    print (3)

    node.destroy_node()
    print (4)
    rclpy.shutdown()
    print (5)


if __name__ == '__main__':
   
    main()
  
