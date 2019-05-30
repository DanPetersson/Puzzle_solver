#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 10:17:52 2019
@author: danpetersson

ERI IST Puzzle
Program to solve puzzle with bird, fishe, flag and flower blicks

Version 3.x:
    Cleaning up code
    Removing class Brick from Puzzle_Final
    Adding prompt for file name
    Adding explanotary text 
    Added result files
    Added in "brick_image_functions_3_1" function "transform_brick_image()"
    
    
Version 2.0:
    Showing visually the bricks moving while executing
    
Version 1.0:
    Solved with showing the picture at the end.

"""

import pathlib
import os
import cv2
import Puzzle_image_lib_3_2.py as bif
#from matplotlib import pyplot as plt

""" Functions for solving the puzzle"""

def get_input():
    default_filename = "Puzzle_pieces.jpg"
    filename = input("Please specify file name for picture input: ")
    if  filename == "":
        filename = default_filename
        print("Default file name used:", filename)
    return filename
    

def init_brickTable(colums, rows):
    # Real table start at [1,1], plus padding with empty blanks
    brick_table = []
    for y in range(0, colums+2):
        col = []
        for x in range(0, rows+2):
            col.append(brickList[0]) 
        brick_table.append(col)
    return(brick_table)        


# Check Postition of brick in Table
def check_pos(brickList, brickTable, brickList_index, col, row):
    brick = brickList[brickList_index]
    if brick.left + brickTable[col-1][row].right == 0  or brick.left * brickTable[col-1][row].right == 0:
        if brick.up + brickTable[col][row-1].down == 0  or brick.up * brickTable[col][row-1].down == 0:
            return True
        else:
            return False
    else:         
        return False
   
# Updates position    
def update_pos(brickList, brickTable, brickList_index, col, row):
    # Add position in brickList
    brickList[brickList_index].col = col
    brickList[brickList_index].row = row
    brickTable[col][row] = brickList[brickList_index]
    brickList[brickList_index].inUse = True
    brickTable[col][row] = brickList[brickList_index]
    return True

def rotation_possible(brickList, index):    
    return brickList[index].rotation < 3

def rotate_brick(brickList, index):
    brick = brickList[index]
    up_tmp = brick.up

    brick.up = brick.left
    brick.left = brick.down
    brick.down = brick.right
    brick.right = up_tmp
    if brick.rotation < 3:
        brickList[index].rotation = brick.rotation + 1
        return True
    else:
        brickList[index].rotation = 0
        return False
    
def next_position(table, col, row):
    # Updates position (col, row) to next possible position 
    col_size = len(table) - 2
    row_size = len(table[0]) - 2
    OK = True
    if col == col_size:
        if row == row_size:
            OK = False
        else:
            col = 1
            row = row + 1
    else:
        col = col + 1
    return OK, col, row, 


def prev_position(table, col, row):
    # Updates position (col, row) to previous possible position 
    col_size = len(table) - 2
    OK = True
    if col == 1:
        if row == 1:
            OK = False
        else:
            col = col_size
            row = row - 1
    else:
        col = col - 1
    return OK, col, row, 


def brick_list_img_rotation(brick_list, image_list):

    img_out_list = image_list.copy()
    for i in range(len(brick_list)):
        img_out_list[i]= image_list[0]
    
    
    for i in range(len(brick_list)):
        if i > 0:
            index = 3 * (brick_list[i].row-1) + brick_list[i].col
            if brick_list[i].inUse:
                img_out_list[index]= bif.rotate_brick(image_list[i], brick_list[i].rotation)
    return img_out_list


def print_brickTable(table):
    # Real table start at [1,1], plus padding with empty blanks
    for y in range(1, len(table[0])-1):
        print("-------------------")
        for x in range(1, len(table)-1):
            print("|",table[x][y].index, table[x][y].rotation, end=' ')
        print("|")
    print("-------------------")
    return(table)        

def print_brickTable_compact(table):
    # Real table start at [1,1], plus padding with blanks
    print("||", end='')
    for y in range(1, len(table[0])-1):
        for x in range(1, len(table)-1):
            print(table[x][y].index, end='')
            print(table[x][y].rotation, end='')
            print("|", end='')
        print("|", end='')
    print('')    
    return(table)   
    
def print_brickTable_file(table, output_file):
    output_file.write("Test\n")
    return(table)   

def print_brickList_compact(brick_list):
    for i in range(len(brick_list)):
        b = brick_list[i]
#        print("i,u,r,d,l,iU =", b.up, b.right, b.down, b.left, b.inUse)
        print(b.inUse, end=" ")
    print("")



""" Main Program """
# =============================================================================
# # Here the main program starts   
# =============================================================================

if __name__ == "__main__":

    # Get the input (filename, columns, rows, figures)    
    image_file = get_input()
    columns = 3                                 # Column of Brick Table
    rows = 3                                    # Rows of Brick Table

    
    cwd = os.getcwd()
    result_dir = cwd + "/Results"
    result_file_path = result_dir + "/Puzzle_log.txt"
    print("Result file path:", result_file_path)
    pathlib.Path(result_dir).mkdir(parents=True, exist_ok=True) 
    output_file = open(result_file_path, "w")

    
    OK, brickList, img_list, bricks_image = bif.brick_list_from_image(image_file, columns*rows, 4)
    
    if OK == False:
        print("Wrong number of bricks found and program will not be able to solve puzzle :(")
        print("See shown images where it can been seen which bricks it thought it found and try a new picture.")
    
    else:
        print("Check the shown images how the solution is found!")
        brickTable = init_brickTable(columns, rows) # the table, orgninally with empty bricks
            
        """ Initalizing Loop for finding solution """
        index, col, row = 1, 1, 1
        stop = False
        prev_OK = True
        
        while not stop:
            
            if index >= len(brickList):
                # if no more bricks in bricklist, move back on position, 
                # rotate or else choose next brick in list
                
                brickTable[col][row] = brickList[0]
                prev_OK, col, row = prev_position(brickTable, col, row)
                if not prev_OK:
                    stop = True
                    print("No (furher) solution found")
                else:            
                    index = brickTable[col][row].index
                    brickList[index].inUse = False
                    if rotation_possible(brickList, index):
                        True__ = rotate_brick(brickList, index)     
                    else:             
                        False__ = rotate_brick(brickList, index)
                        index = index + 1
        
                    
            elif not brickList[index].inUse:
                        
                if check_pos(brickList, brickTable, index, col, row):
                    update_pos(brickList, brickTable, index, col, row)
                    print(".", end="")   
        #            print_brickTable_compact(brickTable)
                    print_brickTable_file(brickTable, output_file)
        
                    tmp_img_list = brick_list_img_rotation(brickList, img_list)
                    tmp_image = bif.brick_list_image(tmp_img_list)
                    cv2.imshow("Intermediate", tmp_image)
                    cv2.waitKey(1)            
                    
                    if col == columns and row == rows:
                        print("\nContratulations, it is solved!")
                        print_brickTable(brickTable)
                        stop = True
                    else:
                        next_OK, col, row = next_position(brickTable, col, row)
                        index = 1
                
                elif rotation_possible(brickList, index):
                    True__ = rotate_brick(brickList, index)
                
                else:             
                    False__ = rotate_brick(brickList, index)
                    index = index + 1
                
            else:
                index = index + 1
        
        #for i in range(len(brickList)):
        #    brickList[i].printProperties()
        
        
        solution_img_list = brick_list_img_rotation(brickList, img_list)
        solution_image = bif.brick_list_image(solution_img_list)
        
        cv2.imshow("Input 3x3", bricks_image)
        cv2.imshow("Solution 3x3", solution_image)
        cv2.imwrite('Puzzle_solution.png', solution_image)
      
    # End of else...
    output_file.close()
    print("Press any key on the shown pictures close the program")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
