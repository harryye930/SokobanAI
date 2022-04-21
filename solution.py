#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
import math  # for infinity
import heapq
from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems


def sokoban_goal_state(state):
    '''
    @return: Whether all boxes are stored.
    '''
    for box_cord in state.boxes:
        if box_cord not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the 
    distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be
    # stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.


    manh_dists = {}  # box1: [box1 to to storg1, box1 to storg2... ]
    for box_loc in state.boxes:
        manh_dists[box_loc] = get_manh_dist_list(box_loc, state.storage)

    min_manh_dist = 0
    for box_loc in manh_dists.keys():
        min_manh_dist += min(manh_dists[box_loc])
    return min_manh_dist


def get_manh_dist_list(loc, locs):
    """
    return a list of manhattan distance between loc and locs
    """
    dists = []
    for single_loc in locs:
        dists.append(manhattan_distance(loc, single_loc))
    return dists


def manhattan_distance(loc_a, loc_b):
    """
    calculate 2d manhattan distance
    """
    return abs(loc_a[0] - loc_b[0]) + abs(loc_a[1] - loc_b[1])


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    return 0  # CHANGE THIS


# def heur_alternate(state):
#     '''a better heuristic'''
#     '''INPUT: a sokoban state'''
#     '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
#     """
#     IDEA: instead of only calculating THE lowest manhattan distance between
#     boxes and storages, we can calculate the optimal manhattan distance
#     for a box and storage point, then stop considering them, which is more
#     realistic since no storage points can store more than 1 box.
#
#     @bug: when some boxes have the same manhattan distance on the same storge
#     point, the program randomly pick one (which may result in worse future
#      manhattan distance) instead of picking THE best combination.
#     """
#     # storg_loc1: [dist box1 to storg1, dist box2 to storg1,...]
#     manh_dists = {}
#     for storg_loc in state.storage:
#         manh_dists[storg_loc] = get_manh_dist_list(storg_loc, state.boxes)
#
#     manh_dists_copy = copy.deepcopy(manh_dists)
#     used_index = []
#     min_manh_dist = 0
#     num_box = len(manh_dists[storg_loc])
#     for _ in range(num_box):
#         storg_loc = min(manh_dists.items(), key=lambda x: min(x[1]))[0]         # storg_loc is the location of storage point with the smallest distance to box
#         original_index = list(range(num_box))                                   # give a list of indecies of current number in original list
#         if len(used_index) == num_box:
#             return min_manh_dist
#         cond = False
#         while cond is False:
#             min_index = min(range(len(manh_dists[storg_loc])), key=manh_dists[storg_loc].__getitem__)
#             if min_index not in used_index:
#                 used_index.append(min_index)
#                 break
#             if manh_dists[storg_loc] != []:
#                 manh_dists[storg_loc].pop(min_index)
#                 original_index.pop(min_index)
#             new_min_index = min(range(len(manh_dists[storg_loc])), key=manh_dists[storg_loc].__getitem__)
#             if original_index[new_min_index] not in used_index:
#                 used_index.append(original_index[new_min_index])
#                 min_index = original_index[new_min_index]
#                 break
#         min_manh_dist += manh_dists_copy[storg_loc][min_index]
#         manh_dists.pop(storg_loc)
#     return min_manh_dist


def updated_manh_dist(start_loc, end_loc, obstacles):
    move_left = start_loc[0] > end_loc[0]
    move_right = start_loc[0] < end_loc[0]
    move_up = start_loc[1] < end_loc[1]
    move_down = start_loc[1] > end_loc[1]
    manh_dist = manhattan_distance(start_loc, end_loc)
    if move_left and (start_loc[0] - 1, start_loc[1]) in obstacles:
        manh_dist += 3
    elif move_right and (start_loc[0] + 1, start_loc[1]) in obstacles:
        manh_dist += 3
    elif move_up and (start_loc[0], start_loc[1] - 1) in obstacles:
        manh_dist += 3
    elif move_down and (start_loc[0], start_loc[1] + 1) in obstacles:
        manh_dist += 3
    return manh_dist


def get_closest_target(start_loc, end_locs, obstacles):
    found = start_loc in end_locs
    if not found:

        end_locs = end_locs.copy()
        manh_dist = []
        for end_loc in end_locs:
            manh_dist.append(updated_manh_dist(start_loc, end_loc, obstacles))

        min_index = min(range(len(manh_dist)), key=manh_dist.__getitem__)
        return end_locs[min_index]
    return start_loc


