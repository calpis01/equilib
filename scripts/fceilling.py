import numpy as np
import pickle

start = 0
end = 1
place = "_lab_f"

for j in range(start, end):
    f = open("line_parameter"+place+"/list%d.txt" %j, 'rb')
    list_row = pickle.load(f)
    if list_row is None: 
        continue
    #print(list_row)
    li = np.sort(list_row)
    #print(li)
    line_list1 = np.array(sorted(li, reverse=False, key=lambda x: x[0]))  #[1]に注目してソート
    print(line_list1)