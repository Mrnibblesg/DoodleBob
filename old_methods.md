# Getting Started with UR3e Robot Arms

Our lab contains two UR3e robot arms, each bolted in place on its own table.

The arms can be controlled either by [URScript](https://www.universal-robots.com/developer/urscript/), the Universal Robots in-house scripting language, or through the [ROS2 driver](https://docs.universal-robots.com/Universal_Robots_ROS_Documentation/index.html), consisting of a C++ API and related libraries. It is also possible to control the arm using a Python ROS2 system by publishing messages using the Universal Robots message format.

URScript is somewhat limited, especially with respect to controlling open-source simulators, so the rest of this guide will focus on ROS2 development. However, there are many ways to interface with the robots and there is no one "correct" way. URScript may be more user-friendly for development of simple motions, especially if you are having trouble getting ROS2 set up.

If your trajectories are complex, is also worth looking into [MoveIt](https://moveit.picknik.ai/main/doc/tutorials/quickstart_in_rviz/quickstart_in_rviz_tutorial.html), open-source motion planning software for robot arms.

# Install using `ros2_shell`

If you are using our pre-built apptainer, launch the shell and navigate to a new ROS2 workspace.

# Installing from Source

The following steps are only needed if you're installing from scratch on your own machine, where you have sudo permissions. This guide assumes you have already installed ROS2 Jazzy.

### ur_robot_driver

The driver is necessary for control of both the physical and simulated robot. Install with:

```bash
sudo apt install ros-jazzy-ur
```

Or see [instructions](https://docs.universal-robots.com/Universal_Robots_ROS2_Documentation/doc/ur_robot_driver/ur_robot_driver/doc/installation/installation.html#build-from-source) for building from source.

### Simulator

Follow the steps below in a new ROS2 workspace.

Download the simulation repository and install dependencies:

```bash
git clone -b ros2 https://github.com/UniversalRobots/Universal_Robots_ROS2_GZ_Simulation.git src/ur_simulation_gz
```

```bash
rosdep update && rosdep install --ignore-src --from-paths src -y
```

# Building the package:

```bash
colcon build --symlink-install
```

Don't forget to source your environment for this package:

```bash
source install/setup.sh
```

# Usage

To launch the simulator and RViz:

```bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur3e
```

To launch an example control script:

```bash
ros2 launch ur_robot_driver test_scaled_joint_trajectory_controller.launch.py
```

The example code is [here](https://github.com/ros-controls/ros2_controllers/blob/master/ros2_controllers_test_nodes/ros2_controllers_test_nodes/publisher_joint_trajectory_controller.py) and can be used as a jumping-off point for your system.
