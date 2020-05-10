import pandas as pd
import matplotlib.pyplot as plt
import threading, queue
from util.Preprocessor import *
import time
from PCB import *
from PageMapModel import *
from util.const import *
from GCplot import *

# read the data and and put it in a table
information, table = read_data()
physical_mem_size, page_size, round_Q, CS = information
time_unit = 0.1
start_time = None
table = table.sort_values(by=['Arrival Time']).reset_index(drop=True)

frame_num = int(physical_mem_size / page_size)  # number of frame

simulator = 'FCFS'
# TODO start of part one of the project

q = queue.Queue()


def worker():
    while True:
        print(UNDERLINE + "open" + ENDC)
        item = q.get()
        if simulator == 'SJF':
            item = item[1]
            print(FAIL+f'SJF p-{item.process_id} {time.time()-start_time}')
        item.state = "run"
        time_in = time.time() - start_time
        print(OKBLUE + f'Working on {item.process_id}' + ENDC)
        wating_time = table[table["Process ID"] == item.process_id]["CPU Burst"].item()
        time.sleep(time_unit * wating_time)
        time_out = time.time() - start_time
        print(OKGREEN + f'Finished {item.process_id} at {time_out} : {int(time_out * 10)}' + ENDC)
        ct.append(int(time_out * 10))
        result.append((item.process_id, int(time_in * 10), int(time_out * 10)))
        map_unit.remove_process(item.page_table)
        q.task_done()
        print(not q.empty())
        if q.empty():
            print(FAIL+"waiting"+ENDC)
            continue
        time.sleep(CS * time_unit)
        print(UNDERLINE + "waiting" + ENDC)


threading.Thread(target=worker, daemon=True).start()
map_unit = PageMap(physical_mem_size, page_size)

# FCFS simulator model

for sem in simulator_list:
    simulator = sem
    result = []
    ct = []
    i = 0
    if sem == 'SJF':
        q = queue.PriorityQueue()
    start_time = time.time()
    for t in table["Arrival Time"].to_numpy():
        if sem == 'FCFS':
            q.put(PCB(table["Process ID"][i], map_unit.add_process(table["Size in Bytes"][i]),
                      time_in=time.time()))
        elif sem == 'SJF':
            q.put((table["CPU Burst"][i], PCB(table["Process ID"][i], map_unit.add_process(table["Size in Bytes"][i]),
                                              time_in=time.time())))

        wait = 0
        if i != table.shape[0] - 1:
            wait = table["Arrival Time"][i + 1] - t
        time.sleep(time_unit * wait)
        print(f'Arrival Time of {table["Process ID"][i]} : ', time.time() - start_time)
        i += 1
    q.join()

print(HEADER + "done" + ENDC)
q.join()
gantt_charts(result)
awt = average_waiting_time(table["Arrival Time"].to_numpy(),
                           table["CPU Burst"].to_numpy(), np.array(ct))
print('\n' + WARNING + f'average waiting time for FCFS : {awt}' + ENDC)
