#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 16:43:32 2019
@author: danpetersson

First test to work with OpenCV to extract bricks from picture
"""


import numpy as np
import cv2

class Brick:

    def __init__(self, index, up, right, down, left):
        self.index = index
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.rotation = 0
        self.inUse = False
        self.row = -1
        self.col = -1
        
    def printProperties(self):
        print("index =", self.index)
#        print("up       =", self.up)
#        print("right    =", self.right)
#        print("down     =", self.down)
#        print("left     =", self.left)
        print("rotation =", self.rotation)
#        print("inUse    =", self.inUse)
        print("col      =", self.col)
        print("row      =", self.row)    


def find_bricks(img):

    
    # Gray and blur
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    img_blur = cv2.blur(img_gray,(5,5),0)
    img_blur_3 = cv2.GaussianBlur(img_gray,(3,3),0)
     
    # dilate (and erode)
    img_edges = cv2.Canny(img_blur_3, 10, 200)
    kernel = np.ones((3, 3), "uint8")
    img_dil = cv2.dilate(img_edges, kernel, iterations=1)
    #img_dil = cv2.erode(img_dil, kernel, iterations=1)

    cv2.imshow("Edges", img_edges)

      
#    ret, img_thresh = cv2.threshold(img_blur, 180, 255, cv2.THRESH_BINARY_INV)
#    img_adapt = cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#                cv2.THRESH_BINARY_INV,51,3)
        
    # Contours
    __, contours, hierarchy = cv2.findContours(img_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#    print("Number of Countours:", len(contours))
#    print(contours)
    img_cont = img.copy()
    index = -1 
    color = (0, 0, 255)
    thickness = 1
    cv2.drawContours(img_cont, contours, index, color, thickness)
    
    cv2.imshow("Contours", img_cont)
      
    img_background = img[0:5, 0:5, :] # Background in image upper left corner
    img_rec = img.copy()
    img_list = []
    img_list.append(img_background)
    
    nr_contours = len(contours)
    
    for i in range(nr_contours):
        cnt = contours[nr_contours - 1 - i]
        x,y,w,h = cv2.boundingRect(cnt)
        img_list.append(img[y:y+h,x:x+w, :])

        cv2.rectangle(img_rec,(x,y),(x+w,y+h),(0,255,0),2)

    return img_list, img_rec 

def get_medium_img_size(image_list):
    img_tmp = image_list[0]
    img_width = 0
    img_hight = 0
    for i in range(len(image_list)):
        img_width += img_tmp.shape[1]
        img_hight += img_tmp.shape[0]     

#    img_width = img_width // len(image_list)
 #   img_hight = img_hight // len(image_list)
    medium_img_size = int((img_width + img_hight) / 2 / len(image_list))
#    print("Average Hight:", img_hight, "Width:", img_width, "Size:", img_size)
    return medium_img_size

def resize_images(img_list, size = 150):
    for i in range(len(img_list)):
        img_list[i] = cv2.resize(img_list[i], (size, size))
#        title = "Image " + str(i)
#        cv2.imshow(title, img_list[i])
    return img_list

def rotate_brick(img, rotations = 1):
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    angle = -90 * rotations
    scale = 1.0
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(img, M, (h, w))
    return rotated

def extract_top(img):
    (h, w) = img.shape[:2]
    x1 = int(w / 4)
    x2 = int(w / 4 * 3)
    y1 = int(h / 8)
    y2 = int(h / 8 * 3)
    top = img[y1:y2, x1:x2,:]
    return top

def extract_top_half(img):
    (h, w) = img.shape[:2]
    y2 = int(h / 2)
    top_half = img[0:y2,:,:]
    return top_half


def top_template_matches(image, template, thresh = 0.8):
    (hight, width, depth) = image.shape
    if depth == 3:
        template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#    print(res)
#    print("Max Val:", max_val, "Max Loc:", max_loc)
#    cv2.imshow("Res matching", res)
    
    max_val = np.around(max_val, decimals=2)
    
    if max_val > thresh:
        return True, max_val
    else:
        return False, max_val
  

def brick_list_image(img_list, rows = 3, columns = 3):
    (h, w, d) = img_list[0].shape
    image = np.ones((h * rows, w * columns, d), dtype="uint8")
    
    for r in range(rows):
        for c in range(columns): 
            r_start =  r * h
            r_stop = (r+1)*h
            c_start = c * w
            c_stop = (c+1)*w
            image[r_start:r_stop,c_start:c_stop,:] = img_list[1 + c + r*rows]
    return image


def print_all_images(img_list):
    print("In print all images, length img_list:", len(img_list))
    for i in range(len(img_list)):
        title = "Brick" + str(i+1)
        cv2.imshow(title, img_list[i])
        

def extract_figure_list(img_list, no = 8):
    figure_list = []
    figure_list.append(np.zeros_like(img_list[0]))
    for i in range(no):
        figure_list.append(img_list[i+1])
    return figure_list


def define_Brick(img, figure_list, index):
    
    best_matches = np.zeros(4)
    
    for rot in range(4):
        top = extract_top(img)
        top_val = 0
        
        for i_fl in range(len(figure_list)):
            bol, val = top_template_matches(figure_list[i_fl], top, thresh = 0.6)
            if val > top_val:
                top_val = val
                best_matches[rot] = i_fl
        
        img = rotate_brick(img, -1)
        
#    print("Best_matches :", best_matches)
    
    for i in range(4):
        if best_matches[i] == 0:
            print("ERROR: MATCHED EMPTY TEMPLATE")
        elif best_matches[i] == 2:
            best_matches[i] = -1
        elif best_matches[i] == 4:
            best_matches[i] = -3
        elif best_matches[i] == 6:
            best_matches[i] = -5
        elif best_matches[i] == 8:
            best_matches[i] = -7

#    print("Best_matches converted:", best_matches)

    brick = Brick(index, best_matches[0],best_matches[1],best_matches[2],best_matches[3])
    return brick

def create_brick_list(img_list, figure_list):
    brick_list = []
    brick_list.append(Brick(0,  0,  0,  0,  0))
#    brick_list[0].printProperties()

    for i in range(len(img_list) - 1):
        brick_list.append(define_Brick(img_list[i+1], figure_list, i+1))
#        brick_list[i+1].printProperties()
    
    return brick_list

def transform_brick_image(brick_image):
    # This function transforms bricks to that they are straigt
    # Finding the circles at the corners
    # maybe add a resize to 500x500 here, to be on the safe side...
    
    def get_circle_centers(circles):
        no_circles = len(circles[0]) 
        centers_list = np.zeros((no_circles,2), dtype="int16")
#        print("Centers_list_zeros:", centers_list)
        for i in range(no_circles):
            centers_list[i][0] = circles[0][i][0]  
            centers_list[i][1] = circles[0][i][1]
 #           print("Centers_list:", centers_list)
        return centers_list           
    
    def sort_circles(pts):
        for i in range(0, len(pts)-1):
            for j in range(0, len(pts)-1-i):
                if pts[j][0] > pts[j+1][0]:
                    pts[j], pts[j+1] = pts[j+1].copy(), pts[j].copy()         
        
        if pts[0][1] > pts[1][1]:
            pts[0], pts[1] = pts[1].copy(), pts[0].copy()
#        print(pts)
            
        if pts[2][1] > pts[3][1]:
            pts[2], pts[3] = pts[3].copy(), pts[2].copy()
#        print(pts)
        return(pts)
    
    def remove_false_circles(circle_centers):
         for i in reversed(range(len(circle_centers))):
             if circle_centers[i][0] < 100 or circle_centers[i][0] > 400 or circle_centers[i][1] < 100 or circle_centers[i][1] > 400:
                 None
             else:
                 circle_centers = np.delete(circle_centers, i, axis=0)
         return circle_centers
    
    img = cv2.resize(brick_image, (500, 500))
    rows,cols,ch = img.shape
    
    img_bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_bw = cv2.medianBlur(img_bw,3)
#    img_bw = (255-img_bw)  
    
    circles = cv2.HoughCircles(img_bw,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=20,minRadius=10,maxRadius=15)
    circles_int = np.uint16(np.around(circles))
#    print("Circles round", circles)

    
    for i in circles_int[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),1)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),1)

    circle_centers = get_circle_centers(circles)
    circle_centers = remove_false_circles(circle_centers)

    if len(circle_centers) == 4:
    
        # bubble sort circles
        circle_centers = sort_circles(circle_centers)
    #    print("Circle centers sorted", circle_centers)
    
    
    #   this part I still might still have to find out how to do and optimize :)
    #   https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
    
        pts1 = np.float32(circle_centers)
        holes = np.float32([[35,35],[35,465],[465,35],[465,465]])
    
        M = cv2.getPerspectiveTransform(pts1,holes)  
    
        dst = cv2.warpPerspective(brick_image, M, (500,500))

        return True, dst

    else:
        return False, img



def brick_list_from_image(image_filename, no_bricks = 9, no_figures = 4):
    
    img = cv2.imread(image_filename)
    
    img_list, img_rec = find_bricks(img)   
    img_list = resize_images(img_list, 500)
    for i in range(1,len(img_list)):
        ___, img_list[i] = transform_brick_image(img_list[i])
    img_list = resize_images(img_list, 200)
        
    figure_list = extract_figure_list(img_list, 2 * no_figures)
    brick_list = create_brick_list(img_list, figure_list)      
    bricks_image = brick_list_image(img_list)
      
    cv2.imshow("bricks", img_rec)
    cv2.waitKey(1)

    if len(img_list)-1 == no_bricks:
        OK = True
    else:
        OK = False

    return OK, brick_list, img_list, bricks_image




# =============================================================================
# # Here the main program starts   
# =============================================================================

if __name__ == "__main__":

    image_file = "20190206_114340_small.jpg"
    columns = 3                                 # Column of Brick Table
    rows = 3                                    # Rows of Brick Table    
    OK, brickList, img_list, bricks_image = brick_list_from_image(image_file, columns*rows, 4)
    """
    for i in range(1,len(img_list)):
        ___, brick_transformed = transform_brick_image(img_list[i])      
        #cv2.imshow("Found Bricks", img_rec)
        cv2.imshow("Transformed Brick", brick_transformed)
        cv2.waitKey(0)
        
    #print_all_images(template_list)
    """            
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

