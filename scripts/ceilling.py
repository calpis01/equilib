# import libraries
import pickle
import numpy as np

# set the start and end numbers for the image files to be analyzed
start = 0
end = 21
# set the place name
place = "_doorn"

# define the function that merges overlapping lines
def celling_score(line_list):
    count = 0
    new_line = [0,0]
    ans = []
    for line in line_list:
        if count == 0:
            start_point = line[0]
            end_point = line[1]
            count+=1
            continue
        next_start_point = line[0]
        next_end_point = line[1]
        if next_start_point < end_point and start_point < next_end_point:
            a = [start_point, end_point, next_start_point, next_end_point]
            a = np.sort(a)
            if a[3] > new_line[1]:
                new_line = [a[0], a[3]]
                start_point = new_line[0]
                end_point = new_line[1]
            if count+1 == len(line_list):
                ans.append([start_point, end_point])
        else:
            ans.append([start_point, end_point])
            start_point = next_start_point
            end_point = next_end_point
        count+=1
    return ans

# create empty lists to store the top scores from the analysis
scores_before_90 = []
scores_after_90 = []

# loop through the image files
for j in range(start, end):
    # load the list of lines from the image file
    with open(f"lines/line_parameter{place}/list{j}.txt", 'rb') as f:
        list_row = pickle.load(f)
        if list_row is None:
            continue
        # sort the lines by the x coordinate of the top left corner
        li = np.sort(list_row)
        line_list1 = sorted(li, key=lambda x: x[0])
        # merge overlapping lines
        merged_lines = celling_score(line_list1)
        # calculate the total score for the image file
        score = sum([cs[1] - cs[0] for cs in merged_lines])
        # store the score in the correct list
        if j <= 90:
            scores_before_90.append(score)
            top_scores_before_90 = sorted(scores_before_90, reverse=True)
        else:
            scores_after_90.append(score)
            top_scores_after_90 = sorted(scores_after_90, reverse=True)

# print the top 5 scores from the analysis
if start < 90:
    for i in range(5):
        print(scores_before_90.index(top_scores_before_90[i]), top_scores_before_90[i])
else:
    for i in range(5):
        print(scores_after_90.index(top_scores_after_90[i]) + start, top_scores_after_90[i])
