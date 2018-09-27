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
   Add '0' to remove an already added number.
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


valid_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

orig_grid = []
gameplay = []
level = ""
save_directory = "/home/kata/codecool/Python/sudoku/cc_python_sudoku/saved_games/"
new_directory = "/home/kata/codecool/Python/sudoku/cc_python_sudoku/puzzles/"


# This prints the ASCII art
def print_title(ascii):
    print(ascii)


# Loading the gameplay csv template and initializing that grid it into a new local list
def load_csv(filename, new=True):
    global save_directory
    global new_directory
    directory = new_directory if new else save_directory
    with open("{0}{1}.csv".format(directory, filename), "r") as f:
        reader = list(csv.reader(f))
        for lst in reader:
            for i in range(0, len(lst), 1):
                lst[i] = int(lst[i])
        return reader


# This function is used to overwrite the original grid locally
def update_csv(filename, matrix):
    global save_directory
    with open("{}{}.csv".format(save_directory, filename), "w") as f:
        writer = csv.writer(f)
        for row in matrix:
            writer.writerow(row)


# Printing the local grid and coloring it. White = new numbers which were 0 in the original file
def print_sudoku():
    global orig_grid
    global gameplay
    global level
    short_level = level.split(chr(95))
    short_level = short_level[0]
    print_board = []
    print_title(sudoku_title)
    print("     +" + "---+"*9)
    for r in range(0, len(gameplay)):
        print_row = []
        for c in range(0, len(gameplay[r])):
            if orig_grid[r][c] != 0:
                if short_level == "demo" or short_level == "easy":
                    print_row.append(colored(gameplay[r][c], "cyan"))
                elif short_level == "medium":
                    print_row.append(colored(gameplay[r][c], "yellow"))
                elif short_level == "notfun":
                    print_row.append(colored(gameplay[r][c], "green"))
            else:
                print_row.append(colored(gameplay[r][c], "white"))
        print_board.append(print_row)
    for i, row in enumerate(print_board):
        print(("     |" + " {}   {}   {} |"*3).format(*[x if x != colored(0, "white") else " " for x in row]))
        if i % 3 == 2:
            print("     +" + "---+"*9)
        else:
            print("     +" + "   +"*9)


# User input without pressing enter
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print(ch)
    return ch


# Asking the player to add the row number
def user_row():
    print("\n Choose a row:")
    row = getch()
    if row.isdigit():
        if int(row) in valid_numbers:
            new_row = int(row)
            return new_row
        else:
            print("That's not a valid number!")
            return user_row()
    elif row == "x":
        print("\nSee you next time!")
        sys.exit()
    elif row == "s":
        print("Your game is saved.")
        save_game()
        return user_row()
    else:
        print("That's not a number!")
        return user_row()


# Asking the player to add the column number
def user_column():
    print(" Choose a column:")
    column = getch()
    if column.isdigit():
        if int(column) in valid_numbers:
            new_column = int(column)
            return new_column
        else:
            print("That's not a valid number!")
            return user_column()
    elif column == "x":
        print("\nSee you next time!")
        sys.exit()
    elif column == "s":
        print("Your game is saved.")
        save_game()
        return user_column()
    else:
        print("That's not a number!")
        return user_column()


# Asking the player to add the number
def user_number():
    print(" Add a number from 1 to 9: ")
    number = getch()
    if number.isdigit():
        if int(number) in valid_numbers:
            new_number = int(number)
            return new_number
        else:
            print("That's not a valid number!")
            return user_number()
    elif number == "x":
        print("\nSee you next time!")
        sys.exit()
    elif number == "s":
        print("Your game is saved.")
        save_game()
        return user_number()
    else:
        print("That's not a number!")
        return user_number()


# Comparing the local gameplay grid to the original one
def check_in_orig_puzzle(row, column):
    global orig_grid
    if int(orig_grid[row][column]) != 0:
        return True
    else:
        return False


# Checking if the gampley grid still includes 0
def check_for_zero():
    global gameplay
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
        print("\nSee you next time!")
        sys.exit()
    else:
        print("Invalid input!")
        return new_game()


# After the grid is filled, user can still edit it
# then check if he/she won and exit or restart the game
def check_continue():
    user_answer = input("Would you like to change anything in your solution? (y / n) ")
    global gameplay
    global level
    loc_level = level.split(chr(95))
    loc_level[1] = "solution"
    loc_level = chr(95).join(loc_level)
    solution = load_csv("{}".format(loc_level))   # kell bele a random generált szám
    if user_answer == "n".lower():
        if gameplay == solution:
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
        return check_continue()


