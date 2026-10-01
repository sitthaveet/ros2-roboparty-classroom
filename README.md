# ROS 2 + RoboParty Classroom

Learn ROS 2 by running real nodes in Docker. We'll get ROS 2 running on your laptop, send messages between nodes, call a service, then bend the joints of a real humanoid model. Four lessons, in order. No robots get hurt.

| ROS 2 | Runs on | Lessons | RViz |
|---|---|---|---|
| Humble | Ubuntu 22.04 (in Docker) | 4 | `localhost:6080` |

The classroom shows a visual model only. It doesn't connect to a physical robot or simulate walking.

**Where to type each command**

- **Host**: your computer's own terminal, for Docker commands.
- **Terminal A, B, C**: shells inside the container, for ROS commands.

**Lessons**

1. [Set up Docker and ROS 2](#lesson-01--set-up-docker-and-ros-2)
2. [Publisher and subscriber](#lesson-02--publisher-and-subscriber)
3. [Services: ask a question, get an answer](#lesson-03--services-ask-a-question-get-an-answer)
4. [URDF: describe a robot, then move it](#lesson-04--urdf-describe-a-robot-then-move-it)

---

## Lesson 01 — Set up Docker and ROS 2

One container with ROS 2 Humble, RViz in your browser, three terminals ready to go. Set it up once, use it for every lesson.

**You'll learn:** Docker image · docker compose · ROS workspace · sourcing

### How the pieces fit

Everything ROS runs inside one container. You edit code on your own computer, and the container sees the same files through a shared folder. RViz runs in the container too; you watch it through a web page.

```text
Your computer   ros2_ws/src/     ── shared folder ──▶  Container "ros"     /opt/ros2_ws/src/
Your browser    localhost:6080   ── noVNC ─────────▶  Container desktop    RViz + joint sliders
```

### 1. Clone the repository

Open a terminal (PowerShell on Windows, Terminal on Mac or Ubuntu), go to the folder where you keep your projects, and run:

**Host** (any folder):
```sh
git clone https://github.com/sitthaveet/ros2-roboparty-classroom
cd ros2-roboparty-classroom
```

You're now in the repository folder, the one with `compose.yaml` and `Dockerfile`. Run every host command in this lesson from here.

No `git`? On Windows install [Git for Windows](https://git-scm.com/download/win) and open a new PowerShell. On a Mac, accept the prompt to install the Command Line Developer Tools, then run the command again. On Ubuntu run `sudo apt install git`.

### 2. Install Docker

#### Windows 11 (Intel / AMD x64)

1. Check that virtualization is on: Task Manager → Performance → CPU.
2. In PowerShell **as Administrator**: `wsl --install --no-distribution`, restart, then `wsl --update`.
3. Install [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) with the **WSL 2 backend** and **Linux containers**.
4. Start Docker Desktop, wait for the engine, then open a normal PowerShell.

#### Ubuntu 22.04 / 24.04 (x86_64)

1. Install Docker Engine and the Compose plugin from the [official Ubuntu guide](https://docs.docker.com/engine/install/ubuntu/).
2. Not in the `docker` group? Put `sudo` in front of every **host** Docker command, like `sudo docker compose up -d --build`.
3. Never use `sudo` for ROS commands inside the container.

#### macOS (Apple silicon or Intel)

1. Check your chip: Apple menu → **About This Mac**. It says **Chip: Apple M…** or **Processor: Intel**.
2. Install [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/) for your chip and drag it to **Applications**.
3. Open Docker Desktop and wait until the engine is running (whale icon in the menu bar).
4. Use the **Terminal** app for host commands. No `sudo` needed.

You need at least 8 GB RAM. We recommend 16 GB RAM and about 15 GB free disk. On Mac and Windows, Docker Desktop has its own memory and disk limits under **Settings → Resources**.

### 3. Check that Docker works

**Host** (repository folder):
```sh
docker version
docker compose version
docker run --rm hello-world
```

`docker version` must list both **Client** and **Server**. `hello-world` prints a success message.

### 4. Build and start the classroom

Use the terminal from step 1, still inside `ros2-roboparty-classroom`. In a new terminal, `cd` back into that folder first.

**Host** (repository folder):
```sh
docker compose up -d --build
docker compose ps
```

The first build downloads the ROS base image and packages. Give it several minutes. When it's done, `docker compose ps` shows the `ros` service running.

### 5. Open RViz in your browser

Go to <http://localhost:6080/vnc.html?autoconnect=true&resize=scale> and click **Connect** if asked. Wait for the robot model and **Global Status: Ok**. A **Joint State Publisher** window with sliders opens too. Save it for Lesson 04.

### 6. Open terminals A, B and C

Open three terminals on your computer, all in the repository folder, and run this in each:

**Host** (once in each of 3 terminals):
```sh
docker compose exec ros bash
```

The prompt changes to `ROS2 classroom>`. These are now terminals A, B and C. ROS and the workspace are already sourced. Check:

**Terminal A**:
```sh
echo $ROS_DISTRO
```

Expected:
```text
humble
```

Run every `ros2`, `colcon` and `source` command in these container shells, never straight in PowerShell. Type `exit` to leave a shell; the classroom keeps running.

### 7. Know where your files live

| Your computer | Container | What it is |
|---|---|---|
| `ros2_ws/src/` | `/opt/ros2_ws/src/` | Source code. Edit here. Shared both ways. |
| (not shared) | `/opt/ros2_ws/install/` | Built packages, made by `colcon build` |
| (not shared) | `/opt/ros/humble/` | ROS 2 itself (the "underlay") |

The workspace is built with `--symlink-install`, so after editing a Python node you only restart it. Rebuild only after adding a new executable or changing `setup.py` or `package.xml`:

**Terminal A** (only when needed):
```sh
cd /opt/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

Read [WORKSPACE.md](WORKSPACE.md) for more on the workspace layout and to build a small workspace yourself.

### Stop and resume

| Command (host) | What it does |
|---|---|
| `docker compose stop` | Stops the classroom after class. The container and its files stay. |
| `docker compose start` | Starts it again next time (start Docker Desktop first on Mac or Windows). Then reopen shells with `docker compose exec ros bash`. |
| `docker compose down` | Removes the container. Files made only inside it are gone; your `ros2_ws/src` files are safe. |

### If something breaks

| Symptom | Check |
|---|---|
| Cannot connect to Docker | Start Docker Desktop or Engine. `docker version` must show Server. |
| Permission denied (Ubuntu) | Use `sudo` for host Docker commands. |
| Compose file not found | Wrong folder. Run `cd ros2-roboparty-classroom` (or the full path) and try again. |
| Port 6080 is busy | In `compose.yaml` change the port to `127.0.0.1:6081:6080`, run `docker compose up -d`, open port 6081. |
| Browser keeps connecting | `docker compose ps` and `docker compose logs ros`. Give it a moment to start. |
| `ros2: command not found` | You're on the host. Enter the container with `docker compose exec ros bash`. |

> **Teacher note:** This GUI edition hasn't been runtime-tested on every platform. Do one full run of Lessons 01–04 on a classroom machine before the session, and have students run the first build before class if the network is slow. Test the Mac route too, ideally on an Apple silicon Mac.

### Checklist

- [ ] I cloned the repository and I'm inside `ros2-roboparty-classroom`
- [ ] `docker run --rm hello-world` printed a success message
- [ ] `docker compose ps` shows the `ros` service running
- [ ] I can see the robot in RViz in my browser
- [ ] Terminals A, B and C show `ROS2 classroom>`
- [ ] `echo $ROS_DISTRO` prints `humble`

---

## Lesson 02 — Publisher and subscriber

Run two Python nodes that chat over a topic, spy on them with the `ros2` tools, then change what they say.

**You'll learn:** node · topic · message type · publisher · callback · timer

### The idea

A **node** is one running program in ROS. Nodes talk by sending **messages** on named **topics**. A publisher sends without knowing who's listening, and any number of subscribers can listen. Both sides must agree on the topic name and the message type.

```text
/classroom_talker  ── publishes every 1.0 s ──▶  /classroom/chatter  ── delivers to ──▶  /classroom_listener
(basic_publisher)                               (std_msgs/String)                      (basic_subscriber)
```

### 1. Start the publisher

**Terminal A**:
```sh
ros2 run ros2_classroom basic_publisher
```

Expected (timestamps differ):
```text
[INFO] [...] [classroom_talker]: Hello RoboParty 0
[INFO] [...] [classroom_talker]: Hello RoboParty 1
[INFO] [...] [classroom_talker]: Hello RoboParty 2
```

`ros2 run <package> <executable>` starts a program from a package. The executable names live in `setup.py`.

### 2. Start the subscriber

**Terminal B**:
```sh
ros2 run ros2_classroom basic_subscriber
```

Expected:
```text
[INFO] [...] [classroom_listener]: Received: Hello RoboParty 5
[INFO] [...] [classroom_listener]: Received: Hello RoboParty 6
```

The count doesn't start at 0. A subscriber only hears messages sent after it joined.

### 3. Inspect the system

Leave A and B running. Use C to look around, one command at a time:

**Terminal C**:
```sh
ros2 node list
ros2 node info /classroom_talker
ros2 topic list -t
ros2 topic info /classroom/chatter --verbose
ros2 interface show std_msgs/msg/String
ros2 topic echo /classroom/chatter
ros2 topic hz /classroom/chatter
```

| Command | Look for |
|---|---|
| `node list` | `/classroom_talker` and `/classroom_listener`. The others (`/robot_state_publisher`, `/rviz2`, …) run the robot display and started on their own. |
| `topic list -t` | `/classroom/chatter [std_msgs/msg/String]`: the topic and its type |
| `topic info --verbose` | Publisher count: 1, Subscription count: 1, plus QoS settings |
| `interface show` | One field: `string data` |
| `topic echo` | `data: Hello RoboParty …`. Stop with Ctrl+C. |
| `topic hz` | Average rate near 1.000, since the timer fires every 1.0 s. Stop with Ctrl+C. |

### 4. Publish from the command line

Stop the publisher in A with Ctrl+C. Keep B running. Now you're the publisher:

**Terminal C**:
```sh
ros2 topic pub --once /classroom/chatter std_msgs/msg/String "{data: 'Hello from terminal C'}"
```

B prints `Received: Hello from terminal C`. The subscriber doesn't care who sent it. Swap `--once` for `--rate 2` to send twice a second, then stop it with Ctrl+C.

### 5. Read the code

Open [`basic_publisher.py`](ros2_ws/src/ros2_classroom/ros2_classroom/basic_publisher.py):

| Line | What it does |
|---|---|
| 8 | The node's name. It's what `ros2 node list` shows. |
| 9 | `create_publisher(type, topic, 10)`: message type, topic name, and queue depth (hold up to 10 messages if things get slow). |
| 11 | A timer calls `tick()` every 1.0 seconds. |
| 14–16 | Build a `String`, fill its `data` field, publish it. |
| 24 | `rclpy.spin()` keeps the node alive so timers and callbacks run, until you press Ctrl+C. |

Open [`basic_subscriber.py`](ros2_ws/src/ros2_classroom/ros2_classroom/basic_subscriber.py):

| Line | What it does |
|---|---|
| 9–10 | `create_subscription(type, topic, callback, 10)`. Type and topic must match the publisher exactly. |
| 12–13 | The **callback**. ROS calls `receive(msg)` every time a message lands. You never call it yourself. |

### 6. Change the code

On your computer, open `ros2_ws/src/ros2_classroom/ros2_classroom/basic_publisher.py` and change the greeting on line 15, for example to `f'Hi from team 3, message {self.count}'`. Save, restart the publisher in A, and B shows your new text. No rebuild needed.

### Try it

1. **Speed it up.** Change the timer on line 11 from `1.0` to `0.2`. What does `ros2 topic hz /classroom/chatter` say now?
   <details><summary>Answer</summary>About 5 Hz. 1 ÷ 0.2 s = 5 messages per second.</details>
2. **Break the connection.** In `basic_subscriber.py` change the topic to `/classroom/chat` and restart B. Why does nothing arrive?
   <details><summary>Answer</summary>They're on two different topics now. <code>ros2 topic list</code> shows both <code>/classroom/chatter</code> and <code>/classroom/chat</code>, each with only one side. Change it back afterwards.</details>
3. **Two listeners.** Run `basic_subscriber` in both B and C. Does each message go to one listener or both?
   <details><summary>Answer</summary>Both. Every subscriber gets its own copy of each message.</details>
4. **Rename the node.** Change `'classroom_talker'` to a name of your own. What changes in `ros2 node list`, and what doesn't?
   <details><summary>Answer</summary>The node shows up under its new name, but B still receives everything. Subscribers match on the topic, not on who's publishing.</details>

### Checklist

- [ ] B receives the messages published by A
- [ ] I can find a topic's name and type with `ros2 topic list -t`
- [ ] I published a message myself with `ros2 topic pub`
- [ ] I changed the greeting and saw it in B after restarting A
- [ ] I can explain what a callback is

---

## Lesson 03 — Services: ask a question, get an answer

Services: one node asks, another answers. Our server adds two integers. You'll call it from the command line and from Python.

**You'll learn:** service server · service client · request / response · `.srv` interface · futures

### The idea

A topic is a one-way stream. A **service** is a question with exactly one answer: a client sends a **request**, the server runs a function and sends back a **response**. Use services for short jobs that need a reply, like "add these numbers" or "reset this sensor."

```text
/classroom_add_client  ── request {a: 7, b: 5} ──▶  /classroom/add   ── handled by ──▶  /classroom_add_server
(add_client or CLI)    ◀── response {sum: 12} ───  (AddTwoInts)                       (add_server)
```

### 1. Start the server

**Terminal A**:
```sh
ros2 run ros2_classroom add_server
```

It prints nothing yet. It's waiting for someone to ask.

### 2. Find the service and its interface

**Terminal C**:
```sh
ros2 service list -t
ros2 interface show example_interfaces/srv/AddTwoInts
```

Expected from `interface show`:
```text
int64 a
int64 b
---
int64 sum
```

Look for `/classroom/add [example_interfaces/srv/AddTwoInts]` in the list. The services ending in `…/get_parameters` and friends come free with every node.

In a `.srv` file, `---` splits the **request** (above) from the **response** (below).

### 3. Call it from the command line

**Terminal C**:
```sh
ros2 service call /classroom/add example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

C shows:
```text
response:
example_interfaces.srv.AddTwoInts_Response(sum=5)
```

A shows:
```text
[INFO] [...] [classroom_add_server]: 2 + 3 = 5
```

### 4. Call it from Python

**Terminal C**:
```sh
ros2 run ros2_classroom add_client
```

Expected:
```text
[INFO] [...] [classroom_add_client]: Sum = 12
```

Unlike the publisher, the client asks once, prints the answer and exits.

### 5. Read the code

Open [`add_server.py`](ros2_ws/src/ros2_classroom/ros2_classroom/add_server.py):

| Line | What it does |
|---|---|
| 9 | `create_service(type, name, callback)` registers `/classroom/add`. |
| 11–14 | The callback gets the filled-in `request` and an empty `response`. It fills `response.sum` and must `return response`. |

Open [`add_client.py`](ros2_ws/src/ros2_classroom/ros2_classroom/add_client.py):

| Line | What it does |
|---|---|
| 9 | The client uses the same type and service name as the server. |
| 11–12 | Wait up to 5 s for the server. No server? Stop with a clear error. |
| 14 | Fill in the request: `a = 7`, `b = 5`. |
| 15–16 | `call_async` returns a **future**, a placeholder for an answer that hasn't arrived yet. `spin_until_future_complete` runs the node until it does, or 5 s pass. |
| 18 | `future.result()` is the response, and `.sum` is its field. |

### Try it

1. **New numbers.** Change line 14 of `add_client.py` to add `100` and `-42`, then run the client again.
   <details><summary>Answer</summary><code>Sum = 58</code>. No rebuild needed, thanks to <code>--symlink-install</code>.</details>
2. **No server.** Stop the server in A, then run `add_client`. What happens, and how long does it take?
   <details><summary>Answer</summary>After about 5 seconds it stops with <code>RuntimeError: Start add_server in another terminal first</code>, from lines 11–12.</details>
3. **Change the rule.** Make the server multiply (`request.a * request.b`), restart A, and call it with `{a: 6, b: 7}`. The field is still called `sum`. Why can't you rename it in Python?
   <details><summary>Answer</summary>Field names come from the <code>AddTwoInts</code> interface, not your code. Both sides share that interface, so a new field name means a new <code>.srv</code> type.</details>
4. **Topic or service?** Pick one for each: a camera sending 30 images a second; asking a robot to save a map; a battery level reported every second.
   <details><summary>Answer</summary>Topic, service, topic. Streams of data use topics; one-off jobs that need a reply use services.</details>

### Checklist

- [ ] I found `/classroom/add` with `ros2 service list -t`
- [ ] I can point to the request and response parts of `AddTwoInts`
- [ ] `ros2 service call` returned `sum=5`
- [ ] `add_client` printed `Sum = 12`
- [ ] I can explain when to use a service instead of a topic

---

## Lesson 04 — URDF: describe a robot, then move it

URDF: how a robot is written down as links and joints. Read a tiny one, show it in RViz, then switch to the RoboParty humanoid and move its joints with sliders.

**You'll learn:** URDF · link · joint types · limits in radians · `/joint_states`

### The idea

A **URDF** (Unified Robot Description Format) is an XML file that describes a robot as a tree. **Links** are the rigid parts. **Joints** connect a *parent* link to a *child* link and say how the child can move. The files are in `ros2_ws/src/ros2_classroom/model/urdf/`.

### 1. Read the simplest robot: a pendulum

Open [`pendulum.urdf`](ros2_ws/src/ros2_classroom/model/urdf/pendulum.urdf). Two links, one joint.

| Line | What it does |
|---|---|
| 7 | `base_link`: a 10 cm grey box. The root of the tree. It doesn't move. |
| 14 | `pendulum_link`: a 1 m rod (centred 0.5 m below the joint) and a red ball 1 m down. Units are metres. |
| 27 | `type="continuous"` spins forever, no limits. `revolute` also rotates but has a `<limit>`. `fixed` doesn't move at all. |
| 28–29 | The joint connects parent `base_link` to child `pendulum_link`. |
| 30 | `axis xyz="0 1 0"`: rotate around the y axis. |

A joint has one number, its **position**, in radians. 1 radian ≈ 57.3°, so π (3.14) is half a turn. ROS always uses radians for angles.

### 2. Show the pendulum in RViz

Open [RViz in your browser](http://localhost:6080/vnc.html?autoconnect=true&resize=scale). RViz, `robot_state_publisher` and the slider window are already running, so don't launch them a second time. To swap the model on screen, use `show_model`:

**Terminal A**:
```sh
ros2 run ros2_classroom show_model pendulum
```

Expected:
```text
[INFO] [...] [classroom_show_model]: RViz now shows pendulum
```

RViz and the **Joint State Publisher** window switch to the pendulum. Drag the `pendulum_joint` slider and watch it swing. If RViz covers the slider window, press Alt+Tab inside the browser desktop or drag RViz aside.

Look familiar? `show_model` is a **service client**, just like `add_client` in Lesson 03. It sends the new URDF to the `/robot_state_publisher/set_parameters` service, and RViz and the sliders follow along.

### 3. Switch to the RoboParty humanoid

**Terminal A**:
```sh
ros2 run ros2_classroom show_model rpo
```

Now RViz shows the full robot from `rpo.urdf`: 24 links, 23 revolute joints, real 3D meshes. It's the same idea as the pendulum, just a much bigger tree.

### 4. Move the joints

1. Find the **Joint State Publisher** window. It now has one slider per humanoid joint.
2. Move `left_arm_roll_joint` slowly and watch the left arm. Then try `left_elbow_pitch_joint`.
3. Click **Randomize** for a surprise pose, and **Center** to go back to the start.
4. Each slider stops at the limits written in the URDF. Compare with the table below.

### 5. See the numbers the sliders send

**Terminal A**:
```sh
ros2 topic echo /joint_states --once
```

Expected (shortened):
```text
name:
- left_thigh_yaw_joint
- left_thigh_roll_joint
- ...
position:
- 0.0
- 0.0
- ...
```

`name[i]` goes with `position[i]`. Move a slider, run it again, and watch your number change.

### What happens when you drag a slider

```text
joint_state_publisher_gui ── angles ──▶ /joint_states ── + URDF ──▶ robot_state_publisher ── where every link is ──▶ /tf ── draws ──▶ rviz2
```

Same publisher/subscriber pattern as Lesson 02, just a different message type.

### RoboParty joints and their limits

From `rpo.urdf`. Values in radians, degrees in brackets.

| Group | Joint | Lower | Upper |
|---|---|---|---|
| Left leg | `left_thigh_yaw_joint` | -1.00 (-57°) | 0.20 (11°) |
| Left leg | `left_thigh_roll_joint` | -0.20 (-11°) | 1.00 (57°) |
| Left leg | `left_thigh_pitch_joint` | -2.09 (-120°) | 0.79 (45°) |
| Left leg | `left_knee_joint` | -0.20 (-11°) | 2.50 (143°) |
| Left leg | `left_ankle_pitch_joint` | -0.60 (-34°) | 0.60 (34°) |
| Left leg | `left_ankle_roll_joint` | -0.50 (-29°) | 0.50 (29°) |
| Right leg | `right_thigh_yaw_joint` | -0.20 (-11°) | 1.00 (57°) |
| Right leg | `right_thigh_roll_joint` | -1.00 (-57°) | 0.20 (11°) |
| Right leg | `right_thigh_pitch_joint` | -2.09 (-120°) | 0.79 (45°) |
| Right leg | `right_knee_joint` | -0.20 (-11°) | 2.50 (143°) |
| Right leg | `right_ankle_pitch_joint` | -0.60 (-34°) | 0.60 (34°) |
| Right leg | `right_ankle_roll_joint` | -0.50 (-29°) | 0.50 (29°) |
| Torso | `torso_joint` | -3.14 (-180°) | 3.14 (180°) |
| Left arm | `left_arm_pitch_joint` | -3.14 (-180°) | 1.57 (90°) |
| Left arm | `left_arm_roll_joint` | -0.25 (-14°) | 3.14 (180°) |
| Left arm | `left_arm_yaw_joint` | -1.57 (-90°) | 1.57 (90°) |
| Left arm | `left_elbow_pitch_joint` | -0.60 (-34°) | 1.57 (90°) |
| Left arm | `left_elbow_yaw_joint` | -1.57 (-90°) | 1.57 (90°) |
| Right arm | `right_arm_pitch_joint` | -3.14 (-180°) | 1.57 (90°) |
| Right arm | `right_arm_roll_joint` | -3.14 (-180°) | 0.25 (14°) |
| Right arm | `right_arm_yaw_joint` | -1.57 (-90°) | 1.57 (90°) |
| Right arm | `right_elbow_pitch_joint` | -0.60 (-34°) | 1.57 (90°) |
| Right arm | `right_elbow_yaw_joint` | -1.57 (-90°) | 1.57 (90°) |

### Try it

1. **Wave hello.** Raise one arm and bend the elbow so the robot waves. Which joints did you use?
   <details><summary>Hint</summary>Lift with <code>left_arm_roll_joint</code>, bend with <code>left_elbow_pitch_joint</code>, then wiggle <code>left_elbow_yaw_joint</code> back and forth.</details>
2. **Mirror image.** `left_arm_roll_joint` runs −0.25 to 3.14, but `right_arm_roll_joint` runs −3.14 to 0.25. Why flipped?
   <details><summary>Answer</summary>Both rotate around the same x axis, but the arms sit on opposite sides of the body. Lifting the left arm outward is a positive rotation; lifting the right one outward is negative.</details>
3. **Biggest range.** Which joint turns the furthest? Check the table, then try it on the robot.
   <details><summary>Answer</summary><code>torso_joint</code>, −3.14 to 3.14: almost a full spin around the vertical axis.</details>
4. **Find it in the file.** Open `rpo.urdf` and search for `left_knee_joint`. Which link is its parent, and which is its child?
   <details><summary>Answer</summary>Parent <code>left_thigh_pitch_link</code>, child <code>left_knee_link</code>.</details>
5. **What else can it show?** Run `ros2 run ros2_classroom show_model` with no model name. What does it tell you?
   <details><summary>Answer</summary>It prints <code>Usage: ros2 run ros2_classroom show_model &lt;pendulum|rpo&gt;</code>. The list is every <code>.urdf</code> file in <code>model/urdf</code>, so a new URDF you add there shows up too (after <code>colcon build</code>).</details>

> **Teacher note:** `show_model` is a new executable. Students who built their container before this change will see `No executable found`. Fix it with `docker compose up -d --build` on the host, or with `colcon build --symlink-install` and `source install/setup.bash` inside the container. After a container restart, RViz starts on `rpo` again.

### Checklist

- [ ] I can name the two links and the joint in `pendulum.urdf`
- [ ] I can explain continuous vs revolute vs fixed joints
- [ ] I switched RViz to the pendulum and back with `show_model`
- [ ] I moved at least three joints with the sliders and watched RViz
- [ ] I saw the slider values in `ros2 topic echo /joint_states`
- [ ] I can describe the path slider → /joint_states → robot_state_publisher → /tf → RViz

---

## Stuck? Ask a human

Raise your hand and tell your instructor two things: the terminal letter (A, B, C or host) and the exact error message. We'll sort it out together.

Want more after class? The [ROS 2 Humble tutorials](https://docs.ros.org/en/humble/Tutorials.html) pick up right where we stop.

## More in this repository

- [WORKSPACE.md](WORKSPACE.md): how a ROS 2 workspace is laid out, and how to build one from scratch.
- [ROBOPARTY-INTERFACES.md](ROBOPARTY-INTERFACES.md): how the classroom topics compare with the real RoboParty project.
- [THIRD_PARTY.md](THIRD_PARTY.md): model attribution and licenses.
