import sys

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = "wmap.txt"

wmap = {}
    
def get_at(x, y):
    if (x, y) in wmap:
        return wmap[(x, y)]
    else:
        return 0

def set_at(x, y, d):
    wmap[(x, y)] = d

    if wmap[(x, y)] == 0:
        del wmap[(x, y)]

def get_wmap():
    return wmap

def tick():
    global wmap
    nwmap = {}

    for pos, val in wmap.items():
        if val == 0:    # empty
            continue
        elif val == 1:  # electron head
            nwmap[pos] = 2
        elif val == 2:  # electron tail
            nwmap[pos] = 3
        elif val == 3:  # conductor
            c = 0

            for oy in [-1, 0, 1]:
                for ox in [-1, 0, 1]:
                    if ox == 0 and oy == 0:
                        continue

                    c += get_at(pos[0] + ox, pos[1] + oy) == 1

            if c == 1 or c == 2:
                nwmap[pos] = 1
            else:
                nwmap[pos] = 3

    wmap = nwmap

def save():
    if len(wmap.values()) == 0:
        with open("dmap.txt", "w") as file:
            file.write("")
        return

    lx, ly = None, None

    for pos, val in wmap.items():
        if val == 0:
            continue

        if lx == None:
            lx = pos[0]
        if ly == None:
            ly = pos[1]

        if pos[0] < lx:
            lx = pos[0]
        if pos[1] < ly:
            ly = pos[1]

    cmap = {}

    for pos, val in wmap.items():
        if val == 0:
            continue

        cmap[(pos[0] - lx, pos[1] - ly)] = val

    lines = []

    for pos, val in cmap.items():
        while len(lines) <= pos[1]:
            lines.append("")

        while len(lines[pos[1]]) <= pos[0]:
            lines[pos[1]] += " "

        line = list(lines[pos[1]])
        line[pos[0]] = " @*O"[val]
        lines[pos[1]] = "".join(line)

    clines = []

    for line in lines:
        while True:
            if len(line) > 0:
                if line[-1] == " ":
                    line = line[:-1]
                else:
                    break
            else:
                break

        clines.append(line)

    with open("dmap.txt", "w") as file:
        file.write("\n".join(clines))

with open(file_name) as file:
    c2n = {"@": 1, "*": 2, "O": 3}
    y = 0
    for line in file.read().split("\n"):
        for x in range(0, len(line)):
            if line[x] in c2n:
                wmap[(x, y)] = c2n[line[x]]

        y += 1
