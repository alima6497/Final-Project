# Name:                     Minesweeper.py
# Author:                   Andre Lima
# Date Created:             April 4, 2023
# Date Last Modified:       April 9, 2023
#
# Purpose: Clear the board without detonating any mines

import random
import os

class Minefield:
    def __init__(self, size, mines):
        self.size = size
        self.mines = mines
        self.map = self.create()
        self.player = self.view()
        self.cleared = 0
        self.trip = False

    # Method: create
    # Description: populates map
    # Return Value:
    #       grid
    def create(self):
        #create list grid
        grid = []

        #append grid with nested lists with length of size self, size number of times
        for row in range(self.size):
            grid.append([])
            for col in range(self.size):
                grid[row].append(0)

        #lays mines to random squares mines number of times
        for mine in range(self.mines):
            while True:
                #select a random square
                randRow = random.randint(0, self.size - 1)
                randCol = random.randint(0, self.size - 1)
                
                #lays mine if none and increments surrounding squares by 1
                if grid[randRow][randCol] != 9:
                    grid[randRow][randCol] = 9
                    
                    for row in range(randRow - 1, randRow + 2, 1):
                        for col in range(randCol -1 , randCol + 2, 1):
                            if row > -1 and col > -1:
                                try:
                                    if grid[row][col] < 9:
                                        grid[row][col] += 1
                                except:
                                    pass

                    break
                #select a new random square if mine already laid
                else:
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - 1)

        return(grid)

    # Method: view
    # Description: populates view
    # Return Value:
    #       grid
    def view(self):
        grid = []

        #append grind with nested list of length size, size number of times
        for row in range(self.size):
            grid.append([])
            for col in range(self.size):
                grid[row].append(10)

        return grid

    # Method: flag
    # Description: toggles flags on un-cleared squares
    # Parameters:
    #       coord: square to flag
    def flag(self, coord):
        while True:
            #checks for a valid input
            while True:
                try:
                    x = coord[0]
                    coord = coord.removeprefix(x)
                    x = ord(x.lower()) - 97
                    y = int(coord) - 1

                    break
                except:
                    coord = input("Please enter a valid input: ")

            try:
                match self.player[x][y]:
                    #if the square has already been cleared send a meesage to the user and wait for input
                    case num if num in range(0, 8):
                        input("This square has already been cleared.\nPress [ENTER] to continue...")

                        break
                    #set the value of the square to 11
                    case 11:
                        self.player[x][y] = 10

                        break
                    #if the square has already been flagged sets the value to 10
                    case other:
                        self.player[x][y] = 11

                        break
            except:
                coord = input("Please enter a valid input: ")

    # Method: dig
    # Description: clears square
    # Parameters:
    #       coord: square to clear
    def dig(self, coord):
        while True:
            #checks for a valid input
            while True:
                try:
                    x = coord[0]
                    coord = coord.removeprefix(x)
                    x = ord(x.lower()) - 97
                    y = int(coord) - 1

                    break
                except:
                    coord = input("Please enter a valid input: ")

            try:
                match self.map[x][y]:
                    #if the square has a value of 0 clears it, set cleared to True, and run plough()
                    case 0:
                        match self.player[x][y]:
                            #if the square has already been cleared send a meesage to the user and wait for input
                            case num if num in range(0, 8):
                                input("This square has already been cleared.\nPress [ENTER] to continue...")

                                break
                            #if the square has been flagged send a meesage to the user and wait for input
                            case 11:
                                input("Thi square has been flagged.\nPress [ENTER] to continue...")

                                break
                            case other:
                                self.player[x][y] = self.map[x][y]
                                self.cleared += 1
                                self.plough()

                                break
                    #clears the square and increments cleared by 1
                    case num if num in range(1, 8):
                        match self.player[x][y]:
                            case num if num in range(0, 8):
                                #if the square has already been cleared send a meesage to the user and wait for input
                                input("This square has already been cleared.\nPress [ENTER] to continue...")

                                break
                            #if the square has been flagged send a meesage to the user and wait for input
                            case 11:
                                input("Thi square has been flagged.\nPress [ENTER] to continue...")

                                break
                            case other:
                                self.player[x][y] = self.map[x][y]
                                self.cleared += 1

                                break
                    #if the square contains a mine clears it and sets trip to True
                    case 9:
                        #if the square has been flagged send a meesage to the user and wait for input
                        if self.player[x][y] == 11:
                            input("Thi square has been flagged.\nPress [ENTER] to continue...")

                            break
                        else:
                            self.player = self.map
                            self.trip = True

                            break
            except:
                coord = input("Please enter a valid input: ")

    # Method: plough
    # Description: clears all surrounding squares of a cleared square of value 0
    def plough(self):
        while True:
            #create flag dug
            dug = False

            #goes through each square
            for idr, row in enumerate(self.player):
                for idc, col in enumerate(row):
                    #checks if the square is cleared and its value is 0
                    if col == 0:
                        #goes through all surrounding squares
                        for x in range(idr - 1, idr + 2, 1):
                            for y in range(idc - 1, idc + 2, 1):
                                if x > -1 and y > -1:
                                    if x != idr or y != idc:
                                        try:
                                            #if the square is not cleared, clears it and sets dug to True
                                            if self.player[x][y] == 10:
                                                self.player[x][y] = self.map[x][y]
                                                self.cleared += 1
                                                dug = True
                                        except:
                                            pass
            
            #exits the loop if no squares were cleared
            if not dug:
                break

    # Method: display
    # Description: prints a string that represents view
    def display(self):
        x = 0
        y = 97

        #print top coordinates and top container 
        output = '{0:>4}'.format('')
        for row in self.player:
            x += 1
            if x < 10:
                output += ' {} '.format(x)
            else:
                output += ' {}'.format(x)

            if x == len(row):
                output += '\n  ┌'
                for col in row:
                    output += '───'
        output += '──┐'

        #print side coordinates, container, and squares
        for row in self.player:
            output += '\n{} │ '.format(chr(y))

            for col in row:
                match col:
                    case 0:
                        output += '\033[30;1m 0 \033[37;0m'
                    case 1:
                        output += '\033[34m 1 \033[37m'
                    case 2:
                        output += '\033[32m 2 \033[37m'
                    case 3:
                        output += '\033[33m 3 \033[37m'
                    case 4:
                        output += '\033[34;1m 4 \033[37;0m'
                    case 5:
                        output += '\033[33;1m 5 \033[37;0m'
                    case 6:
                        output += '\033[36m 6 \033[37m'
                    case 7:
                        output += '\033[35m 7 \033[37m'
                    case 8:
                        output += '\033[37;2m 8 \033[37;0m'
                    case 9:
                        output += '\033[41m δ \033[37;0m'
                    case 10:
                        output += '░░░'
                    case 11:
                        output += '\033[31;47m P \033[37;0m'
                    case other:
                        output += ' {} '.format(str(col))
            output += " │ {}".format(chr(y))
            y += 1
            
        output += '\n  └'

        #print bottom container
        for row in self.player:
            for col in row:
                output += '───'

                break
        output += '──┘'

        x = 0

        #print bottom coordinates
        output += '\n{0:>4}'.format('')
        for row in self.player:
            x += 1
            if x < 10:
                output += ' {} '.format(x)
            else:
                output += ' {}'.format(x)

        print(output)

