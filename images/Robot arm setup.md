We just need to be able to send goals to the robot. Pose goals seem most ideal. We're looking at single pipeline planning - pose goal for the UR3e. We want the end-effector to be in a specific orientation. We likely want to define a specific height for the end-effector to be above the ground.
The tutorial we're referencing is here: https://moveit.picknik.ai/main/doc/examples/motion_planning_python_api/motion_planning_python_api_tutorial.html

To do all this, we need some setup.

We need the URDF and SRDF for UR3e. which we have. We would probably like to define a workcell so it knows where the table is and doesn't plan through it.

URDF isn't stored in one single file, but actually kind of needs to be compiled from a collection of a few xacro files. https://docs.universal-robots.com/Universal_Robots_ROS2_Documentation/doc/ur_description/doc/index.html. xacro is a command within the ros pixi shell and can be passed parameters and used to compile xacro files into URDF files. The repository containing defaults for ur3e is found at https://github.com/UniversalRobots/Universal_Robots_ROS2_Description/tree/rolling/config. I think this is a pixi package you can install. It's `ros-jazzy-ur-description`.

SRDF complements the URDF and makes computation much easier by disabling pairs of links that can never intersect, thus improving trajectory computation time. SRDF for ur3e can be found at https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/tree/main/ur_moveit_config/srdf. One nice thing about SRDF files is that they can contain saved configurations of a robot that can be referenced by string in code.

Extra information on URDF and SRDF can be found here: https://moveit.picknik.ai/main/doc/examples/urdf_srdf/urdf_srdf_tutorial.html. It's possible that it's not necessary.

A work cell describes the environment, and it's also defined as a xacro file. I think all the xacro files go together, and you create a macro (I think.) https://docs.universal-robots.com/Universal_Robots_ROS2_Documentation/doc/ur_tutorials/my_robot_cell/doc/assemble_urdf.html.

Another thing which is necessary is to have the real robot's configuration parameters. If we don't pull the factory config params, the end-effector could be off in the order of centimeters.

We're thinking of using servoing to draw smooth curves because we didn't find a different way to draw arbitrary curves. Maybe not? If we can use splines and cartesian paths, it might just be optimal that way too.


One issue we're having is that we don't know how to connect each of these pieces together inside of a piece of code we'd use to control the robot. Which goes into the launch file and which goes into the node? Are these each just different packages or do we need to create some kind of frankenstein of code to make it work? We're using pixi packages. Are these all packages we can add and reference within python via imports?

Apparently, we should just use a launch file to load the URDF/SRDF, bring up the robot and moveit, then the python script we write is a separate entity that plugs in to the running system. This kind of makes sense when you look at the way we launch our stuff from our `pixi.toml`. To start the simulation (without sending any goal positions to the robot), we run
`mock = "ros2 launch ur_robot_driver ur_control.launch.py ur_type:=ur3e robot_ip:=0.0.0.0 use_mock_hardware:=true launch_dashboard_client:=false kinematics_params_file:=$PIXI_PROJECT_ROOT/myconfig.yaml"`
This references the type of the robot (ur3e), and passes that as a parameter into the launch file ur_control.launch.py from the ur_robot_driver package.
Then when we actually want to send goals, we use `test = "ros2 launch ur_robot_driver test_scaled_joint_trajectory_controller.launch.py"`.
This one doesn't reference the robot type whatsoever, and it works just fine.

One thing that makes me suspect we need to use URDF SRDF stuff anyways is that we do need to specify the ur type when we run the moveit launch file with `ur_moveit.launch.py`. We'll probably need to look at that if we're planning to use the python api for moveit: ``
`moveit = "ros2 launch ur_moveit_config ur_moveit.launch.py ur_type:=ur3e"`
ur_moveit.launch.py can be found here: https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/blob/main/ur_moveit_config/launch/ur_moveit.launch.py
This launch file only references the SRDF, not the URDF.