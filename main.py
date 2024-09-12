from itertools import permutations
from math import comb
start = (0,3)
end = (7,2)


def calculate_number_Ls(start_point,end_point): #Calculates the number of L-moves needed to move between two points
    total_moves = end_point[0] - start_point[0]
    vertical_movement = end_point[1] - start_point[1]
    no_Ls = int(((total_moves + vertical_movement) / 2) - vertical_movement)
    return no_Ls,total_moves


def produce_basic_path(start_point,end_point): # Creates a string for a path between two points, all L-moves and then all U_moves
    no_Ls = calculate_number_Ls(start_point,end_point)[0]
    total_moves = calculate_number_Ls(start_point,end_point)[1]
    basic_path_string = ''
    for i in range(0,total_moves):
        if i < no_Ls:
            basic_path_string = basic_path_string + 'L'
        else:
            basic_path_string = basic_path_string + 'U'
    return basic_path_string

def invert_end(end_point): #Used when finding paths that cross x-axis
    return(end_point[0],-end_point[1])


def non_zero_path_count(start_point,end_point):
    no_Ls_no_restriction = calculate_number_Ls(start_point, end_point)[0]
    total_moves = calculate_number_Ls(start_point, end_point)[1]
    total_paths = comb(total_moves,no_Ls_no_restriction) # Finds number of paths by binomial coefficient between moves and needed L's
    no_Ls_thru_zero = calculate_number_Ls(start_point, invert_end(end_point))[0] # Finds number of L moves needed to get to the "inverted" end point
    no_paths_thru_zero = comb(total_moves,no_Ls_thru_zero) # Total number of paths that cross zero
    return (total_paths - no_paths_thru_zero),total_paths

ways_no_restrictions = [''.join(p) for p in permutations(produce_basic_path(start,end))] #finds all possible permutations
ways_no_restrictions = list(dict.fromkeys(ways_no_restrictions)) #removes duplicates
print(ways_no_restrictions)
print(len(ways_no_restrictions))

inverted_end = invert_end(end)
ways_thru_zero_noninverted = [''.join(p) for p in permutations(produce_basic_path(start,inverted_end))]
ways_thru_zero_noninverted = list(dict.fromkeys(ways_thru_zero_noninverted))
ways_thru_zero_inverted = []

'''This whole for loop checks when the paths to the "negative correspondent" of a goal touch zero, and then inverts all the moves from there.
Used to get the correct prints for (b) and removing them from (c) prints'''
for i in range(0, len(ways_thru_zero_noninverted)): # All paths that go to the negative of a coordinate
    n = start[1]  # Starting point y value
    for j in range(0, len(ways_thru_zero_noninverted[i])):
        if n == 0:
            ways_thru_zero_inverted.append(ways_thru_zero_noninverted[i])
            while(j < len(ways_thru_zero_noninverted[i])):
                if ways_thru_zero_noninverted[i][j] == 'L':
                    list_2_change = list(ways_thru_zero_inverted[-1])
                    list_2_change[j]  = 'U'
                    string_path_inverted = "".join(list_2_change)
                    ways_thru_zero_inverted[-1] = string_path_inverted
                    j = j + 1
                else:
                    list_2_change = list(ways_thru_zero_inverted[-1])
                    ways_thru_zero_inverted[-1] = list_2_change
                    list_2_change[j] = 'L'
                    string_path_inverted = "".join(list_2_change)
                    ways_thru_zero_inverted[-1] = string_path_inverted
                    j = j + 1
            break
        else:
            if ways_thru_zero_noninverted[i][j] == 'L':
                n = n - 1
            if ways_thru_zero_noninverted[i][j] == 'U':
                n = n + 1

print(ways_thru_zero_inverted)

paths_no_zero = list(set(ways_no_restrictions)-set(ways_thru_zero_inverted))
print(paths_no_zero)
print(len(paths_no_zero))
print(non_zero_path_count((7,6),(20,5))[0])

def ballot_possibilities_A_first_draw(A,B):
    return comb(((A+B)-1),(A-1))

def A_strictly_ahead_possibilities(A,B):
    count_end = ((A+B),(A-B))
    strictly_ahead = non_zero_path_count((1,1),count_end)
    return strictly_ahead[0]
def A_strictly_ahead_likelihood(A,B):
    all_draws = ballot_possibilities_A_first_draw(A,B)
    favorable_draws = A_strictly_ahead_possibilities(A,B)
    return (favorable_draws/all_draws)*(A/(A+B))
print(A_strictly_ahead_possibilities(9,2))
print(A_strictly_ahead_likelihood(9,2))