def check_corner(box_loc, boxes, obstacles, game_board_size, storages):
    storages_x_list = []
    storages_y_list = []
    for storage in storages:
        storages_x_list.append(storage[0])
        storages_y_list.append(storage[1])
    left = (box_loc[0] - 1, box_loc[1])
    right = (box_loc[0] + 1, box_loc[1])
    up = (box_loc[0], box_loc[1] - 1)
    down = (box_loc[0], box_loc[1] + 1)
    possible_position = [left, right, up, down]
    stuck = 0
    # at left most or right most column
    if box_loc[0] == 0 or (box_loc[0] == game_board_size[0] - 1):
        # while there is no storage
        if box_loc[0] not in storages_x_list:
            return True

    # at bottom or top most row
    if box_loc[1] == 0 or (box_loc[1] == game_board_size[1] - 1):
        # while there is no storage
        if box_loc[1] not in storages_y_list:
            return True
    stuck_loc = [0, 0, 0, 0]
    for i in range(len(possible_position)):
        # if immediate next is an obstacle or another box
        if possible_position[i] in obstacles or possible_position[i] in boxes:
            stuck += 1
        # if immediate next is left/right limit
        if possible_position[i][0] == -1 or possible_position[i][0] == game_board_size[0]:
            stuck += 1
        # if immediate next is up/down limit
        if possible_position[i][1] == -1 or possible_position[i][1] == game_board_size[1]:
            stuck += 1


        if stuck >= 1:
            stuck_loc[i] = 1
        stuck = 0
    if stuck_loc[0] == stuck_loc[2] == 1 or \
            stuck_loc[0] == stuck_loc[3] == 1 or \
            stuck_loc[1] == stuck_loc[2] == 1 or \
            stuck_loc[1] == stuck_loc[3] == 1:      # left + up/down, right +up/down
        return True
    return False


def four_size_have_more_box_than_storage(game_board_size, boxes, storages):
    four_sides = {"left": [(0, 0), (0, game_board_size[1])],
                  "right": [(game_board_size[0], 0), (game_board_size[0], game_board_size[1])],
                  "top": [(0, 0), (game_board_size[0], 0)],
                  "bottom": [(0, game_board_size[1]), (game_board_size[0], game_board_size[1])]}
    for side in four_sides:
        num_box = 0
        num_storage = 0
        if side == "left":
            for row_num in range(four_sides["left"][1][1]):
                curr_loc = (0, row_num)
                if curr_loc in boxes:
                    num_box += 1
                elif curr_loc in storages:
                    num_storage += 1
            if num_box > num_storage:
                return True
        elif side == "right":
            for row_num in range(four_sides["left"][1][1]):
                curr_loc = (game_board_size[0]-1, row_num)
                if curr_loc in boxes:
                    num_box += 1
                elif curr_loc in storages:
                    num_storage += 1
            if num_box > num_storage:
                return True
        elif side == "top":
            for col_num in range(four_sides["top"][1][0]):
                curr_loc = (col_num, 0)
                if curr_loc in boxes:
                    num_box += 1
                elif curr_loc in storages:
                    num_storage += 1
            if num_box > num_storage:
                return True
        else:
            for col_num in range(four_sides["top"][1][0]):
                curr_loc = (col_num, game_board_size[1]-1)
                if curr_loc in boxes:
                    num_box += 1
                elif curr_loc in storages:
                    num_storage += 1
            if num_box > num_storage:
                return True
    return False


def direct_line_of_sight(start_loc, robots, storages, obstacles, game_board_size):
    increment = 1
    data = {"left": [0, 0],
            "right": [0, 0],
            "up":[0, 0],
            "down": [0, 0]}
    # format: [has_storage, has robot]
    for _ in range(max(game_board_size)):
        left = (start_loc[0] - increment, start_loc[1])
        if left in storages:
            data["left"][0] += 1
            if data["right"][1] != 0:  # means we have robot on the different direction
                return True
        elif left in robots:
            data["left"][1] += 1

        right = (start_loc[0] + increment, start_loc[1])
        if right in storages:
            data["right"][0] += 1
            if data["left"][1] != 0:
                return True
        elif right in robots:
            data["right"][1] += 1

        up = (start_loc[0], start_loc[1] + increment)
        if up in storages:
            data["up"][0] += 1
            if data["down"][1] != 0:
                return True
        elif up in robots:
            data["up"][1] += 1
        down = (start_loc[0], start_loc[1] - increment)
        if down in storages:
            data["down"][0] += 1
            if data["up"][1] != 0:
                return True
        elif down in robots:
            data["down"][1] += 1
        increment += 1
    return False



