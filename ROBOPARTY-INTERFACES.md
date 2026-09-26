# From classroom interfaces to RoboParty

This reference describes the core inference interface at `roboparty_deploy` revision `a8a0f1557cc5d085234b8bac248a8f543342f531` and inference submodule revision `ac448b12c382e3fab42c0e8467a6943987223c4b`. Names can change through configuration or remapping. The classroom does not run this hardware runtime.

## Core topics

Direction is relative to the inference node.

| Topic | Direction | ROS 2 type | Meaning or condition |
|---|---|---|---|
| `/cmd_vel` | Input | `geometry_msgs/msg/Twist` | `linear.x`, `linear.y`, `angular.z`; outside Joy mode and limited by `clip_cmd`. |
| `/joy` | Input | `sensor_msgs/msg/Joy` | Axes and buttons; the inspected source starts in Joy mode. |
| `/joint_ref_states` | Input | `sensor_msgs/msg/JointState` | Joint references in interrupt mode. |
| `elevation_data` | Conditional input | `std_msgs/msg/Float32MultiArray` | Default `perception_obs_topic`, enabled by policy/configuration. |
| `/joint_states` | Output | `sensor_msgs/msg/JointState` | Names such as `joint_1`, plus position, velocity and effort. |
| `/imu` | Output | `sensor_msgs/msg/Imu` | Timestamp, orientation and angular velocity; inspected code does not populate linear acceleration. |
| `/action` | Output | `sensor_msgs/msg/JointState` | Policy output `act_` in `position[]`, names such as `action_1`; do not assume radians. |

`/action` is a **topic**, not a ROS action. Hardware access is handled internally through `RobotInterface`. The inspected data QoS uses BestEffort, KeepLast(1) and Volatile.

These core interfaces use standard messages. This table does not claim that all RoboParty repositories use only standard messages; optional sensor and application modules can define custom interfaces.

## Core services

All ten services use `std_srvs/srv/Trigger`:

`/init_motors`, `/deinit_motors`, `/start_inference`, `/stop_inference`, `/reset_joints`, `/read_joints`, `/read_imu`, `/refresh_joints`, `/clear_errors`, `/set_zeros`.

The request is empty; the response contains `success` and `message`. For example, `/read_imu` returns service status while sensor values are published on `/imu`. `/reset_joints` may acknowledge background work before it finishes. `/set_zeros` affects physical motor calibration. These names are reference material, not commands to run in the classroom.

## Compare with your labs

| Classroom interface | What transfers to the real project |
|---|---|
| GUI → `/joint_states` (`JointState`) | Names and positions describe the visual joints. The GUI values are not motor feedback. |
| URDF + `robot_state_publisher` → TF | Joint names must match the URDF. The inspected inference uses names such as `joint_1`, which require mapping. |
| `/classroom/chatter` (`String`) | Practice publisher/subscriber and callbacks independently of robot control. |
| `/classroom/add` (`AddTwoInts`) | Learn service request/response without calling a hardware service. |

The GUI classroom keeps `base_link` fixed and has no velocity-command, joint-command or reset service for the model. The `/cmd_vel`, `/joint_ref_states` and Trigger services above belong to the external hardware runtime, not this display launch.

## Source references

- [Deployment snapshot](https://github.com/Roboparty/roboparty_deploy/tree/a8a0f1557cc5d085234b8bac248a8f543342f531)
- [Inference node declarations](https://github.com/Roboparty/roboparty_inference/blob/ac448b12c382e3fab42c0e8467a6943987223c4b/src/inference_node.hpp)
- [ROS interface implementation](https://github.com/Roboparty/roboparty_inference/blob/ac448b12c382e3fab42c0e8467a6943987223c4b/src/ros_interface.cpp)
- [Robot description snapshot](https://github.com/Roboparty/rpo_description/tree/37aac9ca665e92731444a1618320078e7ba21569)
