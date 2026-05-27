from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    parameters = PathJoinSubstitution(
        [
            FindPackageShare("doodlebob"),
            "config",
            "pic_drawing_config.yaml"
        ]
    )
    return LaunchDescription(
        [
            Node(
                package="doodlebob",
                executable="picture_trajectory",
                name="doodlebob_picture_trajectory_publisher",
                parameters=[
                    parameters,
                ]
            )
        ]
    )
