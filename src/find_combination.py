from src.item_pool import ItemPools
import numpy as np

def find_combination(pools, target):
    
    target32 = np.float32(target) * 10
    print(f"Finding {target}...")
    print(f"Finding {target32}...")

    component = np.array([],dtype=np.float32)

    result = combination (pools, 0, 0, component, 0, 0, target32)


    print(result)
    print(np.sum(result))


def combination (pools, pool_index, list_index, components, comp_num, pool_comp_num, target):
    # end_condition


    if np.sum(components) > target:
        return np.array([0]) 
    
    if comp_num == 10:
        print(np.sum(components))
        return components
    
    if pool_index >= pools.pools_num:
        return np.array([0]) 
    
    if np.sum(components) > target:
        return np.array([0]) 
    
    if list_index >= pools.item_lens[pool_index]: #reach end of pool while not enough item for current pool
        return np.array([0])
    

    
    #next pool
    if pool_comp_num == pools.item_qtys[pool_index]: #enough item for current pool
        pool_index += 1
        list_index = 0
        pool_comp_num = 0

    pick = combination (pools, pool_index , list_index+1 , np.append(components, pools.item_pools[pool_index][list_index]), comp_num+1, pool_comp_num+1, target)
    
    leave = combination (pools, pool_index , list_index+1 , components, comp_num, pool_comp_num, target)

    if np.sum(pick) > np.sum(leave):
        result = pick
    else:
        result = leave

    return result


