import itertools as it
import time

starttime = time.time()

# u_in = [1, 2, 3, 4]
# u_in = [7, 9, 2, 3]
u_in = [1, 6, 1, 8]
# u_in = [1, 4, 2, 3]
# u_in = [70, 7, 7, 7]
# u_in = [0, 0, 0, 0]

def clt(x, y, o):
    if (o == "+"):
        return (x + y)
    elif o == "-":
        return (x - y)
    elif o == "*":
        return (x * y)
    elif o == "/":
        if y == 0:
            return(0.00000001)
        else:
            return (x / y)

def clt4(a, b, c, d, o_list):
    results= []

    # order: ((a ? b) ? c) ? d
    # print(a, b, c, d, o_list)
    rst1 = clt(x=a, y=b, o=o_list[0])
    # print('clt1: {:} {:} {:} = {:}'.format(a, o_list[0], b, rst1))
    rst2 = clt(x=rst1, y=c, o=o_list[1])
    # print('clt2: {:} {:} {:} = {:}'.format(rst1, o_list[1], c, rst2))
    rst3 = clt(x=rst2, y=d, o=o_list[2])
    # print('clt3: {:} {:} {:} = {:}'.format(rst2, o_list[2], d, rst3))
    results.append(rst3)
    if rst3 == 24:
        pass
        # print("====0 fomular is (({:} {:} {:}) {:} {:}) {:} {:} = {:}".format(a, o_list[0], b, o_list[1], c, o_list[2], d, rst3))
 
    # order: (a ? (b ? c)) ? d
    rst1 = clt(x=b, y=c, o=o_list[1])
    rst2 = clt(x=a, y=rst1, o=o_list[0])
    rst3 = clt(x=rst2, y=d, o=o_list[2])
    if rst3 == 24:
        pass
        # print("====1 fomular is ({:} {:} ({:} {:} {:})) {:} {:} = {:}".format(a, o_list[0], b, o_list[1], c, o_list[2], d, rst3))
        
    results.append(rst3)

    # order: a ? ((b ? c) ? d)
    rst1 = clt(x=b, y=c, o=o_list[1])
    rst2 = clt(x=rst1, y=d, o=o_list[2])
    rst3 = clt(x=a, y=rst2, o=o_list[0])
    results.append(rst3)
    if rst3 == 24:
        pass
        #print("====2 fomular is {:} {:} (({:} {:} {:}) {:} {:}) = {:}".format(a, o_list[0], b, o_list[1], c, o_list[2], d, rst3))
        
 

    # order: (a ? b) ? (c ? d)
    rst1 = clt(x=a, y=b, o=o_list[0])
    rst2 = clt(x=c, y=d, o=o_list[2])
    rst3 = clt(x=rst1, y=rst2, o=o_list[1])
    results.append(rst3)
    if rst3 == 24:
        pass
        # print("====3 fomular is ({:} {:} {:}) {:} ({:} {:} {:}) = {:}".format(a, o_list[0], b, o_list[1], c, o_list[2], d, rst3))
 
    # order: a ? (b ? (c ? d))
    rst1 = clt(x=c, y=d, o=o_list[2])
    rst2 = clt(x=b, y=rst1, o=o_list[1])
    rst3 = clt(x=a, y=rst2, o=o_list[0])
    results.append(rst3)
    if rst3 == 24:
        pass
        # print("====3 fomular is ({:} {:} {:}) {:} ({:} {:} {:}) = {:}".format(a, o_list[0], b, o_list[1], c, o_list[2], d, rst3))
 
    return results


oper = ['-', '+', '*', '/']
rst = {}
for o in oper:
    pass
    # print(clt(x=u_in[0], y=u_in[1], o=o))

m = 0
for i in it.permutations(u_in, 4):
    m += 1
    # print("==", m, i,type(i))

m = 0
for i in oper:
    for j in oper:
        for k in oper:
            m += 1
            # print("==", m, i, j, k)



# rst_list = []
rst_dict = {}
for l in it.permutations(u_in, 4):
    o_list = []
    for i in oper:
        for j in oper:
            for k in oper:
                m += 1
                # o_list.append(i)
                # o_list.append(j)
                # o_list.append(k)
                o_list = [i, j, k]
                # print("==", m, i, j, k)
                rst = clt4(a=l[0], b=l[1], c=l[2], d=l[3], o_list= o_list )
                # order: ((a ? b) ? c) ? d
                # order: (a ? (b ? c)) ? d
                # order: a ? ((b ? c) ? d)
                # order: (a ? b) ? (c ? d)
                # order: a ? (b ? (c ? d))
                if rst[0] == 24:
                    fomula = '(({:} {:} {:}) {:} {:}) {:} {:} = {:}'.format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], int(rst[0]))
                    # rst_list.append(fomula)
                    if fomula not in rst_dict:
                        rst_dict[fomula] = 1
                if rst[1] == 24:
                    fomula = '({:} {:} ({:} {:} {:})) {:} {:} = {:}'.format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], int(rst[1]))
                    # rst_list.append(fomula)
                    if fomula not in rst_dict:
                        rst_dict[fomula] = 1

                if rst[2] == 24:
                    fomula = '{:} {:} (({:} {:} {:}) {:} {:}) = {:}'.format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], int(rst[2]))
                    # rst_list.append(fomula)
                    if fomula not in rst_dict:
                        rst_dict[fomula] = 1
                if rst[3] == 24:
                    fomula = '({:} {:} {:}) {:} ({:} {:} {:}) = {:}'.format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], int(rst[3]))
                    # rst_list.append(fomula)
                    if fomula not in rst_dict:
                        rst_dict[fomula] = 1
                if rst[4] == 24:
                    fomula = '{:} {:} ({:} {:} ({:} {:} {:})) = {:}'.format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], int(rst[4]))
                    # rst_list.append(fomula)
                    if fomula not in rst_dict:
                        rst_dict[fomula] = 1


                # if rst == 24:
                #     fomula = '(({:} {:} {:}) {:} {:}) {:} {:} = {:}'.format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], int(rst))
                #     rst_list.append(fomula)
                #     # print("==== {:} fomular is {:} {:} {:} {:} {:} {:} {:} = {:}".format(m, l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], rst))
    # if (rst == '24'): 
    #     print("fomular is {:} {:} {:} {:} {:} {:} {:} = {:}".format(l[0], o_list[0], l[1], o_list[1], l[2], o_list[2], l[3], rst))

for cnt, i in enumerate(rst_dict, start=1):
    print("Solutaion {:}: {:}".format(cnt, i))

elapsed_time = time.time() - starttime
print('Total {:} results find for input: {:} [Elapase time {:}] '.format(len(rst_dict.keys()), u_in, elapsed_time))
