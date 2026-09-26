from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    share = Path(get_package_share_directory('ros2_classroom'))
    # Keep upstream URDF untouched; resolve relative meshes for RViz at runtime.
    description = (share / 'model/urdf/rpo.urdf').read_text().replace(
        '../meshes/', 'package://ros2_classroom/model/meshes/')
    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             respawn=True, respawn_delay=2.0),
    ])
