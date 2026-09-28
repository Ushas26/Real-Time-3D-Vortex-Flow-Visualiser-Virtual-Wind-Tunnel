# Real-Time 3D Vortex Flow Visualiser

An interactive "virtual wind tunnel" built with Python and PyVista. It shows a uniform airflow disturbed by three vortices, with static streamlines and a continuous stream of animated tracer particles.

## Features

- **Analytic flow field:** a uniform freestream plus three vortices (one strong, two weaker and counter-rotating) on a 40×40×40 structured grid
- **Streamlines:** integrated from the velocity field and rendered as 3D tubes
- **Live particle animation:** 1,500 tracers are advected through the field each frame and re-injected at the inlet once they leave the domain
- **Vortex core lines:** drawn along the flow direction at each vortex position
- **Orbiting camera:** slowly rotates around the domain

## How it works

1. **Domain.** A cube from -5 to 5 on each axis is discretised into a `pv.StructuredGrid`.
2. **Velocity field.** The streamwise component is constant. Each vortex adds a swirl in the y-z plane of the form `v = -Γ·dz / r²`, `w = Γ·dy / r²`, with a small softening term added to `r²` to avoid a singularity at the core. The three contributions are summed by superposition.
3. **Streamlines.** `grid.streamlines("velocity", ...)` seeds and integrates paths through the field.
4. **Particles.** Tracers start on a circular inlet at `x = -5`. A timer callback updates their positions with an explicit Euler step, then resets any particle past `x = 5` to a new random inlet position.

## Requirements

- Python 3.8+
- `pyvista`
- `numpy`

```bash
pip install pyvista numpy
```

## Usage

```bash
python realtime.py
```

An interactive window opens. Close it to stop the animation.

## Configuration

Values you can change at the top of the script or in `update()`:

| Setting | Effect |
|---------|--------|
| `vortices` list (`y`, `z`, `gamma`) | Position, strength and sign of each vortex |
| `n_particles` | Number of animated tracers |
| `dt` in `update()` | Particle step per frame (larger is faster) |
| `camera_angle` increment | Camera orbit speed |
| `np.linspace(-5, 5, 40)` | Domain size and grid resolution |

## Limitations

- **This is a visualisation, not a CFD solver.** The velocity field is prescribed analytically; no Navier-Stokes equations are solved, and there is no turbulence, viscosity, pressure or boundary layer.
- The vortex swirl does not vary along the flow direction, so the vortices are straight, non-decaying lines.
- The particle animation uses a freestream speed of 25, while the grid used for the streamlines uses 20, so the two are not exactly consistent.
- Particles are stepped with a simple explicit Euler method, and the streamlines are computed once rather than updated live.

## Possible extensions

- Make the particle and streamline speeds share one parameter
- Interpolate particle velocities from the grid instead of recomputing the analytic field
- Add vortex decay and interaction along the flow direction
- Colour particles and streamlines by speed or vorticity
- Load a real CFD result (VTK/OpenFOAM) into the same viewer

## Keywords

PyVista, 3D visualisation, vortex flow, streamlines, particle tracing, fluid dynamics, NumPy, scientific visualisation
