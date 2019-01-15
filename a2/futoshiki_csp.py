#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

'''
Construct and return Futoshiki CSP models.
'''

from cspbase import *
import itertools

def futoshiki_csp_model_1(initial_futoshiki_board):
    '''Return a CSP object representing a Futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_1 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))


    The input board is specified as a list of n lists. Each of the n lists
    represents a row of the board. If a 0 is in the list it represents an empty
    cell. Otherwise if a number between 1--n is in the list then this
    represents a pre-set board position.

    Each list is of length 2n-1, with each space on the board being separated
    by the potential inequality constraints. '>' denotes that the previous
    space must be bigger than the next space; '<' denotes that the previous
    space must be smaller than the next; '.' denotes that there is no
    inequality constraint.

    E.g., the board

    -------------------
    | > |2| |9| | |6| |
    | |4| | | |1| | |8|
    | |7| <4|2| | | |3|
    |5| | | | | |3| | |
    | | |1| |6| |5| | |
    | | <3| | | | | |6|
    |1| | | |5|7| |4| |
    |6> | |9| < | |2| |
    | |2| | |8| <1| | |
    -------------------
    would be represented by the list of lists

    [[0,'>',0,'.',2,'.',0,'.',9,'.',0,'.',0,'.',6,'.',0],
     [0,'.',4,'.',0,'.',0,'.',0,'.',1,'.',0,'.',0,'.',8],
     [0,'.',7,'.',0,'<',4,'.',2,'.',0,'.',0,'.',0,'.',3],
     [5,'.',0,'.',0,'.',0,'.',0,'.',0,'.',3,'.',0,'.',0],
     [0,'.',0,'.',1,'.',0,'.',6,'.',0,'.',5,'.',0,'.',0],
     [0,'.',0,'<',3,'.',0,'.',0,'.',0,'.',0,'.',0,'.',6],
     [1,'.',0,'.',0,'.',0,'.',5,'.',7,'.',0,'.',4,'.',0],
     [6,'>',0,'.',0,'.',9,'.',0,'<',0,'.',0,'.',2,'.',0],
     [0,'.',2,'.',0,'.',0,'.',8,'.',0,'<',1,'.',0,'.',0]]


    This routine returns Model_1 which consists of a variable for each cell of
    the board, with domain equal to [1,...,n] if the board has a 0 at that
    position, and domain equal [i] if the board has a fixed number i at that
    cell.

    Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between all relevant
    variables (e.g., all pairs of variables in the same row, etc.).

    All of the constraints of Model_1 MUST BE binary constraints (i.e.,
    constraints whose scope includes two and only two variables).
    '''

