def line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    # Compute determinant
    determinant = A1 * B2 - A2 * B1

    if determinant == 0:
        return None  # Parallel lines (no intersection)

    # Compute intersection point
    x = (B2 * C1 - B1 * C2) / determinant
    y = (A1 * C2 - A2 * C1) / determinant

    return (x, y)


def get_most_likely_tip(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    intercept = line_intersection(line1, line2)
    hi_1, lo_1 = ((x1, y1), (x2, y2)) if y1 > y2 else ((x2, y2), (x1, y1))
    hi_2, lo_2 = ((x3, y3), (x4, y4)) if y3 > y4 else ((x4, y4), (x3, y3))

    # ensure it is in range of the lines
    if intercept[1] > max(y1, y2, y3, y4):
        return hi_1 if hi_1[1] > hi_2[1] else hi_2

    if intercept[1] < min(y1, y2, y3, y4):
        return lo_1 if lo_1[1] < lo_2[1] else lo_2

    return intercept
