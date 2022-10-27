import numpy as np
# 2 case
'''
complete_2 = False
base = 1
total = 1
n = 1
for i in range(5):
    for exponent in range(base):
        total /= base
        print("n="+str(n))
        print(total)
        n+=1

    #total_str += "(1/"+str(base)+"^"+str(exponent)+")"
    base = base*2
'''    

listOfTotals = []

def generalBase(base):
    print("Base="+str(base))
    total = 1
    n = 1
    totalList = []
    while n<189:
        for exponent in range(base):
            total /= base
            print("n="+str(n))
            print(total)
            totalList.append(total)
            n+=1
            if n > 189:
                break
        base = base*2
    return(totalList)



listOfTotals.append(generalBase(2))
listOfTotals.append(generalBase(3))
listOfTotals.append(generalBase(5))
listOfTotals.append(generalBase(7))
arrayOfTotals = np.array(listOfTotals)
arrayOfTotals = np.transpose(arrayOfTotals)
print(arrayOfTotals)
listofMax = np.argmax(arrayOfTotals,axis=1)
print(listofMax)
prettyList = []
n=0
for i in list(listofMax):
    n += 1
    if i == 0:
        prettyList.append(("n="+str(n),2))
    elif i == 1:
        prettyList.append(("n="+str(n),3))
    elif i == 2:
        prettyList.append(("n="+str(n),5))
    elif i == 3:
        prettyList.append(("n="+str(n),7))
print(prettyList)