from Map import Map_Obj


class Node:
    def __init__(self, pos):
        self.pos = pos
        self.parent = None
        self.g = -1     # Initial values that will be given later
        self.h = -1
        self.f = self.g + self.h

    def __eq__(self, other):        # Added to know whether two nodes are the same
        return self.pos == other.pos


class Open_set:
    def __init__(self):
        self.nodes = []

    def __contains__(self, item):
        return item in self.nodes       # Checks if a node is in the open set

    def sort(self):
        self.nodes.sort(key=lambda x: x.f, reverse=True)    # Sort on decreasing f-value

    def push(self, node):
        self.nodes.append(node)         # Appends a node to the set, and then sorts the set
        self.sort()

    def pop(self):
        return self.nodes.pop()         # Returns the last node in the set

    def is_empty(self):
        return len(self.nodes) == 0


def heuristic(current_pos, goal_pos):   # Manhattan distance
    return abs(goal_pos[0] - current_pos[0]) + abs(goal_pos[1] - current_pos[1])


def get_neighbours(node, map):          # Returns a set of valid neighbours in all cardinal directions
    current_y = node.pos[0]
    current_x = node.pos[1]
    intmap, strmap = map.get_maps()
    mapsize_y = intmap.shape[0]
    mapsize_x = intmap.shape[1]
    neighbours = []
    if map.get_cell_value([current_y, current_x - 1]) != -1 and current_x > 0:
        node_W = Node([current_y, current_x - 1])
        neighbours.append(node_W)
    if map.get_cell_value([current_y - 1, current_x]) != -1 and current_y > 0:
        node_N = Node([current_y - 1, current_x])
        neighbours.append(node_N)
    if map.get_cell_value([current_y, current_x + 1]) != -1 and current_x < mapsize_x:
        node_E = Node([current_y, current_x + 1])
        neighbours.append(node_E)
    if map.get_cell_value([current_y + 1, current_x]) != -1 and current_y < mapsize_y:
        node_S = Node([current_y + 1, current_x])
        neighbours.append(node_S)
    return neighbours


def path_to_goal(start_node, goal_node, map):       # Replaces nodes in the map to visualize the best path
    current_node = goal_node.parent
    while current_node != start_node:
        map.replace_map_values(current_node.pos, 0, goal_node.pos)
        current_node = current_node.parent


def Astar(task):                        # This is where the magic happens
    closed_set = []
    open_set = Open_set()
    map = Map_Obj(task=task)
    goal_pos = map.goal_pos
    start_node = Node(map.start_pos)    # Sets values for start node
    start_node.g = 0
    start_node.h = heuristic(start_node.pos, goal_pos)
    start_node.f = start_node.h
    open_set.push(start_node)           # Puts start node into open set

    while not open_set.is_empty():
        current_node = open_set.pop()   # Chooses the last node in the open set
        print("Currently expanding", current_node.pos)
        print('Nodes in Open Set', len(open_set.nodes))
        if current_node.pos == goal_pos:    # Checks if current node is the goal
            print("Goal found")
            path_to_goal(start_node, current_node, map)
            map.show_map()
            return      # Stops process if goal found
        else:
            closed_set.append(current_node)     # Puts expanded node in closed set
            neighbours = get_neighbours(current_node, map)
            for neighbour in neighbours:
                if neighbour not in closed_set:  # Puts all valid neighbours that have not yet been expanded in open set
                    neighbour.h = heuristic(neighbour.pos, goal_pos)
                    neighbour.g = current_node.g + map.get_cell_value(neighbour.pos)
                    neighbour.f = neighbour.h + neighbour.g
                    neighbour.parent = current_node
                    open_set.push(neighbour)


Astar(1)
#Astar(2)
#Astar(3)
#Astar(4)
