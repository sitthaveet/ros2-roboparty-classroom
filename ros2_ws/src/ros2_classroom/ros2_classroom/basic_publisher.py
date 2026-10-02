"""Publish a mock camera image as a String once per second. Change the text and run again."""
import random
import string
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MockCamera(Node):
    def __init__(self):
        super().__init__('classroom_camera')
        self.publisher = self.create_publisher(String, '/camera/camera/color/image_raw', 10)
        self.timer = self.create_timer(1.0, self.tick)

    def tick(self):
        image = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        msg = String()
        msg.data = f'hello world, here is the image: {image}'
        self.publisher.publish(msg)
        self.get_logger().info(msg.data)

def main():
    rclpy.init()
    try:
        rclpy.spin(MockCamera())
    except KeyboardInterrupt:  # Ctrl+C
        pass

if __name__ == '__main__': main()
