from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
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
    urdf_path = LaunchConfiguration("urdf_path")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name="urdf_path",
                description="The path to the URDF file of the robot."
            ),
            Node(
                package="doodlebob",
                executable="picture_trajectory",
                name="doodlebob_picture_trajectory_publisher",
                parameters=[
                    parameters,
                    {
                        "urdf_path": urdf_path
                    }
                ]
            )
        ]
    )
