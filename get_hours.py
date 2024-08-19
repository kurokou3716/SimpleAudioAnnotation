from pydub.utils import mediainfo
import sys 
from tqdm import tqdm
import pandas as pd

infile = sys.argv[1]
filelist = list(pd.read_csv(infile)['filename'])
source = 'datasets/ViSEC/flacs'
total_dur = 0
for filename in tqdm(filelist):
    filepath = f'{source}/{filename}'
    total_dur += float(mediainfo(filepath)['duration'])
print(infile)
print(f'-> {total_dur} s')
print(f'-> {total_dur/3_600:.2f} h')