#!/usr/bin/env python

"""
Created on Tue Aug  6 10:40:11 2019

@author: Simon

This code is written based on a solution to the knights tour from
http://blog.justsophie.com/python-knights-tour-revisited/
"""

# Import pygame and visualizer.py for animation of knights tour
try:
    import pygame
    from visualizer import Model, View
    GUI_ON = True
except ImportError:
    GUI_ON = False


class PathFound(RuntimeError):
    pass


# KnightsTour method for an NxN chessboard.
# Input: N: size of chessboard, start_pos: (x,y) to start tour from
# closed_loop: true or false if searching for closed loop solution
# printtext: true or false if print statements
# Output: return a path if it exist for the given parameters
# return None if no path exist
def KnightsTour(N,start_pos,closed_loop,printtext=None):
    if(printtext is None):
        printtext = True
    def printl(*text):
        if printtext:
            string = ""
            for t in text:
                string += str(t)
            print(string)
    if (start_pos[0]>=N or start_pos[1]>=N or start_pos[0]< 0 or start_pos[1] < 0):
        raise IndexError("Start position is not valid")
    if(N<5):
        printl("There exist no solution for NxN when N<5");
    if(N%2==1 and closed_loop):
        printl("There exists no closed loop tour for NxN"
                        ,"when N is uneven")
    # Adjust starting position if closed loop
    if(closed_loop):
        initial_pos = (int(N/2), int(N/2))
        printl("Adjusting starting point to ", initial_pos)
    else:
        initial_pos = (start_pos[0], start_pos[1])
    end_positions = []
    # Chessboard created as nested lists
    board = [0] * N
    for i in range(N):
        board[i] = [0] * N
        
    # Generate a list of all possible destinations from a given position
    # Input: current_position Position of knight
    # Output: List of all possible location to move in one step
    def gen_possible_moves(current_position):
        possible_moves = []
        move_set = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                    (2, 1), (2, -1), (-2, 1), (-2, -1)] # Moves of knight
        # Check if move result in a position inside the chessboard
        for move in move_set:
            new_x = current_position[0] + move[0]
            new_y = current_position[1] + move[1]
            if(new_x >= N or new_y >= N or new_x < 0 or new_y < 0):
                continue
            else:
                possible_moves.append((new_x,new_y))
                
        return possible_moves
    
    # Generate a list of all possible destination not previous visited from
    # a given position ranked after the heuristic Warnsdorff's rule
    # which rank destinations with fewest possible new move the highest
    # Input: current_position Position of knight
    # Output: List of all possible not visited location to move in one step
    # ranked after Warnsdorff's rule
    def heuristics(current_position):
        possible_moves = gen_possible_moves(current_position)
        not_visited = []
        
        for move in possible_moves:
            # Check if locations allready used
            if (board[move[0]][move[1]] == 0):
                not_visited.append(move)
                
        # Rank moves
        destination_scores = []
        for destination_option in not_visited:
            score = [destination_option, 0]
            moves = gen_possible_moves(destination_option)
            for m in moves:
                if board[m[0]][m[1]] == 0:
                    score[1] += 1
            destination_scores.append(score)
            
        sorted_scores = sorted(destination_scores, key = lambda s : s[1])
        sorted_destination = [s[0] for s in sorted_scores]
        
        return sorted_destination
   
    # Tour method adding current position to path, and marking the position
    # used on the chessboard
    # Input: level: number of chess squares current in path,
    # path: current path of the knight tour
    # current_pos: (x,y) for the newest starting point for the search
    # Output: list of position in the path if it exists
    def tour(level, path, current_pos):
        # Add current position to path and board
        board[current_pos[0]][current_pos[1]] = level
        path.append(current_pos)
        printl("Current: ", current_pos)
        # Check if all chess squares have been visited
        if level == (N*N):
            # If closed loop is choosen check if it is satisfied
            if closed_loop:
                if path[-1] in end_positions:
                    raise PathFound
                # If not try backtracking and continue
                else:
                    board[current_pos[0]][current_pos[1]] = 0
                    try:
                        path.pop()
                        path[-1]
                        printl("Not closed loop, going back to: ", path[-1])
                    except IndexError:
                        raise Exception("No closed path exists")
            else:
                raise PathFound
        # If not all chess squares have been visited use current position
        # and find possible next moves
        else:
            ranked_moves = heuristics(current_pos)
            for move in ranked_moves:
                tour(level+1, path, move)
            
            # If dead end remove current position and backtrack
            board[current_pos[0]][current_pos[1]] = 0
            try:
                path.pop()
                path[-1]
                printl("Backtracking to: ", path[-1])
            except IndexError:
                raise Exception("No path")
                
    # Start knights tour
    try:
        path = []
        # If closed loop solution create list for final check
        if closed_loop:
            end_positions = gen_possible_moves(initial_pos)
        tour(1,path,initial_pos)
    except PathFound:
        if closed_loop:
            printl("Readjust starting point back to original position")
            start = path.index(start_pos)
            path_from_start = path[start:]
            for x in path[0:start]:
                path_from_start.append(x)
            path = path_from_start
        return path

size = 10           
tour = KnightsTour(size,(2,0),True)
print(tour)

speed = 0.05
square_size = 50
if GUI_ON:
    pygame.init()
    dimensions = (square_size*size, square_size*size)
    model = Model(size, size, tour, square_size)
    view = View(model, dimensions, speed)
    view.animate_path()
    

                