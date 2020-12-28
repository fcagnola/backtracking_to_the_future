import timeit
# setup is a multi-line string that includes the code that needs to be run just once (like the import functions)
#       and the definition of the algorithm
# statement is the code that needs to be run X times, so the lines that call the algorithm (or algorithms)
# number is the number of times the statement needs to be run. If not specificed, it will be run 1000 times

def singleevaluator(setup, statement, number=1000):
    a = timeit.timeit(setup=setup, stmt= statement, number=number)
    return a



# listoffunctions is the list of the function names you want to compare
# setup is a string that contains all the definitions and import of all the functions
# listofstatements is a list that contains a statement for each function
# number is the number of times the statements needs to be run. If not specified, it will be run 1000 times
# IMPORTANT: THE ORDER IN WHICH YOU PUT YOUR FUNCTIONS, SETUPS AND STATEMENTS MATTER: the first function in the list
# must match with the first statement in your list
# That also means that len(listofffunctions)and len(listofstatements) must be equal


def multipleniceevaluator(listoffunctions, setup, listofstatements, number=1000):
    if len(listoffunctions) == len(listofstatements):
       listofextimes = []
       for el in listoffunctions:
           time = singleevaluator(setup, listofstatements[listoffunctions.index(el)], number)
           listofextimes.append(time)
           print("The execution time of function " + el + " is " + str(time))
       print("The most efficient function is " + str(listoffunctions[listofextimes.index(min(listofextimes))]) +
             " that runs in " + str(min(listofextimes)) + " seconds.")
       print("The least efficient function is " + str(listoffunctions[listofextimes.index(max(listofextimes))]) +
             " that runs in " + str(max(listofextimes)) + " seconds.")
    else:
        print("Invalid input, the length of the lists you have put as input is different")











credits = ''' the algorithm takes inspiration from
the functions described here: https://www.studytonight.com/post/calculate-time-taken-by-a-program-to-execute-in-python#'''