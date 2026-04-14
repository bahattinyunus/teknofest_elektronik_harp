# Changelog

All notable changes to the Aegis-AI (TEKNOFEST 2026 Electronic Warfare) project will be documented here.

## [3.0.0-OMEGA] - 2026-04-14
### Added
- **DRFM Deception Kernel**: Implemented `DRFMKernel` for high-fidelity signal capture and coherent re-radiation.
- **Advanced Deception Jamming**: Integrated `DRFMJammer` into the jamming suite (RGPO, VGPO, Combined).
- **Swarm Intelligence Mode**: Added `correlate_emitters` to `TacticalCOP` for autonomously identifying and suppressing multi-node UAV swarms.
- **LPI De-masking Upgrade**: Added Spectral Entropy detection to `LPIDetector` to complement existing WVD/SVD/STFT methods (now 5-method voting).
- **Mission Engine OMEGA**: Added dynamic `Drone Swarm` and `Cognitive Radar` scenarios to the simulation suite.
- **Bayesian Risk Assessment**: Upgraded `AutonomyManager` with weighted risk indexing based on detection confidence.
- **Project MANIFESTO**: Established the core Electronic Warfare doctrine for the Aegis-AI platform.
- **Premium Documentation Overhaul**: Massive README update with high-density technical depth and OMEGA-tier aesthetics.
- **OMEGA Visuals**: Generated and integrated high-fidelity mission banners.

## [2.0.0] - 2026-03-11
### Added
- **Full Spec Compliance**: Completed all TEKNOFEST 2026 requirements including ED, ET, and AI.
- **Advanced EA Assets**: Implemented `GNSSJammer` (GPS L1 Spoofing), `AnalogVoiceJammer` (Voice Spoofing), and `SpoofingJammer` (RGPO/VGPO).
- **Tactical Dashboard 2.0**: Redesigned UI with glassmorphism, Tactical Map visualization, Hardware Health monitoring (Jetson/SDR), and real-time SDR tuning controls.
- **SigMF Recording**: Integrated `SigMFExporter` for standardized RF data capture directly from the dashboard.
- **2D Geolocation**: Added `Geolocator` with triangulation logic and tactical map display.
- **End-to-End ADSS Integration**: Wired `AutonomyManager` directly to `JammerCoordinator` for autonomous multi-jammer response.
- **Hardware Integration Plan**: Added `DONANIM_PLANI.md` for USRP B210 and Jetson Orin deployment.
- **AI/AMC Report**: Added `AI_MODULASYON_SINIFLANDIRMA.md` for AI modulation classification analysis.

## [1.5.0] - 2026-03-09
### Added
- **Phase 4 - Deep Learning Integration**: Added PyTorch CNN model core (`DummyDLClassifier`) in `src/ai_engine/dl_classifier.py` for direct I/Q signal classification.
- **Classification Engine Update**: Fused `SignalClassifier` rule-based engine with DL inference for robust classification.
- **Data Export Strategy**: Added `export_dataset()` to `ScenarioManager` to facilitate easy generation of `.npy` datasets for future DL model training.
- **DL Validation Suite**: Upgraded `verify_eh.py` and `test_aegis.py` with specific tests to validate PyTorch availability and inference execution without crashing.

## [1.4.0] - 2026-03-09
### Added
- **Phase 3 Scenarios**: `LPI Stealth Radar` (FMCW chirp) and `Fire Control Radar` (narrow-pulse, high rep-rate) added to `ScenarioManager`.
- **Multi-Emitter Simulation**: `MissionEngine` now spawns 4 emitter types: `Radar_L`, `Comm_Link`, `LPI_Radar`, and `Radar_FC`. Added `add_emitter` / `remove_emitter` dynamic control.
- **Dashboard APIs**: New `/api/mission`, `/api/spectrum_history`, and `/api/jammer` (POST) endpoints added to the Flask dashboard.
- **Verification Suite**: `verify_eh.py` fully overhauled with color-coded pass/fail output and comprehensive tests for all new features.

### Changed
- Refined `verify_eh.py` to be a professional, color-coded verification CLI tool.

## [1.3.0] - 2026-03-08
### Added
- **ADSS Threat Prioritization**: `get_highest_priority_threat()` in `AutonomyManager` surfaces the highest-risk emitter.
- **Adaptive Noise Jammer**: `AdaptiveNoiseJammer` scales transmit power based on threat risk level.
- **Jammer Coordinator**: `JammerCoordinator` orchestrates multiple jammers for multi-threat environments.
- **Confidence Standardization**: `LPIDetector.detect_all()` now returns a float confidence (0.0-1.0) with `confidence_text` for readability.

### Fixed
- `ValueError` in `AutonomyManager` when displaying confidence as a non-float (string was returned by LPI detector).

## [1.2.0] - 2026-02-28
### Added
- **Global EW Ecosystem**: Added international competition and competitor analysis to README.
- **LPI Detection**: Integrated Low Probability of Intercept (LPI) radar detection into the verification suite.
- **Unified Branding**: Created a new high-impact, single TEKNOFEST-specific banner.
- **Professional Governance**: Added LICENSE (MIT), CHANGELOG, and expanded requirements.txt.

### Changed
- Refined `verify_eh.py` with robust path handling and system-wide verification checks.
- Optimized README search-ability and international context.

## [1.1.0] - 2026-02-26
### Added
- Core Signal Processing (FFT, DOA).
- Autonomous Mission Engine.
- Flask-based Dashboard prototype.

## [1.0.0] - 2026-02-23
- Initial project structure.
- Basic signal processing modules.
