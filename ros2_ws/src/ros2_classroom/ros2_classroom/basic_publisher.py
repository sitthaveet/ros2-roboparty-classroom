"""Publish a String once per second. Change the text and run again."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('classroom_talker')
        self.publisher = self.create_publisher(String, '/classroom/chatter', 10)
        self.count = 0
        self.timer = self.create_timer(1.0, self.tick)

    def tick(self):
        msg = String()
        msg.data = f'Hello RoboParty {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(msg.data)
        self.count += 1

def main():
    rclpy.init()
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
