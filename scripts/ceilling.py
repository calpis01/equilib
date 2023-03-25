import pickle
import numpy as np

start = 0
end = 21
place = "_doorn"
def celling_score(line_list):
    count = 0
    new_line = [0,0]
    ans = np.array([0,0])
    for line in line_list:
        if count == 0:
            siten1 = line[0]
            shuten1 = line[1]
            """new_line = np.array([siten1,shuten1])
            print(new_line)
            count+=1
            continue"""
        siten2 = line[0]
        shuten2 = line[1]
        if siten2 < shuten1 and siten1 < shuten2:
            a = [siten1, shuten1, siten2, shuten2]
            a = np.sort(a)
            if a[3] > new_line[1]:
                #print("a[3]:",a[3], "newline:", new_line[1]) 
                new_line = np.array([a[0],a[3]])
                #print(new_line)
                siten1 = new_line[0]
                shuten1 = new_line[1]
            if count+1 == len(line_list):
                #print(siten1, shuten1)
                ans = np.block([[ans], [siten1,shuten1]])
        else :
            #print(siten1, shuten1)
            ans = np.block([[ans], [siten1,shuten1]])
            siten1 = siten2
            shuten1 = shuten2
        count+=1
    return ans
score_list1 = []
score_list2 = []
for j in range(start, end):
    f = open("line_parameter"+place+"/list%d.txt" %j, 'rb')
    list_row = pickle.load(f)
    if list_row is None: 
        continue
    #print(list_row)
    li = np.sort(list_row)
    #print(li)
    line_list1 = np.array(sorted(li, reverse=False, key=lambda x: x[0]))  #[1]に注目してソート
    #print(line_list1)

    sortedlist = celling_score(line_list1)
    #print(sortedlist)
    score = 0
    
    for cs in sortedlist:
        score += cs[1] - cs[0]
    #print(score)
    if j <= 90: 
        score_list1.append(score)
        score_rank1 = sorted(score_list1, reverse=True)
    else:
        score_list2.append(score)
        score_rank2 = sorted(score_list2, reverse=True)


#for i in range(0,5): print(score_list2.index(score_rank2[i])+90) 
if start < 90:
    for i in range(0,5): print(score_list1.index(score_rank1[i]), score_rank1[i]) 
else:
    for i in range(0,5): print(score_list2.index(score_rank2[i])+int(start), score_rank2[i]) 

for i in range(0,46): print(score_list1[i]) 
#print(score_rank1[:5])

# [[ 20   3 100]
#  [  1 200  30]
#  [300  10   2]]

