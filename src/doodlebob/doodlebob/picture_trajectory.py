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
# - Define launch file. (DONE)
# - Define parameter file to store parameters like positions. (DONE)
# Perform test 1. (DONE)

# Test 2: Integrate an IK solver so we can move the arm to arbitrary points while keeping the end-effector pointed down.
# - Try ikpy first.
# - If it's not enough, then moveit.

# Test 3: How do we know where the paper to draw on is? Maybe start with an assumption.
# - Define a paper size.
# - Define the paper rotation.
# - Define the origin of the sheet of paper, ensuring it doesn't intersect with the base of the robot.
# Perform test 3: Trace the edges of the drawing area with the robot arm based on define paper size and orientation.

# Test 4: Test movement trajectory based on an SVG input file. Pass the file on the command line?

class PictureTrajectoryPublisher(Node):
    def __init__(self):
        # The node name, shows up when you type ros2 node list.
        # Can be overwritten in the launch file.
        super().__init__("picture_trajectory_publisher")
        # By this point, the parameters defined in the launch file can be registered
        # with the node for use and then used by using declare_parameter and then get_parameter.
        # The default parameter also specifies the expected type of the parameter.
        # Declare all parameters
        self.declare_parameter("goal_names", [""])
        self.declare_parameter("goal_publish_delay_seconds", 10)
        self.declare_parameter("joints", [""])
        self.declare_parameter("controller", "")
        self.declare_parameter("topic", "")

        # Read parameters
        self.goal_names = self.get_parameter("goal_names").value
        self.publish_delay = self.get_parameter("goal_publish_delay_seconds").value
        self.joints = self.get_parameter("joints").value
        self.controller = self.get_parameter("controller").value
        self.topic = self.get_parameter("topic").value

        self.goals = []
        for name in self.goal_names:
            point = JointTrajectoryPoint()
            position_subparam = name + ".positions"
            
            # Get the nested joint rotation values
            self.declare_parameter(name, rclpy.Parameter.Type.DOUBLE_ARRAY)
            self.declare_parameter(position_subparam, [float()])
            positions = self.get_parameter(position_subparam).value

            if len(positions) != len(self.joints):
                raise ValueError(f"Length of joint angle list for goal position {name} doesn't match actual amount of joints {len(self.joints)}.")
            point.positions = positions
            point.time_from_start = Duration(sec=4)
            self.goals.append(point)
            
        if len(self.goals) == 0:
            raise Exception("No valid goal found. Exiting.")

        publish_topic = "/" + self.controller + "/" + self.topic
        self.i = 0



        self.get_logger().info("Starting loop")
        self.publisher_ = self.create_publisher(JointTrajectory, publish_topic, 1)
        self.timer = self.create_timer(self.publish_delay, self.timer_callback)
    # This one doesn't cause an early exit.
    #def timer_callback(self):


    #    traj = JointTrajectory()
    #    traj.joint_names = self.joints
    #    traj.points.append(self.goals[self.i])
    #    self.publisher_.publish(traj)

    #    self.i += 1
    #    self.i %= len(self.goals)

    # This one does. why??
    def timer_callback(self):
        # self.get_logger().info(f"Sending goal {self.goals[self.i]}.")
        traj = JointTrajectory()
        traj.joint_names = self.joints
        traj.points.append(self.goals[self.i])
        self.publisher_.publish(traj)
        
        self.i += 1
        self.i %= len(self.goals)

    def joint_state_callback(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)

    picture_trajectory_publisher = PictureTrajectoryPublisher()

    try:
        rclpy.spin(picture_trajectory_publisher)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        print("Keyboard interrupt received. Shutting down node.")
    except Exception as e:
        print(f"Unhandled exception: {e}")


if __name__ == "__main__":
    main()


