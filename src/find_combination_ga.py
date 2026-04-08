from src.item_pool import ItemPools
import numpy as np

POP_SIZE = 200
GEN = 500
MUT_RATE = 0.1
CROSS_RATE = 0.8
ELITE_RATE = 0.05
ELITE_SIZE = int(POP_SIZE * ELITE_RATE)


def find_combination_ga(pools, target):
    

    target32 = np.float32(target) * 10
    print(f"Finding {target}...")

    master_pool = np.array([])
    for i in range(pools.pools_num):
        master_pool = np.append(master_pool, pools.item_pools[i])

    master_id_pool = np.array([],dtype = np.int64)
    for i in range(pools.pools_num):
        master_id_pool = np.append(master_id_pool, pools.item_id_pools[i])

    pop = init_pop(pools.item_lens, pools.item_qtys, pools.pools_num)
    best_fitness = float('inf')
    best_individual = None 
    
    for gen in range(GEN):
        fitness = get_fitness(pop, np.array(master_pool), target32)
        
        best_idx = np.argmin(fitness)

        if fitness[best_idx] < best_fitness:
            best_fitness = fitness[best_idx]
            best_individual = pop[best_idx].copy()
        
        if gen % 50 == 0:
            print(f"Gen {gen} - Best Fitness: {fitness[best_idx]:.9f}")
        
        if fitness[best_idx] == 0:
            print("Exact combination found!")
            best_individual = pop[best_idx]
            best_combination_ids = [master_id_pool[idx] for idx in best_individual]
            print("Best Combination IDs:", best_combination_ids)
            return best_combination_ids
        

        # Selection
        parent1_indices = np.random.choice(range(POP_SIZE), size=POP_SIZE, replace=True)
        parent2_indices = np.random.choice(range(POP_SIZE), size=POP_SIZE, replace=True)

        #crossover
        new_pop = crossover(pop[parent1_indices], pop[parent2_indices], pools.item_qtys, pools.pools_num)
        
        #mutation
        mutation(new_pop, pools.item_lens, pools.pools_num)

        # Elitism
        elite_indices = np.argpartition(fitness, ELITE_SIZE)[:ELITE_SIZE]
        new_pop[:ELITE_SIZE] = pop[elite_indices]

        pop = new_pop


    
    print(f"Best Fitness after all generations: {best_fitness:.9f}")
    print(f"Best Sum: {np.sum(master_pool[best_individual]) / 10:.9f}")

    best_combination_ids = master_id_pool[best_individual]
    
    return best_combination_ids





def init_pop(item_lens, item_qtys, pools_num):
    pop = np.empty((POP_SIZE, 10), dtype=np.int64)

    for j in range(POP_SIZE):
        individual_indices = []
        current_index = 0
        for i in range(pools_num):
            choice = np.random.choice(range(current_index, current_index + item_lens[i]), size=item_qtys[i], replace=False)
            current_index += item_lens[i]
            individual_indices.extend(choice)
        
        pop[j] = individual_indices

    return pop

def get_fitness(pop, master_values, target):
    selected_matrix = master_values[pop]
    sums = np.sum(selected_matrix, axis=1)
    error = np.abs(sums - target)
    return error

def crossover(parent1, parent2, item_qtys, pools_num):
    # parent1 ( POP_SIZE , 10) and parent2 ( POP_SIZE , 10) are the selected parents for crossover
    # pools are group of items, choose item_qtys[i] items for each pool
    
    child = parent1.copy()

    for i in range(POP_SIZE):
        if np.random.rand() < CROSS_RATE:
            current_qty = 0
            for j in range(pools_num):
                # avoid duplicate index by taking the union of the two parents' segments and randomly choosing from it
                child[i] [current_qty:current_qty+item_qtys[j]] = np.random.choice(
                    np.union1d(parent1[i][current_qty:current_qty+item_qtys[j]], parent2[i][current_qty:current_qty+item_qtys[j]]),
                    size=item_qtys[j],
                    replace=False
                )
                current_qty += item_qtys[j]
      
    return child

def mutation(pop, item_lens, pools_num):
    for i in range(POP_SIZE):
        if np.random.rand() < MUT_RATE:
            mutate_pt = np.random.randint(0, 10)
            data = pop[i][mutate_pt]
            index_range = item_lens[0]-1
            for j in range(pools_num):
                if data == index_range:
                    data -= 1
                    break;
                elif data < index_range:
                    data += np.random.choice([-1,1])
                    break;
                else:
                    index_range += item_lens[j]

            if np.union1d(pop[i], [data]).size == 11: # check if the new data is not already in the individual
                pop[i][mutate_pt] = data
                
# 0 ~ item_lens[0]-1 for pool 0
# item_lens[0] ~ item_lens[0]+item_lens[1]-1 for pool 1