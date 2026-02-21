import numpy as np

class KalmanFilterDOA:
    """
    Linear Kalman Filter for tracking and smoothing the Direction of Arrival (DOA) 
    of an emitter. Handles noise in DF measurements and provides velocity estimation.
    """
    def __init__(self, dt=0.1, q_noise=1e-4, r_noise=1e-1):
        # State: [angle, angular_velocity]
        self.x = np.array([0.0, 0.0])
        
        # State Transition Matrix
        self.F = np.array([[1, dt],
                           [0, 1]])
        
        # Measurement Matrix (we only measure angle)
        self.H = np.array([[1, 0]])
        
        # Initial Covariance
        self.P = np.eye(2) * 10
        
        # Process Noise Covariance
        self.Q = np.eye(2) * q_noise
        
        # Measurement Noise Covariance
        self.R = np.eye(1) * r_noise

    def predict(self):
        """
        Step 1: Predict next state and covariance.
        """
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        # Wrap angle to [0, 360)
        self.x[0] = self.x[0] % 360
        return self.x

    def update(self, z):
        """
        Step 2: Update state with new measurement.
        z: measured angle from DirectionFinder
        """
        # Measurement residual
        y = np.array([z]) - self.H @ self.x
        
        # Handle wrap-around for angle residual
        if y[0] > 180: y[0] -= 360
        if y[0] < -180: y[0] += 360
        
        # Kalman Gain
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # New State
        self.x = self.x + K @ y
        self.P = (np.eye(2) - K @ self.H) @ self.P
        
        # Wrap angle to [0, 360)
        self.x[0] = self.x[0] % 360
        return self.x

    def get_state(self):
        return {
            "bearing": self.x[0],
            "angular_velocity": self.x[1],
            "uncertainty": np.trace(self.P)
        }
