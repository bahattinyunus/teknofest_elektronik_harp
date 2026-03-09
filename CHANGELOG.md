# Changelog

All notable changes to the Aegis-AI (TEKNOFEST 2026 Electronic Warfare) project will be documented here.

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
