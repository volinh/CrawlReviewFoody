import os

def preprocess_data(raw_data):
    bad_points = []
    good_points = []
    n_points = []
    for i in raw_data:
        arr = i.split("\t",maxsplit=2)
        line = arr[1].strip()
        if float(arr[0]) < 6 :
            bad_points.append(i)
        elif float(arr[0]) <7 :
            n_points.append(i)
        else:
            good_points.append(i)
    return bad_points,n_points,good_points

list_file = os.listdir("data2")
print(len(list_file))
list_data = []
for i in list_file:
    with open("data2/"+i,"r") as file:
        lines = file.readlines()
        list_data.extend(lines)
print(len(list_data))

b_points ,n_points,g_points = preprocess_data(list_data)
for i in n_points:
    print(i)
print(len(n_points))