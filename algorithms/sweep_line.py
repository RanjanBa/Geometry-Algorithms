from bintrees import AVLTree
from functools import cmp_to_key

from utilities.line_segment import LineSegment


def __cmp(a, b):
    if a[0].x == b[0].x:
        return a[0].y - b[0].y
    return a[0].x - b[0].x


def linesToSortedPoints(lines):
    points = []
    for line in lines:
        if line.start.x <= line.end.x:
            points.append((line.start, True, line, False))
            points.append((line.end, False, line, False))
        else:
            points.append((line.start, False, line, True))
            points.append((line.end, True, line, True))

    points.sort(key=cmp_to_key(__cmp))
    return points


def sweepLine(lines):
    points = linesToSortedPoints(lines)

    print(len(points))
    for pt in points:
        print(pt[0], pt[1])

    active_lines = AVLTree()
    intersectedLines = []

    for i in range(len(points)):
        pt = points[i]

        line1 = pt[2]
        active_lines.insert((pt[0].y, pt[0].x), line1)

        if pt[1] == True:
            if active_lines.count <= 1:
                continue
            try:
                prev = active_lines.prev_key((pt[0].y, pt[0].x))
                line2 = active_lines[prev]
                check = LineSegment.checkSegmentIntersection(line1, line2)
                print(line1, line2, check)
                if check:
                    intersectedLines.extend([line1, line2])
            except:
                print(f'{pt[0]} twa da 1!')

            try:
                succ = active_lines.succ_key((pt[0].y, pt[0].x))
                line2 = active_lines[succ]
                check = LineSegment.checkSegmentIntersection(line1, line2)
                print(line1, line2, check)
                if check:
                    intersectedLines.extend([line1, line2])
            except:
                print(f'{pt[0]} twa da 2!')
        else:
            if pt[3]:
                active_lines.remove((pt[2].end.y, pt[2].end.x))
            else:
                active_lines.remove((pt[2].start.y, pt[2].start.x))

            if active_lines.count > 2:
                try:
                    prev = active_lines.prev_key((pt[0].y, pt[0].x))
                    line1 = active_lines[prev]
                    try:
                        succ = active_lines.succ_key((pt[0].y, pt[0].x))
                        line2 = active_lines[succ]
                        check = LineSegment.checkSegmentIntersection(
                            line1, line2)
                        print(line1, line2, check)
                        if check:
                            intersectedLines.extend([line1, line2])
                    except:
                        print(f'{pt[0]} twa da 3!')
                except:
                    print(f'{pt[0]} twa da 4!')

            active_lines.remove((pt[0].y, pt[0].x))
    print(f'active lines : {active_lines.count}')
    active_lines.clear()

    return intersectedLines
