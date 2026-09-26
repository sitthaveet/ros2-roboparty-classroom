"""Wait for the server, send a request, and wait for its future."""
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

def main():
    rclpy.init()
    node = Node('classroom_add_client')
    client = node.create_client(AddTwoInts, '/classroom/add')
    try:
        if not client.wait_for_service(timeout_sec=5.0):
            raise RuntimeError('Start add_server in another terminal first')
        request = AddTwoInts.Request()
        request.a, request.b = 7, 5
        future = client.call_async(request)
        rclpy.spin_until_future_complete(node, future, timeout_sec=5.0)
        if not future.done(): raise TimeoutError('No service response')
        node.get_logger().info(f'Sum = {future.result().sum}')
    finally:
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__': main()
