# Original filepath: .pixi/envs/default/lib/python3.12/site-packages/ros2_controllers_test_nodes/publisher_joint_trajectory_controller.py
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from ikpy.chain import Chain
import numpy as np

# Test 2: Integrate an IK solver so we can move the arm to arbitrary points while keeping the end-effector pointed down.
# - Try ikpy first.
# - If it's not enough, then moveit.
# Perform test 2: Move robot arm so end-effector goals reach the corners of a square. (DONE)

# Test 2.5: Create an ikpy helper script to visualize paths compared to the checkpoints.
# - For debug.

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
        self.declare_parameter("urdf_path", "")

        # Read parameters
        self.goal_names = self.get_parameter("goal_names").value
        self.publish_delay = self.get_parameter("goal_publish_delay_seconds").value
        self.joints = self.get_parameter("joints").value
        self.controller = self.get_parameter("controller").value
        self.topic = self.get_parameter("topic").value
        self.urdf_path = self.get_parameter("urdf_path").value

        self.get_logger().info("URDF file: " + self.urdf_path)
        # Load ikpy chain from URDF file. Then, generate joint trajectories from points in config, adding them to the goal
        self.chain = Chain.from_urdf_file(
            self.urdf_path,
            active_links_mask=[False, False, True, True, True, True, True, True, False] # Derived from the following two lines
        )
        # links = [(l.name, l.has_rotation) for l in chain.links]
        # self.get_logger().info(f"Active links: {str(links)}")


        self.setpoints = []
        self.prepare_setpoints()
        # self.get_logger().info(str(self.goals))
        self.goals = []
        self.interpolate_trajectory()


        if len(self.setpoints) == 0:
            raise Exception("No valid goal found. Exiting.")

        publish_topic = "/" + self.controller + "/" + self.topic
        self.i = 0
        self.log_list(self.goals)

        self.publisher_ = self.create_publisher(JointTrajectory, publish_topic, 1)
        traj = JointTrajectory()
        traj.joint_names = self.joints
        traj.points.extend(self.goals)
        self.publisher_.publish(traj)
        self.get_logger().info("Finishing, about to exit.")
        exit(0)
    
    # Generate the actual trajectory by taking the overarching goals and generating checkpoints between them
    def interpolate_trajectory(self):
        if len(self.setpoints) < 2:
            return

        # move to config file
        interpolation_dist = 0.05
        prev_angles = np.zeros(len(self.chain.links))
        time = 2

        for idx in range(1, len(self.setpoints)):
            prev = self.setpoints[idx-1]
            point = self.setpoints[idx]

            for goal_coords in self.interpolate_to_goal(prev, point, interpolation_dist):
                goal = JointTrajectoryPoint()
                target = self.make_target_frame(*goal_coords)
                raw_angles = self.chain.inverse_kinematics_frame(
                    target,
                    initial_position=prev_angles,
                    orientation_mode="Z"
                )
                # Only keep active links
                angles = raw_angles[2:8]


                # Set the final values and continue to the next goal.
                goal.positions = angles
                goal.time_from_start = Duration(sec=time)
                
                self.goals.append(goal)
                time += 1
                prev_angles = raw_angles

    # Return a list of checkpoints at an interval from from_pt to to_pt, excluding the initial point.
    def interpolate_to_goal(self, from_pt, to_pt, interval):
        from_pt = np.array(from_pt)
        to_pt = np.array(to_pt)
        checkpoints = []

        displacement = to_pt - from_pt
        step = (displacement / np.linalg.norm(displacement)) * interval

        next = from_pt
        while np.linalg.norm(to_pt - next) > interval:
            next += step
            checkpoints.append(next)

        return checkpoints + [to_pt]

    # Use the IK solver to generate trajectories.
    # To use this, we must have passed in the URDF path.
    # Only handles setpoints defined as goal points, not joint angles.
    def prepare_setpoints(self):

        self.declare_parameter("pen_tip_dist", rclpy.Parameter.Type.DOUBLE)
        self.pen_tip_dist = self.get_parameter("pen_tip_dist").value

        for name in self.goal_names:
            # Extract the goal and create xyz coordinates
            point_subparam = name + ".point"
            self.declare_parameter(name, rclpy.Parameter.Type.DOUBLE_ARRAY)
            self.declare_parameter(point_subparam, [float()])
            
            self.setpoints.append(self.get_parameter(point_subparam).value + [self.pen_tip_dist])

    def make_target_frame(self, x, y, z):
        # End-effector pointing straight down: Z-axis of EE = world -Z
        frame = np.eye(4)
        frame[:3, 3] = [x, y, z]          # position
        frame[:3, 2] = [0, 0, 1]          # EE z-axis points world-down
        frame[:3, 0] = [1, 0, 0]          # EE x-axis
        frame[:3, 1] = [0, 1, 0]          # EE y-axis
        return frame
    
    def log(self, s):
        self.get_logger().info(s)

    def log_val(self, v, s=""):
        self.get_logger().info(f"{s}: Type: {type(v)}, {v}")

    def log_list(self, l):
        for idx, item in enumerate(l):
            self.get_logger().info(f"{idx}: {str(item)}")

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


