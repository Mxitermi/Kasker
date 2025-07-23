from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from pathlib import Path

from matplotlib.patches import Circle
from matplotlib.widgets import Button

listOfPoints = []
circles = []
mask_color = (57, 237, 222, 255)  # RGBA color for the mask
cur_pic = 0
finished = False
count_of_pics = 0
path_to_pics = ""

def load_new_picture(path):
    original_img = Image.open(path)
    original_img = original_img.convert("RGBA")
    mask = Image.new("RGBA", original_img.size, (255, 255, 255, 0))  
    #
    return original_img, mask
    
    #img_array = np.array(img)
    #print(img_array[0, 0])  # Print the RGB value of the pixel at (0, 0)
    
    # Convert numpy array back to PIL Image
    #img_from_array = Image.fromarray(img_array)

def clearClickedPoints():
    global ix, iy
    display_coords = ax.transData.transform((ix, iy))
    for circle in circles:
        if circle.contains_point(display_coords):
            if(circle.center[0] == listOfPoints[0][0] and circle.center[1] == listOfPoints[0][1]):
                return False, circle
            else:
                listOfPoints.clear()
                return True, circle
    return False, None

def drawCircle(x, y, radius=10):
    global ax, fig
    circle = Circle((x, y), radius, color='red', fill=False)
    circles.append(circle)
    ax.add_patch(circle)
    
def updateClickedPoints(x, y):
    listOfPoints.append([x, y])

def updateLines():
    global ax, fig
    x_values = [listOfPoints[-1][0], listOfPoints[-2][0]]
    y_values = [listOfPoints[-1][1], listOfPoints[-2][1]]
    ax.plot(x_values, y_values, color='blue', linewidth=1, linestyle='--')
    plt.draw()

def clearEverything():
    ax.clear()
    ax.imshow(Image.alpha_composite(original, mask))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

def redrawLinesCircles():
    clearEverything()
    for i in range(len(circles) - 1):
        ax.add_patch(circles[i])
        x_values = [listOfPoints[i][0], listOfPoints[i + 1][0]]
        y_values = [listOfPoints[i][1], listOfPoints[i + 1][1]]
        ax.plot(x_values, y_values, color='blue', linewidth=1, linestyle='--')
    if(len(circles) > 0):
        ax.add_patch(circles[-1])
    plt.draw()

def maskCompletet():
    global finished, listOfPoints, circles, ax, cur_pic
    
    clearEverything()
    
    cur_pic -= 1
    original, mask = load_new_picture(getPath(path_to_pics))

    mask = cv2.fillPoly(img = np.array(mask), pts = [np.array(listOfPoints, np.int32)], color=mask_color)
    
    mask = Image.fromarray(mask)
  

    # Display composited image
    composited_image = Image.alpha_composite(original, mask)
    ax.set_xlim(0, composited_image.width)
    ax.set_ylim(composited_image.height, 0)  # Flip y-axis for correct orientation
    ax.imshow(composited_image)
    listOfPoints.clear()
    circles.clear()
    finished = True

def onclick(event):
    global ix, iy, listOfPoints

    # Ignore clicks outside the axes (e.g., on the button)
    if event.inaxes != ax:
        return

    ix, iy = event.xdata, event.ydata
    isInside, circle = clearClickedPoints()
    if(isInside):
        circles.remove(circle)
        listOfPoints.clear()
        listOfPoints = [c.center for c in circles]
        
        redrawLinesCircles()
    else:
        if circle is None:
            updateClickedPoints(ix, iy)
            if len(listOfPoints) == 1:
                listOfPoints.append([ix, iy])
            else:
                updateLines()
            drawCircle(ix, iy)
        else:
            maskCompletet()
    
def save(event):
    global finished, mask, original
    if finished:
        mask.save("mask.png")
        print("Saved mask and original image.")
    else:
        print("Mask is not complete. Cannot save.")
    plt.close()

def clear(event):
    global finished, mask, original, listOfPoints, circles, ax, cur_pic, path_to_pics
    finished = False
    listOfPoints.clear()
    circles.clear()
    cur_pic -= 1
    original, mask = load_new_picture(getPath(path_to_pics))
    clearEverything()
    composited_image = Image.alpha_composite(original, mask)
    ax.imshow(composited_image)
    plt.draw()

def getPath(path):
    global cur_pic, count_of_pics

    if os.path.exists(path):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_dir = Path(path)
        images = sorted([
            str(p) for p in image_dir.iterdir()
            if p.suffix.lower() in valid_extensions
        ])
        count_of_pics = len(images)
        cur_pic += 1
        return images[cur_pic - 1] if images else None
    else:
        print(f"Path '{path}' is invalid.")
        quit()
         
def previousPicture(event):
    global cur_pic, path_to_pics
    if(cur_pic > 1):
        cur_pic -= 2
        path = getPath(path_to_pics)
        original, mask = load_new_picture(path)
        clearEverything()
        listOfPoints.clear()
        composited_image = Image.alpha_composite(original, mask)
        ax.set_xlim(0, composited_image.width)
        ax.set_ylim(composited_image.height, 0)  # Flip y-axis for correct orientation
        ax.imshow(composited_image)
        plt.draw()

def nextPicture(event):
    global cur_pic, count_of_pics, path_to_pics
    if(cur_pic != count_of_pics):
        path = getPath(path_to_pics)
        original, mask = load_new_picture(path)
        clearEverything()
        listOfPoints.clear()
        composited_image = Image.alpha_composite(original, mask)
        ax.set_xlim(0, composited_image.width)
        ax.set_ylim(composited_image.height, 0)  # Flip y-axis for correct orientation
        ax.imshow(composited_image)
        plt.draw()

if __name__ == "__main__":
    print("Up and running!")
    print("Please type in the path to the folder which contains the pictures you want to label.\nIf you want to use the default folder (test_pictures/), just press enter.")
    path = "test_pictures/"
    path = input("Path to picture: ") or path
    path_to_pics = path
    path = getPath(path)
    
    original, mask = load_new_picture(path)
    plt.ion()    
    

    # Create figure and axis
    fig, ax = plt.subplots()

    # Display composited image
    composited_image = Image.alpha_composite(original, mask)
    ax.set_xlim(0, composited_image.width)
    ax.set_ylim(composited_image.height, 0)  # Flip y-axis for correct orientation
    ax.imshow(composited_image)

    # Connect click event handler
    fig.canvas.mpl_connect("button_press_event", onclick)

    # Add "Finish" button
    buttonf_ax = fig.add_axes([0.8, 0.01, 0.13, 0.05])  # [left, bottom, width, height]
    finish_button = Button(buttonf_ax, 'Save Mask')
    finish_button.on_clicked(save)

    # Add "clear" button
    buttonc_ax = fig.add_axes([0.65, 0.01, 0.13, 0.05])  # [left, bottom, width, height]
    clear_button = Button(buttonc_ax, 'Clear Mask')
    clear_button.on_clicked(clear)

    buttonp_ax = fig.add_axes([0.1, 0.01, 0.1, 0.05])  # [left, bottom, width, height]
    previous_button = Button(buttonp_ax, 'Previous')
    previous_button.on_clicked(previousPicture)


    # Add "clear" button
    buttonn_ax = fig.add_axes([0.22, 0.01, 0.1, 0.05])  # [left, bottom, width, height]
    next_button = Button(buttonn_ax, 'Next')
    next_button.on_clicked(nextPicture)

    plt.draw()
    plt.show(block=True)
    