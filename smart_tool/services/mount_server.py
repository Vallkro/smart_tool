#Based on Add_two_ints_server
#http://www.apache.org/licenses/LICENSE-2.0

from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class mountServer(Node):

    def __init__(self):
        super().__init__('mount_server')
        self.srv = self.create_service(AddTwoInts, 'mount', self.mount_callback)

    def mount_callback(self, request, response):
	#------------------CODE GOES HERE---------------------

        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response


def main(args=None):
    rclpy.init(args=args)

    node = mountServer()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - Done automatically when node is garbage collected)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
