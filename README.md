# ROS 2 + RoboParty Classroom

Learn ROS 2 nodes, topics, services, workspaces and TF by controlling a RoboParty **visual model** in RViz. This project runs ROS 2 Humble on Ubuntu 22.04 inside Docker and displays RViz in your browser.

The examples do not connect to a physical robot or run a walking controller, physics simulator or RL policy.

## 1. Download this repository

On the GitHub repository page, select **Code → Download ZIP**, then extract the entire archive. On Windows, use **Extract All**. Open the extracted folder containing `compose.yaml` and `Dockerfile`; do not run commands inside the ZIP. You do not need Git when downloading the ZIP.

If you use Git, copy the HTTPS URL from **Code**, clone it, and open the resulting repository folder. Keep all files together.

## 2. Prepare Docker

### Windows 11, Intel/AMD x64

1. Enable hardware virtualization if it is disabled in Task Manager → Performance → CPU.
2. If WSL is not installed, open PowerShell **as Administrator**, run `wsl --install --no-distribution`, and restart when prompted. Run `wsl --update` afterwards. Existing WSL installations only need to be checked/updated.
3. Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) and use its **WSL 2 backend** with **Linux containers**. You do not need to install an Ubuntu distribution separately for this workflow.
4. Start Docker Desktop and wait for its engine to be ready. Open a new, normal PowerShell window.

