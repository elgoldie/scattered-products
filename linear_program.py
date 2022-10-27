from gekko import GEKKO

m = GEKKO()
#Defining Variables
x1,x2,x3,x4 = [m.Var(lb=0, ub=1) for i in range(4)]




#initial values
x1.value = 0.25
x2.value = 0.25
x3.value = 0.25
x4.value = 0.25

#Constraints
m.Equation(x1+x2>=0.5)

#Objective Function
m.Maximize(x1*x2*x3*x4)

#Set global options
m.options.IMODE = 3 #steady state optimization

#Solve simulation
m.solve()

#Results
print('')
print('Results')
print('x1: ' + str(x1.value))
print('x2: ' + str(x2.value))
print('x3: ' + str(x3.value))
print('x4: ' + str(x4.value))