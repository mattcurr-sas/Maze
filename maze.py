import heapq
import math

# Maze dimensions
ROW, COL = 6, 8

# Starting position
start = (0, 0)

# Finish position
finish = (5, 7)

# Define maze
maze = [
    [1, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 0, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1],
]

# Define cost of moving in different directions
cost = {
    'N': 15,
    'S': 1,
    'W': 20,
    'E': 1,
}

# Define heuristic function using Euclidean distance
def heuristic(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def astar(maze, start, finish, file_path):
    # Initialize open and closed lists
    open_list = []
    closed_list = set()
    # SET PATH ARRAY TO RECIVE POSITION AND PATH COST
    path = []
    # Initialize start node
    start_node = (start, 0)
    # Add start node to open list
    heapq.heappush(open_list, (heuristic(start, finish), start_node))

    # Loop until finish node is found or open list is empty
    while open_list:
        # Pop node with lowest cost from open list
        current_cost, current_node = heapq.heappop(open_list)
        current_pos, current_path_cost = current_node
        # Check if current node is the finish node
        visited_nodes = closed_list.union(set([current_pos]))
        if current_pos == finish:
            # Construct path and return
            #while current_node:
                #path.append(current_pos)
                #current_cost, current_node = current_node
                #current_pos, current_path_cost = current_node
            write_data_to_file(path, visited_nodes, file_path)
            return list(reversed(path)), visited_nodes
        # Loop over adjacent nodes
        for direction, (dx, dy) in [('N', (-1, 0)), ('S', (1, 0)), ('W', (0, -1)), ('E', (0, 1))]:
            # Calculate new position and cost
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            new_path_cost = current_path_cost + cost[direction]
            if not (0 <= new_pos[0] < ROW and 0 <= new_pos[1] < COL) or not maze[new_pos[0]][new_pos[1]]:
                # Check if new position is a wall or outside the maze and add to closed list
                continue
            # Calculate heuristic cost
            heuristic_cost = heuristic(new_pos, finish)
            if dx == 0:
                # If moving vertically, add normal cost
                new_cost = new_path_cost
            else:
                # If moving horizontally, add penalty cost
                new_cost = new_path_cost
            # Check if node is already in closed list and add 100 for back tracking
            if new_pos in closed_list:
                new_cost = new_path_cost + 100
            # Check if node is already in open list and has lower cost
            for _, node in open_list:
                pos, path_cost = node
                if pos == new_pos and path_cost <= new_path_cost:
                    break
            else:
                # Add new node to open list
                new_node = (new_pos, new_path_cost)
                heapq.heappush(open_list, (new_cost + heuristic_cost, new_node))
        # Add current node to closed list
        heapq.heappush(path, (current_pos , current_path_cost))
        closed_list.add(current_pos)
    # If finish node is not found, return None
    return None, None


def write_data_to_file(path, visited_nodes, file_path):
    with open(file_path, 'w') as f:
        f.write('Optimal Path:\n')
        for i, node in enumerate(path):
            if i == 0:
                f.write(f'{node} - Start\n')
            elif i == len(path) - 1:
                f.write(f'{node} - Finish\n')
            else:
                f.write(f'{node} - {cost} cost\n')
        f.write(f'Total cost: {cost}\n')
        f.write('Visited Nodes:\n')
        for node in visited_nodes:
            f.write(f'{node}\n')



# Call A* algorithm function
path, visited_nodes = astar(maze, start, finish, 'training_data.txt')
        
if path is not None:
            print('Optimal Path:')
            for i, node in enumerate(path):
                if i == 0:
                    print(f'{node} - Start')
                elif i == len(path) - 1:
                    print(f'{node} - Finish')
                else:
                    print(f'{node} - {cost} cost')
            print(f'Total cost: {cost}')
else:
    print('No path found')
