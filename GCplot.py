import numpy as np
import matplotlib.pyplot as plt
from util.const import *


def gantt_charts(data, title):
    ticks = []
    fig = plt.figure(figsize=[6.4, 4.8])
    for i in data:
        plt.plot(np.arange(i[1], i[2]), np.ones(i[2] - i[1]),
                 color=colors[i[0]], lw=20, label=labels[i[0]])
        ticks.append(i[2])
    leg=plt.legend()
    for line in leg.get_lines():
        line.set_linewidth(2.0)
    plt.yticks([])
    plt.xticks(ticks)
    plt.title(title)
    plt.show()
