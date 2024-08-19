import typer
import pandas as pd
import yaml
from random import choice
from glob import glob

app = typer.Typer()

@app.command()
def gen_blank_result(
    dataset = typer.Argument(

    ), 
    config_file = typer.Argument(

    ),
    outfile = typer.Argument(

    ),
    include_folder = typer.Option(
        None
    ),
    exclude_folder = typer.Option(
        None
    ),
    num_file = typer.Option(
        None
    ),
    random : bool = typer.Option(
        False, '--random'
    )
):
    """
    """
    raw_df = pd.read_csv(
        dataset, delimiter='|'
    )
    configs = yaml.safe_load(open(config_file))

    proc_df = raw_df
    num_proc = 0

    if include_folder != None:
        include_files = glob(f'{include_folder}/*.txt')
        include_filenames = []
        for include_file in include_files:
            include_filenames += [x.strip() for x in open(include_file).readlines()]
        include_df = raw_df[raw_df['filename'].isin(include_filenames)]
        proc_df = raw_df[~raw_df['filename'].isin(include_filenames)]
        num_proc -= len(include_df)
    if exclude_folder != None:
        print("Exclude ", exclude_folder)
        exclude_files = glob(f'{exclude_folder}/*.txt')
        exclude_filenames = []
        for exclude_file in exclude_files:
            exclude_filenames += [x.strip() for x in open(exclude_file).readlines()]
        proc_df = raw_df[~raw_df['filename'].isin(exclude_filenames)]
        if num_file != None:
            num_proc = int(num_file)
        else:
            num_proc = len(raw_df) - len(exclude_filenames)
        print(num_proc)

    if num_proc == 0:
        num_proc = len(raw_df)

    # include_folder
    proc_df = proc_df.sample(n=num_proc)
    if include_folder:
        proc_final = pd.concat([
            proc_df, include_df
        ], axis=0).sample(frac=1)
    if exclude_folder:
       proc_final = proc_df.sample(n=num_proc) 

    print(proc_final.head())

    proc_rows = proc_final.to_dict('records')
    print(len(proc_rows))
    temps = []
    for row in proc_rows:
        temp = {
            'filename' : str(row['filename'])
        }
        for k in configs['labels']:
            label = configs['labels'][k]
            temp_field = label['fieldname']
            if label['type'] == 'radio':
                valueList = label['values']
                if random:
                    temp[temp_field] = choice(valueList)
                else:
                    temp[temp_field] = valueList[0]
            elif label['type'] == 'text_area':
                temp[temp_field] = label['values']
        temps.append(temp)

    df = pd.DataFrame(temps)
    df.to_csv(outfile, index=False, sep='|')

if __name__ == '__main__':
    app()