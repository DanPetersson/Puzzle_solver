# Puzzle_solver

This python program containing two source code solves a 3x3 puzzle. The program takes a picture of the pieces as input, finds the pieces and then grahically shows the solving process.

Files:
- Puzzle_solver_3_x.py     : The main python 3.x program solving the puzzle
- Puzzle_image_lib_3_x.py  : Library with classes and functions handling the images, importing cv2
- Puzzle_pieces.jpg        : Input sample picture of puzzle pieces


Requirements on input picture (see attached sample as example)
- Uniform background, so pieces can be autmatically extracted
- Pieces with matching sides shall have these poiting upwards in pairs, e.g. front and back of a bird.
  - Last piece does not have a partner
- Order is from top to bottom i picutre, i.e. the "hight or y" of upper left corner of each piece determines the order
