from glob import glob
from setuptools import setup

package_name = 'ros2_classroom'

setup(
    name=package_name,
    version='2.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/config', glob('config/*.rviz')),
        ('share/' + package_name + '/model/urdf', glob('model/urdf/*.urdf')),
        ('share/' + package_name + '/model/meshes', glob('model/meshes/*')),
    ],
    entry_points={'console_scripts': [
        'basic_publisher = ros2_classroom.basic_publisher:main',
        'basic_subscriber = ros2_classroom.basic_subscriber:main',
        'add_server = ros2_classroom.add_server:main',
        'add_client = ros2_classroom.add_client:main',
        'show_model = ros2_classroom.show_model:main',
    ]},
)
