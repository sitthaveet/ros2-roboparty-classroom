# Understanding a ROS 2 workspace

A workspace is a directory containing one or more ROS packages and the files generated when you build them. `ros2_ws` is our directory name; `ros2_classroom` is a package name. A package can provide several executables, and a running executable can create one or more nodes.

## Where files live

On your host, edit source files under `ros2_ws/src`. Inside the classroom container, the workspace is `/opt/ros2_ws`:

```text
/opt/ros2_ws/
├── src/                      # Source packages: edit these
│   └── ros2_classroom/
│       ├── package.xml       # Package metadata and dependencies
│       ├── setup.py          # Python installation and executable entry points
│       ├── ros2_classroom/   # Python modules
│       ├── launch/           # Start several nodes together
│       ├── config/           # RViz configuration
│       └── model/            # URDF and meshes
├── build/                    # Intermediate build files
├── install/                  # Installed packages and environment setup
└── log/                      # Build logs
```

`colcon build` creates `build`, `install` and `log`. Run it from the **workspace root**, not from `src` or a package directory. Commit source and configuration to Git; do not commit generated build folders.

## Build and source the supplied workspace

On your host, open a classroom shell with `docker compose exec ros bash` (see README for first-time setup). ROS and the supplied workspace are loaded automatically. Then run:

```bash
cd /opt/ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 pkg prefix ros2_classroom
```

Expected package prefix: `/opt/ros2_ws/install/ros2_classroom`.

- `/opt/ros/humble` is the **underlay**: the installed ROS distribution.
- `/opt/ros2_ws/install` is the **overlay**: packages built for this project.
- `source` updates the current shell's environment. In this classroom image, `/root/.bashrc` sources the workspace, so `docker compose exec ros bash` prepares ROS and the supplied workspace automatically. A new practice workspace still needs its own `source install/setup.bash` after building.
- `--symlink-install` links supported source files instead of copying them. Restart a Python node after changing its code. Changes to dependencies, entry points or package structure still need a rebuild.
- `source` does not compile code, and `colcon build` does not automatically update other open terminals.

For a clean build, use a fresh shell with only the ROS underlay sourced. Avoid building against an older copy of the same workspace overlay.

## Exercise: create a small workspace from scratch

Use a **new classroom container shell**. This exercise creates a separate workspace at `/tmp/practice/ros2_ws` and leaves the supplied robot package unchanged. It is temporary: removing the container removes this exercise. Copy any work you want to keep to the host-mounted `/opt/ros2_ws/src` before removing the container.

### 1. Create the source directory

```bash
mkdir -p /tmp/practice/ros2_ws/src
cd /tmp/practice/ros2_ws/src
source /opt/ros/humble/setup.bash
```

### 2. Create a Python package

```bash
ros2 pkg create --build-type ament_python --node-name hello_node my_first_package --dependencies rclpy
```

`my_first_package` is the package name. The command creates `package.xml`, `setup.py`, a Python module and an executable entry point named `hello_node`. The classroom image already contains the ROS dependencies used in this exercise. Run package creation once; it will not overwrite an existing package directory.

### 3. Build from the workspace root

```bash
cd /tmp/practice/ros2_ws
colcon build --symlink-install
```

Expect a successful summary for one package. Inspect the generated directories:

```bash
ls
```

You should see `src`, `build`, `install` and `log`.

### 4. Source and run

```bash
source install/setup.bash
ros2 pkg prefix my_first_package
ros2 run my_first_package hello_node
```

The generated example prints `Hi from my_first_package.` and exits. It is a minimal executable scaffold; it does not create a persistent ROS node until you add node code. Compare it with the publisher/subscriber in `ros2_classroom` to see a node, timer and callback.

### 5. Try another terminal

Open another classroom shell. Before sourcing your practice workspace, `ros2 pkg prefix my_first_package` should fail. Then run:

```bash
source /tmp/practice/ros2_ws/install/setup.bash
ros2 run my_first_package hello_node
```

The executable is now discoverable in this terminal too. Close the practice shells when finished and open a new classroom shell to return to the robot labs.

## Common mistakes

| Mistake | Fix |
|---|---|
| Building inside `src` | Change to the parent `ros2_ws` directory first. |
| Package not found after a successful build | Source that workspace's `install/setup.bash` in the current shell. |
| Treating a folder name as an executable | Use `ros2 run PACKAGE EXECUTABLE`; see `setup.py` for entry points. |
| Editing generated files | Edit `src`, then rebuild when necessary. |
| Running Bash commands in PowerShell | Enter the container shell before using `source`, `ros2` or `colcon`. |

See the official ROS 2 Humble tutorials for [creating a workspace](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html) and [creating a package](https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html).
