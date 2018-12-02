# Re-entry script

import krpc
import math
import time
#  from console_utils import status_console

conn = krpc.connect(name='Reentry and Landing')
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
obt_frame = vessel.orbit.body.non_rotating_reference_frame
srf_frame = vessel.orbit.body.reference_frame
orb_speed = conn.add_stream(getattr, vessel.flight(obt_frame), 'speed')
srf_speed = conn.add_stream(getattr, vessel.flight(srf_frame), 'speed')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
surface_altitude = conn.add_stream(getattr, vessel.flight(), 'surface_altitude')
long = conn.add_stream(getattr, vessel.flight(obt_frame), 'longitude')

ksc_long = -75
ksc_rad = 1.301492

deorbit_long = -136.79
deorbit_rad = -2.386225

#  status_console(conn)

ap.engage()
#  ap.sas_mode = ap.sas_mode.retrograde
# Point to retrograde
ap.target_direction = (0, -1, 0)
ap.wait()
vessel.control.toggle_action_group(3)

#  def ksc_phase_angle():
reentry_phase_angle = 62
ksc_loc = (ksc_rad - reentry_phase_angle * math.pi/180)

def reentry_positioning():
    position = 0

    print("--Initiating reentry positioning sequence--")

    while abs(position - ksc_loc) > 0.01:
        position = (long() + 180) * math.pi/180
        print(abs(position - ksc_loc))
        time.sleep(1)

def deorbit_sequence():
    print("--Initiating deorbit burn sequence--")

    while (vessel.orbit.periapsis_altitude > 0):
        vessel.control.throttle = 1.0
    vessel.control.throttle = 0.0
    print("--Deorbit burn complete--")
    vessel.control.toggle_action_group(2)
    vessel.control.toggle_action_group(3)

def reentry_slowdown_sequence():
    print("--Tracking reentry altitude and speed--")

    while altitude() > 36000:
        pass

    print("--Initiating upper reentry slowdown burn sequence--")
    while (orb_speed() > 1800):
        vessel.control.throttle = 1.0
    vessel.control.throttle = 0.0

    while altitude() > 26000:
        pass

    print("--Initiating lower reentry slowdown burn sequence--")
    while (srf_speed() > 250):
        vessel.control.throttle = 1.0
    vessel.control.throttle = 0.0

def landing_sequence():
    print("--Initiating landing sequence--")

    print("--deploying landing legs--")
    suicide_burn_sequence()

def suicide_burn_sequence():
    while surface_altitude() > 850:
        pass

    print("--Initiating suicide landing burn sequence--")
    vessel.control.gear = True

    while (srf_speed() > 20):
        vessel.control.throttle = 1.0
    vessel.control.throttle = 0.0

    while surface_altitude() > 2:
        #  ap.sas = False
        ap.disengage()

        if srf_speed() > 7:
            vessel.control.throttle = 0.3
        else:
            vessel.control.throttle = 0
    vessel.control.throttle = 0

def system_shutdown():
    print("--Initiating system shut down--")

reentry_positioning()
deorbit_sequence()
reentry_slowdown_sequence()
landing_sequence()
system_shutdown()
