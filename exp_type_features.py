import json 
import os
import numpy as np 
import matplotlib.pyplot as plt
import extract_feats as feat
import statistics as stat
import compute_ellipse as cell

if __name__ == '__main__':
    avg_dev = [[] for i in range(6)]
    avg_dev_s = [[] for i in range(6)]
    rmsd_exp = [[] for i in range(6)]
    avg_area = [[] for i in range(6)]
    fig ,axarr = plt.subplots(2, 3)
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    for _,_,i in os.walk('/home/joshuakt/Balance/dec23'):
        for f in i:
            with open(os.path.join('/home/joshuakt/Balance/dec23/',f), 'r') as f:
                data = json.load(f)

            desc = data['metadata']['description']

            for tracklet in data['data']:

                x = tracklet['x']
                y = tracklet['y']
                z = tracklet['z']
                t = tracklet['t']
                tx = feat.trim(x)
                ty = feat.trim(y)
                id = tracklet['id']
                
                if 'feet apart' in desc and 'eyes open' in desc:
                    ridx =  0
                    cidx =  0
                    idx = 0
                    description = 'eyes open; feet apart;\n facing device'
                    
    
                if 'feet apart' in desc and 'eyes closed' in desc:
                    ridx =  1
                    cidx =  0
                    idx = 3
                    description = 'eyes closed; feet apart;\n facing device' 
                    
                if 'left behind right' in desc and 'eyes open' in desc:
                    ridx =  0
                    cidx =  1
                    idx = 1
                    description = 'eyes open; feet — left behind right;\n facing device' 
    
                if 'left behind right' in desc and 'eyes closed' in desc:
                    ridx =  1
                    cidx =  1
                    idx = 4
                    description = 'eyes closed; feet — left behind right;\n facing device'
    
                if 'tandem' in desc and 'eyes open' in desc: 
                    ridx =  0
                    cidx =  2
                    idx = 2
                    description = 'eyes open; feet tandem lbr;\n facing device' 
    
                if 'tandem' in desc and 'eyes closed' in desc: 
                    ridx =  1
                    cidx =  2
                    idx = 5
                    description = 'eyes closed; feet tandem lbr;\n facing device'

                if len(tx) != 0 and len(ty) != 0:
                    avg_dev[idx].append(feat.avg_dev(tx, ty))
                    avg_dev_s[idx].append(feat.avg_dev_s(x, y))
                    sx, sy = feat.calibrate_center(tx, ty)
                    avg_area[idx].append(cell.area(sx, sy))
                    axarr[ridx,cidx].plot(sx, sy)
                    axarr[ridx,cidx].set_xlim(-0.6, 0.6)
                    axarr[ridx,cidx].set_ylim(-.4, .4)
                    axarr[ridx,cidx].set(xlabel='x (m)', ylabel='y (m)', title=description)
                    rmsd_exp[idx].append(feat.rms_center_distance(tx, ty))
    
#    print(sum(avg_dev_s_1)/len(avg_dev_s_1))
#    print(sum(avg_dev_s_2)/len(avg_dev_s_2))
#    print(sum(avg_dev_s_3)/len(avg_dev_s_3))
#    print(sum(avg_dev_s_4)/len(avg_dev_s_4))
#    print(sum(avg_dev_s_5)/len(avg_dev_s_5))
#    print(sum(avg_dev_s_6)/len(avg_dev_s_6))
#    print('--------------')
#    print(stat.stdev(avg_dev_s_1))
#    print(stat.stdev(avg_dev_s_2))
#    print(stat.stdev(avg_dev_s_3))
#    print(stat.stdev(avg_dev_s_4))
#    print(stat.stdev(avg_dev_s_5))
#    print(stat.stdev(avg_dev_s_6))

    avgdev = [sum(i)/len(i) for i in avg_dev]
    dc_sd = [stat.stdev(i) for i in avg_dev]
    rmsd = [sum(i)/len(i) for i in rmsd_exp]
    rmsd_sd = [stat.stdev(i) for i in rmsd_exp]
    avgarea = [sum(i)/len(i) for i in avg_area]
    area_sd = [stat.stdev(i) for i in avg_area]

    for i in range(len(avg_dev)):
        print(sum(avg_dev[i])/len(avg_dev[i]))
        print(dc_sd[i])
        print('--------------')
    print('==============')
    for i in range(len(rmsd_exp)):
        print(sum(rmsd_exp[i])/len(rmsd_exp[i]))
        print(rmsd_sd[i])
        print('--------------')
    print('==============')
    for i in range(len(avg_area)):
        print(sum(avg_area[i])/len(avg_area[i]))
        print(area_sd[i])
        print('--------------')

#    exp_types = ['eyes open;\n feet apart;\n facing device', 'eyes open;\n feet lbr;\n facing device', 'eyes open;\n feet tandem lbr;\n facing device', 'eyes closed;\n feet apart;\n facing device', 'eyes closed;\n feet lbr;\n facing device', 'eyes closed;\n feet tandem lbr;\n facing device']
    exp_types = ['open;\n apart', 'open;\n lbr', 'open;\n tandem lbr', 'closed;\n apart', 'closed;\n lbr', 'closed;\n tandem lbr']

    plt.figure(2)
    plt.bar(np.arange(len(avgdev)), avgdev, yerr= dc_sd)
    plt.xticks(np.arange(len(avgdev)), exp_types, fontsize = 15, rotation = 45)
    plt.ylabel('deviation from center (m)', fontsize = 25)
    plt.title('average deviation from center for each exp type', fontsize = 25)

    plt.figure(3)
    plt.bar(np.arange(len(rmsd)), rmsd, yerr= rmsd_sd)
    plt.xticks(np.arange(len(rmsd)), exp_types, fontsize = 15, rotation = 45)
    plt.ylabel('RMS distance from center', fontsize = 25)
    plt.title('average RMS distance from center for each exp type', fontsize = 25)
    plt.show()

    plt.figure(4)
    plt.bar(np.arange(len(avgarea)), avgarea, yerr= area_sd)
    plt.xticks(np.arange(len(avgarea)), exp_types, fontsize = 15, rotation = 45)
    plt.ylabel('Average Area of Ellipse', fontsize = 25)
    plt.title('Average Area of Best Fitting Ellipse', fontsize = 25)
    plt.show()
