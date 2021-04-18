"""
SUMMARY

Auxiliary functions, provided here to avoid clutter
"""


"""
Transforms a point (P = [x, y]) using the x, y intervals (Δxy = [Δx, Δy]) into the corresponding discrete point (D = [xd, yd])
loc_min = [x_min, y_min]
"""
def discretize_location(P, loc_min, Δxy):
    x_from_start = P[0] - loc_min[0]
    y_from_start = P[1] - loc_min[1]

    xd = int(x_from_start//Δxy[0])
    yd = int(y_from_start//Δxy[1])

    return [xd, yd]



"""
Transforms a discretized point (PD = [xd, yd]) using the x, y intervals (Δxy = [Δx, Δy]) into the corresponding point (P = [x, d])
loc_min = [x_min, y_min]
"""
def continuous_location(PD, loc_min, Δxy):

    x = PD[0]*Δxy[0] + loc_min[0]
    y = PD[1]*Δxy[1] + loc_min[1]

    return [x, y]



"""
Obtains the points in the border of a cell (starting at bottom left (BL = [x_bl, y_bl])), starting point not repeated
"""
def cell_borders(BL, Δxy):
    [x_bl, y_bl] = BL
    Δx = Δxy[0]
    Δy = Δxy[1]

    x_border = [x_bl, x_bl + Δx, x_bl + Δx, x_bl]
    y_border = [y_bl, y_bl, y_bl + Δy, y_bl + Δy]

    return [x_border, y_border]


"""
Appends the first element of the array to the end, useful when plotting
"""
def first_append_to_last(arr):
    return arr + [arr[0]]



"""
Calculates the RMS (root mean square) value of an array
"""
def RMS(arr):
    n = len(arr)
    sq_sum = sum(a**2 for a in arr)
    return (sq_sum/n)**0.5