#IMPLEMENT
    sat_tups = [[],[],[]]
    cons = []
    vars = []
    dom = []
    rows = []
    csp = CSP("futoshiki", vars)
    #domain unassign
    for i in range(1,len(initial_futoshiki_board) + 1):
        dom.append(i)
    
    #sattups
    for a in itertools.product(range(1,len(initial_futoshiki_board) + 1),
                               range(1,len(initial_futoshiki_board) + 1)):
            if a[0] != a[1]:
                sat_tups[0].append([a[0],a[1]])
            if a[0] > a[1]:
                sat_tups[1].append([a[0],a[1]])
            if a[0] < a[1]:
                sat_tups[2].append([a[0],a[1]])
    for aa in range(0, len(initial_futoshiki_board)):
        rows.append([])                 
        #assign variables
    for b in range(0, len(initial_futoshiki_board)):               
        for c in range(0, 2*len(initial_futoshiki_board)-1, 2):
            #equals 0
            if initial_futoshiki_board[b][c] == 0:
                var = Variable("Variable{}{}".format(b,c/2), dom)    
            #equals other value,give specific value to the variable
            else:
                var = Variable("Variable{}{}".format(b,c/2), [initial_futoshiki_board[b][c]])
            rows[b].append(var)
            csp.add_var(var)                
        vars.append(rows[b])
    
    for d in range(0,len(initial_futoshiki_board)):
       
        #just !=
    
        for e in range(0, len(initial_futoshiki_board)):
            for f in range(e+1,len(initial_futoshiki_board)):
                #row
                cr = Constraint("C{}{},{}{}".format(d,e,d,f), [vars[d][e], vars[d][f]])
                #column
                cc = Constraint("C{}{},{}{}".format(e,d,f,d), [vars[e][d], vars[f][d]])
                cr.add_satisfying_tuples(sat_tups[0])
                cc.add_satisfying_tuples(sat_tups[0])
                cons.append(cr)
                cons.append(cc)
                
        for g in range(1, 2*len(initial_futoshiki_board)-1, 2):
            v1_col = int((g-1)//2)
            v2_col = int((g+1)//2)
            
            if initial_futoshiki_board[d][g] == '>':
                cn = Constraint("C{}{},{}{}".format(d,v1_col,d,v2_col), [vars[d][v1_col], vars[d][v2_col]])
                cn.add_satisfying_tuples(sat_tups[1])
                cons.append(cn)
            elif initial_futoshiki_board[d][g] == '<':
                cn = Constraint("C({}{},{}{})".format(d,v1_col,d,v2_col), [vars[d][v1_col], vars[d][v2_col]])
                cn.add_satisfying_tuples(sat_tups[2])
                cons.append(cn)

    for con in cons:
        csp.add_constraint(con)    
    return csp, vars
                

   
                
    
        
        


##############################

def futoshiki_csp_model_2(initial_futoshiki_board):
    '''Return a CSP object representing a futoshiki CSP problem along with an
    array of variables for the problem. That is return

    futoshiki_csp, variable_array

    where futoshiki_csp is a csp representing futoshiki using model_2 and
    variable_array is a list of lists

    [ [  ]
      [  ]
      .
      .
      .
      [  ] ]

    such that variable_array[i][j] is the Variable (object) that you built to
    represent the value to be placed in cell i,j of the futoshiki board
    (indexed from (0,0) to (n-1,n-1))

    The input board takes the same input format (a list of n lists of size 2n-1
    specifying the board) as futoshiki_csp_model_1.

    The variables of Model_2 are the same as for Model_1: a variable for each
    cell of the board, with domain equal to [1,...,n] if the board has a 0 at
    that position, and domain equal [n] if the board has a fixed number i at
    that cell.

    However, Model_2 has different constraints. In particular, instead of
    binary non-equals constaints Model_2 has 2*n all-different constraints:
    all-different constraints for the variables in each of the n rows, and n
    columns. Each of these constraints is over n-variables (some of these
    variables will have a single value in their domain). Model_2 should create
    these all-different constraints between the relevant variables, and then
    separately generate the appropriate binary inequality constraints as
    required by the board. There should be j of these constraints, where j is
    the number of inequality symbols found on the board.  
    '''

#IMPLEMENT

    sat_tups = [[],[],[]]
    cons = []
    vars = []
    rows = []
    dom = []
    cols = []
    csp = CSP("futoshiki", vars)
    #domain unassign
    for i in range(1,len(initial_futoshiki_board) + 1):
        dom.append(i)
    
    #sattups
    for a in itertools.product(range(1,len(initial_futoshiki_board) + 1),
                               range(1,len(initial_futoshiki_board) + 1)):
    
        if a[0] > a[1]:
            sat_tups[1].append([a[0],a[1]])
        if a[0] < a[1]:
            sat_tups[2].append([a[0],a[1]])
    for p in itertools.permutations(range(1,len(initial_futoshiki_board) + 1)):
        sat_tups[0].append(p)
    
        #assign variables
    for aa in range(0, len(initial_futoshiki_board)):
            rows.append([])     
    for b in range(0, len(initial_futoshiki_board)):              
        for c in range(0, 2*len(initial_futoshiki_board)-1, 2):
            #equals 0
            if initial_futoshiki_board[b][c] == 0:
                var = Variable("Variable{}{}".format(b,c/2), dom)    
            #equals other value,give specific value to the variable
            else:
                var = Variable("Variable{}{}".format(b,c/2), [initial_futoshiki_board[b][c]])
            rows[b].append(var)
            csp.add_var(var)                
        vars.append(rows[b])
        
    for a in range(0, len(initial_futoshiki_board)):
        cols.append([])     
    
    for d in range(0,len(initial_futoshiki_board)):
        #just !=
        for e in range(0, len(initial_futoshiki_board)):
            cols[d].append(vars[e][d])
                #row
        cr = Constraint("Crow{}".format(d), vars[d])
                #column
                
        cc = Constraint("Ccol{}".format(e), cols[d])
        cr.add_satisfying_tuples(sat_tups[0])
        cc.add_satisfying_tuples(sat_tups[0])
        cons.append(cr)
        cons.append(cc)
                
        for g in range(1, 2*len(initial_futoshiki_board)-1, 2):
            v1_col = int((g-1)//2)
            v2_col = int((g+1)//2)
            
            if initial_futoshiki_board[d][g] == '>':
                cn = Constraint("C{}{},{}{}".format(d,v1_col,d,v2_col), [vars[d][v1_col], vars[d][v2_col]])
                cn.add_satisfying_tuples(sat_tups[1])
                cons.append(cn)
            elif initial_futoshiki_board[d][g] == '<':
                cn = Constraint("C({}{},{}{})".format(d,v1_col,d,v2_col), [vars[d][v1_col], vars[d][v2_col]])
                cn.add_satisfying_tuples(sat_tups[2])
                cons.append(cn)

    for con in cons:
        csp.add_constraint(con)    
    return csp, vars