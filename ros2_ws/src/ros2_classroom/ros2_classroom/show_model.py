"""Swap the model shown in RViz: ros2 run ros2_classroom show_model pendulum"""
import sys
from pathlib import Path
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.srv import SetParameters
from ament_index_python.packages import get_package_share_directory

def main():
    folder = Path(get_package_share_directory('ros2_classroom')) / 'model/urdf'
    models = sorted(f.stem for f in folder.glob('*.urdf'))
    if len(sys.argv) != 2 or sys.argv[1] not in models:
        sys.exit(f'Usage: ros2 run ros2_classroom show_model <{"|".join(models)}>')
    model = sys.argv[1]
    # Same mesh path fix as display.launch.py.
    description = (folder / f'{model}.urdf').read_text().replace(
        '../meshes/', 'package://ros2_classroom/model/meshes/')

    rclpy.init()
    node = Node('classroom_show_model')
    client = node.create_client(SetParameters, '/robot_state_publisher/set_parameters')
    if not client.wait_for_service(timeout_sec=5.0):
        raise RuntimeError('robot_state_publisher is not running')
    request = SetParameters.Request()
    request.parameters = [Parameter('robot_description', value=description).to_parameter_msg()]
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
    result = future.result().results[0]
    if not result.successful:
        raise RuntimeError(result.reason)
    # robot_state_publisher republishes /robot_description; RViz and the slider GUI follow it.
    node.get_logger().info(f'RViz now shows {model}')
    rclpy.shutdown()

if __name__ == '__main__': main()
