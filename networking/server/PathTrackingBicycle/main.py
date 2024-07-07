import numpy as np
import matplotlib.pyplot as plt
import csv, os

from PathTrackingBicycle.controller2d import Controller2D
from PathTrackingBicycle.bicyclemodel import NonLinearBicycleModel, LinearBicycleModel

# from controller2d import Controller2D
# from bicyclemodel import NonLinearBicycleModel, LinearBicycleModel

# waypoint file to load
WAYPOINTS_FILENAME = 'E:\\drive\\Image Stitching\\Networking\\server\\server\\PathTrackingBicycle\\trajectory.txt'
INTERP_DISTANCE_RES = 0.01  # distance between interpolated points
INTERP_LOOKAHEAD_DISTANCE = 20  # lookahead in meters
DIST_THRESHOLD_TO_LAST_WAYPOINT = 10.0  # some distance from last position before simulation ends

# use linear or nonlinear bicycle models
non_linear_model = True  # True, False
if non_linear_model:
    trajectory_path = "trajectory_non_linear.png"
    speed_path = "speed_non_linear.png"
else:
    trajectory_path = "trajectory_linear.png"
    speed_path = "speed_linear.png"

# show the animation plot during the simulation, default is False.
show_animation = False


def waypoint_generator(waypoints_np=None):
    #############################################
    # Load Waypoints
    #############################################
    waypoints = None if waypoints_np is None else waypoints_np.tolist()
    if waypoints_np is None:
        waypoints_file = WAYPOINTS_FILENAME
        with open(waypoints_file) as waypoints_file_handle:
            waypoints = list(csv.reader(waypoints_file_handle,
                                        delimiter=',',
                                        quoting=csv.QUOTE_NONNUMERIC))
            waypoints_np = np.array(waypoints)

    # Linear interpolation computations, we can also use spine interpolation
    wp_distance = []  # distance array
    for i in range(1, waypoints_np.shape[0]):
        wp_distance.append(
            np.sqrt((waypoints_np[i, 0] - waypoints_np[i - 1, 0]) ** 2 +
                    (waypoints_np[i, 1] - waypoints_np[i - 1, 1]) ** 2))
    # last distance is 0 because it is the distance from the last waypoint to the last waypoint
    wp_distance.append(0)

    # Linearly interpolate between waypoints and store in a list
    wp_interp = []  # interpolated values
    # (rows = waypoints, columns = [x, y, v])
    wp_interp_hash = []
    # hash table which indexes waypoints_np to the index of the waypoint in wp_interp
    interp_counter = 0  # counter for current interpolated point index
    reached_the_end = False

    for i in range(waypoints_np.shape[0] - 1):
        # Add original waypoint to interpolated waypoints list (and append
        # it to the hash table)
        wp_interp.append(list(waypoints_np[i]))
        wp_interp_hash.append(interp_counter)
        interp_counter += 1

        # Interpolate to the next waypoint. First compute the number of
        # points to interpolate based on the desired resolution and
        # incrementally add interpolated points until the next waypoint
        # is about to be reached.
        num_pts_to_interp = int(np.floor(wp_distance[i] / \
                                         float(INTERP_DISTANCE_RES)) - 1)
        wp_vector = waypoints_np[i + 1] - waypoints_np[i]
        wp_uvector = wp_vector / np.linalg.norm(wp_vector)
        for j in range(num_pts_to_interp):
            next_wp_vector = INTERP_DISTANCE_RES * float(j + 1) * wp_uvector
            wp_interp.append(list(waypoints_np[i] + next_wp_vector))
            interp_counter += 1
    # add last waypoint at the end
    wp_interp.append(list(waypoints_np[-1]))
    wp_interp_hash.append(interp_counter)
    interp_counter += 1

    # ==================================    
    # Controller 2D Class and vehicle model declaration
    # ==================================
    controller = Controller2D(waypoints)
    if non_linear_model:
        state = NonLinearBicycleModel(x=waypoints_np[0][0], y=waypoints_np[0][1], yaw=np.radians(waypoints_np[0][2]))
    else:
        state = LinearBicycleModel(x=waypoints_np[0][0], y=waypoints_np[0][1], yaw=np.radians(waypoints_np[0][2]))

    start_x, start_y, start_yaw = state.x, state.y, state.yaw
    state.update(throttle=0, delta=0)
    x_history = [start_x]
    y_history = [start_y]
    yaw_history = [start_yaw]
    speed_history = [0]
    # Index of waypoint that is currently closest to the car, assumed to be the first index
    closest_index = 0
    steps = 0
    # reference track and speed for plotting usage
    x_ref = list(waypoints_np[:, 0])
    y_ref = list(waypoints_np[:, 1])
    speed_ref = []

    # for debug
    speed_error = []
    throttle_history = []

    while True:
        steps = steps + 1

        # Update position, timestamp
        current_x, current_y, current_yaw = state.x, state.y, state.yaw
        if non_linear_model:
            current_speed = state.vx
        else:
            current_speed = state.v

        # for debug use
        # if steps % 1000 == 0:
        #     print(
        #         "step {s}, cx {cx}, cy {cy}, cv {cv}".format(s=steps, cx=current_x, cy=current_y, cv=current_speed))

        # Store history
        x_history.append(current_x)
        y_history.append(current_y)
        yaw_history.append(current_yaw)
        speed_history.append(current_speed)

        # Controller update
        closest_distance = np.linalg.norm(np.array([
            waypoints_np[closest_index, 0] - current_x,
            waypoints_np[closest_index, 1] - current_y]))
        new_distance = closest_distance
        new_index = closest_index
        while new_distance <= closest_distance:
            closest_distance = new_distance
            closest_index = new_index
            new_index += 1
            if new_index >= waypoints_np.shape[0]:  # End of path
                break
            new_distance = np.linalg.norm(np.array([
                waypoints_np[new_index, 0] - current_x,
                waypoints_np[new_index, 1] - current_y]))

        new_distance = closest_distance
        new_index = closest_index
        while new_distance <= closest_distance:
            closest_distance = new_distance
            closest_index = new_index
            new_index -= 1
            # Beginning of path
            if new_index < 0:
                break
            new_distance = np.linalg.norm(np.array([
                waypoints_np[new_index, 0] - current_x,
                waypoints_np[new_index, 1] - current_y]))

        # Once the closest index is found, return the path that has 1
        # waypoint behind and X waypoints ahead, where X is the index
        # that has a lookahead distance specified by INTERP_LOOKAHEAD_DISTANCE
        waypoint_subset_first_index = closest_index - 1
        if waypoint_subset_first_index < 0:
            waypoint_subset_first_index = 0

        waypoint_subset_last_index = closest_index
        total_distance_ahead = 0
        while total_distance_ahead < INTERP_LOOKAHEAD_DISTANCE:
            total_distance_ahead += wp_distance[waypoint_subset_last_index]
            waypoint_subset_last_index += 1
            if waypoint_subset_last_index >= waypoints_np.shape[0]:
                waypoint_subset_last_index = waypoints_np.shape[0] - 1
                break

        # Use the first and last waypoint subset indices into the hash
        # table to obtain the first and last indicies for the interpolated
        # list. Update the interpolated waypoints to the controller
        # for the next controller update.
        new_waypoints = \
            wp_interp[wp_interp_hash[waypoint_subset_first_index]: \
                      wp_interp_hash[waypoint_subset_last_index] + 1]
        # update waypoints
        controller.update_waypoints(new_waypoints)
        # Update the other controller values and controls
        controller.update_values(current_x, current_y, current_yaw,
                                 current_speed)

        controller.update_controls()
        speed_ref.append(controller._desired_speed)

        # for debug use, to better visualise, we multiply throttle with 5
        throttle_history.append(5 * (controller.throttle))
        speed_error.append(controller._e)

        # Output controller command to the vehicle and update the states
        state.update(throttle=controller.throttle, delta=controller.steer)

        # Find if reached the end of waypoint. If the car is within DIST_THRESHOLD_TO_LAST_WAYPOINT to the last waypoint,
        # then simulation will be terminated.
        dist_to_last_waypoint = np.linalg.norm(np.array([
            waypoints[-1][0] - current_x,
            waypoints[-1][1] - current_y]))
        
        if dist_to_last_waypoint < DIST_THRESHOLD_TO_LAST_WAYPOINT:
            reached_the_end = True
            print("Reached the end of path. Writing to controller_output...")

        if reached_the_end:
            # save the plot at the end of the simulation
            plot_fn(x_history, y_history, x_ref, y_ref, speed_history, speed_ref, speed_error, throttle_history)
            # plot_debug(speed_error)  # for debug
            break
        
        if show_animation:
            plt.cla()
            plot_vehicle(x_history, y_history, x_ref, y_ref, steps) 

    return x_history, y_history, speed_history, x_ref, y_ref, speed_ref, speed_error, throttle_history


