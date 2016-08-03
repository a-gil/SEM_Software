import csv
import ast

mylist = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

csvFilename = 'coordinates.csv'

#with open(csvFilename, 'wb') as myfile:
#    wr = csv.writer(myfile)
#    wr.writerow(mylist)
    
with open('coordinates.csv', 'rb') as f:
    reader = csv.reader(f)
    
    #make a list of the csv file
    your_list = list(reader)
    
    #Remove nested list
    your_list = your_list[0]

l = 0
while l < len(your_list):
    print(your_list[l])
    values = ast.literal_eval(your_list[l])
    your_list.remove(your_list[l])
    your_list.insert(l, values)
    print(your_list[l])
    
    l = l+1