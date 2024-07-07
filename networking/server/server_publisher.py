import socket
import os
import numpy as np
from PIL import Image
import pygame
from utils import Button
from utils import background_loader, get_ip, write_trajectroy_data_to_csv, calculate_piecewise_cubic_bezier_with_yaw, add_tangent_point, sub_vectors, draw_arrow
from utils import GREEN, BLUE, BLACK, RED
from PathTrackingBicycle.main import waypoint_generator

# path of this directory
CWD = os.path.dirname(os.path.abspath(__file__))

RESET_BOOL = False
MARK_POINTS_BOOL = False
INIT_POINT_BOOL = True
SAVE_PATH_BOOL = False
RUN_SERVER_BOOL = False
SHOW_PATH_BOOL = False

def default_handler():
    global RESET_BOOL, MARK_POINTS_BOOL, SAVE_PATH_BOOL, RUN_SERVER_BOOL, SHOW_PATH_BOOL

    RESET_BOOL = False
    MARK_POINTS_BOOL = False
    SAVE_PATH_BOOL = False
    RUN_SERVER_BOOL = False
    SHOW_PATH_BOOL = False


def reset_handler():
    global RESET_BOOL, MARK_POINTS_BOOL, SAVE_PATH_BOOL, RUN_SERVER_BOOL, SHOW_PATH_BOOL

    if RESET_BOOL:
        RESET_BOOL = False
    else:
        RESET_BOOL = True
        MARK_POINTS_BOOL = False
        SAVE_PATH_BOOL = False
        RUN_SERVER_BOOL = False
        SHOW_PATH_BOOL = False

def mark_points_handler():
    global RESET_BOOL, MARK_POINTS_BOOL, SAVE_PATH_BOOL, RUN_SERVER_BOOL, SHOW_PATH_BOOL

    if MARK_POINTS_BOOL:
        MARK_POINTS_BOOL = False
    else:
        MARK_POINTS_BOOL = True
        RESET_BOOL = False
        SAVE_PATH_BOOL = False
        RUN_SERVER_BOOL = False
        SHOW_PATH_BOOL = False

def save_path_handler():
    global RESET_BOOL, MARK_POINTS_BOOL, SAVE_PATH_BOOL, RUN_SERVER_BOOL, SHOW_PATH_BOOL

    if SAVE_PATH_BOOL:
        SAVE_PATH_BOOL = False
    else:
        SAVE_PATH_BOOL = True
        RESET_BOOL = False
        MARK_POINTS_BOOL = False
        RUN_SERVER_BOOL = False
        SHOW_PATH_BOOL = False

def show_path_handler():
    global RESET_BOOL, MARK_POINTS_BOOL, SAVE_PATH_BOOL, RUN_SERVER_BOOL, SHOW_PATH_BOOL

    if SHOW_PATH_BOOL:
        SHOW_PATH_BOOL = False
    else:
        SHOW_PATH_BOOL = True
        SAVE_PATH_BOOL = False
        RESET_BOOL = False
        MARK_POINTS_BOOL = False
        RUN_SERVER_BOOL = False

def run_server_handler():
    global RESET_BOOL, MARK_POINTS_BOOL, SAVE_PATH_BOOL, RUN_SERVER_BOOL, SHOW_PATH_BOOL

    if RUN_SERVER_BOOL:
        RUN_SERVER_BOOL = False
    else:
        RUN_SERVER_BOOL = True
        RESET_BOOL = False
        MARK_POINTS_BOOL = False
        SAVE_PATH_BOOL = False
        SHOW_PATH_BOOL = False

IMAGE_PATH = CWD + "/image2.png"
byte_image, width, height, disp_size, mode,init_height, init_width, half_x, half_y, aspect_factor = background_loader(IMAGE_PATH)

pygame.init()
screen = pygame.display.set_mode(disp_size)
pygame.display.set_caption('TestBed')

background = pygame.image.fromstring(byte_image, disp_size, mode)

