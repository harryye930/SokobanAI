import os  # for time functions
import math  # for infinity
import heapq
from solution import *
from sokoban import sokoban_goal_state, PROBLEMS
import os



def load_problems():
    PROBLEMS = (
        SokobanState("START", 0, None, 6, 4,  # dimensions
                     ((2, 1), (2, 2)),  # robots
                     frozenset(((1, 1), (1, 2), (4, 1), (4, 2))),  # boxes
                     frozenset(((2, 1), (2, 2), (3, 1), (3, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 5, 5,  # dimensions
                     ((2, 1), (2, 3)),  # robots
                     frozenset(((1, 1), (1, 3), (3, 1), (3, 3))),  # boxes
                     frozenset(((0, 0), (0, 4), (4, 0), (4, 4))),  # storage
                     frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)))  # obstacles
                     ),
        SokobanState("START", 0, None, 5, 5,  # dimensions
                     ((2, 2),),  # robots
                     frozenset(((1, 1), (1, 3), (3, 1), (3, 3))),  # boxes
                     frozenset(((0, 0), (0, 4), (4, 0), (4, 4))),  # storage
                     frozenset(((1, 0), (2, 0), (3, 0), (1, 4), (2, 4), (3, 4)))  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 4,  # dimensions
                     ((2, 1), (2, 2)),  # robots
                     frozenset(((1, 1), (4, 2))),  # boxes
                     frozenset(((2, 1), (2, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 4,  # dimensions
                     ((2, 1), (2, 2)),  # robots
                     frozenset(((4, 2),)),  # boxes
                     frozenset(((2, 1),)),  # storage
                     frozenset()  # obstacles
                     ),
        ## Number 5 ##
        SokobanState("START", 0, None, 5, 5,  # dimensions
                     ((4, 0), (4, 4)),  # robots
                     frozenset(((3, 1), (3, 2), (3, 3))),  # boxes
                     frozenset(((0, 0), (0, 2), (0, 4))),  # storage
                     frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                     ),
        SokobanState("START", 0, None, 5, 5,  # dimensions
                     ((4, 0), (4, 4)),  # robots
                     frozenset(((3, 1), (3, 2))),  # boxes
                     frozenset(((0, 0), (0, 2))),  # storage
                     frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                     ),
        SokobanState("START", 0, None, 5, 5,  # dimensions
                     ((4, 0),),  # robots
                     frozenset(((3, 1), (3, 2), (3, 3))),  # boxes
                     frozenset(((0, 0), (0, 2), (0, 4))),  # storage
                     frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((0, 0), (0, 2), (0, 4)),  # robots
                     frozenset(((1, 0), (1, 2), (1, 4))),  # boxes
                     frozenset(((5, 0), (5, 2), (0, 5))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((0, 0), (0, 2), (0, 4), (5, 5)),  # robots
                     frozenset(((1, 0), (4, 1), (1, 2), (4, 3), (1, 4), (4, 5))),  # boxes
                     frozenset(((5, 0), (0, 1), (5, 2), (0, 3), (5, 4), (0, 5))),  # storage
                     frozenset()  # obstacles
                     ),
        ## Number 10 ##
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((5, 5), (5, 4), (4, 5)),  # robots
                     frozenset(((3, 1), (2, 2), (1, 4), (3, 4))),  # boxes
                     frozenset(((0, 0), (0, 1), (1, 0), (1, 1))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((5, 5), (5, 4), (4, 5)),  # robots
                     frozenset(((3, 1), (1, 4), (3, 4))),  # boxes
                     frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((5, 5), (5, 4), (4, 5)),  # robots
                     frozenset(((3, 1), (2, 2), (1, 4))),  # boxes
                     frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((5, 5), (5, 4)),  # robots
                     frozenset(((3, 1), (1, 4), (3, 4))),  # boxes
                     frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 6, 6,  # dimensions
                     ((5, 5), (5, 4)),  # robots
                     frozenset(((3, 1), (2, 2), (1, 4))),  # boxes
                     frozenset(((0, 0), (0, 1), (1, 0))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 8, 8,  # dimensions
                     ((0, 5), (1, 6), (2, 7)),  # robots
                     frozenset(((5, 6), (4, 5), (6, 2), (5, 2), (4, 6))),  # boxes
                     frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 8, 8,  # dimensions
                     ((0, 5), (1, 6), (2, 7)),  # robots
                     frozenset(((6, 2), (5, 6), (4, 4), (6, 3))),  # boxes
                     frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 8, 8,  # dimensions
                     ((0, 5), (1, 6), (2, 7)),  # robots
                     frozenset(((5, 4), (5, 5), (6, 3), (4, 2), (6, 5), (5, 3))),  # boxes
                     frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 8, 8,  # dimensions
                     ((0, 5), (1, 6), (2, 7)),  # robots
                     frozenset(((6, 6), (5, 6), (6, 2), (4, 3), (5, 1), (6, 5))),  # boxes
                     frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 8, 8,  # dimensions
                     ((0, 5), (1, 6), (2, 7)),  # robots
                     frozenset(((6, 6), (4, 5), (4, 1), (4, 3), (5, 2), (5, 3))),  # boxes
                     frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
                     frozenset()  # obstacles
                     ),
        SokobanState("START", 0, None, 5, 5,  # dimensions
                     ((4, 0),),  # robots
                     frozenset(((3, 1), (3, 2), (3, 3))),  # boxes
                     frozenset(((0, 0), (0, 2), (3, 2))),  # storage
                     frozenset(((2, 0), (2, 1), (2, 3), (2, 4)))  # obstacles
                     ),
        SokobanState("START", 0, None, 4, 7,  # dimensions
                     ((0, 3),),  # robots
                     frozenset(((1, 2), (1, 3), (1, 4))),  # boxes
                     frozenset(((2, 1), (2, 5), (1, 3))),  # storage
                     frozenset(((1, 1), (1, 5)))  # obstacles
                     )
    )
    return PROBLEMS

if __name__ == "__main__":
    # state1 = SokobanState("START", 0, None, 6, 6,  # dimensions
    #                       ((0, 0), (4, 1), (2, 4), (3, 5)),  # robots
    #                       frozenset(((1, 0), (4, 0), (5, 2), (3, 4), (4, 4), (2, 5))),  # boxes
    #                       frozenset(((5, 0), (0, 1), (5, 2), (0, 3), (5, 4), (0, 5))),  # storage
    #                       frozenset()  # obstacles
    #                       )
    # state1.print_state()

    s0 = PROBLEMS[1]  # Problems get harder as i gets bigger
    se = SearchEngine('best_first', 'full')
    se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_alternate)
    final, stats = se.search(2)

    if final:
        # final.print_path()
        print("SOLVED")
    else:
        print("UNSOLVED")


    # test = heur_alternate(state1)

    # state2 = SokobanState("START", 0, None, 8, 8,  # dimensions
    #              ((0, 5), (1, 6), (2, 7)),  # robots
    #              frozenset(((6, 2), (5, 6), (4, 4), (6, 3))),  # boxes
    #              frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
    #              frozenset()  # obstacles
    #              )
    # state3 = SokobanState("START", 0, None, 6, 6,  # dimensions
    #              ((0, 0), (0, 2), (0, 4), (5, 5)),  # robots
    #              frozenset(((1, 0), (4, 1), (1, 2), (4, 3), (1, 4), (4, 5))),  # boxes
    #              frozenset(((5, 0), (0, 1), (5, 2), (0, 3), (5, 4), (0, 5))),  # storage
    #              frozenset()  # obstacles
    #              )
    # state4 = SokobanState("START", 0, None, 8, 8,  # dimensions
    #                       ((0, 5), (1, 6), (2, 7)),  # robots
    #                       frozenset(((5, 6), (4, 5), (6, 2), (5, 2), (4, 6))),  # boxes
    #                       frozenset(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2))),  # storage
    #                       frozenset()  # obstacles
    #                       )
    # # manh_distance_one_to_one_buggy(state4)
    # for i in range(len(PROBLEMS)):
    #     print(i, heur_manhattan_distance(PROBLEMS[i]), heur_alternate(PROBLEMS[i]))
    #

