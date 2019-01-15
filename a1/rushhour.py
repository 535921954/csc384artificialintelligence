#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add on ly standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
from copy import deepcopy
from search import *
from random import randint

##################################################
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################


class rushhour(StateSpace):
    def __init__(self, action, gval,goal_entrance,goal_direction, board_size, vehicle_list, parent):
#IMPLEMENT
        """Initialize a rushhour search state object."""
        
        
        super().__init__(action, gval, parent)
        self.board_size = board_size
        self.vehicle_list = vehicle_list
        self.goal_entrance = goal_entrance
        self.goal_direction = goal_direction
        
    def successors(self):
#IMPLEMENT
        
        '''Return list of rushhour objects that are the successors of the current object'''
        States = list()
        vehicles_copy = deepcopy(self.vehicle_list)
        index = 0
        next_loc = [0,0]
        for v in self.vehicle_list:
            if v[3] ==True:
                if v[1][0] + 1 > self.board_size[1]-1:
                    next_loc[0] = (v[1][0] + 1)%self.board_size[1]
                    next_loc[1] = v[1][1]
                if v[1][0] + 1 <= self.board_size[1]-1:
                    next_loc[0] = v[1][0] + 1
                    next_loc[1] = v[1][1]                        
                v_a = deepcopy(v)
                v_a[1] = (next_loc[0],next_loc[1]) 
                if avalible_tile(self, v_a):
                    v_after = deepcopy(vehicles_copy)
                    

                    name = v_after[index][0]
                    action = "move_vehicle"+ '('+name+','+'E)'
                    v_after[index][1] = (next_loc[0],next_loc[1])
                   
                    States.append(rushhour(action,self.gval+1,self.goal_entrance,self.goal_direction,self.board_size,v_after,self.parent))
                if v[1][0] -1 >= 0:
                    next_loc[0] = v[1][0] - 1
                    next_loc[1] = v[1][1]
                if v[1][0] -1 < 0:
                    next_loc[0] = v[1][0] - 1 + self.board_size[1]
                    next_loc[1] = v[1][1]                    
                v_a = deepcopy(v)
                v_a[1] = (next_loc[0],next_loc[1])
                if avalible_tile(self, v_a):
                    v_after = deepcopy(vehicles_copy)
                    

                    name = v_after[index][0]
                    action = "move_vehicle"+ '('+name+','+'W)'
                    v_after[index][1] = (next_loc[0],next_loc[1])
           
                    States.append(rushhour(action,self.gval+1,self.goal_entrance,self.goal_direction,self.board_size,v_after,self.parent))
            
            if v[3] == False:
                if v[1][1] + 1 > self.board_size[0] - 1:
                    next_loc[1] = (v[1][1] + 1)%self.board_size[0]
                    next_loc[0] = v[1][0]
                if v[1][1] + 1 <= self.board_size[0] - 1:
                    next_loc[1] = v[1][1] + 1
                    next_loc[0] = v[1][0]                    
                    
                v_a = deepcopy(v)
                v_a[1] = (next_loc[0],next_loc[1]) 
                if avalible_tile(self, v_a):
                    v_after = deepcopy(vehicles_copy)
                    
                    #print(v_after)
                    name = v_after[index][0]
                    action = "move_vehicle"+ '('+name+','+'N)'
                    v_after[index][1] = (next_loc[0],next_loc[1])
                    #print(index)
                    #print(v_after)
                    States.append(rushhour(action,self.gval+1,self.goal_entrance,self.goal_direction,self.board_size,v_after,self.parent))
                    
                if v[1][1] - 1 >= 0:
                    next_loc[0] = v[1][0]
                    next_loc[1] = v[1][1] - 1
                if v[1][1] - 1 < 0:
                    next_loc[0] = v[1][0]
                    next_loc[1] = v[1][1] -1 + self.board_size[0]
                v_a = deepcopy(v)
                v_a[1] = (next_loc[0],next_loc[1]) 
                if avalible_tile(self, v_a):
                    v_after = deepcopy(vehicles_copy)
                    

                    name = v_after[index][0]
                    action = "move_vehicle"+ '('+name+','+'S)'
                    v_after[index][1] = (next_loc[0],next_loc[1])

                    States.append(rushhour(action,self.gval+1,self.goal_entrance,self.goal_direction,self.board_size,v_after,self.parent))
            index += 1 
            #print(index)
            #for s in States:
               # s.print_state()
        return States
                
                    
                
        

    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        vehicles_str = ""
        for v in self.vehicle_list:
            index = 1
            vehicles_str += str(index) + '.name:' + v[0] +',location:'+'('+ str(v[1][0]) +','+str(v[1][1])+',length:'+v[2]+',is_horzontal:'+v[3]+'is_goal:'+v[4]+';'
            index+=1
        return vehicles_str

    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