reset_button = Button(([1000, 200], [200, 30]), GREEN, reset_handler, text='Reset')
mark_points = Button(([1000, 240], [200, 30]), GREEN, mark_points_handler, text='Mark Points')
show_path_button = Button(([1000, 280], [200, 30]), GREEN, show_path_handler, text='Show Path')
save_path_button = Button(([1000, 320], [200, 30]), GREEN, save_path_handler, text='Save Path')
run_server_button = Button(([1000, 360], [200, 30]), GREEN, run_server_handler, text='Run Server')

SAMPLES_PER_BEZIER = 10
prev_point = None
WAYPOINTS = []
TANGENT_POINTS = []
BEZIER_POINTS = []
YAW_ANGLES = []
TRAJECTORY_POINTS = []

X_HISTORY, Y_HISTORY, SPEED_HISTORY = [], [], []
X_REF, Y_REF, SPEED_REF = [], [], []
SPEED_ERROR, THROTTLE_HISTORY = [], []

def transform(point):
    x = point[1] + half_x - init_width
    y = point[2] + half_y - init_height
    x = int(x / aspect_factor)
    y = int(y / aspect_factor)
    return x, y

def handle(UDPServerSocket):
    global prev_point, WAYPOINTS, TANGENT_POINTS, BEZIER_POINTS, INIT_POINT_BOOL, YAW_ANGLES, TRAJECTORY_POINTS
    global X_HISTORY, Y_HISTORY, SPEED_HISTORY, X_REF, Y_REF, SPEED_REF, SPEED_ERROR, THROTTLE_HISTORY
    running = True

    while running:

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            reset_button.is_hovered(mouse_pos)
            mark_points.is_hovered(mouse_pos)
            save_path_button.is_hovered(mouse_pos)
            show_path_button.is_hovered(mouse_pos)
            run_server_button.is_hovered(mouse_pos)

            if event.type == pygame.QUIT:
                running = False
                print("Closing the server")

            if event.type == pygame.MOUSEBUTTONDOWN:

                reset_button.is_clicked(mouse_pos)
                mark_points.is_clicked(mouse_pos)
                save_path_button.is_clicked(mouse_pos)
                show_path_button.is_clicked(mouse_pos)
                run_server_button.is_clicked(mouse_pos)

                if RESET_BOOL:
                    print("Resetting")
                    global background
                    background = pygame.image.fromstring(byte_image, disp_size, mode)
                    WAYPOINTS.clear()
                    TANGENT_POINTS.clear()
                    BEZIER_POINTS.clear()
                    YAW_ANGLES.clear()
                    TRAJECTORY_POINTS.clear()
                    INIT_POINT_BOOL = True

                    X_HISTORY.clear()
                    Y_HISTORY.clear()
                    SPEED_HISTORY.clear()
                    X_REF.clear()
                    Y_REF.clear()
                    SPEED_REF.clear()
                    SPEED_ERROR.clear()
                    THROTTLE_HISTORY.clear()

                    prev_point = None

                if MARK_POINTS_BOOL and not (mark_points.is_colliding(mouse_pos)
                                             or reset_button.is_colliding(mouse_pos)
                                             or save_path_button.is_colliding(mouse_pos)
                                             or run_server_button.is_colliding(mouse_pos)):
                    if INIT_POINT_BOOL:
                        initial_point = (1468, 672)
                        try:
                            data, addr = UDPServerSocket.recvfrom(1024)
                            data = np.frombuffer(data, dtype='<u2', count=-1)
                            data = data.reshape((-1, 4))

                            for point in data:
                                _curr_point = transform(point)
                                initial_point = _curr_point
                                break

                            UDPServerSocket.sendto(data, addr)
                            print("Received data -> ", data)

                        except socket.timeout:
                            print("No data received: Timeout Occured.")
                            pass
                            
                        WAYPOINTS.append(initial_point)
                        print("Initial Position at (1468, 672)")
                        INIT_POINT_BOOL = False
                    else:
                        print("Marking points", mouse_pos)
                        WAYPOINTS.append(mouse_pos)
                    # print("Marking points", mouse_pos)
                    # WAYPOINTS.append(mouse_pos)
                    add_tangent_point(WAYPOINTS, TANGENT_POINTS)

                if SHOW_PATH_BOOL:
                    print("Showing path...")

                    beizer_np = np.array(BEZIER_POINTS).astype(np.float32)
                    beizer_np = beizer_np.reshape((-1, 2))
                    yaw_np = np.array(YAW_ANGLES).astype(np.float32)
                    yaw_np = yaw_np.reshape((-1, 1))
                    bezier_yaw_np = np.hstack((beizer_np, yaw_np))
                    X_HISTORY, Y_HISTORY, SPEED_HISTORY, X_REF, Y_REF, SPEED_REF, SPEED_ERROR, THROTTLE_HISTORY = waypoint_generator(bezier_yaw_np)
                    print("Path shown.")

                if SAVE_PATH_BOOL:
                    print("Saving path...")
                    for i in range(len(BEZIER_POINTS) - 1):
                        pygame.draw.line(screen, (0, 0, 0), BEZIER_POINTS[i], BEZIER_POINTS[i + 1])
                    write_trajectroy_data_to_csv(BEZIER_POINTS, YAW_ANGLES)

                    print("Saved path.")

            if event.type == pygame.MOUSEBUTTONUP:
                mark_points.is_released()
                save_path_button.is_released()
                show_path_button.is_released()
                reset_button.is_released(reset_handler)

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        reset_button.draw(screen)
        mark_points.draw(screen)
        save_path_button.draw(screen)
        show_path_button.draw(screen)
        run_server_button.draw(screen)


        if MARK_POINTS_BOOL:
            for point in WAYPOINTS:
                pygame.draw.circle(screen, (10, 10, 10), point, 5)

            for pair in TANGENT_POINTS:
                for point in pair:
                    pygame.draw.circle(screen, (255, 0, 0), point, 3)

            BEZIER_POINTS, YAW_ANGLES = calculate_piecewise_cubic_bezier_with_yaw(WAYPOINTS, TANGENT_POINTS, SAMPLES_PER_BEZIER)
            
        if RUN_SERVER_BOOL:
            # recieve with timeout
            try:
                data, addr = UDPServerSocket.recvfrom(1024)
                data = np.frombuffer(data, dtype='<u2', count=-1)
                data = data.reshape((-1, 4))

                for point in data:
                    curr_point = transform(point)

                    if prev_point is None:
                        prev_point = curr_point
                    
                    TRAJECTORY_POINTS.append(curr_point)
                    prev_point = curr_point

                UDPServerSocket.sendto(data, addr)
                print("Received data -> ", data)

            except socket.timeout:
                print("No data received: Timeout Occured.")
                pass

        for point in WAYPOINTS:
            pygame.draw.circle(screen, RED, point, 4, 3)
        
        for i in range(len(BEZIER_POINTS) - 1):
            pygame.draw.line(screen, BLACK, BEZIER_POINTS[i], BEZIER_POINTS[i + 1])
            if i > 0:  # Draw arrow from second point onwards
                p0 = BEZIER_POINTS[i - 1]
                p1 = BEZIER_POINTS[i]
                direction = sub_vectors(p1, p0)
                draw_arrow(screen, p1, direction)

        for point in TRAJECTORY_POINTS:
            pygame.draw.circle(screen, GREEN, point, 1)
        
        for i in range(len(TRAJECTORY_POINTS) - 1):
            pygame.draw.line(screen, GREEN, TRAJECTORY_POINTS[i], TRAJECTORY_POINTS[i + 1])

        for i in range(len(X_HISTORY) - 1):
            pygame.draw.line(screen, BLUE, (X_HISTORY[i]/1, Y_HISTORY[i]/1), (X_HISTORY[i + 1]/1, Y_HISTORY[i + 1]/1))

        pygame.display.flip()
        pygame.display.update()


def main():
    HOST = get_ip()  # Standard loopback interface address (localhost)
    PORT = 12345  # Port to listen on (non-privileged ports are > 1023)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.settimeout(0.1)
    UDPServerSocket.bind((HOST, PORT))
    print("UDP server up and listening")

    handle(UDPServerSocket)

    pygame.quit()


if __name__ == '__main__':
    main()
