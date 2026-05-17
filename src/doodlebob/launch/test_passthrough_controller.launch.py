# Description: After a robot has been loaded, this will execute a series of trajectories.
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            # we create a node using this call. It can be any node in any package.
            # The executable is just the code module to run as this node. It's like specifying package and node.
            # You can also specify the namespace in case you want to use the same node and name somewhere else.
            Node(
                package="doodlebob",
                executable="test_passthrough.py",
                name="test_passthrough_node",
                output="screen",
            ),
        ]
    )

