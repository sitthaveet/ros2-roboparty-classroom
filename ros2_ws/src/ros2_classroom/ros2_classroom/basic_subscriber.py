"""A callback runs whenever a matching message arrives."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Listener(Node):
    def __init__(self):
        super().__init__('classroom_listener')
        self.subscription = self.create_subscription(
            String, '/classroom/chatter', self.receive, 10)

    def receive(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

def main():
    rclpy.init()
    node = Listener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
