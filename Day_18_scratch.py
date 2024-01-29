import sys

with open('Day_18_input.txt' if len(sys.argv) == 1 else sys.argv[1]) as h: file = h.read()
lines = file.split('\n')
dirmap = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}
minx, maxx = 1e9, 0
miny, maxy = 1e9, 0
y, x = 0, 0
for line in lines:
    d, s, c = line.split()
    d, s, c = d, int(s), c[1:-1]
    d, s = dirmap[int(c[-1])], int(c[1:-1], 16)  # CHANGE BELOW
    if d == 'R':
        x += s
        maxx = max(maxx, x)
    elif d == 'L':
        x -= s
        minx = min(minx, x)
    elif d == 'U':
        y -= s
        miny = min(miny, y)
    elif d == 'D':
        y += s
        maxy = max(maxy, y)
edges = []
ep = 0
y, x = -miny, -minx
lastdir = ''
for line in lines:
    d, s, c = line.split()
    d, s, c = d, int(s), c[1:-1]
    d, s = dirmap[int(c[-1])], int(c[1:-1], 16)  # CHANGE ABOVE
    if d == 'R':
        dy, dx = 0, s
    elif d == 'L':
        dy, dx = 0, -s
    elif d == 'U':
        dy, dx = -s, 0
    elif d == 'D':
        dy, dx = s, 0
    ep += s
    edge = [(y, x), (y + dy, x + dx), d, lastdir, '']
    if len(edges) > 0:
        edges[-1][4] = d
    edges.append(edge)
    lastdir = d
    y, x = y + dy, x + dx
edges[0][3] = edges[-1][2]
edges[-1][4] = edges[0][2]
miny, maxy = miny - miny, maxy - miny
minx, maxx = minx - minx, maxx - minx
verts = sorted([edge for edge in edges if edge[2] == 'D' or edge[2] == 'U'], key=lambda x: (x[0][1], x[0][0]))
ans = 0
for i, vert1 in enumerate(verts):
    p1, p2, d, le, re = vert1
    if vert1[2] == 'U':
        p1y, p1x = p1
        p2y, p2x = p2
        top, bottom = min(p1y, p2y), max(p1y, p2y)
        if le == 'L' and re == 'R':
            rng = (top + 1, bottom - 1)
        elif le == 'L' and re == 'L':
            rng = (top, bottom - 1)
        elif le == 'R' and re == 'R':
            rng = (top + 1, bottom)
        elif le == 'R' and re == 'L':
            rng = (top, bottom)
        ranges = [rng]
        while ranges:
            top, bottom = ranges.pop()
            for j, vert2 in enumerate(verts[(i + 1) % len(verts):]):
                p1, p2, d, le, re = vert2
                if vert2[2] != 'D': continue
                p1y, p1x = p1
                p2y, p2x = p2
                top2, bottom2 = min(p1y, p2y), max(p1y, p2y)
                maxtop, minbottom = max(top, top2), min(bottom, bottom2)
                if maxtop > minbottom: continue
                ans += (minbottom - maxtop + 1) * (p1x - vert1[0][1] - 1)
                if top < top2: ranges.append((top, top2 - 1))
                if bottom2 < bottom: ranges.append((bottom2 + 1, bottom))
                break
print(ans + ep)
