from termcolor import colored
import csv
import numpy
import random
import sys
import os
import termios
import time
import tty


sudoku_title = r"""

        ___         _       _
       / __> _ _  _| | ___ | |__ _ _
       \__ \| | |/ . |/ . \| / /| | |
       <___/`___|\___|\___/|_\_\`___|


   Press 'x' to quit your current game.
   Press 's' to save your current game.
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


valid_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# This prints the ASCII art
def print_title(ascii):
    print(ascii)


# Loading the gameplay csv template and initializing that grid it into a new local list
def load_csv(filename):
    with open("{}.csv".format(filename), "r") as f:
        reader = list(csv.reader(f))
        for lst in reader:
            for i in range(0, len(lst), 1):
                lst[i] = int(lst[i])
        return reader


# This function is used to overwrite the original grid locally
def update_csv(filename, matrix):
    with open("{}.csv".format(filename), "w") as f:
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)


# Printing the local grid and coloring it. White = new numbers which were 0 in the original file
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


# User input without pressing enter
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# Asking the player to add the row number
def user_row():
    print("Choose a row:")
    row = getch()
    if row.isdigit():
        if int(row) in valid_numbers:
            new_row = int(row)
            return new_row
        else:
            print("That's not a valid number!")
            return user_row()
    elif row == "x":
        print("See you next time!")
        sys.exit()
    else:
        print("That's not a number!")
        return user_row()


# Asking the player to add the column number
def user_column():
    print("Choose a column:")
    column = getch()
    if column.isdigit():
        if int(column) in valid_numbers:
            new_column = int(column)
            return new_column
        else:
            print("That's not a valid number!")
            return user_column()
    elif column == "x":
        print("See you next time!")
        sys.exit()
    else:
        print("That's not a number!")
        return user_column()


# Asking the player to add the number
def user_number():
    print("Add a number from 1 to 9: ")
    number = getch()
    if number.isdigit():
        if int(number) in valid_numbers:
            new_number = int(number)
            return new_number
        else:
            print("That's not a valid number!")
            return user_number()
    elif number == "x":
        print("See you next time!")
        sys.exit()
    else:
        print("That's not a number!")
        return user_number()


# Comparing the local gameplay grid to the original one
def check_in_orig_puzzle(row, column, grid):
    if int(load_csv(grid)[row][column]) != 0:
        return True
    else:
        return False


# Checking if the gampley grid still includes 0
def check_for_zero(grid):
    gameplay = load_csv("{}_puzzle".format(grid))
    for i in range(0, len(gameplay)):
        for num in gameplay[i]:
            if num == 0:
                return True
    return False


# Resetting the game
def new_game():
    new = input("Would you like to play again? (y / n) ").lower()
    if new == "y":
        return True
    elif new == "n":
        print("See you next time!")
        sys.exit()
    else:
        print("Invalid input!")
        return new_game()


# After the grid is filled, user can still edit it, then check if he/she won and exit or restart the game
def check_continue(grid, level):
    user_answer = input("Would you like to change anything in your solution? (y / n) ")
    gameplay = load_csv("{}_puzzle".format(grid))
    easy_solution = load_csv("{}_solution".format(level))
    if user_answer == "n".lower():
        if gameplay == easy_solution:
            time.sleep(1)
            print_title(winner_giraffe)
        else:
            time.sleep(1)
            print_title(loser_giraffe)
        return False
    elif user_answer == "y".lower():
        return True
    else:
        print("Invalid input. Please try again.")
        return check_continue(grid, level)


# Adding a new number to the grid, also checking if the index was 0 in the original layout
def add_number(user_row, user_column, user_number, grid, level):
    u_row = user_row() - 1  # u = user
    u_column = user_column() - 1    # The 1st element is the 0th, that's why -1
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


# Saves the current gameplay in to an external files
def save_game():
    global gameplay
    global orig_board
    update_csv("save_gameplay.csv", gameplay)
    update_csv("save_orig_board.csv", orig_board)


# Loads the saved gameplay from the external files
def load_game():
    global gameplay
    global orig_board
    gameplay = load_csv("save_gameplay.csv")
    orig_board = load_csv("save_orig_board.csv", orig_board)


def print_main_menu():
    os.system("clear")
    print_title(sudoku_title)
    print("\t---------Main menu---------\n")
    print("\tNew Game     -  press: '1'")
    print("\tLoad Game    -  press: '2'")
    print("\tExit Game    -  press: '3'\n")


def start_main_menu():
    invalid = False
    while True:
        print_main_menu()
        if invalid:
            print("\tInvalid option!")
        time.sleep(0.5)
        option = input("\tChoose an option: ")
        if option == "1":
            time.sleep(0.5)
            start_game(user_row, user_column, user_number, "gameplay", start_screen(print_levels()))
            invalid = False
        elif option == "2":
            time.sleep(0.5)
            load_game()
            invalid = False
        elif option != "3":
            invalid = True
        else:
            break


# User can choose diffculty
def select_level():
    level = input("\tChoose your level: ").lower()
    while level not in ["0", "1", "2", "3", "x"]:
        print("\tInvalid input!")
        level = input("\tChoose your level: ")
    return level


def print_levels():
    os.system('clear')
    print_title(sudoku_title)
    print("\t(-------Levels-------)\n")
    print("\tDemo     -  press: '0'")
    print("\tEasy     -  press: '1'")
    print("\tMedium   -  press: '2'")
    print("\tNot fun  -  press: '3'\n")
    time.sleep(0.5)
    level = select_level()
    if level == "0":
        return "demo"
    elif level == "1":
        return "easy"
    elif level == "2":
        return "medium"
    elif level == "3":
        return "notfun"
    elif level == "x":
        print("See you next time!")
        sys.exit()


# Starting the game with a clear terminel to avoid "jumping line"
def start_screen(orig_grid):
    os.system('clear')
    print_sudoku(orig_grid, orig_grid)
    return orig_grid


# The actual game:
def start_game(user_row, user_column, user_number, gameplay, level):
    start = time.time()
    while True:
        if not add_number(user_row, user_column, user_number, gameplay, level):
            break
    end = time.time()
    play_time = round(end - start)
    if play_time < 60:
        if play_time == 1:
            print("You solved the puzzle in {} second.".format(play_time))
        else:
            print("You solved the puzzle in {} seconds.".format(play_time))
    else:
        minutes = play_time // 60
        seconds = play_time % 60
        if minutes == 1 and seconds == 1:
            print("You solved the puzzle in {0} minute & {1} second".format(minutes, seconds))
        elif minutes > 1 and seconds == 1:
            print("You solved the puzzle in {0} minutes & {1} second".format(minutes, seconds))
        else:
            print("You solved the puzzle in {0} minutes & {1} seconds".format(minutes, seconds))
    if new_game():
        start_game(user_row, user_column, user_number, "gameplay", start_screen(print_levels()))


# Let the fun begin
start_main_menu()
