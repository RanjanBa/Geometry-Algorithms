"""
Contains functions for calculating
=======
* check if there is any intersection points of given set of line segments
* pair of line segments of given set of line segments
* intersection points of given set of line segments

Algorithm used:
-----------
* Shamos-Hoey Algorithm
* Bentley-Ottmann Algorithm
See : (http://geomalgorithms.com/a09-_intersect-3.html)
"""

from queue import PriorityQueue
from functools import cmp_to_key

from utilities.red_black_tree import RedBlackTree, Node
from utilities.line_segment import LineSegment


def compare(p1, p2):
    if p1.x < p2.x:
        return -1
    elif p1.x > p2.x:
        return 1

    if p1.x == p2.x:
        if p1.ptype == p2.ptype:
            if p1.y < p2.y:
                return -1
            else:
                return 1
        else:
            if p1.ptype == 0:
                return -1
            else:
                return 1

def anySegmentsIntersect(lines):
    S = []
    for i in range(len(lines)):
        if lines[i].start.x > lines[i].end.x or (lines[i].start.x == lines[i].end.x and lines[i].start.y > lines[i].end.y):
            end = lines[i].start
            start = lines[i].end
            lines[i] = LineSegment(start, end)
        pt1 = Point(lines[i].start.x, lines[i].start.y, 0)
        S.append(pt1)
        pt2 = Point(lines[i].end.x, lines[i].end.y, 1)
        S.append(pt2)

        pt1.other_end = pt2
        pt2.other_end = pt1

    sortedPoints = sorted(S, key=cmp_to_key(compare))

    dict = {}
    for pt in sortedPoints:
        dict[pt] = Node(pt)

    T = RedBlackTree()

    # Step 3
    for pt in sortedPoints:
        nd = dict[pt]
        # print(T)
        # print('node : ', nd, '\tp: ', nd.parent.key, '\tl: ', nd.left.key, '\tr: ', nd.right.key)
        if nd.key.ptype == 0:
            T.insert(nd)
            line1 = LineSegment(nd.key, nd.key.other_end)
            prd = T.predecessor(nd)
            if prd:
                line2 = LineSegment(prd.key, prd.key.other_end)
                if LineSegment.checkSegmentIntersection(line1, line2):
                    return (line1, line2)
            else:
                print('pred not found : ', nd)

            ssc = T.successor(nd)
            if ssc:
                line2 = LineSegment(ssc.key, ssc.key.other_end)
                if LineSegment.checkSegmentIntersection(line1, line2):
                    return (line1, line2)
            else:
                print('succ not found : ', nd)
        if nd.key.ptype == 1:
            T.delete(dict[nd.key.other_end])
            T.insert(nd)
            prd = T.predecessor(nd)
            ssc = T.successor(nd)
            if prd and ssc:
                line1 = LineSegment(prd.key, prd.key.other_end)
                line2 = LineSegment(ssc.key, ssc.key.other_end)
                print(line1, '\t', line2)
                if LineSegment.checkSegmentIntersection(line1, line2):
                    print('intersect : ', T.size)
                    return (line1, line2)
                else:
                    print('does not intersect')
            else:
                print('prev or succ not found : ', nd)
            T.delete(nd)
    return None


def pairOfIntersectedLineSegment(lines):
    """
        Return:
            lines (pair of LineSegment or None)
        Args:
            lines (LineSegment)

        It will spit out any pair of line segment that are intersected with each other.
        Shamos-Hoey Algorithm is used here.
    """

    # pq = PriorityQueue()

    # for i in range(len(lines)):
    #     if lines[i].start.x > lines[i].end.x or (lines[i].start.x == lines[i].end.x and lines[i].start.y > lines[i].end.y):
    #         end = lines[i].start
    #         start = lines[i].end
    #         lines[i] = LineSegment(start, end)

    #     pq.put((lines[i].start.x, -1, i))
    #     pq.put((lines[i].end.x, 1, i))

    # avl = AVLTree()
    # while not pq.empty():
    #     tp = pq.get()
    #     idx = tp[2]
    #     print('tp : ', tp[0])
    #     # line segment left end event
    #     if tp[1] == -1:
    #         key = (lines[idx].start.y, idx)
    #         avl.insert(key, True)
    #         line1 = lines[idx]
    #         try:
    #             prev_item = avl.prev_item(key)
    #             line2 = lines[prev_item[0][1]]
    #             if LineSegment.checkSegmentIntersection(line1, line2):
    #                 return (line1, line2)
    #         except:
    #             print('prev not found for ', idx, ', cnt ', avl.count)

    #         try:
    #             succ_item = avl.succ_item(key)
    #             line2 = lines[succ_item[0][1]]
    #             if LineSegment.checkSegmentIntersection(line1, line2):
    #                 return (line1, line2)
    #         except:
    #             print('next not found for ', idx, ', cnt ', avl.count)

    #     # line segment right end event
    #     elif tp[1] == 1:
    #         avl.remove((lines[idx].start.y, idx))
    #         key = (lines[idx].end.y, idx)
    #         avl.insert(key, True)
    #         try:
    #             prev_item = avl.prev_item(key)
    #             line1 = lines[prev_key[0][1]]
    #             try:
    #                 succ_item = avl.succ_item(key)
    #                 line2 = lines[succ_key[0][1]]

    #                 if LineSegment.checkSegmentIntersection(line1, line2):
    #                     return (line1, line2)
    #             except:
    #                 pass
    #         except:
    #             pass

    #         avl.remove(key)
    return None


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
    """
        Return:
            lines (LineSegment)
        Args:
            lines (LineSegment)

        find all intersected line pairs
    """
    pq = PriorityQueue()
    for line in lines:
        pq.put((line.start.x, line.start.y, 0))
        pq.put((line.end.x, line.end.y, 1))

    # points = linesToSortedPoints(lines)

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


def minDistancePair(points):
    """
        Return:
            pair of points
        Args:
            points (Vector2)
    """
    pq = AVLTree()

    for pt in points:
        pq.insert((pt.x, pt.y), 0)
