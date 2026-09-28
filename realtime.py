import pyvista as pv
import numpy as np

#Create virtual wind tunnel coordinates
x = np.linspace(-5, 5, 40)
y = np.linspace(-5, 5, 40)
z = np.linspace(-5, 5, 40)


#Create full 3D grid
X, Y, Z = np.meshgrid(
    x,
    y,
    z,
    indexing="ij"
)



vortices = [
    {"y": 0.0,  "z": 0.0,  "gamma": 10},
    {"y": 1.0,  "z": 1.0,  "gamma": 5},
    {"y": -1.0, "z": -1.0, "gamma": -5}
]

#Distance from vortex center
r2 = Y**2 + Z**2 + 0.1

#Create Freestream airflow
U = np.ones_like(X) * 20

#Creates swirl velocities
V = np.zeros_like(Y)
W = np.zeros_like(Z)

for vortex in vortices:

    dy = Y - vortex["y"]
    dz = Z - vortex["z"]

    r2 = dy**2 + dz**2 + 0.05

    gamma = vortex["gamma"]

    V += -gamma * dz / r2
    W +=  gamma * dy / r2


#Create CFD grid
grid = pv.StructuredGrid(
    X,
    Y,
    Z
)


#Combine velocities
vectors = np.column_stack(
    (
        U.ravel(),
        V.ravel(),
        W.ravel()
    )
)


#Store velocity field
grid["velocity"] = vectors


#Generate streamlines
streamlines = grid.streamlines(
    "velocity",
    source_radius=0.5,
    n_points=500
)


#Create particle injector
n_particles = 1500


#Camera angle
theta = np.random.uniform(
    0,
    2*np.pi,
    n_particles
)


#Random radius
radius = np.random.uniform(
    0,
    1,
    n_particles
)


#Build circular inlet
particles = np.column_stack(
    (
        np.full(n_particles, -5),
        radius*np.cos(theta),
        radius*np.sin(theta)
    )
)


#Converting to renderable object
poly = pv.PolyData(
    particles
)


#Convert streamlines to tubes
tubes = streamlines.tube(
    radius=0.02
)


#Visualisation
plotter = pv.Plotter()

# Vortex centerline
for vortex in vortices:

    core = pv.Line(
        (-5, vortex["y"], vortex["z"]),
        ( 5, vortex["y"], vortex["z"])
    )

    plotter.add_mesh(
        core.tube(radius=0.03)
    )

plotter.add_mesh(
    core,
    color="red",
    line_width=5
)

tubes = streamlines.tube(
    radius=0.03
)

plotter.add_mesh(
    tubes
)

particle_actor = plotter.add_mesh(
    poly,
    point_size=5,
    render_points_as_spheres=True
)

camera_angle = 0

def update():
    global particles
    global camera_angle

    x = particles[:,0]
    y = particles[:,1]
    z = particles[:,2]

    r2 = y**2 + z**2 + 0.25

    u = np.ones_like(x) * 25

    v = np.zeros_like(y)
    w = np.zeros_like(z)

    for vortex in vortices:

        dy = y - vortex["y"]
        dz = z - vortex["z"]

        r2 = dy**2 + dz**2 + 0.05

        gamma = vortex["gamma"]

        v += -gamma * dz / r2
        w +=  gamma * dy / r2

    dt = 0.001 #time particles move each frame (particles move slower)

    particles[:,0] += u*dt

    particles[:,1] += v*dt

    particles[:,2] += w*dt

    #Detecting exiting particles
    escaped = particles[:,0] > 5

    theta = np.random.uniform(
    0,
    2*np.pi,
    escaped.sum()
    )

    radius = np.random.uniform(
        0,
        1,
        escaped.sum()
    )

    #Reinjecting new particles
    particles[escaped,0] = -5

    particles[escaped,1] = radius*np.cos(theta)

    particles[escaped,2] = radius*np.sin(theta)

    poly.points = particles

    #Rotate camera
    camera_angle += 0.001

    plotter.camera_position = [
    (
        15*np.cos(camera_angle),
        15*np.sin(camera_angle),
        8
    ),
    (0,0,0),
    (0,0,1)
    ]


plotter.add_timer_event(
    max_steps=100000,
    duration=5,
    callback=lambda step: update()
)

plotter.show()