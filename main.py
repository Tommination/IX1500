from itertools import permutations
from math import comb
start = (0,3)
end = (7,2)


def calculate_number_Ls(start_point,end_point): #Calculates the number of L-moves needed to move between two points
    total_moves = end_point[0] - start_point[0]  # total number of moves betwwen two points (x-value difference)
    vertical_movement = end_point[1] - start_point[1]  # (y-value difference, needed to figure out how many moves of which kind)
    no_Ls = int(((total_moves + vertical_movement) / 2) - vertical_movement)  # calculates number of L-moves given x and y differences.
    return no_Ls,total_moves


def produce_basic_path(start_point,end_point): # Creates a string for a path between two points, all L-moves and then all U_moves
    no_Ls = calculate_number_Ls(start_point,end_point)[0]  # number of L-moves
    total_moves = calculate_number_Ls(start_point,end_point)[1]  # total number of neede moves
    basic_path_string = ''
    for i in range(0,total_moves):  # Fills out a string given an amount of moves and amount that should be L-type.
        if i < no_Ls:
            basic_path_string = basic_path_string + 'L'
        else:
            basic_path_string = basic_path_string + 'U' #if the number of L-moves has been reached the rest are U.
    return basic_path_string

def invert_end(end_point): #Used when finding paths that cross x-axis
    return(end_point[0],-end_point[1]) #Returns end-point with y-value negated


def non_zero_path_count(start_point,end_point):  #finds number of paths between two points not crossing zero
    no_Ls_no_restriction = calculate_number_Ls(start_point, end_point)[0]  # L-moves needed for any path between points
    total_moves = calculate_number_Ls(start_point, end_point)[1]
    total_paths = comb(total_moves,no_Ls_no_restriction) # Finds number of paths by binomial coefficient between moves and needed L's
    '''Finds number of L moves needed to get to the "inverted" end point, which gives the same number of paths as those that reach 
    a given endpoint and touch zero on the way, explained in the report'''
    no_Ls_thru_zero = calculate_number_Ls(start_point, invert_end(end_point))[0]
    no_paths_thru_zero = comb(total_moves,no_Ls_thru_zero) # Number of paths that cross zero
    return (total_paths - no_paths_thru_zero),total_paths

ways_no_restrictions = [''.join(p) for p in permutations(produce_basic_path(start,end))] # finds all possible permutations (is a lot)
ways_no_restrictions = list(dict.fromkeys(ways_no_restrictions)) # removes duplicates
print("The number of possible paths between (0,3) and (7,2) is: " + str(len(ways_no_restrictions)))
print("All possible paths between (0,3) and (7,2) are: " + str(ways_no_restrictions) + '\n')


inverted_end = invert_end(end)
ways_thru_zero_noninverted = [''.join(p) for p in permutations(produce_basic_path(start,inverted_end))]
ways_thru_zero_noninverted = list(dict.fromkeys(ways_thru_zero_noninverted))  # List of all the paths that go to the "inverted" endpoint.
ways_thru_zero_inverted = []  # list that will be filled with the "corrected" paths

'''This whole for loop checks when the paths to the "inverted" endpoint of a goal touch zero, and then inverts all the moves from there.
meaning the endpoint ends up being the correct one.

Used to get the correct prints for (b) and removing them from (c) prints'''
for i in range(0, len(ways_thru_zero_noninverted)): # All paths that go to the negative of a coordinate
    n = start[1]  # Starting point y value
    for j in range(0, len(ways_thru_zero_noninverted[i])):
        if n == 0:  # When the path has touched zero, invert the rest of the moves
            ways_thru_zero_inverted.append(ways_thru_zero_noninverted[i]) # Adds an element to the list of "corrected" paths
            while(j < len(ways_thru_zero_noninverted[i])):  # While loop for the rest of the given path
                if ways_thru_zero_noninverted[i][j] == 'L': # If the letter is L, change it to be U in the "corrected" list
                    list_2_change = list(ways_thru_zero_inverted[-1])
                    list_2_change[j]  = 'U'
                    string_path_inverted = "".join(list_2_change)
                    ways_thru_zero_inverted[-1] = string_path_inverted
                    j = j + 1
                else: # Same as above but for U.
                    list_2_change = list(ways_thru_zero_inverted[-1])
                    ways_thru_zero_inverted[-1] = list_2_change
                    list_2_change[j] = 'L'
                    string_path_inverted = "".join(list_2_change)
                    ways_thru_zero_inverted[-1] = string_path_inverted
                    j = j + 1
            break
        else: # if path hasn't touched zero update the y-position, to see when it does.
            if ways_thru_zero_noninverted[i][j] == 'L':
                n = n - 1
            if ways_thru_zero_noninverted[i][j] == 'U':
                n = n + 1

print("The number of possible paths between (0,3) and (7,2) touching or crossing the x-axis is: " + str(len(ways_thru_zero_inverted)))
print("Those paths are: " + str(ways_thru_zero_inverted) + '\n')

paths_no_zero = list(set(ways_no_restrictions)-set(ways_thru_zero_inverted))
print("The number of possible paths between (0,3) and (7,2) NOT touching or crossing the x-axis is: " + str(len(paths_no_zero)))
print("Those paths are: " + str(paths_no_zero) + '\n')

print("The number of possible paths between (7,6) and (20,5) NOT touching or crossing the x-axis is: " + str(non_zero_path_count((7,6),(20,5))[0]) + '\n')

def ballot_possibilities_A_first_draw(A,B):
    return comb(((A+B)-1),(A-1))  # All possible draws assuming A drawn in first position

def A_strictly_ahead_possibilities(A,B):
    count_end = ((A+B),(A-B))  # The end coordinates after all votes have been counted
    strictly_ahead = non_zero_path_count((1,1),count_end)  # how many paths don't touch zero
    return strictly_ahead[0]
def A_strictly_ahead_likelihood(A,B):
    all_draws = ballot_possibilities_A_first_draw(A,B)
    favorable_draws = A_strictly_ahead_possibilities(A,B)
    return (favorable_draws/all_draws)*(A/(A+B))

print("TASK 2:")
print("The number of draws in which A is striclty ahead is:" + str(A_strictly_ahead_possibilities(9,2)))
print("The likelihood of A being striclty ahead is:" + str(A_strictly_ahead_likelihood(9,2)))