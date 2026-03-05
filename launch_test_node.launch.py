import os
from pathlib import Path
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

here = os.path.dirname(os.path.abspath(__file__))

def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder(robot_name="ur", package_name="ur_moveit_config")
        .robot_description(
            file_path="config/ur.urdf.xacro",
            mappings={"ur_type": "ur3e"}
        )
        .robot_description_semantic(Path("srdf") / "ur.srdf.xacro", {"name": "ur3e"})
        .moveit_cpp(file_path=os.path.join(here, "pipeline.yaml"))
        .to_moveit_configs()
    )

    test_node = Node(
        name="test_drawing_node",
        executable=os.path.join(os.path.dirname(__file__), "test_node.py"),
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription([test_node])
