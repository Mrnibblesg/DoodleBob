import rclpy
from rclpy.node import Node

# ROS2 devs rely heavily on runtime introspection tools.
# Viewing a system live is how we discover how things are done.
# What's there, what types things use, and what interfaces look like.
# This is how we can discover what packages to use and how to use them.

# To figure out what we're doing from nothing (hopefully)
# what's running?
# ros2 node list
# ros2 control list_controllers

# what does a specific node expose?
# ros2 node info /passthrough_trajectory_controller

# what actions are available?
# ros2 action list -t

# what does that action's type's interface look like?
# ros2 interface show control_msgs/action/FollowJointTrajectory

# Watch it live:
# ros2 action info /passthrough_trajectory_controller/follow_joint_trajectory
# ros2 topic echo /joint_states

class PassthroughClient(Node):
    def __init__(self):
        super().__init__('passthrough_client')
        # import & create the action client

    def send_trajectory(self):
        self.get_logger().info('Waiting for action server...')
        #self._client.wait_for_server()

        # Send it
        self.get_logger().info('Passthrough test.')
        rclpy.shutdown()


    def goal_response_callback(self, future):
        pass

    def feedback_callback(self, feedback_msg):
        pass

    def result_callback(self, future):
        rclpy.shutdown()
        pass


def main(args=None):
    rclpy.init(args=args)
    node = PassthroughClient()
    node.send_trajectory()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        print("Keyboard interrupt received. Shutting down node.")
    except Exception as e:
        print(f"Unhandled exception: {e}")

if __name__ == '__main__':
    main()
