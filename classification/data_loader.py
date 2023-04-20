import os
import re
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

'''
This code converts the given CNF clauses to a format that will be useful for constructing the graph

Example of files' format:

--8 rows of metadata--
1 -18 3 0
6 7 -9 0
...
%
0
\n

where each line is a clause that has 3 variables (or their negation if minus(-) is used) and the 0 that corresponds to
the AND operator. The number of row is the number of clauses .
'''


def dataset_processing():

    print("Start the processing...\n")

    # create columns of dataset
    dictionary = {"numberOfVariables": [],
                  "numberOfClauses": [],
                  "variablesSymb": [],
                  "variablesNum": [],
                  "edges": [],
                  "edgeAttr": [],
                  "label": []}

    # create dataframe
    df = pd.DataFrame(dictionary)

    directory = "../dataset"

    satisfiable_num = 0
    unsatisfiable_num = 0

    for dirName in os.listdir(directory):
        curr_dir = directory + "/" + dirName
        if os.path.isdir(curr_dir):
            # the directory's name stored information about its contents :[UF/UUF<#variables>.<#clauses>.<#cnfs>]
            dir_info = dirName.split(".")
            # number of variables in each data-file regarding the folder
            number_of_variables = int((re.findall(r'\d+', dir_info[0]))[0])
            # number of clauses in each
            # data-file regarding the folder
            number_of_clauses = int(dir_info[1])
            # get label of these data : UUF means UNSAT and UF means SAT
            y = 0 if dir_info[0][:3] == "UUF" else 1

            # we want to see the balancing of the dataset
            if y == 1:
                satisfiable_num += int(dir_info[2])
            else:
                unsatisfiable_num += int(dir_info[2])

            # Nodes:
            #     0 - numberOfVariables- 1                                      : x_1 - x_n
            #     numberOfVariables - 2*numberOfVariables                       : ~x_1 - ~x_n
            #     2*numberOfVariables - 2*numberOfVariables + numberOfClauses   : c_1 - c_m

            nodes = [i for i in range(0, 2 * number_of_variables + number_of_clauses)]
            # node with symbolic values
            '''
            node_values = ["x" + str(i + 1) for i in range(0, numberOfVariables)]
            node_values += ["-x" + str(i + 1) for i in range(0, numberOfVariables)]
            node_values += ["c" + str(i + 1) for i in range(0, numberOfClauses)]
            '''
            '''
            node_values = [i+1 for i in range(0, numberOfVariables)]
            node_values += [-(i+1) for i in range(0, numberOfVariables)]
            node_values += [numberOfVariables for i in range(0, numberOfClauses)]
            '''

            node_values = [[np.random.uniform()] for _ in range(0, 2 * number_of_variables + number_of_clauses)]

            for fileName in os.listdir(curr_dir):
                f = open(curr_dir + "/" + fileName, "r")
                clauses = f.readlines()[8:]
                clauses = [line.strip() for line in clauses]  # remove '\n' from the end and '' from the start
                clauses = [line[:-2] for line in clauses]     # keep only the corresponding variables
                clauses = [line for line in clauses if line != '']  # keep only the lines that correspond to a clause

                '''
                if len(clauses) != numberOfClauses:
                    # if the lines(clauses) that we processed are not the correct number(), raise Exception
                    raise Exception("Something went wrong with the line processing")
                '''

                # edges
                edges_1 = []
                edges_2 = []

                # compute edge attributes as x_i -> ~x_i are
                # connected via a different edge than c_j and x_i
                edge_attr = []

                # make the edges from x_i -> ~x_i and ~x_i -> x_i
                for i in range(number_of_variables):

                    temp = [i + number_of_variables]
                    edges_1 += [i]
                    edges_1 += temp
                    edges_2 += temp
                    edges_2 += [i]

                    # first characteristic is :  connection between x_i and ~x_i
                    # second characteristic is :  connection between c_j and x_i
                    edge_attr += [[1, 0]]
                    '''
                    # third characteristic is :  connection between c_j and c_k
                    edgeAttr += [[1,0,0]]
                    '''

                # make the edges from corresponding c_j -> x_i (NOW VICE VERSA)
                count = 0
                for clause in clauses:
                    clause_vars = clause.split(" ")
                    clause_vars = [int(var) for var in clause_vars]
                    # create the corresponding edges
                    for xi in clause_vars:
                        temp = [xi-1] if xi > 0 else [abs(xi)-1+number_of_variables]
                        edges_1 += [count + 2*number_of_variables]
                        edges_1 += temp
                        edges_2 += temp
                        edges_2 += [count + 2*number_of_variables]

                        edge_attr += [[0, 1]]

                    count += 1
                '''
                # make the edges from c_j -> c_k
                for i in range(numberOfClauses-1):
                    clausesPos = 2*numberOfVariables+i
    
                    #temp = [clausesPos+1 for _ in range(0,numberOfClauses-i-1)]
                    for j in range(1, numberOfClauses - i):
                        edges_1 += [clausesPos]
                        edges_1 += [clausesPos+j]
    
                        edges_2 += [clausesPos+j]
                        edges_2 += [clausesPos]
    
                        edgeAttr += [[0, 0, 1]]
                '''
                '''
                totalNumOfEdges = 3*numberOfClauses +
                if len(edgeAttr) != numberOfClauses:
                    # if the lines(clauses) that we processed are not the correct number(), raise Exception
                    raise Exception("Something went wrong with the line processing")
                '''
                '''
                if fileName == "uf4.cnf":
                    print(nodes)
                    print(node_values)
                    print(clauses)
                    print(edges_1)
                    print(edges_2)
                '''

                f.close()

                # insert new row in dataframe :
                # "numberOfVariables","numberOfClauses", "variablesSymb", "variablesNum", "edges", "edgeAttr","label"
                df.loc[len(df)] = [number_of_variables, number_of_clauses,
                                   node_values, nodes, [edges_1, edges_2],
                                   [edge_attr, edge_attr], [y]]

    print(f'Satisfiable CNFs   : {satisfiable_num}')
    print(f'Unsatisfiable CNFs : {unsatisfiable_num}\n')

    sat_ratio = satisfiable_num/(satisfiable_num+unsatisfiable_num)

    print(f'Ratio of SAT   : {sat_ratio:.4f}')
    print(f'Ratio of UNSAT : {1.0-sat_ratio:.4f}')

    # store dataset in format that supports long lists
    store = pd.HDFStore('store.h5')
    store['df'] = df
    store.close()

    print("\nProcessing completed.")

    # return this for later purposes
    return unsatisfiable_num/satisfiable_num