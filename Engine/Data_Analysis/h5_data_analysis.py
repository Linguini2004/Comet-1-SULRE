import h5py
import numpy as np
import csv
import os




try: 
    print('The home directory has been saved as: ', home_directory)
except:
    home_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)    
    print('Saving the home directory as: ', home_directory)
    
burn_10s_directory = home_directory+"\Data\Hot_Fire_10s"
burn_3s_directory = home_directory+"\Data\Hot_Fire_3s"

data_directory_path = burn_10s_directory #Set to either 3s or 10s burn respectively
data_path = "groups/air/PT100"

os.chdir(data_directory_path)

h5_data = os.listdir()[0]

f = h5py.File(h5_data, "r")

def save_data(time, data, filename):
    time_arr = np.array(time)
    data_arr = np.array(data)

    with open("%s.csv" % filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Time", "Sensor_Data"])
        for i in range(len(data_arr)):
            writer.writerow([time_arr[i], data_arr[i]])
        

def h5_tree(val, pre=''):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if items == 0:
            if type(val) == h5py._hl.group.Group:
                print(pre + '└── ' + key)
                h5_tree(val, pre+'    ')
            else:
                pass
                print(pre + '└── ' + key + ' (%d)' % len(val))
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                pass
                print(pre + '├── ' + key + ' (%d)' % len(val))
                

def search(val, search_param, pre=''):
    items = len(val)
    for key, val in val.items():
        items -= 1
        if key == search_param:
            return val
        
    raise Exception("Group or data does not exist, chech data_path")


with h5py.File(h5_data, 'r') as hf:
    
    h5_tree(hf)
    
    print("========================================================================================")
    
    relavent_groups = data_path.split("/")
    gp_fname = "_".join(relavent_groups)
    nxt_group = hf
    for group in relavent_groups:
        nxt_group = search(nxt_group, group)
    time = search(nxt_group, "time")
    data = search(nxt_group, "data")
    
    
    os.chdir(home_directory+"\Data_Analysis")
    save_data(time, data, gp_fname)

    
