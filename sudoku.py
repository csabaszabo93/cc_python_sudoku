import sys
import numpy
import os
import csv
from termcolor import colored
import time

sudoku_title =r"""
    
     ___         _       _        
    / __> _ _  _| | ___ | |__ _ _ 
    \__ \| | |/ . |/ . \| / /| | |
    <___/`___|\___|\___/|_\_\`___|
                              

 """


winner_giraffe = r"""
 
                                       ._ o o
                                       \_`-)|_
                                    ,""       \ 
                                  ,"  ## |   ಠ ಠ. 
                                ," ##   ,-\__    `.    
                              ,"       /     `--._;)   You won! 
                            ,"     ## /                
                          ,"   ##    /
 
 
                    """


loser_giraffe = r"""
 
                                       ._ o o
                                       \_`-)|_
                                    ,""       \ 
                                  ,"  ## |   ಠ ಠ. 
                                ," ##   ,-\__    `.    
                              ,"       /     `--._;)   Your solution is not correct. You lost!! 
                            ,"     ## /                
                          ,"   ##    /
 
 
                    """


valid_numbers = [1,2,3,4,5,6,7,8,9]

#This prints the ASCII art
def print_title(ascii):
    print(ascii)

#Loading the gameplay csv template and initializing that grid it into a new local list
def load_csv(filename):
    with open("{}.csv".format(filename), "r") as f:
        reader = list(csv.reader(f))
        for lst in reader:
            for i in range(0, len(lst), 1):
                lst[i] = int(lst[i])
        return reader

#This function is used to overwrite the original grid locally
def update_csv(filename, matrix):
    with open("{}.csv".format(filename), "w") as f:
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)

#Printing the local grid and coloring it. White = new numbers which were 0 in the original file
def print_sudoku(grid, level):
    board = load_csv("{}_puzzle".format(grid))
    orig_board = load_csv("{}_puzzle".format(level))
    print_board = []
    update_csv("gameplay_puzzle", board)
    print_title(sudoku_title)
    print("+" + "---+"*9)
    for r in range(0, len(board)):
        print_row = []
        for c in range(0, len(board[r])):
            if orig_board[r][c] != 0:
                print_row.append(colored(board[r][c], "cyan"))
            else:
                print_row.append(colored(board[r][c], "white"))
        print_board.append(print_row)
    for i, row in enumerate(print_board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != colored(0, "white") else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+"*9)
        else:
            print("+" + "   +"*9)

#Asking the player to add the row number
def user_row():
    row = input("Choose a row: ")
    if row.isdigit():
        if int(row) in valid_numbers:
            new_row = int(row)
            return new_row
        else:
            print("That's not a valid number!")
            return user_row()
    else:
       print("That's not a number!")
       return user_row()

#Asking the player to add the column number
def user_column():
    column = input("Choose a column: ")
    if column.isdigit():
        if int(column) in valid_numbers:
            new_column = int(column)
            return new_column
        else:
            print("That's not a valid number!")
            return user_column()
    else:
       print("That's not a number!")
       return user_column()

#Asking the player to add the number
def user_number():
    number = input("Add a number from 1 to 9: ")
    if number.isdigit():
        if int(number) in valid_numbers:
            new_number = int(number)
            return new_number
        else:
            print("That's not a valid number!")
            return user_number()
    else:
       print("That's not a number!")
       return user_number()

#Comparing the local gameplay grid to the original one
def check_in_orig_puzzle(row, column, grid):
    if int(load_csv(grid)[row][column]) != 0:
        return True
    else:
        return False

#Checking if the gampley grid still includes 0
def check_for_zero(grid):
    gameplay = load_csv("{}_puzzle".format(grid))
    for i in range(0, len(gameplay)):
        for num in gameplay[i]:
            if num == 0:
                return True
    return False

#Resetting the game
def new_game():
    new = input("Would you like to play again? (y / n) ").lower()
    if new == "y":
        return True
    elif new == "n":
        return False
    else:
        print("Invalid input!")
        return new_game()

#After the grid is filled, user can still edit it, then check if he/she won and exit or restart the game
def check_continue(grid, level):
    user_answer = input("Would you like to change anything in your solution? (y / n) ")
    gameplay = load_csv("{}_puzzle".format(grid))
    easy_solution = load_csv("{}_solution".format(level))
    if user_answer == "n".lower():
        if gameplay == easy_solution:
            print_title(winner_giraffe)
        else:
            print_title(loser_giraffe)
        return False
    elif user_answer == "y".lower():
        return True
    else:
        print("Invalid input. Please try again.")
        return check_continue(grid, level)

#Adding a new number to the grid, also checking if the index was 0 in the original layout
def add_number(user_row, user_column, user_number, grid, level):
    u_row = user_row() - 1     #u = user
    u_column = user_column() - 1    #The 1st element is the 0th, that's why -1
    if check_in_orig_puzzle(u_row, u_column, "{}_puzzle".format(level)):
        print("You can't overwrite the original layout!")
        return "continue"
    else: 
        add_num = user_number()
        gameplay = load_csv("{}_puzzle".format(grid))
        gameplay[u_row][u_column] = add_num
        update_csv("{}_puzzle".format(grid), gameplay)
        os.system('clear')
        print_sudoku(grid, level)
        if not check_for_zero(grid):
            if check_continue(grid, level):
                return True
            else:
                return False
        else:
            return True

#User can choose diffculty
def select_level():
    level = input("\tChoose your level: ")
    if level not in ["1", "2", "3"]:
        return select_level()
    else:
        return level


def print_levels():
    os.system('clear')
    print_title(sudoku_title)
    print("\t(-------Levels-------)\n")
    print("\tEasy     -  press: '1'")
    print("\tMedium   -  press: '2'")
    print("\tNot fun  -  press: '3'\n")
    level = select_level()
    if level == "1":
        return "easy"
    elif level == "2":
        return "medium"
    elif level == "3":
        return "notfun"

#Starting the game with a clear terminel to avoid "jumping line"
def start_screen(orig_grid):
    os.system('clear')
    print_sudoku(orig_grid, orig_grid)
    return orig_grid

#The actual game:
def start_game(user_row, user_column, user_number, gameplay, level):
    start = time.time()
    while True:
        if not add_number(user_row, user_column, user_number, gameplay, level):
            break
    end = time.time()
    play_time = round(end - start)
    if play_time < 60:
        print("You spent {} sec with creating your solution.".format(play_time))
    else:
        minutes = play_time // 60
        seconds = play_time % 60
        print("You spent {0} min & {1} sec with creating your solution.".format(minutes, seconds))
    if new_game():
        start_game(user_row, user_column, user_number, "gameplay", start_screen(print_levels()))

#Let the fun begin
start_game(user_row, user_column, user_number, "gameplay", start_screen(print_levels()))