def plot_vehicle(x_traj, y_traj, x_ref, y_ref, frame):
    plt.plot(x_traj, y_traj, 'b--')
    plt.plot(x_ref, y_ref, 'r-')
    # for stopping simulation with the esc key.
    plt.gcf().canvas.mpl_connect('key_release_event',
                                 lambda event: [exit(0) if event.key == 'escape' else None])

    # plt.xlim(-250, 400)
    # plt.ylim(-800, 100)
    plt.title('frame={}'.format(frame))

    plt.pause(0.01)


def plot_fn(x_history, y_history, x_ref, y_ref, speed_history, speed_ref, speed_error, throttle):
    os.makedirs("results", exist_ok=True)
    plt.figure(1)
    plt.plot(x_history, y_history, 'b-', label='real')
    plt.plot(x_ref, y_ref, 'r--', label='ref')
    plt.title('Vehicle trajectory')
    # plt.xlim(-250, 400)
    # plt.ylim(-800, 100)
    plt.legend()
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.savefig('results/' + trajectory_path)

    plt.figure(2)
    plt.plot(speed_history, 'b-', label='real')
    plt.plot(speed_ref, 'r--', label='ref')
    # plt.plot(speed_error, 'k', label='error')  # v_desired - v
    # for visualization, we multiply 2
    plt.plot(throttle, 'g', label='throttle')
    plt.title('Vehicle speed')
    plt.legend()
    plt.grid(True)
    plt.xlabel('waypoint # ')
    plt.ylabel('speed (m/s)')
    plt.savefig('results/' + speed_path)


def plot_debug(speed_error):
    # plot for debug use
    plt.figure(3)
    plt.plot(speed_error)
    plt.title('Vehicle speed tracking error')
    plt.savefig('results/tracking_error')


if __name__ == '__main__':
    waypoint_generator()