# Adding a new number to the grid, also checking if the index was 0 in the original layout
def add_number(user_row, user_column, user_number):
    u_row = user_row() - 1  # u = user
    u_column = user_column() - 1  # The 1st element is the 0th, that's why -1
    global gameplay
    if check_in_orig_puzzle(u_row, u_column):
        print("You can't overwrite the original layout!")
        return True
    else:
        add_num = user_number()
        gameplay[u_row][u_column] = add_num
        os.system('clear')
        print_sudoku()
        if not check_for_zero():
            if check_continue():
                return True
            else:
                return False
        else:
            return True


# Saves the current gameplay in to an external files
def save_game():
    global gameplay
    global orig_grid
    global level
    update_csv("{}_save_gameplay".format(level), gameplay)
    update_csv("{}_save_orig_board".format(level), orig_grid)


# Generates the string format number list fo choose save game
def generate_str_num_list(length):
    for num in range(1, length + 1):
        yield str(num)


# Asks the user which file has to be loaded
def choose_save_game(length):
    game = input("\n    Choose a gameplay to load: ")
    while game not in generate_str_num_list(length) and game != "x":
        print("Invalid option")
        game = input("    Choose a gameplay to load: ")
    return game


# Prints the list of saved games
def print_save_list():
    global gameplay
    global orig_grid
    global save_directory
    global level
    save_list = sorted([item[:-4] for item in os.listdir(save_directory) if "gameplay" in item])
    orig_list = sorted([item[:-4] for item in os.listdir(save_directory) if "orig" in item])
    index = 1
    print(sudoku_title)
    print("\t(----Saved Games----)\n")
    for item in save_list:
        print("    {0}) {1}".format(index, item))
        index += 1
    index = choose_save_game(len(save_list))
    if index == "x":
        print("\nSee you next time!")
        sys.exit()
    else:
        index = int(index) - 1
    gameplay_to_load = save_list[index]
    orig_grid_to_load = orig_list[index]
    gameplay = load_csv(gameplay_to_load, False)
    orig_grid = load_csv(orig_grid_to_load, False)
    level = save_list[index].split(chr(95))
    level = chr(95).join(level[:3])


# Loads the saved gameplay from the external files
def load_game():
    time.sleep(0.5)
    os.system("clear")
    print_save_list()
    time.sleep(0.5)
    start_game(user_row, user_column, user_number)


def print_main_menu():
    os.system("clear")
    print_title(sudoku_title)
    print("    (------------- Main menu -------------)\n")
    print("\t   New Game    -   press: '1'")
    print("\t   Load Game   -   press: '2'\n")


# Starts the main menu
def start_main_menu():
    invalid = False
    while True:
        print_main_menu()
        if invalid:
            print("\t   Invalid option!")
        time.sleep(0.5)
        option = input("\t   Choose an option: ")
        if option == "1":
            time.sleep(0.5)
            print_levels()
            invalid = False
        elif option == "2":
            time.sleep(0.5)
            load_game()
            invalid = False
        elif option == "x":
            print("\nSee you next time!")
            break
        else:
            invalid = True


# User can choose diffculty
def select_level():
    global level
    global gameplay
    global orig_grid
    u_level = input("\t   Choose your level: ").lower()
    while u_level not in ["0", "1", "2", "3", "x"]:
        print("\tInvalid input!")
        u_level = input("\t Choose your level: ").lower()
    if u_level == "0":
        u_level = "demo"
    elif u_level == "1":
        u_level = "easy"
    elif u_level == "2":
        u_level = "medium"
    elif u_level == "3":
        u_level = "notfun"
    elif u_level == "x":
        time.sleep(0.5)
        print("\nSee you next time!")
        sys.exit()
    if u_level != "demo":
        num = random.randint(1, 10)
        level = "{}_puzzle_{}".format(u_level, num)
    else:
        level = "{}_puzzle".format(u_level)
    gameplay = load_csv(level)
    orig_grid = load_csv(level)
    start_game(user_row, user_column, user_number)


def print_levels():
    os.system('clear')
    print_title(sudoku_title)
    print("    (-------------- Levels ---------------)\n")
    print("\t    Demo       -    press: '0'")
    print("\t    Easy       -    press: '1'")
    print("\t    Medium     -    press: '2'")
    print("\t    Not fun    -    press: '3'\n")
    select_level()


# Starting the game with a clear terminel to avoid "jumping line"
def start_screen():
    os.system('clear')
    print_sudoku()


# The actual game:
def start_game(user_row, user_column, user_number):
    start_screen()
    start = time.time()
    while True:
        if not add_number(user_row, user_column, user_number):
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
        start_main_menu()


# Let the fun begin
start_main_menu()
