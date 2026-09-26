"""Integration checks against the running classroom container."""
import time
import subprocess
import os
import signal
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from pathlib import Path
import xml.etree.ElementTree as ET
from ament_index_python.packages import get_package_share_directory
from tf2_ros import Buffer, TransformListener
from std_msgs.msg import String
from example_interfaces.srv import AddTwoInts

rclpy.init()
n = Node('classroom_smoke_test')
state = {'joints': None, 'text': None}
def save_joints(m): state['joints'] = m
def save_text(m): state['text'] = m.data
subs = [n.create_subscription(JointState, '/joint_states', save_joints, 10),
        n.create_subscription(String, '/classroom/chatter', save_text, 10)]
buffer = Buffer()
listener_tf = TransformListener(buffer, n)
root = ET.parse(Path(get_package_share_directory('ros2_classroom')) / 'model/urdf/rpo.urdf').getroot()
limits = {j.attrib['name']: (float(j.find('limit').attrib['lower']), float(j.find('limit').attrib['upper']))
          for j in root.findall('joint') if j.attrib['type'] == 'revolute'}
links = [link.attrib['name'] for link in root.findall('link') if link.attrib['name'] != 'base_link']
def pump(seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end: rclpy.spin_once(n, timeout_sec=0.05)
def until(check, seconds=8):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if check(): return
        rclpy.spin_once(n, timeout_sec=0.05)
    raise AssertionError('Timed out waiting for expected ROS data')
def call(name, cls, req):
    c=n.create_client(cls,name)
    assert c.wait_for_service(timeout_sec=8), name
    f=c.call_async(req)
    rclpy.spin_until_future_complete(n,f,timeout_sec=8)
    assert f.done(), name
    result=f.result();n.destroy_client(c);return result
procs=[]
try:
    until(lambda: state['joints'] is not None)
    message = state['joints']
    assert len(message.name) == len(message.position) == len(limits)
    assert len(set(message.name)) == len(message.name)
    assert set(message.name) == set(limits), 'Joint names must match URDF'
    for name, position in zip(message.name, message.position):
        lower, upper = limits[name]
        assert math.isfinite(position) and lower - 1e-6 <= position <= upper + 1e-6, name
    until(lambda: all(buffer.can_transform('base_link', link, rclpy.time.Time()) for link in links))
    print(f'PASS: {len(limits)} GUI joint states within URDF limits and complete TF tree from base_link')
    procs.append(subprocess.Popen(['ros2','run','ros2_classroom','basic_publisher'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True))
    until(lambda: state['text'] is not None)
    assert state['text'].startswith('Hello RoboParty ')
    procs.append(subprocess.Popen(['ros2','run','ros2_classroom','add_server'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True))
    req=AddTwoInts.Request();req.a=7;req.b=5
    assert call('/classroom/add',AddTwoInts,req).sum==12
    client=subprocess.run(['ros2','run','ros2_classroom','add_client'],capture_output=True,text=True,timeout=15)
    assert client.returncode==0 and 'Sum = 12' in client.stdout+client.stderr
    listener=subprocess.Popen(['ros2','run','ros2_classroom','basic_subscriber'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,start_new_session=True)
    procs.append(listener);pump(2);os.killpg(listener.pid, signal.SIGINT)
    out=listener.communicate(timeout=5)[0]
    assert 'Received: Hello RoboParty' in out, out
    print('PASS: Python publisher, subscriber, AddTwoInts server and asynchronous client')
finally:
    for p in procs:
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGINT)
            try: p.wait(timeout=5)
            except subprocess.TimeoutExpired: os.killpg(p.pid, signal.SIGKILL)
    n.destroy_node();rclpy.shutdown()
