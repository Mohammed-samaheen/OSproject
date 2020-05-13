import numpy as np
import matplotlib.pyplot as plt
from util.const import *


def grantt_charts(data, title):
    ticks = []
    leg_list = []
    fig = plt.figure(figsize=[8.2, 4.8])
    ax = fig.subplots()
    for i in data:
        x = np.arange(i[1], i[2])
        y = np.ones(i[2] - i[1])
        if x.size == 1:
            plt.scatter(x, y, color=colors[i[0]], lw=10, marker='|', s=229,
                        label=labels[i[0]] if i[0] not in leg_list else '')

        ax.plot(x, y, color=colors[i[0]], lw=15,
                label=labels[i[0]] if i[0] not in leg_list else '')
        leg_list.append(i[0])
        ticks.append(i[2])
    leg = ax.legend()
    for line in leg.get_lines():
        line.set_linewidth(2.0)
    plt.yticks([])
    plt.xticks(ticks)
    plt.title(title)
    # plt.savefig('./result/test4/'+title)
    plt.show()
