import pandas as pd
import sys 

file_1, file_2 = sys.argv[1:3]

print("File: ", file_2)

fileList_1 = pd.read_csv(file_1)['filename']
set_1 = set(fileList_1)
print(f"{len(fileList_1)} {len(set_1)}| File: {file_1}")
fileList_2 = pd.read_csv(file_2)['filename']
set_2 = set(fileList_2)
print(f"{len(fileList_2)} {len(set_2)}| File: {file_2}")
same = set_1.intersection(set_2)

print(f"~> Num same: {len(same)}")

