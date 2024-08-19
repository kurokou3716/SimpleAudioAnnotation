import sys , os 
import pandas as pd 

infile = sys.argv[1]
users = ['Trang', 'Hau', 'Chi']
folder_path = os.path.dirname(infile)
filename = os.path.basename(infile)

df = pd.read_csv(infile)
for user in users:
    temp_df = df.sample(frac=1)
    temp_name = f'{folder_path}/{user}_{filename}'
    print(temp_name)
    temp_df.to_csv(temp_name, index=False)