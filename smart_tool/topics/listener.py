

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import smbus2
import time
import struct
##import Jetson.GPIO as GPIO


bus = smbus2.SMBus(0)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

#Slave Address 2
address_2 = 0x05
dataSize=4

previousCommand=""

   
#while True:
#   data = raw_input("Enter the data to be sent : ")
#   #data_list = list(data)
#    #for i in data_list:
#       #Sends to the Slaves 
#    writeNumber(int(ord(data)))
#    time.sleep(.1)

#    writeNumber(int(0x0A))
#    readNumber()
#    print("hej")
#    time.sleep(.1)
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
        timer_period = 1
        self.tmr = self.create_timer(timer_period, self.timer_callback)
    def chatter_callback(self, msg):
        global previousCommand
        self.get_logger().info('I heard: [%s]' % msg.data)
        if msg.data !=previousCommand :
            
            previousCommand=msg.data            
            print(msg.data)
            writeNumber(int(ord(msg.data)))
            time.sleep(.1)
            writeNumber(int(0x0A))
            #readNumber()
            #data2=get_data()
            #print(get_float(data2,0))
            time.sleep(.1)
            
    def timer_callback(self):

#[0]=state;
#[1]=stage;
#[2]=angle.bytes[0];
#[3]=angle.bytes[1];
#[4]=torqueUni.bytes[0];
#[5]=torqueUni.bytes[1];
#[6]=accelerationX.bytes[0];
#[7]=accelerationX.bytes[1];
#[8]=accelerationX.bytes[2];
#[9]=accelerationX.bytes[3];
#[10]=accelerationY.bytes[0];
#[11]=accelerationY.bytes[1];
#[12]=accelerationY.bytes[2];
#[13]=accelerationY.bytes[3];
#[14]=accelerationY.bytes[0];
#[15]=accelerationY.bytes[1];
#[16]=accelerationY.bytes[2];
#[17]=accelerationY.bytes[3];
#[18]=0;
#[19]=0;
#[20]=0;
        dataList=[]
        for i in range(0,20):
            dataList.append(readNumber())
            time.sleep(0.1)
        #Pick out the numbers            
        state=chr(dataList[0])
        stage=int(dataList[1])
        shorts=struct.unpack('<HH',bytearray(dataList[2:6]))
        angle=shorts[0]
        torque=shorts[1]

        floats=struct.unpack('<fff',bytearray(dataList[6:18]))
        accX=floats[0]
        accY=floats[1]
        accZ=floats[2]


        msg = String()
        msg.data = 'State : {} Stage : {} Angle : {} Torque : {} \n Acceleration X : {:.4} m/s^2 Acceleration Y : {:.4} m/s^2 Acceleration Z : {:.4} m/s^2 Pubnum[{}]'.format(state,stage,angle,torque,accX,accY,accZ,self.i)
        #msg.data = msg2+'Hello World: TOOL{0}'.format(self.i)
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
    print (-1)
    main()
    print (0.0)
