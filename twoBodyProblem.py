from decimal import Decimal, getcontext
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import json
import os

getcontext().prec = 100

# Simulation parameters
output_dir = os.path.join("EE", "exports")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "satellite_trajectory.json")  # JSON file output location

# Constants
mu = Decimal('398600441800000')  # μ = G * m(Earth) (gravitational parameter)

min = 60
hour = min * 60
day = hour * 24
rot_day = Decimal("86164.098903691") # time for one Earth rotation

simulation_duration = 30 * rot_day # simulation duration（sec）

t = Decimal(0) # init time
dt = Decimal('1') # time per step (sec)


class CelBody(object):
    # constants of nature
    # universal constant of gravitation
    def __init__(self, id, name, x0, v0, mu, color, lw):
        # name of the body (string)
        self.id = id
        self.name = name
        # gravitational parameter (m^3/s^2)
        self.mu = Decimal(mu)
        # initial position of the body (m)
        self.x0 = np.array(x0, dtype=object)
        # position (m). set to initial value.
        self.x = self.x0.copy()
        # initial velocity of the body (m/s)
        self.v0 = np.array(v0, dtype=object)
        # velocity (m/s). set to initial value.
        self.v = self.v0.copy()
        self.a = np.zeros([3], dtype=object)
        self.color = color
        self.lw = lw

# all celestial bodies
Bodies = [
    CelBody(0, 'Earth', [Decimal('0'), Decimal('0'), Decimal('0')], [Decimal('0'), Decimal('0'), Decimal('0')], mu=Decimal('398600441800000'), color='yellow', lw=10),
    CelBody(1, 'Satellite', [Decimal('0'), Decimal('42164172.365635383577096799539293955083066031653837348012252877476964638009148844154889181355716636945118781593343809856252972310123832275430095527195841108481741103906413079508017867973849688974305655'), Decimal('0')], [Decimal('-3074.6599995581131635343976149417506860553199673459634939196623537622866740578479534786575132710526141913312784129905210182570627182021366203776860929871905369761728458547363926825506497502959246256577'), Decimal('0'), Decimal('0')], mu=Decimal('0'), color='blue', lw=3),
]

paths = [[b.x[:2].copy()] for b in Bodies]

satellite_trajectory = []

v = Decimal(0)
with tqdm(total=float(simulation_duration), desc="Simulating") as pbar:
    while t < simulation_duration:
        # compute forces/accelerations
        for body in Bodies:
            body.a *= Decimal('0')
            for other in Bodies:
                # no force on itself
                if body == other:
                    continue  # jump to next loop
                rx = body.x - other.x
                r3 = sum(rx**Decimal('2')) ** Decimal('1.5')
                body.a += -other.mu * rx / r3

        for n, planet in enumerate(Bodies):
            # use the symplectic Euler method for better conservation of the constants of motion
            planet.v += planet.a * dt
            planet.x += planet.v * dt
            paths[n].append(planet.x[:2].copy())
        t += dt
        pbar.update(float(dt))

        # 衛星の座標を記録
        satellite_position = {
            "time": float(t),
            "x": str(Bodies[1].x[0]),
            "y": str(Bodies[1].x[1]),
            "z": str(Bodies[1].x[2])
        }
        satellite_trajectory.append(satellite_position)

with open(output_file, 'w') as json_file:
    json.dump(satellite_trajectory, json_file, indent=4)

plt.figure(figsize=(8, 8))
for n, planet in enumerate(Bodies):
    px, py = np.array(paths[n]).T
    plt.plot(px, py, color=planet.color, lw=planet.lw)
plt.title("2D Paths of Celestial Bodies")
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.grid(True)
plt.savefig(os.path.join(output_dir, "2D_paths.png"))
plt.show()

data = {}
for n, planet in enumerate(Bodies):
    data[planet.name + '_x'] = [pos[0] for pos in paths[n]]
    data[planet.name + '_y'] = [pos[1] for pos in paths[n]]

df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
satellite_to_body_distance = [np.linalg.norm(np.array(path)[:2] - Bodies[0].x[:2]) for path in paths[1]]
plt.plot([float(dt * i) for i in range(len(satellite_to_body_distance))], satellite_to_body_distance, color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Distance from Satellite to Earth (m)')
plt.title('Distance from Satellite to Earth over Time')
plt.grid(True)
plt.savefig(os.path.join(output_dir, "distance_over_time.png"))
plt.show()