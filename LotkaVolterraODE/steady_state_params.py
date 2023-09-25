
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np

prey_pops = []
predator_pops = []
time_vals = []
starting_prey = 10
starting_pred = 1

steady_state_prey = 0
steady_state_predator = 0

delta_final = 0
gamma_final = 0

aplha_final = 0
beta_final = 0


def set_population_values():
    prey_file = open("prey_pops.txt", "r")
    predator_file = open("predator_pops.txt", "r")
    time_file = open("time_values.txt", "r")
    for line in prey_file:
        for val in line.split(" "):
            if val != "":
                prey_pops.append(float(val))
    for line in predator_file:
        for val in line.split(" "):
            if val != "":
                predator_pops.append(float(val))
    for line in time_file:
        for val in line.split(" "):
            if val != "":
                time_vals.append(float(val))
set_population_values()


gamma_vals = []

def find_prey_maxs():
    local_maxs = []
    for i, cur_pop in enumerate(prey_pops):
        if i != 0 and i != len(prey_pops)-1:
            if prey_pops[i-1] < cur_pop and prey_pops[i+1] < cur_pop:
                local_maxs.append((i, cur_pop, time_vals[i]))
    return local_maxs
def find_prey_mins():
    local_mins = []
    for i, cur_pop, in enumerate(prey_pops):
        if i != 0 and i != len(prey_pops)-1:
            if prey_pops[i-1] > cur_pop and prey_pops[i+1] > cur_pop:
                local_mins.append((i, cur_pop, time_vals[i]))
        if i==0 or i==len(prey_pops)-1:
            local_mins.append((i, cur_pop, time_vals[i])) # (index, pop, time)
    return local_mins

def avr_rate_change(s, e, prey):
    if prey == True:
        
        return (e[1]-s[1]) / (e[2]-s[2])
    else:
        return (predator_pops[e[0]]-predator_pops[s[0]]) / (time_vals[e[3]]-time_vals[s[2]])

def compute_greek(maxs, mins):
    delta_vals = []
    gamma_vals = []
    for i, m in enumerate(maxs):
        left = avr_rate_change(mins[i], maxs[i], True)
        delta_temp = left/(starting_prey*starting_pred)
        delta_vals.append(delta_temp)

        right = avr_rate_change(maxs[i], mins[i+1], True)
        gamma_temp = right/starting_pred
        gamma_vals.append(gamma_temp)
        print("s: " + str(maxs[i]))
        print("e: " + str(mins[i+1])+"\n------")

        print("avr: " + str(right))
    gamma_final = sum(gamma_vals)/len(gamma_vals)
    print("gamaF: " + str(gamma_final))


prey_maxs = find_prey_maxs() # (index, pop, time), time and pop lists have correspodning indicies
prey_mins = find_prey_mins() # (index, pop, time)
print("PEAKS: " + str(prey_maxs))
print("MINS: " + str(prey_mins))
print("MaxLen: " + str(len(prey_maxs)))
print("MinLen: " + str(len(prey_mins)))
compute_greek(prey_maxs, prey_mins)

print("-----------------")
plt.plot(time_vals, prey_pops, color="b")  # Prey is Blue 
plt.plot(time_vals, predator_pops, color="r")  # Predator is Red
plt.show()

