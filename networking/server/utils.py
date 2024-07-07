import socket
import os
from sys import platform
import numpy as np
from PIL import Image
import pygame
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


RED = [255, 0, 0]
BLUE = [0, 0, 255]
DARK_RED = [200, 10, 10]
BLACK = [0, 0, 0]
GREY = [230, 230, 230]
GREEN = [0, 255, 0]
DARK_GREEN = [10, 200, 10]


def background_loader(image_path):
    img = Image.open(image_path)
    width, height = img.size

    half_x = 1750
    half_y = 800
    init_width = width // 2
    init_height = height // 2
    aspect_factor = 2

    img = img.crop((init_width - half_x, init_height - half_y, init_width + half_x, init_height + half_y))

    width, height = img.size
    img = img.resize((int(width / aspect_factor), int(height / aspect_factor)))

    mode = img.mode
    disp_size = img.size
    byte_image = img.tobytes()

    return byte_image, width, height, disp_size, mode, init_height, init_width, half_x, half_y, aspect_factor


# class Control_Points:
#     def __init__(self, x_history, y_history, speed_history, x_ref, y_ref, speed_ref, speed_error, throttle_history):
#         self.x_history = x_history
#         self.y_history = y_history
#         self.speed_history = speed_history
#         self.x_ref = x_ref
#         self.y_ref = y_ref
#         self.speed_ref = speed_ref
#         self.speed_error = speed_error
#         self.throttle_history = throttle_history
    
#     def publish():


class Button:

    def __init__(self, rect, color, command, text=''):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.command = self._command if (command == None)  else command
        self.clicked = False
    
    def _command(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.text != '':
            font = pygame.font.SysFont('impact', 32)
            text = font.render(self.text, 1, (0, 0, 0))
            surface.blit(text, (self.rect.x + (self.rect.width / 2 - text.get_width() / 2),
                                self.rect.y + (self.rect.height / 2 - text.get_height() / 2)))
            
    def click(self):
        self.command()
        self.clicked = True
    
    def unclick(self):
        self.clicked = False

    def is_colliding(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False
    
    def is_clicked(self, pos):
        self.is_hovered(pos)
        if self.rect.collidepoint(pos):
            self.click()
        else:
            self.unclick()

    def is_released(self, command = None):
        if self.clicked:
            self.unclick()
            if command != None:
                command()
            print("RELEASED", self.text, "Value:", self.clicked)
    
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.color = DARK_GREEN
        else:
            self.color = GREEN


def get_ip():
    if platform == "linux" or platform == "linux2":
        gw = os.popen("ip -4 route show default").read().split()
        gw = gw[2]
    elif platform == "win32":
        os.system('ipconfig | findstr /i "Gateway" > temp.txt')
        with open("temp.txt", "r") as f:
            gw = f.readlines()[-1].strip().split(" ")[-1]

    print("Deafault Gateway: ", gw)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw, 0))
    ipaddr = s.getsockname()[0]
    print(f"Host IP is {ipaddr}")
    return ipaddr

def bicycle_kinematic_model(y, t, v, L, Kp, x_goal, y_goal):
    """
    Bicycle kinematic model with proportional control.

    Parameters:
        y (list): State variables [x, y, theta].
        t (float): Time.
        v (float): Velocity of the bicycle (m/s).
        L (float): Wheelbase of the bicycle (meters).
        Kp (float): Proportional gain for the controller.
        x_goal (float): Goal x position.
        y_goal (float): Goal y position.

    Returns:
        dydt: Derivatives of state variables.
    """
    x, y, theta = y
    x_dot = v * np.cos(theta)
    y_dot = v * np.sin(theta)

    # Proportional control for steering
    delta_desired = np.arctan2(y_goal - y, x_goal - x)
    delta_error = delta_desired - theta
    delta_dot = Kp * delta_error

    theta_dot = (v / L) * np.tan(delta_dot)

    dydt = [x_dot, y_dot, theta_dot]
    return dydt


def add_vectors(v1, v2):
    return [a + b for a, b in zip(v1, v2)]

def sub_vectors(v1, v2):
    return [a - b for a, b in zip(v1, v2)]

def scale_vector(v, scalar):
    return [a * scalar for a in v]

def magnitude(v):
    return math.sqrt(sum(a**2 for a in v))

def normalize_vector(v):
    mag = magnitude(v)
    return [a / mag for a in v]

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


