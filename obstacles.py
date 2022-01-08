def hex_reachable(start, movement):
    visited = set() # set of hexes
    add start to visited
    var fringes = [] # array of arrays of hexes
    fringes.append([start])

    for each 1 < k ≤ movement:
        fringes.append([])
        for each hex in fringes[k-1]:
            for each 0 ≤ dir < 6:
                var neighbor = hex_neighbor(hex, dir)
                if neighbor not in visited and not blocked:
                    add neighbor to visited
                    fringes[k].append(neighbor)

    return visited
