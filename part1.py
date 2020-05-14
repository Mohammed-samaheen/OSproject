import threading, queue
from util.Preprocessor import *
import time
from PCB import *
from PageMapModel import *
from util.const import *
from GCplot import *


# this function work as cpu that process the processes in the ready queue and it's run in
# diffract thread from the main thread,and it's work for all cpu simulators[FCFS,SJF,RR]
def worker():
    while True:
        if q.empty():
            continue

        item = q.get()
        if simulator == 'SJF':
            item = item[2]

        # get the process from ready queue and put it in the cpu
        item.state = "run"  # chane the state of the process
        time_in = time.time() - start_time  # take the time when the process entered the cpu
        finished = True
        print(OKBLUE + f'Working on {item.process_id}' + ENDC)

        # work of the state process by waiting CPU Burst of the process
        if simulator == 'RR':
            p_burst = burst_time.loc[burst_time["Process ID"] == item.process_id, 'CPU Burst'].item()

            if p_burst - round_Q > 0:
                wating_time = round_Q
                finished = False
            else:
                wating_time = p_burst
                finished = True
            burst_time.loc[burst_time["Process ID"] == item.process_id, 'CPU Burst'] -= wating_time
        else:
            wating_time = table[table["Process ID"] == item.process_id]["CPU Burst"].item()
        time.sleep(time_unit * wating_time)
        time_out = time.time() - start_time  # take the time when the process leave the cpu
        print(OKGREEN + f'Finished {item.process_id} at {time_out} : {int(time_out * 10)}' + ENDC)

        # recoded the result
        if finished:
            copy_table.loc[copy_table["Process ID"] == item.process_id, 'Finish time'] = int(time_out * 10)
        else:
            q.put(item)
        result.append((item.process_id, int(time_in * 10), int(time_out * 10)))

        # remove the process and free the memory from it
        map_unit.remove_process(item.page_table)
        q.task_done()
        if q.empty():
            continue
        time.sleep(CS * time_unit)


# read the data and and put it in a table
information, table = read_data()
physical_mem_size, page_size, round_Q, CS = information
table = table.sort_values(by=['Arrival Time']).reset_index(drop=True)
burst_time = table[['Process ID', 'CPU Burst']].copy()

# general variables for cpu time unit and refrain time
time_unit = 0.1
start_time = None
simulator = None  # name of the cpu  simulator
q = queue.Queue()  # ready queue

threading.Thread(target=worker, daemon=True).start()  # run worker function in diffract thread
map_unit = PageMap(physical_mem_size, page_size)  # map unit between pages and frames

# iteration for all simulator mode and find the result for each of them
for sem in simulator_list:
    result = []  # final result
    copy_table = table.copy()
    copy_table["Finish time"] = np.zeros(table.shape[0])  # complete time for each process
    i = 0
    if sem == 'SJF':
        q = queue.PriorityQueue()

    simulator = sem
    start_time = time.time()
    for t in table["Arrival Time"].to_numpy():
        print(f'process {table["Process ID"][i]} arrived at: {time.time() - start_time}')
        if sem == 'SJF':
            q.put((table["CPU Burst"][i], time.time() - start_time, PCB(table["Process ID"][i],
                                                                        map_unit.add_process(table["Size in Bytes"][i]),
                                                                        time_in=time.time())))
        else:
            q.put(PCB(table["Process ID"][i], map_unit.add_process(table["Size in Bytes"][i]),
                      time_in=time.time() - start_time))

        wait = 0
        if i != table.shape[0] - 1:
            wait = table["Arrival Time"][i + 1] - t

        time.sleep(time_unit * wait)
        i += 1

    q.join()

    grantt_charts(result, sem)
    result_table, average_turnaround_time, average_waiting_time = summary(copy_table)

    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', None)

    print(result_table)
    print('\n' + WARNING + f'average turnaround time for {sem} : {average_turnaround_time}' + ENDC)
    print(WARNING + f'average waiting time for {sem} : {average_waiting_time}' + ENDC)
    print(WARNING + f'cpu utilization for {sem} : {cpu_utilization(result)}' + ENDC + '\n')
    print(OKBLUE+'----------------'*6+ENDC+'\n')