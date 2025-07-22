from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

listOfPoints = []
circles = []

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

def redrawLinesCircles():
    ax.clear()
    ax.imshow(Image.alpha_composite(original, mask))
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    

    for i in range(len(circles) - 1):
        ax.add_patch(circles[i])
        x_values = [listOfPoints[i][0], listOfPoints[i + 1][0]]
        y_values = [listOfPoints[i][1], listOfPoints[i + 1][1]]
        ax.plot(x_values, y_values, color='blue', linewidth=1, linestyle='--')
    if(len(circles) > 0):
        ax.add_patch(circles[-1])
    plt.draw()

def maskCompletet():
    x_values = [listOfPoints[-1][0], listOfPoints[0][0]]
    y_values = [listOfPoints[-1][1], listOfPoints[0][1]]
    ax.plot(x_values, y_values, color='blue', linewidth=1, linestyle='--')

def onclick(event):
    global ix, iy, listOfPoints
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
            
            


if __name__ == "__main__":
    print("Up and running!")
    path = "test_pictures/car.jpg"
    original, mask = load_new_picture(path)
    plt.ion()    
    fig, ax = plt.subplots()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    fig.canvas.mpl_connect("button_press_event", onclick)
    mixed = Image.alpha_composite(original, mask)
    ax.imshow(mixed)
    plt.draw()
    plt.show(block=True)