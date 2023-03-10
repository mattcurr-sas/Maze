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
    'N': 1,
    'S': 1,
    'W': 1,
    'E': 1,
}

# Define heuristic function using Euclidean distance
def heuristic(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
final = []
def astar(maze, start, finish, file_path):
    # Initialize open and closed lists
    open_list = []
    closed_list = set()
    # Initialize start node
    start_node = (start, 0, [])
    # Add start node to open list
    heapq.heappush(open_list, (heuristic(start, finish), start_node))

    # Loop until finish node is found or open list is empty
    while open_list:
        # Pop node with lowest cost from open list
        current_cost, current_node = heapq.heappop(open_list)
        current_pos, current_path_cost, current_path = current_node
        # Check if current node is the finish node
        if current_pos == finish:
            # Construct path and return
            current_path.append(finish)
            write_data_to_file(current_path, closed_list, file_path)
            final = current_path
            return current_path, closed_list, final
        # Add current node to closed list
        closed_list.add(current_pos)
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
            # Check if node is already in closed list and has lower cost
            if new_pos in closed_list:
                continue
            # Check if node is already in open list and has lower cost
            for _, node in open_list:
                pos, path_cost, _ = node
                if pos == new_pos and path_cost <= new_path_cost:
                    break
            else:
                # Add new node to open list
                new_node = (new_pos, new_path_cost, current_path + [current_pos])
                heapq.heappush(open_list, (new_cost + heuristic_cost, new_node))
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


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl


def visualize_astar(maze, start, finish, final):
    # Create a numpy array to represent the maze
    maze_array = np.array(maze)
    
    # Set the start and finish positions in the maze array
    maze_array[start] = 2
    maze_array[finish] = 3
    
    # Set the visited nodes in the maze array
    for node in final:
        if node != start and node != finish and 0 <= node[0] < maze_array.shape[0] and 0 <= node[1] < maze_array.shape[1]:
            maze_array[node] = 4   # Set visited node value to 4 if not the start or finish node
    
    # Create a colormap for the maze
    cmap = mpl.colors.ListedColormap(['black', 'white', 'green', 'red', 'yellow'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
    # Create a figure and plot the maze
    fig, ax = plt.subplots(figsize=(8,6))
    ax.imshow(maze_array, cmap=cmap, norm=norm)
    
    # Set the ticks for the axes
    ax.set_xticks(np.arange(-.5, maze_array.shape[1], 1))
    ax.set_yticks(np.arange(-.5, maze_array.shape[0], 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(axis='both', length=0)
    
    # Create a legend for the colors
    legend_elements = [mpl.patches.Patch(facecolor='white', edgecolor='black', label='Free Space'),
                       mpl.patches.Patch(facecolor='black', edgecolor='black', label='Wall'),
                       mpl.patches.Patch(facecolor='green', edgecolor='black', label='Start'),
                       mpl.patches.Patch(facecolor='red', edgecolor='black', label='Finish'),
                       mpl.patches.Patch(facecolor='yellow', edgecolor='black', label='Visited')]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1))
    
    # Add a title to the plot
    ax.set_title('A* Algorithm Visualization')
    
    # Show the plot
    plt.show()







# Call A* algorithm function
path, visited_nodes, final = astar(maze, start, finish, 'training_data.txt')

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
    
    # Call visualization function
    visualize_astar(maze, start, finish, final)
else:
    print('No path found')
