from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval

def bfs(starting_room_id):
    queue = Queue()
    queue.enqueue([starting_room_id])
    visited = set()

    while queue.size() > 0:
        # grab path
        path = queue.dequeue()
        # take last in path
        current_room = path[-1]
        visited.add(current_room)

        for direction in checked_rooms_dict[current_room]:
            if checked_rooms_dict[current_room][direction] == '?':
                return path    
            elif checked_rooms_dict[current_room][direction] not in visited:
                # create a new path to append direction
                new_path = list(path)
                new_path.append(checked_rooms_dict[current_room][direction])
                queue.enqueue(new_path)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = list()

# Will hold all data of rooms checked
checked_rooms_dict = dict()

rev_dir = {'n':'s', 's':'n', 'e':'w', 'w':'e'}
prev_room_id = 0

while len(checked_rooms_dict) != len(room_graph):
    current_room = player.current_room
    room_id = current_room.id
    crd = dict() # current_room_dictonary

    # Check to see if player has explored the room already
    if room_id not in checked_rooms_dict:
        # Record exits and label as '?'
        for passage in current_room.get_exits():
            crd[passage] = '?'
        # Update with previous room id
        if traversal_path:
            prev_dir = rev_dir[traversal_path[-1]]
            crd[prev_dir] = prev_room_id
        # Update overall dictonary
        checked_rooms_dict[room_id] = crd
    # If it already exists, grab data from overall dictionary
    else:
        crd = checked_rooms_dict[room_id]

    # Check to see if there are still unknown rooms connected
    unknown_exits = list()
    for direction in crd:
        if crd[direction] == '?':
            unknown_exits.append(direction)

    # If unknowns exist, go in one of the directions
    if len(unknown_exits) != 0:
        # Shuffling can potentially reach lower (980s)
        # But could also result higher (1020s)
        # Random off, currently hits 1003
        random.shuffle(unknown_exits)
        direction = unknown_exits[0]
        traversal_path.append(direction)
        player.travel(direction)
        # Update the ?'s
        room_move = player.current_room
        checked_rooms_dict[current_room.id][direction] = room_move.id
        prev_room_id = current_room.id
    # Otherwise, find a way back to closest room with an unknown exit
    else:
        # Find closest room via BFS
        path_to_next = bfs(room_id)

        # Make sure there's actually something being returned
        if path_to_next is not None and len(path_to_next) > 0:
            # Have the player travel back to room with unknown exits
            for index in range(len(path_to_next) - 1):
                for direction in checked_rooms_dict[path_to_next[index]]:
                    if checked_rooms_dict[path_to_next[index]][direction] == path_to_next[index + 1]:
                        traversal_path.append(direction)
                        player.travel(direction)
        else:
            break
                    

print(traversal_path)
print(checked_rooms_dict)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
