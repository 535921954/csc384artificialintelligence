from BayesianNetwork import *
import copy
import itertools

##Implement all of the following functions

## Do not modify any of the objects passed in as parameters!
## Create a new Factor object to return when performing factor operations



'''
multiply_factors(factors)

Parameters :
              factors : a list of factors to multiply
Return:
              a new factor that is the product of the factors in "factors"
'''
def multiply_factors(factors):
    if len(factors) == 1:
        return factors[0]
        
    factor1 = factors[0]
  
    for i in range(1,len(factors)):
        factor2 = factors[i]
        factor1 = multiply_two_factors(factor1, factor2)
    
    return factor1

def non_duplicate_vars_index(factor1, factor2):
    non_duplicate_vars_index = []
    
    scope1 = factor1.get_scope()
    scope2 = factor2.get_scope()
    for var_index  in range(len(scope2)):
        var = scope2[var_index]
        if var not in scope1:
            non_duplicate_vars_index.append(var_index)
    return non_duplicate_vars_index
    

def get_union_vars(factor1, factor2):
    unique_vars_index = non_duplicate_vars_index(factor1, factor2)
    union_vars = factor1.get_scope()[:]
    for i in unique_vars_index:
        union_vars.append(factor2.get_scope()[i])
    return union_vars

def get_assignment2(factor1, factor2, assignment1, assignment):
    scope1 = factor1.get_scope()
    scope2 = factor2.get_scope()
    assignment2 = []
    replacement_index = 0
    for i in range(len(scope2)):
        var = scope2[i]
        if var not in scope1:
            assignment2.append(assignment[replacement_index+len(assignment1)])
            replacement_index += 1
        else:
            index = scope1.index(var)
            assignment2.append(assignment[index])
    return assignment2
            
    
    
def multiply_two_factors(factor1, factor2):
    
    # todo consider empty case

    if (len(factor1.get_scope()) == 0 and len(factor2.get_scope()) == 0):
        new_factor = Factor('{}*{}'.format(factor1.name, factor2.name), [])
        new_factor.add_value_at_assignment(factor1.get_value([])*factor2.get_value([]), [])
        return new_factor
    
    
    union_vars = get_union_vars(factor1, factor2)
    new_factor = Factor('{}*{}'.format(factor1.name, factor2.name), union_vars)    
        
    
    for assignment in new_factor.get_assignment_iterator():
        assignment1 = assignment[:len(factor1.get_scope())]
        assignment2 = get_assignment2(factor1, factor2, assignment1, assignment)
        if (len(factor1.get_scope()) == 0):
            factor1_value = factor1.get_value([])
        else:
            factor1_value = factor1.get_value(assignment1)
        if(len(factor2.get_scope()) == 0):
            facor2_value = factor2_get_value([])
        else:
            factor2_value = factor2.get_value(assignment2)
        product = factor1_value * factor2_value
        new_factor.add_value_at_assignment(product, assignment)
        
    return new_factor  
            
    
        



'''
restrict_factor(factor, variable, value):

Parameters :
              factor : the factor to restrict
              variable : the variable to restrict "factor" on
              value : the value to restrict to
Return:
              A new factor that is the restriction of "factor" by
              "variable"="value"
      
              If "factor" has only one variable its restriction yields a 
              constant factor
'''
def restrict_factor(factor, variable, value):
    if variable not in factor.get_scope():
        new_factor = factor
        return new_factor
    
    new_vars = factor.get_scope()
    
    var_dom_list = []
    v_index = 0
    for i, val in enumerate(factor.get_scope()):
        if val == variable:
            var_dom_list.append([value])
            v_index += i
        else:
            var_dom_list.append(val.domain())
    all_comb = itertools.product(*var_dom_list) #check what iter tools does.
    list_all_comb = list(all_comb)
    new_vars.pop(v_index)
    new_factor = Factor("r-{}".format(factor.name), new_vars)

    for cc in list_all_comb:
        ccl = list(cc)
        new_prob = factor.get_value(ccl)
        ccl.pop(v_index)
        ccl.append(new_prob)
        new_factor.add_values([ccl])
    return new_factor    

    
'''    
sum_out_variable(factor, variable)

Parameters :
              factor : the factor to sum out "variable" on
              variable : the variable to sum out
Return:
              A new factor that is "factor" summed out over "variable"
'''
def sum_out_variable(factor, variable):
    new_vars = factor.get_scope()
    for i, v in enumerate(factor.get_scope()):
        if v == variable:
            new_vars.pop(i)
    
        # restricted_factors_list = []
        # for val in var.domain():
        #     restricted_factors_list.append(restrict_factor(f, var, val), val)
    
    new_factor = Factor("s-{},{}".format(factor.name, variable.name), new_vars)
    
    var_dom_list = [v.domain() for v in new_vars]
    all_comb = itertools.product(*var_dom_list)
    list_all_comb = list(all_comb)
    
    for cur_comb in list_all_comb:
        sum_tot = 0
        for rval in variable.domain():
            for j, a_val in enumerate(cur_comb):
                new_vars[j].set_assignment(a_val)
            variable.set_assignment(rval)
            cur_value = factor.get_value_at_current_assignments()
            sum_tot += cur_value
        new_factor.add_value_at_current_assignment(sum_tot)

    return new_factor   


    
'''
VariableElimination(net, queryVar, evidenceVars)

 Parameters :
              net: a BayesianNetwork object
              queryVar: a Variable object
                        (the variable whose distribution we want to compute)
              evidenceVars: a list of Variable objects.
                            Each of these variables should have evidence set
                            to a particular value from its domain using
                            the set_evidence function. 

 Return:
         A distribution over the values of QueryVar
 Format:  A list of numbers, one for each value in QueryVar's Domain
         -The distribution should be normalized.
         -The i'th number is the probability that QueryVar is equal to its
          i'th value given the setting of the evidence
 Example:

 QueryVar = A with Dom[A] = ['a', 'b', 'c'], EvidenceVars = [B, C]
 prior function calls: B.set_evidence(1) and C.set_evidence('c')

 VE returns:  a list of three numbers. E.g. [0.5, 0.24, 0.26]

 These numbers would mean that Pr(A='a'|B=1, C='c') = 0.5
                               Pr(A='a'|B=1, C='c') = 0.24
                               Pr(A='a'|B=1, C='c') = 0.26
'''       
def VariableElimination(net, queryVar, evidenceVars):

    factors = []

    for factor in net.factors():
        for e in evidenceVars:
            if e in factor.get_scope():
                factor = restrict_factor(factor, e, e.get_evidence())
        factors.append(factor)

    hiddens = min_fill_ordering(factors, queryVar)
    for var in hiddens:
        var_factors = []
        for fac in factors:
            if var in fac.get_scope():
                var_factors.append(fac)
        for f in var_factors:
            factors.remove(f)
        mulfi = multiply_factors(var_factors)
        factors.append(sum_out_variable(mulfi, z))

    new_factor = multiply_factors(factors)
    qv_dom = queryVar.domain()
    qv_dist = []
    p_sum = 0
    for i, d in enumerate(qv_dom):
        new_prob = new_factor.get_value([d])
        qv_dist.append(new_prob)
        p_sum += new_prob

    if p_sum > 0:
        npr = [fp / p_sum for fp in qv_dist]
    else:
        npr = [float('inf') for fip in qv_dist]
    return npr