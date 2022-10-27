from gekko import GEKKO
import numpy as np

lp = GEKKO()
#Defining Variables
N = int(input("N= "))

#Parameters -- have to do with granularity
a_const = 10
a = lp.Param(value=a_const) # distance between buckets on log scale
m_const = 300
m = lp.Param(value=m_const) # number of buckets overall

n = lp.Array(lp.Var,m_const,value=1,lb=0,ub=N, integer=True)

ylist = []
#constraint_list = []
for i in range(len(n)):
    ylist.append((-i/a))
    #constraint_list.append(2**(-i/a))
y = np.array(ylist)
#constraint = np.array(constraint_list)

#initial values
"""
x1.value = 0.25
x2.value = 0.25
x3.value = 0.25
x4.value = 0.25
"""
#Constraints

A_rows = []

for j in range(m_const):
    row_list = []
    for i in range(m_const):
        if j-a_const <= i <= j:
            row_list.append(2**y[i])
        else:
            row_list.append(0)
    row = np.array(row_list)
    A_rows.append(row)

A = np.array(A_rows)




An = np.dot(A,n)
#lp.Equation(np.dot(n,constraint)<=1)
for i in range(m_const):
    lp.Equation(An[i] <= 1)
lp.Equation(np.sum(n)==N)

#Objective Function
lp.Maximize(np.dot(n,y))

#Set global options
lp.options.IMODE = 3 #steady state optimization

#Solve simulation
lp.solve(disp=True)

#Results
print('')
print('Results')
for i in range(len(n)):
    print("n_"+str(i)+"="+str(int(n[i].value[0])))

#print(A)
