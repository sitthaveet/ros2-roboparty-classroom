"""A callback runs whenever a matching message arrives."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Viewer(Node):
    def __init__(self):
        super().__init__('classroom_viewer')
        self.subscription = self.create_subscription(
            String, '/camera/camera/color/image_raw', self.receive, 10)

    def receive(self, msg):
        self.get_logger().info(f'Received: {msg.data}')

def main():
    rclpy.init()
    try:
        rclpy.spin(Viewer())
    except KeyboardInterrupt:  # Ctrl+C
        pass

if __name__ == '__main__': main()
