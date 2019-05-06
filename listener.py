import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import smbus2
import time

bus = smbus2.SMBus(0)

# This is the address we setup in the Arduino Program
#Slave Address 1
address = 0x04

#Slave Address 2
address_2 = 0x05
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
    data = ""
    for i in range(0, 10):
            data += chr(bus.read_byte(address_2));
    print (data)
    time.sleep(.01);
    return data    
  


class Listener(Node):

    def __init__(self):
        super().__init__('listener')
        self.sub = self.create_subscription(String, 'chatter', self.chatter_callback)

    def chatter_callback(self, msg):
        self.get_logger().info('I heard: [%s]' % msg.data)
        if msg.data !=previousCommand :
            previousCommand=msg.data            
            print(msg.data)
            writeNumber(int(ord(msg.data)))
            time.sleep(.1)
            writeNumber(int(0x0A))
            readNumber()
            time.sleep(.1)

            
    
    
                


def main(args=None):
    rclpy.init(args=args)

    node = Listener()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