def heur_alternate(state):
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    """
    IDEA: For every bot, they are going to move whatever case that is closest 
    (calculated base on the manhattan distance, or maybe updated manhattan 
    distance that check if there is obstacle between?) and the manhattan distance 
    between the box and the closest storage (or updated manh distance)
    """
    bots = []
    storages = []
    for x in state.robots:
        bots.append(x)
    for x in state.storage:
        storages.append(x)


    dist = 0
    for box_loc in state.boxes:
        if box_loc in state.storage:
            storages.remove(box_loc)
        else:  # box in storage, check if there is unfilled storage near it
            box_left = (box_loc[0] - 1, box_loc[1])
            box_right = (box_loc[0] + 1, box_loc[1])
            box_up = (box_loc[0], box_loc[1]-1)
            box_down = (box_loc[0], box_loc[1]+1)
            possibles = [box_left, box_right, box_up, box_down]
            for loc in possibles:
                if loc in storages and loc not in state.boxes:
                    dist += 1

    for box_loc in state.boxes:
        if box_loc not in state.storage:
            stuck = check_corner(box_loc, state.boxes, state.obstacles, (state.width, state.height), storages) #or \
            #four_size_have_more_box_than_storage((state.width, state.height), state.boxes, state.storage)
            if stuck:
                return math.inf
            line_of_sight = direct_line_of_sight(box_loc, bots, storages, state.obstacles, (state.width, state.height))
            if line_of_sight:
                dist -= 1.2  # we favour a direct line of sight

            closest_bot = get_closest_target(box_loc, bots, state.obstacles)
            dist += updated_manh_dist(box_loc, closest_bot, state.obstacles)
            # dist += manhattan_distance(box_loc, closest_bot)
            closest_storage = get_closest_target(box_loc, storages, state.obstacles)
            dist += updated_manh_dist(box_loc, closest_storage, state.obstacles)
            # dist += manhattan_distance(box_loc, closest_storage)

    return dist




















def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    return sN.gval + weight * sN.hval


# SEARCH ALGORITHMS
def weighted_astar(initial_state, heur_fn, weight, timebound):
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a warehouse state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of weighted astar algorithm'''
    se = SearchEngine('best_first', 'full')
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    se.init_search(initial_state, goal_fn=sokoban_goal_state,
                   heur_fn=heur_fn, fval_function=wrapped_fval_function)
    final, stats = se.search(timebound)
    return final, stats


def iterative_astar(initial_state, heur_fn, weight=1, timebound=5):  # uses f(n), see how autograder initializes a search line 88
    '''Provides an implementation of realtime a-star, as described in the HW1 handout'''
    '''INPUT: a warehouse state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of realtime astar algorithm'''

    start_time = os.times()[0]
    remain_time = timebound
    g_val = math.inf
    h_val = math.inf
    f_val = g_val + weight * h_val
    costbound = (g_val, h_val, f_val)
    best_final = None
    best_stats = None
    while remain_time > 0:
        # same as weighted a* #
        se = SearchEngine('best_first', 'full')
        wrapped_fval_function = (lambda sN: fval_function(sN, weight))
        se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn, fval_function=wrapped_fval_function)
        # end same as weighted a* #
        final, stats = se.search(timebound, costbound)

        if final:
            costbound = (final.gval, heur_fn(final), final.gval + weight * heur_fn(final))
            best_final = final
            best_stats = stats
        elif final is None or final is False:
            return best_final, best_stats

        remain_time = timebound - (os.times()[0] - start_time)
        weight = weight / 3
        # print(weight)
    return best_final, best_stats


def iterative_gbfs(initial_state, heur_fn, timebound=5):  # only use h(n)
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    start_time = os.times()[0]
    remain_time = timebound
    last_runtime = timebound -1
    costbound = (math.inf, math.inf, math.inf)
    best_final = None
    best_stats = None
    while remain_time > last_runtime:
        # same as weighted a* #
        se = SearchEngine('best_first', 'full')
        se.init_search(initial_state, goal_fn=sokoban_goal_state, heur_fn=heur_fn)
        # end same as weighted a* #
        final, stats = se.search(timebound, costbound)

        if final:
            costbound = (final.gval, math.inf, math.inf)
            best_final = final
            best_stats = stats
        else:
            return False, stats
        last_runtime = os.times()[0] - start_time
        remain_time = timebound - last_runtime
    return best_final, best_stats