Docker requires at least 8 GB RAM; 16 GB RAM and approximately 15 GB free space are recommended for this workshop. See [Docker's WSL requirements](https://docs.docker.com/desktop/features/wsl/) for supported versions.

### Ubuntu Linux 22.04 / 24.04, x86_64

Install Docker Engine and the Compose plugin using the [official Ubuntu installation guide](https://docs.docker.com/engine/install/ubuntu/). This route is for an Ubuntu host, not a second Docker installation inside Windows WSL.

The commands below use `docker`. **On Ubuntu, prefix every host-side Docker command with `sudo`** if your user does not already have Docker access. For example: `sudo docker compose up -d --build`. Do not add `sudo` to ROS commands inside the container.

### Check Docker on your host

```sh
docker version
docker compose version
docker run --rm hello-world
```

`docker version` must show both Client and Server. `hello-world` should print a success message. Windows users can also check that `docker info --format '{{.OSType}}'` prints `linux`.

The earlier classroom edition was validated on Linux x86_64. This GUI edition has been checked statically, but has not yet been built or runtime-tested in this editing environment. Verify the GUI, RViz and lab checks on your teaching machine before class.

## 3. Start the classroom

Open a terminal in the repository folder. On Windows, enter `powershell` in File Explorer's address bar while viewing that folder.

Run these commands **on your host**:

```sh
docker compose up -d --build
docker compose ps
```

The first build downloads the ROS base image and packages and can take several minutes. The `ros` service should be running.

**Updating to the GUI edition:** stop the old classroom from its original folder with `docker compose stop`, then use the complete updated ZIP in a separate folder. This update changes the Dockerfile, launch file, package setup, RViz configuration and tests; replacing only the Dockerfile is not enough. Back up your edits first, then copy only your own exercise files into the new `ros2_ws/src` without overwriting the supplied package. Start the new edition with `docker compose up -d --build`. `docker compose start` alone does not apply this update. Before removing or recreating a container, copy any work stored only inside it (such as `/tmp/practice/ros2_ws/src`) to your host.

Open [RViz in your browser](http://localhost:6080/vnc.html?autoconnect=true&resize=scale). If shown, click **Connect**. Wait for the robot model and `Global Status: Ok`. The Joint State Publisher window opens automatically too. If RViz covers it, use Alt+Tab inside the browser desktop (or the noVNC keyboard controls) to switch windows.

## 4. Open terminals A, B and C

Open three host terminals in the same repository folder. In each one, run:

```sh
docker compose exec ros bash
```

You should see `ROS2 classroom>`. Interactive Bash automatically sources ROS and the workspace through `/root/.bashrc`, which loads `/etc/classroom/entrypoint-rc.sh`. Run the command once in each new terminal. **Run all `ros2`, `colcon` and `source` commands below inside this container shell**, not directly in Windows PowerShell.

Type `exit` to return to your host terminal; this does not stop the classroom. The existing `scripts/shell.sh` helper remains available for compatibility with older instructions.

```sh
echo $ROS_DISTRO
```

Expected result: `humble`.

## Repository and workspace

```text
repository/
├── README.md
├── WORKSPACE.md
├── Dockerfile
├── compose.yaml
├── docker/                  # Container startup and browser desktop
├── scripts/                 # Shell helper and checks
├── tests/                   # Integration checks
└── ros2_ws/
    └── src/
        └── ros2_classroom/   # ROS package: code, launch, URDF and meshes
```

Docker builds the ROS workspace at **`/opt/ros2_ws`**. Your host's `ros2_ws/src` is mounted at `/opt/ros2_ws/src`, so source edits are visible inside the container. `build/`, `install/` and `log/` are generated inside the container and are not committed to Git.

Read [WORKSPACE.md](WORKSPACE.md) to understand the layout and create a small workspace yourself.

## Lab 1 — Nodes and topics

Terminal A:
```sh
ros2 run demo_nodes_cpp talker
```

Terminal B:
```sh
ros2 run demo_nodes_cpp listener
```

Terminal C:
```sh
ros2 node list
ros2 node info /talker
ros2 topic list -t
ros2 topic info /chatter --verbose
ros2 interface show std_msgs/msg/String
ros2 topic echo /chatter --once
```

Stop A with **Ctrl+C**, then publish from C:
```sh
ros2 topic pub --once /chatter std_msgs/msg/String "{data: 'Hello RoboParty'}"
```

B should display your message. Try `--rate 2` instead of `--once`, then stop all demo nodes before continuing.

## Lab 2 — Edit a Python publisher

A:
```sh
ros2 run ros2_classroom basic_publisher
```
B:
```sh
ros2 run ros2_classroom basic_subscriber
```
C:
```sh
ros2 topic echo /classroom/chatter --once
```

On your host, edit `ros2_ws/src/ros2_classroom/ros2_classroom/basic_publisher.py`. Change the greeting, save, then stop and restart A. B should receive the new greeting. Python source changes are visible through the bind mount and `--symlink-install`.

After adding an executable or changing package metadata, rebuild **inside the container**:
```sh
cd /opt/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Source `install/setup.bash` in every existing shell that needs the updated environment. If you change apt packages in `Dockerfile`, rebuild from the host with `docker compose up -d --build` instead. Stop both nodes when finished.

## Lab 3 — Services

A:
```sh
ros2 run ros2_classroom add_server
```
C:
```sh
ros2 service list -t
ros2 interface show example_interfaces/srv/AddTwoInts
ros2 service call /classroom/add example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
ros2 run ros2_classroom add_client
```

The CLI request returns `sum: 5`. The Python client sends 7 and 5 and prints `Sum = 12`. Read `add_server.py` and `add_client.py`. In a service interface, `---` separates the request from the response. Stop the server after this lab.

## Lab 4 — Move a joint with sliders

RViz, `robot_state_publisher` and `joint_state_publisher_gui` already run automatically. Do not start duplicate instances.

1. Open the **Joint State Publisher** window in the browser desktop.
2. Find `left_arm_roll_joint` and `left_elbow_pitch_joint`.
3. Move each slider slowly and watch the arm in RViz. Values represent radians and the slider range follows the URDF joint limits.
4. Read the published state in your classroom shell:

```sh
ros2 topic echo /joint_states --once
ros2 interface show sensor_msgs/msg/JointState
```

`name[i]` identifies the joint whose angle is `position[i]`. The GUI publishes `/joint_states`; `robot_state_publisher` combines those angles with the URDF and publishes TF. RViz displays the result. Do not publish competing joint states from another node during this exercise.

## Lab 5 — Observe joint TF

In RViz, set **Fixed Frame = base_link**, then **Add → TF** and enable **Show Names**. In a classroom shell:

```sh
ros2 run tf2_ros tf2_echo base_link left_arm_roll_link
```

Move `left_arm_roll_joint` in the GUI and observe the changing orientation. The joint origin position can stay constant while its orientation changes. Press **Ctrl+C** to stop `tf2_echo` when finished.

This edition keeps the base fixed: it does not integrate velocity commands, move the whole robot through a world frame, or simulate walking.

## Lab 6 — Inspect the display graph

```sh
ros2 node list
ros2 topic info /joint_states --verbose
ros2 node info /robot_state_publisher
```

Identify the publisher and subscriber of `/joint_states`, then explain the path: GUI → JointState → robot_state_publisher + URDF → TF → RViz. Node names can differ from executable names; use the names printed by `ros2 node list`.

The GUI replaces the custom teaching bridge. There are no classroom joint-command, velocity or reset endpoints. The service exercise remains **Lab 3 — AddTwoInts**, separate from the model display.

## Stop and resume

Run on the host in the repository folder:

Stop after class:
```sh
docker compose stop
```

Resume later (start Docker Desktop first on Windows):
```sh
docker compose start
```

`stop` stops the classroom processes without removing the container or its files; `start` starts the processes again, not their previous in-memory state. Open a new ROS terminal with `docker compose exec ros bash`. Closing a terminal or browser tab alone does not stop the classroom.

To remove this project's container and network, use `docker compose down`. The host source files and built image remain. Files created only inside a removed container are lost.

## Troubleshooting

| Symptom | What to check |
|---|---|
| Cannot connect to Docker | Start Docker Desktop/Engine; check that `docker version` shows Server. |
| Ubuntu permission denied | Use `sudo` for host Docker commands. |
| Compose file not found | Open the extracted repository folder containing `compose.yaml`. |
| Port 6080 is busy | Change the mapping to `127.0.0.1:6081:6080`, run `up -d`, and open port 6081. |
| Browser keeps connecting | Check `docker compose ps` and `docker compose logs ros`; wait for startup. |
| RViz is blank | Check Fixed Frame `base_link`, RobotModel `/robot_description`, and `ros2 node list`. |
| `ros2` command not found | Enter with `docker compose exec ros bash`. If using an older image, update the Dockerfile and rebuild as described in section 3. |
| Topic exists but no data arrives | Check that a publisher is running and topic name, type and QoS agree. |
| Sliders are hidden | Switch to Joint State Publisher with Alt+Tab in the browser desktop or move the RViz window. |
| Python change is not visible | Save the file in the host's `ros2_ws/src`, then restart that node. |
| GUI is missing | Check `docker compose logs ros` and `/tmp/robot-error.log` inside the container; rebuild the complete updated package. |

The browser port is bound to localhost and ROS discovery is local to the container. Read [ROBOPARTY-INTERFACES.md](ROBOPARTY-INTERFACES.md) to compare classroom topics with the real project, and [THIRD_PARTY.md](THIRD_PARTY.md) for model attribution and licenses.
