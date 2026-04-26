# Mergen-AI OMEGA Developer Guide: Technical Deep Dive

This document provides a comprehensive technical breakdown of the **Mergen-AI OMEGA v3.0** system architecture, focusing on the mathematical models and signals engineering principles used in the TEKNOFEST 2026 competition.

---

## 🏗️ Architecture Overview

The system follows a modular, low-latency pipeline architecture designed for asynchronous Signal Intelligence (SIGINT) and Electronic Attack (EA).

### 1. Sensing Layer: Electronic Support (ED)
The sensing layer utilizes **Software Defined Radio (SDR)** front-ends (ettus USRP B210) to digitize the EM spectrum.
- **Acquisition**: I/Q samples are buffered and processed in 10-20ms windows.
- **Spectral Estimation**: `SpectrumAnalyzer` uses Welch's method for Power Spectral Density (PSD) estimation.
- **LPI Detection**: `LPIDetector` implements **Wigner-Ville Distribution (WVD)** to identify chirp-like signals that are hidden in the gürültü floor (Spectral Entropy analysis).

### 2. Decision Layer: Autonomous Decision Support System (ADSS)
The ADSS acts as the system's "brain," fusing multiple inputs:
- **Threat Library**: Correlation of extracted parameters (PRI, PW, Freq) against known emitter profiles.
- **Bayesian Risk Engine**: Calculates real-time threat scores based on proximity, lethality, and intent.
- **Swarm Correlation**: Identifies coordinated emitter groups by analyzing spatial (AOA) and temporal (Timing) correlations.

### 3. Action Layer: Electronic Attack (ET)
- **DRFM Kernel**: `DRFMKernel` captures and buffers incoming signals to generate coherent false targets (RGPO/VGPO).
- **Adaptive Jamming**: `JammerCoordinator` dynamically manages power allocation and look-through scheduling to maintain tracking while jamming.

---

## 🔬 Mathematical Models

### A. Digital Radio Frequency Memory (DRFM)
Coherent deception is achieved by re-transmitting a delayed and frequency-shifted version of the captured signal $s(t)$:
$$s_{jam}(t) = K \cdot s(t - \tau) \cdot e^{j 2\pi f_d t}$$
where $\tau$ is the range delay (RGPO) and $f_d$ is the Doppler shift (VGPO).

### B. Direction Finding (MUSIC Algorithm)
For the 12-antenna Vivaldi array, we estimate the Direction of Arrival (DOA) by decomposing the covariance matrix $R_{xx}$:
$$R_{xx} = E[x(t)x^H(t)] = U_s \Lambda_s U_s^H + U_n \Lambda_n U_n^H$$
The MUSIC pseudospectrum is given by:
$$P_{MU}(\theta) = \frac{1}{a^H(\theta) U_n U_n^H a(\theta)}$$
where $U_n$ spans the noise subspace and $a(\theta)$ is the array steering vector.

### C. Kalman Tracking (`src/signal_processing/tracking.py`)
Multi-target tracking uses a Constant Velocity (CV) model:
- **State Vector**: $x = [\theta, \omega]^T$ (Angle, Angular Velocity)
- **Transition**: $F = \begin{bmatrix} 1 & \Delta t \\ 0 & 1 \end{bmatrix}$
- **Measurement**: $z = \theta + v$, where $v \sim N(0, R)$

---

## 🛠️ Development & Simulation

### Scenario Engine
The `ScenarioManager` allows testing against complex mission environments:
1. **Saturation Attack**: 100+ noise-like emitters.
2. **LPI Stealth**: High-duty cycle FMCW radars.
3. **Swarm Incursion**: Coordinated movement of 10+ small emitters with frequency hopping.

### Verification Suite
- `launcher.py`: Unified console for all system modes.
- `verify_eh.py`: Runs automated sanity checks on DSP, AI, and Jamming modules.
- `src/dashboard/cli_dashboard.py`: Real-time situational awareness console.

---

## 📅 Road to TRL 9
1. [x] **Cognitive Logic** (Bayesian Risk & Swarm ID)
2. [x] **DRFM Core** (Coherent RGPO/VGPO)
3. [ ] **Distributed EH** (TDOA Geolocation fusion between 2 units)
4. [ ] **Field Validation** (2.4GHz / 5.8GHz Tactical testing)

---
*Document Version: 3.0.0-OMEGA*
