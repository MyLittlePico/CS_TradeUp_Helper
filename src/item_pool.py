import numpy as np

class ItemPools:
    def __init__(self): 
        self.item_pools = []
        self.item_lens = []
        self.item_qtys = []

        self.pools_num = 0

    def add_new_pool(self, data_list, number_to_use):
        if number_to_use >0 :
            self.item_pools.append( np.sort(np.array(data_list, dtype=np.float32)) )
            self.item_lens.append( len(data_list) )
            self.item_qtys.append( number_to_use )
            self.pools_num += 1




