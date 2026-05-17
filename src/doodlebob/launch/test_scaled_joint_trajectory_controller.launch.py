# Description: After a robot has been loaded, this will execute a series of trajectories.

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # what does this do?
    # Find this package(ur robot driver)'s share within the .pixi/envs/default directory. The PathJoinSubstitution just combines these paths.
    # We load the config containing the test goal locations.
    position_goals = PathJoinSubstitution(
        [
            FindPackageShare("ur_robot_driver"),
            "config",
            "test_goal_publishers_config.yaml",
        ]
    )

    # ???
    check_starting_point = LaunchConfiguration("check_starting_point")

    # Our list of actions for this LaunchDescription. We define an argument and then create a node which uses that argument.
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "check_starting_point",
                default_value="true",
                description="Verify that the robot is at a preconfigured pose in order to avoid large unexpected motions.",
            ),
            # we create a node using this call. It can be any node in any package.
            # The executable is just the code module to run as this node. It's like specifying package and node.
            # You can also specify the namespace in case you want to use the same node and name somewhere else.
            Node(
                package="doodlebob",
                executable="doodle_test_node",
                name="publisher_scaled_joint_trajectory_controller",
                parameters=[
                    position_goals,
                    {
                        "check_starting_point": check_starting_point,
                    },
                ],
                output="screen",
            ),
        ]
    )
