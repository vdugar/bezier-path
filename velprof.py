from numpy.polynomial.polynomial import *
import math
import pylab

V = 300            # Target average speed of centre of mass, in mm/s
B = 1000            # Wheel-base, in mm
STEP = 0.005         # Step-count for parameter 'u'
NUM_STEPS = 199      # Number of velocity values
D = 210             # Wheel dia in mm

# 15, 150
x = [150.000000, 602.885683, -1655.771366, 902.885683]                # Parameters for cubic eqn of x
y = [0.000000, 2250.000000, -2250.000000, 1500.000000]              # Parameters for cubic eqn of y
init_del_d = 150
init_del_theta = 75 * math.pi / 180.0                               # From x-axis

def comp_slope(dx, dy, u):
    """
    Returns the slope (in radians) of the curve at point 'u'
    given the parametric equations for its derivative.
    """

    dx = polyval(u, dx)
    dy = polyval(u, dy)

    if dx == 0:
        return math.pi / 2.0
    else:
        return math.atan2(dy, dx)


def comp_vel_profile(x, y):
    """
    Given parametric equations for the curve, this function
    returns a list of 3-tuples ->
    (right-speed, left-speed, time)
    """

    dx = polyder(x)
    dy = polyder(y)

    u = STEP
    count = 1
    vel_prof = []

    while count <= NUM_STEPS:
        del_theta = comp_slope(dx, dy, u) - comp_slope(dx, dy, u - STEP)
        x1 = polyval(u, x)
        y1 = polyval(u, y)
        x2 = polyval(u - STEP, x)
        y2 = polyval(u - STEP, y)
        del_d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        t = del_d / V

        v_right = (B * del_theta / (2 * t)) + V
        v_left = 2 * V - v_right

        vel_prof.append((v_right, v_left, t))

        count += 1
        u += STEP
    
    return vel_prof


def anal_vel_profile(x, y):
    """
    Analyzes the velocity profile-
    * Displays the graph for velocities
    * Computes the generated path
    """

    vel_prof = comp_vel_profile(x, y)

    # Printing out (vel, dist) array
    print "\n\n"
    for elem in vel_prof:
        print "{%d, %d}," % (-1 * int(elem[1] * 60 / math.pi / D), int(elem[1] * elem[2]))

    vel_r, vel_l, t = zip(*vel_prof)
    vel_r = [val * 60.0 / math.pi / D for val in vel_r]
    vel_l = [val * 60.0 / math.pi / D for val in vel_l]

    dist = [vel_prof[i][0] * vel_prof[i][2] for i in range(len(vel_prof))]
    print dist
    print sum(dist  )
    exit()          
    # Computing array of velocity differences
    vel_diff = []
    for i in range(1, len(vel_r)):
        vel_diff.append(vel_r[i] - vel_r[i-1])

    # Plotting velocities first

    pylab.plot(vel_r, 'r-', vel_l, 'b-')
    pylab.grid(True)
    pylab.xlabel("Seq number")
    pylab.ylabel("speed (rpm)")
    pylab.title("Right speed -> Red\nLeft speed -> blue")
    pylab.show()

    # Now for time
    t = [1000 * elem for elem in t]
    pylab.plot(t, 'r-');
    pylab.grid(True)
    pylab.xlabel("Seq number")
    pylab.ylabel("Time (ms)")
    pylab.title("Time for each segment")
    pylab.show() 

    # Plotting velocity-difference graph
    pylab.plot(vel_diff, 'b-')
    pylab.grid(True)
    pylab.xlabel("Sequence no.")
    pylab.ylabel("Velocity difference (rpm)")
    pylab.title("Difference b/w subsequent velocities")
    pylab.show()

    # Now for the generated path
    dx = polyder(x)
    dy = polyder(y)
    path_x = [init_del_d, ]
    path_y = [0, ]
    orig_path_x = [polyval(0, x), ]
    orig_path_y = [polyval(0, y), ]
    theta = init_del_theta
    for i, val in enumerate(vel_prof):
        orig_path_x.append(polyval(1.0*(i+1)/(NUM_STEPS+1), x))
        orig_path_y.append(polyval(1.0*(i+1)/(NUM_STEPS+1), y))

        del_r = val[0] * val[2]             # Linear displacement of right wheel
        del_l = val[1] * val[2]             # Linear displacement of left wheel
        del_theta =  (del_r - del_l) / B    # Angle through which bot turns
        del_d = (del_r + del_l) / 2         # Linear disp. of CoM
        # Now compute radius of curvature of the curve
        # roc = del_d / del_theta
        # Use roc to find new x_pos and y_pos
        # theta_d = math.pi - (math.pi / 2 + theta)
        # x_pos = path_x[i] - (roc * (1 - math.cos(del_theta)) * math.cos(theta_d) - roc * math.sin(del_theta) * math.sin(theta_d))
        # y_pos = path_y[i] + roc * (1 - math.cos(del_theta)) * math.sin(theta_d) + roc * math.sin(del_theta) * math.cos(theta_d)

        theta += del_theta
        x_pos = path_x[i] + del_d * math.cos(theta)
        y_pos = path_y[i] + del_d * math.sin(theta)
        path_x.append(x_pos)
        path_y.append(y_pos)
        print (theta / math.pi * 180), comp_slope(dx, dy, 1.0*(i+1)/(NUM_STEPS+1)) / math.pi * 180

    pylab.plot(orig_path_x, orig_path_y, "bo", path_x, path_y, "ro")
    pylab.xlabel("X (mm)")
    pylab.ylabel("Y (mm)")
    pylab.title("Red-> Approximate path of bot\nBlue-> Required Path")
    pylab.show()

anal_vel_profile(x, y)

