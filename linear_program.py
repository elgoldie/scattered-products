from gekko import GEKKO
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
import graphing
x_list = []
y_list = []
ticks_list = []
for N in range(33,34):
    #if N % 10 == 0:
    ticks_list.append(N)
    lp = GEKKO()
    #Defining Variables
    epsilon = np.finfo('float').eps
    #Parameters -- have to do with granularity
    a_const = 10
    a = lp.Param(value=a_const) # distance between buckets on log scale
    m_const = 100
    m = lp.Param(value=m_const) # number of buckets overall
    print("N="+str(N))
    n = lp.Array(lp.Var,m_const,value=1,lb=0,ub=N, integer=True)

    ylist = []
    #constraint_list = []
    for i in range(len(n)):
        ylist.append((-i/a_const))
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
            if j-a_const < i <= j:
                row_list.append(2**y[i])
            else:
                row_list.append(0)
        row = np.array(row_list)
        A_rows.append(row)

    A = np.array(A_rows)
    #A = scipy.sparse.csr_matrix(A_rows, shape=(m_const,m_const))
    #print(A)
    #print(n[0])
    #print(type(n))
    #print(type(A))



    An = A.dot(n)
    #lp.Equation(np.dot(n,constraint)<=1)
    for i in range(m_const):
        lp.Equation(An[i] <= 1)
    lp.Equation(np.sum(n)==N)

    #Objective Function
    lp.Maximize(np.dot(n,y))

    #Set global options
    lp.options.IMODE = 3 #steady state optimization
    lp.options.SOLVER = 1 #1 is APOPT, 3 is Integer Point
    #lp.solver_options = ['minlp_max_iter_with_int_sol 500','minlp_maximum_iterations 600']


    # begin timing
    start_time = datetime.now()
    #Solve simulation
    try:
        lp.solve(disp=True,debug=True)

        #Results
        iterations = lp.options.ITERATIONS
        solvetime = lp.options.SOLVETIME
        print("Iterations: "+str(iterations))
        non_emptyPoints = {}
        non_emptyPoints_export = {}
        product = 1
        f = open("results_general.txt","a")
        print('')
        print('Results')
        f.write("N="+str(N))
        f.write("\n")
        for i in range(len(n)):
            if round(n[i].value[0]) != 0:
                print('\033[96m \033[1m'+"n_"+str(i)+"="+str(round(n[i].value[0]))+"|x="+str(2**(-i/a_const))+" | "+str(n[i].value[0])+'\033[0m')
                non_emptyPoints["n_"+str(i)] = round(n[i].value[0])
                non_emptyPoints_export[i] = n[i].value[0]
                f.write("n_"+str(i)+"="+str(round(n[i].value[0]))+"|x="+str(2**(-i/a_const))+" | "+str(n[i].value[0]))
                f.write("\n")
                for j in range(round(n[i].value[0])):
                    product = np.multiply(product, 2**(-i/a_const))
            #else:
                #print("n_"+str(i)+"="+str(round(n[i].value[0]))+"|x="+str(2**(-i/a_const)))


        print(non_emptyPoints)
        print(non_emptyPoints_export)
        print(product)
        f.write("Product="+str(product))
        f.write("\n")
        end_time = datetime.now()
        Duration = 'Duration: {}'.format(end_time - start_time)
        print(Duration)
        f.write(Duration)
        f.write("\n")
        f.write("Solvetime (s)="+str(solvetime))
        f.write("\n")
        f.write("Iterations: "+str(iterations))
        f.write("\n")
        f.write("===============")
        f.write("\n")
        f.close()

        # Plotting
        for i in range(len(n)):
            count = round(n[i].value[0])
            x_value = 2**(-i/a_const)
            y_value = N
            for i in range(count):
                x_list.append(x_value)
                y_list.append(y_value)

            


    except:
        
        non_emptyPoints = {}
        non_emptyPoints_export = {}
        product = 1
        f = open("results_general.txt","a")
        print('')
        print('Results')
        f.write("N="+str(N))
        f.write("\n")
        f.write("Max Iterations Reached")
        f.write("\n")
        end_time = datetime.now()
        Duration = 'Duration: {}'.format(end_time - start_time)
        print(Duration)
        f.write(Duration)
        f.write("\n")
        f.write("===============")
        f.write("\n")
        f.close()

x_vals, y_vals, sizes = graphing.dataReduction(x_list,y_list,10)

plt.scatter(x_vals, y_vals, sizes)
plt.xscale('log')
plt.yticks(ticks_list)
plt.xlabel('Position of x_i')
plt.ylabel('N')
plt.show()