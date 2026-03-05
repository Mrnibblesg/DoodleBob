import rclpy
from moveit.planning import MoveItPy
from moveit_configs_utils import MoveItConfigsBuilder
from pathlib import Path

moveit_config = (
    MoveItConfigsBuilder(robot_name="ur", package_name="ur_moveit_config")
    .robot_description_semantic(Path("srdf") / "ur.srdf.xacro", {"name": "ur3e"})
    .moveit_cpp(Path("config") / "pipeline.yaml")
    .to_moveit_configs()
).to_dict()

rclpy.init()

ur = MoveItPy(node_name="ur", config_dict=moveit_config)
ur_arm = ur.get_planning_component("ur_manipulator")
