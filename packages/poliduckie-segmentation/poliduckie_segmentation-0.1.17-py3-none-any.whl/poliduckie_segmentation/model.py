import os

import casadi as ca
import numpy as np

class Model:
    def __init__(self, dt=10):
        pkg_path = os.path.abspath(__file__)
        model_path = os.path.join(os.path.dirname(pkg_path), 'models', 'robot_model.casadi')
        self.model = ca.Function.load(model_path)

    def get_model(self):
        return self.model
      
    def step(self, x, y, theta, speed, angular_speed, action, wheel_distance=0.10467):
        linear_speed, angular_speed = action
        left_speed = (2*linear_speed - wheel_distance*angular_speed)/2
        right_speed = 2*linear_speed - left_speed
        return self.model([x, y, theta, speed, angular_speed], [left_speed, right_speed])
    
    def step_wheel_speed(self, x, y, theta, speed, angular_speed, action):
        return self.model([x, y, theta, speed, angular_speed], action)
