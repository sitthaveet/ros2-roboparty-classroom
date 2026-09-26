"""Return one response for each AddTwoInts request."""
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddServer(Node):
    def __init__(self):
        super().__init__('classroom_add_server')
        self.service = self.create_service(AddTwoInts, '/classroom/add', self.add)

    def add(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'{request.a} + {request.b} = {response.sum}')
        return response

def main():
    rclpy.init()
    node = AddServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
