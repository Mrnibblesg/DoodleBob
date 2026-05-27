# Original filepath: .pixi/envs/default/lib/python3.12/site-packages/ros2_controllers_test_nodes/publisher_joint_trajectory_controller.py
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState

# We'll need:
# - config file for parameters (joint names, etc.)
# - Launch file for node setup

# To-do (ordered):
# Test 1: Move the tool to a custom start position.
# - Define launch file.
# - Define parameter file to store parameters like positions.
# Perform test 1.

# Test 2: How do we know where the paper to draw on is? Maybe start with an assumption.
# - Define a paper size.
# - Define the paper rotation.
# - Define the origin of the sheet of paper, ensuring it doesn't intersect with the base of the robot.
# Perform test 2.

# Test 3: Test movement trajectory based on an SVG input file. Pass the file on the command line?
# Integrate moveit?

class PictureTrajectoryPublisher(Node):
    def __init__(self):
        # The node name, shows up when you type ros2 node list.
        # Can be overwritten in the launch file.
        super().__init__("picture_trajectory_publisher")
        # By this point, the parameters defined in the launch file can be registered
        # with the node for use and then used by using declare_parameter and then get_parameter.
        # Declare all parameters

        # Read parameters
        
        self.get_logger().info("HELLO WORLD")
        controller_name = ""
        publish_topic = "/" + controller_name + "/" + "joint_trajectory"
        wait_sec_between_publish = 1
        self.publisher_ = self.create_publisher(JointTrajectory, publish_topic, 1)
        self.timer = self.create_timer(wait_sec_between_publish, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        self.get_logger().info("Timestep: " + self.i)
        self.i += 1
        pass

    def joint_state_callback(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)

    publisher_joint_trajectory = PictureTrajectoryPublisher()

    try:
        rclpy.spin(publisher_joint_trajectory)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        print("Keyboard interrupt received. Shutting down node.")
    except Exception as e:
        print(f"Unhandled exception: {e}")


if __name__ == "__main__":
    main()