# Function: splash
# Description: prints splash screen
# Parameters:
#       screen: name of text file
def splash(screen):
    #set cwd to Minesweeper.py file location
    os.chdir(os.path.dirname(__file__))

    #open .txt file and print contents
    try:
        with open('{}.txt'.format(screen)) as splash:
            print(splash.read())
    except:
        print("No file found")

# Function: confimationDialog
# Description: presents the user with a y/n dialog
# Parameters:
#       inputString: yes or no question
#       yesString: prints if user enters 'y'
#       noString: prints if user enters 'n'
# Return Value: 
#       boolean
def confirmationDialog(inputString, yesString = "", noString = ""):
    #prompt the user for 'y' or 'n'
    confirmation = input("{} [Y/N]: ".format(inputString)).upper()

    #loops until user gives a valid input and prints applicable string
    while True:
        if confirmation == "Y":
            if yesString:
                print("\n" + yesString)

            return True
        elif confirmation == "N":
            if yesString:
                print("\n" + noString)

            return False
        else:
            confirmation = input("Please enter a valid input: ").upper()

difficulty = {
    1 : {'level' : 'beginner', 'size' : 9, 'mines' : 10},
    2 : {'level' : 'intermediate', 'size' : 16, 'mines' : 40},
    3 : {'level' : 'expert', 'size' : 26, 'mines' : 60}
}
#initialize gameState
gameState = 'start'

#main game loop
while True:
    match gameState:
        #start screen
        case 'start':
            #print the splash screen and waits for user input before continuing
            os.system('cls')
            splash(gameState)
            input("\n\n\t\tPress [Enter] to start")
            
            #print levels and prompts user to select difficulty
            os.system('cls')
            splash(gameState)

            for level, info in difficulty.items():
                print("{0}. {1}\t\t{2}x{2}\t{3} mines".format(level, info['level'].capitalize(), info['size'], info['mines']))

            level = input("\nSelect difficulty [1-3]: ")

            #create minefield based on user level selection
            while True:
                try:
                    minefield = Minefield(difficulty[int(level)]['size'], difficulty[int(level)]['mines'])

                    break
                except:
                    level = input("Please enter a valid input: ")

            #change gameState to play
            gameState = 'play'

        #game mechanics
        case 'play':
            #print minefield
            os.system('cls')
            minefield.display()

            #prompt player for square to dig or flag
            coord = input("\nEnter coordinate to dig [a1]. Prefix with [-] to flag:\n")

            if coord[0] == '-':
                minefield.flag(coord.removeprefix('-'))
            else:
                minefield.dig(coord)

            #check for win condition; change gameState to 'win' if met
            if minefield.cleared == (minefield.size ** 2 - minefield.mines):
                gameState = 'win'

            #check for lose condition; change gameState to 'lose' if met
            if minefield.trip:
                gameState = 'lose'

        #win screen
        case 'win':
            #print minefield and win splash screen
            os.system ('cls')
            minefield.display()
            splash(gameState)
            
            #ask user if they want to play again
            if confirmationDialog("Do you want to play again?"):
                gameState = 'start'
            else:
                break

        #lose screen
        case 'lose':
            #print minefield and lose splash screen
            os.system ('cls')
            minefield.display()
            splash(gameState)
            
            #ask user if they want to play again
            if confirmationDialog("Do you want to play again?"):
                gameState = 'start'
            else:
                break

#print quit splash screen
os.system('cls')
splash('quit')
