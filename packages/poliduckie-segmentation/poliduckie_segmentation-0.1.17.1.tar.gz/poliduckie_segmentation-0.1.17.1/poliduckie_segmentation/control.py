import os

import casadi as ca
import numpy as np

class MPC:
    def __init__(self, dt=10, N=2):
        pkg_path = os.path.abspath(__file__)
        model_path = os.path.join(os.path.dirname(pkg_path), 'models', 'mpc_model', f'MPC_N{N}.casadi')
        self.model = ca.Function.load(model_path)
        self.delay = round(0.15/dt)
        self.u_delay0 = ca.DM(np.zeros((2, self.delay)))

    def get_model(self):
        return self.model

    def mpc_wheel_speed(self, x, r, tr=None, u_delay=None,  Q1=1e3, Q2=5e-4, Q3=1, R=1e-3):
        """
        x: state
        r: reference
        tr: angular reference
        u_delay: delayed control input
        Q1: weight on position error
        Q2: weight on angular error
        Q3: weight on max speed
        R: weight on control input
        
        returns: [left wheel speed, right wheel speed]
        """
        if tr is None:
            Q2 = 0
            tr = 0
        if u_delay is None:
            u_delay = self.u_delay0
        return np.around(self.model(x, r, tr, u_delay, Q1, Q2, Q3, R).toarray().reshape(-1), 2)
    
    def mpc(self, x, r, tr=None, u_delay=None,  Q1=1e3, Q2=5e-4, Q3=1, R=1e-3):
        """
        x: state
        r: reference
        tr: angular reference
        u_delay: delayed control input
        Q1: weight on position error
        Q2: weight on angular error
        Q3: weight on max speed
        R: weight on control input
        
        returns: [linear speed, angular speed]
        """
        left_speed, right_speed = self.mpc_wheel_speed(x, r, tr=tr, u_delay=u_delay,  Q1=Q1, Q2=Q2, Q3=Q3, R=R)
        linear_speed = (left_speed + right_speed)/2
        angular_speed = (right_speed - left_speed)/0.10467
        
        return np.array([linear_speed, angular_speed])
