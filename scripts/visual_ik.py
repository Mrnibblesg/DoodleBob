import ikpy.chain
import ikpy.utils.plot as plot_utils
import numpy as np
import matplotlib.pyplot as plt

# To view what it's like when the arm can't reach a point, set all 0.25 to 0.3
c1 = [0.1, 0.1, 0.15]
c2 = [0.1, 0.25, 0.15]
c3 = [0.25, 0.25, 0.15]
c4 = [0.25, 0.1, 0.15]
targets = [c1, c2, c3, c4, c1]

start_conf = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]

def main():
    fig, ax = plot_utils.init_3d_figure()

    chain = ikpy.chain.Chain.from_urdf_file("../configs/ur3e.urdf")
    
    #print(f"Link amount: {len(chain.links)}")
    #print("Names:")
    #for link in chain.links:
    #    print(f"{link.name}")
    
    all_targets = [targets[0]]

    for idx in range(len(targets)-1):
        start = targets[idx]
        end = targets[idx+1]
        all_targets.extend(interpolate_trajectory(start, end))
    ax.plot([0,1], [0,1], 'red', zs=[0,-1])


    # To view the arm's configuration when it targets this point
    debug_point = c3

    reached = []
    zero_config = [0] * len(chain.links)
    prev_angles = zero_config

    # Generate all actual points that the robot arm goes to
    for point in all_targets:
        end_point, prev_angles = arm_config_from_coord(chain, point, prev_angles)

        if debug_point is not None and point[0] == debug_point[0] and point[1] == debug_point[1] and point[2] == debug_point[2]:
            chain.plot(prev_angles, ax, target=point)

        reached.append(end_point)
    # chain.plot(chain.inverse_kinematics(targets[0]), ax, target=targets[0])
    # visualize_points(all_targets, ax, "red")
    visualize_points(reached, ax, "blue")

    plt.show()

# Return a list of points resulting from an interpolated cartesian trajectory
# between start and end, each point separated by interval
def interpolate_trajectory(start, end, interval=0.025):
    start = np.array(start)
    end = np.array(end)
    points = []
    difference = end - start
    dist = np.linalg.norm(difference)
    step = (difference / dist) * interval
    
    next = start
    while (np.linalg.norm(end - next) >= interval):
        next += step
        points.append(next.copy())
    
    points.append(end)
    return points

def make_target_frame(x, y, z):
    # End-effector pointing straight down: Z-axis of EE = world -Z
    frame = np.eye(4)
    frame[:3, 3] = [x, y, z]          # position
    frame[:3, 2] = [0, 0, 1]          # EE z-axis points world-down
    frame[:3, 0] = [1, 0, 0]          # EE x-axis
    frame[:3, 1] = [0, 1, 0]          # EE y-axis
    return frame

# Return the FK point after trying to make the chain reach the coordinate
def arm_config_from_coord(chain, coordinate, prev_angles):
    target_frame = make_target_frame(*coordinate)
    angles = chain.inverse_kinematics_frame(
            target_frame,
            initial_position=prev_angles,
            orientation_mode="Z"
    )

    return chain.forward_kinematics(angles)[:3, 3], angles


# Draw a line between each point.
def visualize_points(points, ax, color):
    for idx in range(len(points)-1):
        curr = points[idx]
        next = points[idx+1]
        ax.plot([curr[0], next[0]], [curr[1], next[1]], color, zs=[curr[2], next[2]])

if __name__ == "__main__":
    main()
