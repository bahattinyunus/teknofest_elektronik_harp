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

    def triangulate(self, sensor_positions, bearings, weights=None):
        """
        Estimates goal position (intersection) from 2+ sensors with bearings.
        Uses Weighted Least Squares for better accuracy.
        sensor_positions: List of (lat, lon)
        bearings: List of angles in degrees
        weights: Optional list of weights based on SNR or distance
        """
        if len(sensor_positions) < 2 or len(bearings) < 2:
            return None
            
        if weights is None:
            weights = np.ones(len(sensor_positions))
            
        # Linear triangulation in local cartesian coordinates
        y_coords = []
        x_coords = []
        for pos in sensor_positions:
            y = (pos[0] - self.ref_lat) * 111139
            x = (pos[1] - self.ref_lon) * 111139 * np.cos(np.radians(self.ref_lat))
            y_coords.append(y)
            x_coords.append(x)
            
        # Solve for intersection: A * X = B
        A = []
        B = []
        for i in range(len(sensor_positions)):
            rad = np.radians(90 - bearings[i])
            sin_a = np.sin(rad)
            cos_a = np.cos(rad)
            
            # Line equation in form: sin(a)*x - cos(a)*y = sin(a)*x_i - cos(a)*y_i
            # This handles vertical/horizontal lines naturally
            A.append([sin_a * weights[i], -cos_a * weights[i]])
            B.append((sin_a * x_coords[i] - cos_a * y_coords[i]) * weights[i])
                
        # Weighted Least squares solution
        res, _, _, _ = np.linalg.lstsq(A, B, rcond=None)
        
        # Convert back to Lat/Lon
        est_lat = self.ref_lat + (res[1] / 111139)
        est_lon = self.ref_lon + (res[0] / (111139 * np.cos(np.radians(self.ref_lat))))
        
        return round(est_lat, 6), round(est_lon, 6)

class MultiTargetTrackerManager:
    """
    Manages multiple KalmanFilterDOA instances for different emitters.
    Handles track association and lifecycle (creation/deletion).
    """
    def __init__(self, max_tracks=10):
        self.trackers = {} # emitter_id -> KalmanFilterDOA
        self.max_tracks = max_tracks

    def update_emitter(self, emitter_id, measured_bearing):
        """
        Updates an existing tracker or creates a new one for a given emitter.
        """
        if emitter_id not in self.trackers:
            if len(self.trackers) >= self.max_tracks:
                return # Capacity limit
            self.trackers[emitter_id] = KalmanFilterDOA()
            # Initialize with the first measurement
            self.trackers[emitter_id].x[0] = measured_bearing
        
        return self.trackers[emitter_id].update(measured_bearing)

    def predict_all(self):
        """
        Performs prediction step for all active trackers.
        """
        for tracker in self.trackers.values():
            tracker.predict()

    def get_all_states(self):
        """
        Returns a dictionary of all tracked emitter states.
        """
        return {eid: t.get_state() for eid, t in self.trackers.items()}

    def remove_dead_tracks(self, active_ids):
        """
        Removes trackers for emitters that are no longer being detected.
        """
        dead_ids = [eid for eid in self.trackers if eid not in active_ids]
        for eid in dead_ids:
            del self.trackers[eid]
