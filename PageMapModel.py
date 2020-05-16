import numpy as np
import pandas as pd
import warnings


class PageMap:

    def __init__(self, physical_mem_size, page_size):
        self.physical_mem_size = physical_mem_size
        self.page_size = page_size

        # frames in the physical memory
        self.frames = np.arange(int(physical_mem_size / page_size))
        self.frame_state = np.zeros(self.frames.size)
        self.frame_value = np.zeros(self.frames.size)

    # allocate the memory and creat page table of the process
    def add_process(self, process_size):
        process_page_num = int(process_size / self.page_size)
        process_page = np.arange(process_page_num)
        num_free_frames = (self.frame_state == 0).sum()
        np.random.shuffle(process_page)
        flage = True

        if process_page_num >= num_free_frames:
            self.frame_value[self.frame_state == 0] = process_page[:num_free_frames]
            map_page = (self.frames[self.frame_state == 0].tolist())
            self.frame_state[self.frame_state == 0] = 1
        else:
            tem = self.frame_value[self.frame_state == 0]
            tem[:process_page_num] = process_page[:]
            self.frame_value[self.frame_state == 0] = tem
            tem = self.frame_state[self.frame_state == 0]
            tem[:process_page_num] = 1
            self.frame_state[self.frame_state == 0] = tem
            map_page = (self.frames[:process_page_num].tolist())

        if process_page_num > num_free_frames:
            map_page += (['HDD'] * int(process_page_num - num_free_frames))
            flage = False
        if flage:
            valid = np.ones(process_page_num) == True
        else:
            valid = np.array(map_page) != 'HDD'

        page_table = {
            'page-number': np.array(process_page).astype(int),
            'map-value': np.array(map_page),
            'valid': valid
        }

        return pd.DataFrame(page_table).sort_values(by='page-number')

    def remove_process(self, page_table):
        mem_frame = page_table["map-value"].to_numpy()
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            mem_frame = mem_frame[mem_frame != 'HDD'].astype(int)

        self.frame_state.put(mem_frame, 0)
        self.frame_value.put(mem_frame, 0)

    def allocate_frame(self, process_size, logical_address):
        cumulative_mem = np.arange(start=0, stop=self.physical_mem_size, step=self.page_size)
        cumulative_process = np.arange(start=0, stop=process_size, step=self.page_size)

        for i in cumulative_process:
            if logical_address <= cumulative_process:
                expected_page = i-1

        #still needs some additional code