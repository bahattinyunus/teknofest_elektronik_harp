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

class Geolocator:
    """
    Implements 2D Geolocation (Lat/Lon) using Triangulation from multiple DoA measurements.
    """
    def __init__(self, reference_lat=39.9255, reference_lon=32.8662):
        self.ref_lat = reference_lat
        self.ref_lon = reference_lon

    def triangulate(self, sensor_positions, bearings):
        """
        Estimates goal position (intersection) from 2+ sensors with bearings.
        sensor_positions: List of (lat, lon)
        bearings: List of angles in degrees
        """
        if len(sensor_positions) < 2 or len(bearings) < 2:
            return None
            
        # Linear triangulation (simplified for small areas like 1x1km)
        # Using simple line intersection in local cartesian coordinates
        # Conversion: 1 degree lat ~ 111km, 1 degree lon ~ 111km * cos(lat)
        
        y_coords = []
        x_coords = []
        for pos, angle in zip(sensor_positions, bearings):
            # Local coordinate transform (relative to ref)
            y = (pos[0] - self.ref_lat) * 111139
            x = (pos[1] - self.ref_lon) * 111139 * np.cos(np.radians(self.ref_lat))
            
            # Line equation: y - y_i = tan(90 - angle) * (x - x_i)
            # angle 0 (N) -> slope infinite, angle 90 (E) -> slope 0
            rad = np.radians(90 - angle)
            slope = np.tan(rad)
            
            y_coords.append(y)
            x_coords.append(x)
            
        # Solve for intersection (min least squares for N sensors)
        # A * X = B
        A = []
        B = []
        for i in range(len(sensor_positions)):
            angle = bearings[i]
            rad = np.radians(90 - angle)
            # y = m*x + c  => m*x - y = -c
            # c = y_i - m*x_i
            m = np.tan(rad)
            if np.abs(m) > 1e6: # Handle vertical lines (N/S)
                A.append([1, 0])
                B.append(x_coords[i])
            else:
                A.append([m, -1])
                B.append(m * x_coords[i] - y_coords[i])
                
        # Least squares solution
        res, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
        
        # Convert back to Lat/Lon
        est_lat = self.ref_lat + (res[1] / 111139)
        est_lon = self.ref_lon + (res[0] / (111139 * np.cos(np.radians(self.ref_lat))))
        
        return round(est_lat, 6), round(est_lon, 6)
