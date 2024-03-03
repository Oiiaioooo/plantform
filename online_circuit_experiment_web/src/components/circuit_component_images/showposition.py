import matplotlib.animation as animation
import matplotlib.pyplot as plt
from PIL import Image


fig = plt.figure()
img = Image.open('8720DM.png')
#updata = True

width = img.size[0]
height = img.size[1]
print(img.size,"width/height=",width/height)
x = width/2
y = height/2
def on_press(event):
    #print("my position:" ,event.button,event.xdata, event.ydata)
    if event.xdata>width/2:
        x_propotion = (event.xdata-width/2)/width
        anchor_x = 'x+{:.3f}*width'.format(x_propotion)
    else:
        x_propotion = -(event.xdata-width/2)/width
        anchor_x = 'x-{:.3f}*width'.format(x_propotion)
    if event.ydata > height / 2:
        y_propotion = (event.ydata - height / 2) / height
        anchor_y = 'y+{:.3f}*height'.format(y_propotion)
    else:
        y_propotion = -(event.ydata - height / 2) / height
        anchor_y = 'y-{:.3f}*height'.format(y_propotion)
    print("x:"+anchor_x+",\n"+"y:"+anchor_y+",")
plt.imshow(img, animated= True)

fig.canvas.mpl_connect('button_press_event', on_press)
plt.show()
