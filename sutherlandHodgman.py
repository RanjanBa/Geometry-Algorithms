# rect = (top, right, bottom, left)
def sutherland(polygon, rect):
    top = rect[0]
    right = rect[1]
    bottom = rect[2]
    left = rect[3]
    for pt in polygon:
