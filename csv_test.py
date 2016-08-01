import csv
import ast

mylist = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]

csvFilename = 'coordinates.csv'

#with open(csvFilename, 'wb') as myfile:
#    wr = csv.writer(myfile)
#    wr.writerow(mylist)
    
with open('coordinates.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)
    
ast.literal_eval(flattened[0])