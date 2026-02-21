# Aegis-AI Developer Guide

## 🏗️ Architecture Overview

The system follows a modular, pipeline-based architecture designed for low-latency signal processing and autonomous response.

### Core Pipeline
1. **Signal Generation / Acquisition**: Data is either simulated (`MissionEngine`) or acquired from SDRs.
2. **Spectral Analysis**: `SpectrumAnalyzer` performs FFT and peak detection.
3. **Parameter Extraction**: `ParameterExtractor` calculates PRI, PW, and Duty Cycle from raw samples.
4. **Direction Finding & Tracking**: 
    - `DirectionFinder` computes the instantaneous DoA.
    - `KalmanFilterDOA` smooths These measurements to maintain a stable track of the emitter.
5. **AI Classification**: `SignalClassifier` identifies the signal type (CW, BPSK, QPSK, etc.).
6. **Autonomy & Response**: `AutonomyManager` consults the `ThreatLibrary` and triggers the appropriate `Jammer`.

## 🔬 Implementation Details

### Kalman Filter (`src/signal_processing/tracking.py`)
Uses a constant-velocity model to predict the next bearing.
- **State Vector**: $x = [\theta, \dot{\theta}]^T$
- **Process Noise ($Q$)**: Configurable to account for sudden target maneuvers.
- **Measurement Noise ($R$)**: Tuned based on the SNR of the detected signal.

### Mission Engine (`src/simulation/mission_engine.py`)
Generates multiple `Emitter` objects with independent trajectories. It uses a time-stepped simulation to feed the pipeline with realistic data scenarios.

## 🛠️ Development & Deployment

### Environment
- Highly recommended to use the provided `Dockerfile` to ensure consistent dependency environments.
- Use `verify_eh.py` as a regression test before any major commit.

### CI/CD
The GitHub Actions workflow (`.github/workflows/main.yml`) performs:
- Dependency installation.
- Code verification via `verify_eh.py`.
- Basic syntax linting.

## 🚀 Future Research
- Integration of **Deep Learning (CNN)** directly into the I/Q processing path.
- Implementation of **AOA (Angle of Arrival)** triangulation using multiple sensors.
- Hardware-in-the-loop (HIL) testing with USRP devices.
