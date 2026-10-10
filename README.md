# arm-control-lab
Seven-axis arm kinematics, dynamics and trajectory-tracking lab in MuJoCo

A from-scratch motion control experiment bench built on a **Franka Research 3**:
I derive the kinematics and dynamics myself instead of calling a toolbox,
validate every derivation against MuJoCo, then close the loop with a controller
and measure the tracking error.

**Task:**&#8203; drive a 7-DoF Franka Research 3 in MuJoCo to pick a cube from a
start point and place it at a target point while avoiding a table-mounted
obstacle — with the end-effector tracking error measured and reproducible.

## Status

Under active development since October 2026.

| Version | Target | Contents | State |
| --- | --- | --- | --- |
| **v0.1** | Jan 2027 | Hand-written kinematics + dynamics library, Cartesian trajectory tracking in MuJoCo (PD + gravity compensation) | in progress |
| **v0.2** | Apr 2027 | Pick-and-place closed loop, ROS 2 wrapper, inverse-kinematics core rewritten in C++ | planned |
| **v0.3** | Jul 2027 | Controller upgrade (computed torque → MPC) and transfer to a real arm | planned |
| **v1.0** | Sep 2027 | Portfolio packaging: report, demo video, write-up | planned |

## Modules

**Done**

- [x] `robot_config.py` — Franka Research 3 (7-DoF) DH table, joint limits and accessors
- [x] `io_utils.py` — joint-trajectory save/load to CSV (with a missing-file guard)

**Planned (v0.1)**

- [ ] `transform.py` — rotations, quaternions, homogeneous transforms
- [ ] `robot.py` — forward kinematics, geometric Jacobian, inverse kinematics
- [ ] `dynamics.py` — Lagrangian dynamics, recursive Newton–Euler
- [ ] `trajectory.py` — joint-space and Cartesian trajectories
- [ ] `sim.py` — MuJoCo model loading, state I/O, stepping
- [ ] `controller.py` — PD + gravity compensation, later computed torque
- [ ] Cross-validation tests: FK / Jacobian / IK / RNEA against MuJoCo

## Metrics

Measured values are filled in as each milestone lands — these are results, not
targets.

| Metric | Value |
| --- | --- |
| Cartesian tracking RMSE | — |
| Joint steady-state error | — |
| Control loop rate | — |
| FK / RNEA agreement with MuJoCo | — |

## Design decisions

A running log of the choices that were not obvious, and why.
_(updated as the project progresses)_

## Environment

- Python 3.11+, NumPy, Matplotlib
- MuJoCo, plus MuJoCo Menagerie for reference models

## Background

Mechanical engineering MSc. Rigid-body dynamics, kinematics and classical
control are my coursework, so this repo focuses on the part that is not:
turning those derivations into working code and validating them against a
simulator rather than trusting that they "look right".

## License

MIT
