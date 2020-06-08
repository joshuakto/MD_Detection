import json
import os
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    exp = input('Process Experiment: ')
    for _,_,i in os.walk(os.path.join('/home/joshuakt/Balance', exp)):
        for f in i:
            with open(os.path.join('/home/joshuakt/Balance', exp, f), 'r') as f:
                data = json.load(f)

            desc = data['metadata']['description']
    
            if ('feet apart' in desc and 'eyes open' in desc) or ('tandem' in desc and 'eyes closed' in desc):
    
                for tracklet in data['data']:
    
                    x = tracklet['x']
                    y = tracklet['y']
                    z = tracklet['z']
                    t = tracklet['t']
                    id = tracklet['id']
                    v = []
                    for i in range(0, len(x) - 1):
                        d = ((y[i+1] - y[i])**2 + (x[i+1] - x[i])**2)**.5
                        v.append(d)
                    v.insert(0, v[0])
    
                    fig ,axarr = plt.subplots(2, 3)
                    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
                    axarr[0, 0].plot(x, y)
                    axarr[0, 0].set(xlabel='x', ylabel='y', title='x-y positon over time')
    
                    t = np.arange(len(x))
                    plot1 = axarr[0, 1].scatter(x, y, c = t)
                    axarr[0, 1].set(xlabel='x', ylabel='y', title='Scatter plot of x-y data over time (color chage proportional to time)')
                    cbar = fig.colorbar(plot1, ax=axarr[0, 1])
                    cbar.ax.set_ylabel('time')
    
                    axarr[1, 0].plot(t, v)
                    axarr[1, 0].set(xlabel='t', ylabel='v', title='velocity over time')
    
                    axarr[1, 1].plot(t, y)
                    axarr[1, 1].set(xlabel='t', ylabel='y', title='x over time')
    
                    axarr[1, 2].plot(t, x)
                    axarr[1, 2].set(xlabel='t', ylabel='x', title='y over time')
    
                    axarr[0, 2].set(title=desc)
                    # fig.suptitle('Balancing Test Data')
                    # plt.figtext(.1, .02, desc)

    plt.show()




