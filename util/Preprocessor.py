import pandas as pd
import numpy as np


def read_data(file_name='processes.txt'):
    with open('./testfile/Test File 1.txt', 'r+') as d:
        content = d.readlines()

    information = tuple(map(int, content[:4]))
    pre_data = np.array(content[4:])
    pre_data = pre_data[pre_data != '\n']
    data = np.array([list(map(int, x.split('  '))) for x in pre_data])

    table = pd.DataFrame(data=data, columns=['Process ID', 'Arrival Time',
                                             'CPU Burst', 'Size in Bytes'])
    return information, table


def summary(table):
    table["Turnaround Time"] = table["Finish time"] - table["Arrival Time"]
    table["Waiting Time"] = table["Turnaround Time"] - table["CPU Burst"]

    return table, table["Turnaround Time"].mean(), table["Waiting Time"].mean()


def cpu_utilization(data):
    process_time = sum([x[2] - x[1] for x in data])
    return (process_time / data[-1][2]) * 100
