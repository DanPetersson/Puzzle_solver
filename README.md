# Puzzle_solver

This python program containing two source code files solves a 3x3 puzzle. The program takes a picture of the puzzle pieces as input, extracts the pieces and then graphically shows the solving process.

Files:
- Puzzle_solver_3_x.py     : The main python 3.x program solving the puzzle
- Puzzle_image_lib_3_x.py  : Library with classes and functions handling the images, importing cv2
- Puzzle_pieces.jpg        : Input sample picture of puzzle pieces


Requirements on input picture (see attached sample as example)
- Uniform background, so pieces can be automatically extracted
- Pieces with matching sides shall have these pointing upwards in pairs, e.g. front and back of a bird.
  - Last piece does not have a partner
- Order is from top to bottom in picture, i.e. the "hight or y" of upper left corner of each piece determines the order