#IMPLEMENT
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the vehicle (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                       <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        return self.vehicle_list
        

    def get_board_properties(self):
        #IMPLEMENT
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return (self.board_size, self.goal_entrance, self.goal_direction)
#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
#IMPLEMENT
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
    for v in state.get_vehicle_statuses():
        if v[4] == True:
            if state.get_board_properties()[2] == 'W':
                if v[1][0] <= state.get_board_properties()[1][0]:
                    num_move1 = state.get_board_properties()[1][0] - v[1][0]
                    num_move2 = v[1][0] - state.get_board_properties()[1][0] +state.get_board_properties()[0][1]
                else:
                    num_move1 = v[1][0] - state.get_board_properties()[1][0]
                    num_move2 = state.get_board_properties()[1][0] - v[1][0] + state.get_board_properties()[0][1]                    
            if state.get_board_properties()[2] == 'E':
                if v[1][0]+v[2]-1 > state.get_board_properties()[1][0]:
                    num_move1 = v[1][0]+v[2]-1 - state.get_board_properties()[1][0]
                    num_move2 = state.get_board_properties()[1][0] - (v[1][0]+v[2]-1) + state.get_board_properties()[0][1]
                else:
                    num_move1 = state.get_board_properties()[1][0] - (v[1][0]+v[2]-1)
                    num_move2 = v[1][0]+v[2]-1 - state.get_board_properties()[1][0] +state.get_board_properties()[0][1]                    
                        
            if state.get_board_properties()[2] == 'N':
                if v[1][1] <= state.get_board_properties()[1][1]:
                    num_move1 = state.get_board_properties()[1][1] - v[1][1]
                    num_move2 = v[1][1] - state.get_board_properties()[1][1] +state.get_board_properties()[0][0]
                else:
                    num_move1 = v[1][1] - state.get_board_properties()[1][1]            
                    num_move2 = state.get_board_properties()[1][1] - v[1][1] + state.get_board_properties()[0][0]
            if state.get_board_properties()[2] == 'S':
                if v[1][1]+v[2]-1 <= state.get_board_properties()[1][1]:
                    num_move1 = state.get_board_properties()[1][1] - (v[1][1]+v[2]-1)
                    num_move2 = v[1][1]+v[2]-1 - state.get_board_properties()[1][1] +state.get_board_properties()[0][0]
                else:
                    num_move1 = v[1][1]+v[2]-1 - state.get_board_properties()[1][1]            
                    num_move2 = state.get_board_properties()[1][1] - (v[1][1]+v[2]-1) + state.get_board_properties()[0][0]                
    if num_move1 > num_move2:
        return num_move2
    else:
        return num_move1
def rushhour_goal_fn(state):
#IMPLEMENT
    '''Have we reached a goal state'''
    for v in state.vehicle_list:
        if v[4] == True:
            if state.get_board_properties()[2] == 'N' or state.get_board_properties()[2] == 'W':
                if v[1] == state.get_board_properties()[1]:
                    return True
            else:
                if state.get_board_properties()[2] == 'S':
                    if (v[1][0],v[1][1]+v[2]-1) == state.get_board_properties()[1]:
                        return True
                if state.get_board_properties()[2] == 'E':
                    if (v[1][0]+v[2]-1,v[1][1]) == state.get_board_properties()[1]:
                        return True
    return False


def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
#IMPLEMENT
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''
    s = rushhour('START',0,goal_entrance, goal_direction,board_size,vehicle_list,None)
    return s
########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_min_moves)

#helper
'''
def duplicate_l(alist):
    des = list()
    for v in alist:
        des.append(v)
    return des
'''
def avalible_tile(state, vehicle):
    (a,b) = vehicle[1]
    (x,y) = state.board_size
    a_t = a + vehicle[2] -1
    b_t = b + vehicle[2] -1
    tiles = list()
    for v in state.get_vehicle_statuses():
        if v[0] != vehicle[0]:
            tiles.append((v[1][0],v[1][1]))
            for num in range(v[2]):
                if v[3] == True:
                    if v[1][0] + num > state.get_board_properties()[0][1]-1:
                        tiles.append((((v[1][0]+num)%state.get_board_properties()[0][1]),v[1][1]))
                    else:
                        tiles.append((v[1][0]+num, v[1][1]))
                else:   
                    if v[1][1] + num > state.get_board_properties()[0][0]-1:
                        tiles.append((v[1][0],(v[1][1]+num)%state.get_board_properties()[0][0]))
                    else:
                        tiles.append((v[1][0],v[1][1]+num))
    if (a,b) in tiles:
        return False
    if (a_t,b_t) in tiles:
        return False
    return True

  
