import krpc
from time import sleep
import numpy as np
from math import sqrt

conn = krpc.connect(name="Launch Program")
space_center = conn.space_center
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
flight = vessel.flight()

# Wait for the user to trigger the first staging
while vessel.control.current_stage == 5:
    sleep(0.1)

# Launch
vessel.control.throttle = 1
ap.engage()
ap.target_pitch_and_heading(90, 90)

sleep(0.1)
#  space_center.physics_warp_factor = 3
sleep(0.1)

# Gravity turn
while vessel.orbit.apoapsis_altitude < 100000:
    pitch = np.interp(
        flight.mean_altitude/1000.0,
        [0, 5, 10, 20, 40, 100],
        [88, 80, 75, 70, 65, 65]
    )

    ap.target_pitch_and_heading(pitch, 90)
    thr = 2 * 9.81 * vessel.mass / vessel.available_thrust # Limit to 2g acceleration
    vessel.control.throttle = thr
    sleep(0.1)

# MECO
space_center.physics_warp_factor = 0
vessel.control.throttle = 0
sleep(0.5)

# Stage separation
vessel_S2 = vessel.control.activate_next_stage()[0]
sleep(0.1)
