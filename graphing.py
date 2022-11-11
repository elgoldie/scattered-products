
# data1&data2
'''
data1 = [1, 0.5, 0.5, 0.125, 0.0625]
data2 = [0, 0, 0, 0, 0]
scaling_factor = 30
'''
def dataReduction(data1,data2,scaling_factor=10):

    #making list of tuples
    data_tuples = []
    for i in range(len(data1)):
        data_tuple = (data1[i],data2[i])
        data_tuples.append(data_tuple)

    print(data_tuples)

    counted_data_tuples = []
    for i in data_tuples:
        count = data_tuples.count(i)
        counted_data_tuple = (i[0], i[1], count)
        counted_data_tuples.append(counted_data_tuple)
    print(counted_data_tuples)

    unique_data_tuples = []
    for i in counted_data_tuples:
        if i in unique_data_tuples:
            pass
        else:
            unique_data_tuples.append(i)
    print(unique_data_tuples)

    # Scaling of sizes and separation of dat
    x_vals = []
    y_vals = []
    sizes = []
    for i in unique_data_tuples:
        x_value = i[0]
        y_value = i[1]
        size = i[2]*scaling_factor
        x_vals.append(x_value)
        y_vals.append(y_value)
        sizes.append(size)
    
    return (x_vals,y_vals,sizes)
    
# plot graph
'''
plt.scatter(x_vals, y_vals, sizes)
plt.xscale('log')
plt.xlabel('Position of x_i')
plt.ylabel('N')
plt.show()
'''