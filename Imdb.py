from skimage import io
import matplotlib.pyplot as plt
from ImdbScrape import *


m = input("Enter the movie name: ")
m = m.replace(" ","")
urls,imgs,titles = getmovies(m.lower())


fig = plt.figure()
axes = []
for i in range(2):
    ax = plt.subplot(1, 2, i + 1)
    axes.append(ax)
    ax.set_title(titles[i])
    image = io.imread(imgs[i])        
    ax.imshow(image)
    plt.xticks([ ])
    plt.yticks([ ])

def onpick(event):
    if event.inaxes == axes[0]:
        create_csv(urls,0,m)
    elif event.inaxes == axes[1]:
        create_csv(urls,1,m)  
    
fig.canvas.mpl_connect("button_press_event", onpick)
plt.show()
   


        