# Tangent point initialization
def init_tangent_point(control_points, tangent_points, cur_idx):
    prev_idx = cur_idx - 1
    next_idx = cur_idx + 1

    p_cur = control_points[cur_idx]
    p_prev = control_points[prev_idx]
    p_next = control_points[next_idx]

    v_left = sub_vectors(p_prev, p_cur)
    v_right = sub_vectors(p_next, p_cur)

    unit_v_left = normalize_vector(v_left)
    unit_v_right = normalize_vector(v_right)

    bisector = add_vectors(unit_v_left, unit_v_right)

    d_product = dot_product(v_left, bisector)
    proj = d_product / (magnitude(bisector) + 1e-9)

    unit_bisector = normalize_vector(bisector)
    parallel_proj = scale_vector(unit_bisector, proj)

    perpendicular_proj = sub_vectors(v_left, parallel_proj)
    unit_perp_proj = normalize_vector(perpendicular_proj)

    mag_v_left = magnitude(v_left)
    mag_v_right = magnitude(v_right)
    mag_tangent_point = min(mag_v_left, mag_v_right) / 2

    v_left_tangent = add_vectors(p_cur, scale_vector(unit_perp_proj, mag_tangent_point))
    v_right_tangent = sub_vectors(scale_vector(p_cur, 2.0), v_left_tangent)

    tangent_points[cur_idx] = [v_left_tangent, v_right_tangent]

# Adding tangent points
def add_tangent_point(control_points, tangent_points):
    num_control_points = len(control_points)
    cur_tangent_points = [control_points[-1], control_points[-1]]
    tangent_points.append(cur_tangent_points)

    if num_control_points > 2:
        cur_idx = num_control_points - 2
        init_tangent_point(control_points, tangent_points, cur_idx)


# Cubic Bezier calculation
def get_cubic_bezier(p0, p1, p2, p3, t):
    c0 = (1 - t) ** 3
    c1 = 3 * (1 - t) ** 2 * t
    c2 = 3 * (1 - t) * t ** 2
    c3 = t ** 3

    v0 = scale_vector(p0, c0)
    v1 = scale_vector(p1, c1)
    v2 = scale_vector(p2, c2)
    v3 = scale_vector(p3, c3)

    return add_vectors(add_vectors(v0, v1), add_vectors(v2, v3))

def get_cubic_bezier_derivative(p0, p1, p2, p3, t):
    c0 = -3 * (1 - t) ** 2
    c1 = 3 * (1 - t) ** 2 - 6 * t * (1 - t)
    c2 = 6 * t * (1 - t) - 3 * t ** 2
    c3 = 3 * t ** 2

    v0 = scale_vector(p0, c0)
    v1 = scale_vector(p1, c1)
    v2 = scale_vector(p2, c2)
    v3 = scale_vector(p3, c3)

    return add_vectors(add_vectors(v0, v1), add_vectors(v2, v3))

def calculate_yaw_angle(tangent):
    reference = [1, 0] #x-axis
    return angle_between_vectors(reference, tangent)

# Piecewise cubic Bezier curve calculation
def calculate_piecewise_cubic_bezier_with_yaw(control_points, tangent_points, samples_per_bezier):
    cubic_bezier = []
    yaw_angles = []
    num_control_points = len(control_points)

    for i in range(num_control_points - 1):
        p0 = control_points[i]
        p3 = control_points[i + 1]
        p1 = tangent_points[i][1]
        p2 = tangent_points[i + 1][0]

        cubic_bezier.append(p0)

        t = 0.0
        delta_t = 1.0 / (samples_per_bezier - 1.0)
        for j in range(1, samples_per_bezier - 1):
            t += delta_t
            bezier_point = get_cubic_bezier(p0, p1, p2, p3, t)
            tangent = get_cubic_bezier_derivative(p0, p1, p2, p3, t)
            yaw_angle = calculate_yaw_angle(tangent)

            cubic_bezier.append(bezier_point)
            yaw_angles.append(yaw_angle)

        if len(yaw_angles) > 0:
            yaw_angles.append(yaw_angles[-1])

    return cubic_bezier, yaw_angles

def angle_between_vectors(v1, v2):
    dot = dot_product(v1, v2)
    mag_v1 = magnitude(v1)
    mag_v2 = magnitude(v2)
    return math.degrees(math.acos(dot / (mag_v1 * mag_v2)))

def draw_arrow(screen, p, direction, length=20, color=(255, 0, 0)):
    endpoint = add_vectors(p, scale_vector(normalize_vector(direction), length))
    pygame.draw.line(screen, color, p, endpoint)
    pygame.draw.circle(screen, color, endpoint, 3)


def write_trajectroy_data_to_csv(x_history, y_history, speed_history, x_ref, y_ref, speed_ref, speed_error, throttle_history, filename='trajectory.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x_history', 'y_history', 'speed_history', 'x_ref', 'y_ref', 'speed_ref', 'speed_error', 'throttle_history'])
        for x_h, y_h, s_h, x_r, y_r, s_r, s_e, t_h in zip(x_history, y_history, speed_history, x_ref, y_ref, speed_ref, speed_error, throttle_history):
            writer.writerow([x_h, y_h, s_h, x_r, y_r, s_r, s_e, t_h])
